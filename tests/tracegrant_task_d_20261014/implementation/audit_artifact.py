"""Independently audit tables and source preservation, then hash artifacts."""
from pathlib import Path
import hashlib
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def main():
    pins = json.loads((ROOT / 'pins.json').read_text(encoding='utf-8'))
    for name, expected in pins['sources_sha256'].items():
        assert hashlib.sha256((ROOT / 'sources' / name).read_bytes()).hexdigest() == expected, name
    # Original secondary source outside the fresh artifact remains identical.
    assert hashlib.sha256((ROOT.parent / 'TraceGrant_Step_by_Step_Guide.md').read_bytes()).hexdigest() == pins['sources_sha256']['TraceGrant_Step_by_Step_Guide.md']
    summary = json.loads((ROOT / 'results/summary.json').read_text(encoding='utf-8'))
    for group in ('valid_cases', 'invalid_contracts', 'invalid_inputs', 'controls'):
        rows = json.loads((ROOT / 'results' / f'{group}.json').read_text(encoding='utf-8'))
        numerator, denominator = sum(bool(row['matched']) for row in rows), len(rows)
        assert summary[group] == dict(numerator=numerator, denominator=denominator, fraction=numerator / denominator)
    probes = json.loads((ROOT / 'results/exploratory_probes.json').read_text(encoding='utf-8'))
    assert len(probes) == summary['exploratory_probes']['denominator'] == 2
    assert sum(p['receipt_valid'] for p in probes) == summary['exploratory_probes']['illustrative_effects_receipt_verified']
    crashes = json.loads((ROOT / 'results/crash_controls.json').read_text(encoding='utf-8'))
    assert len(crashes) == summary['crash_controls']['denominator'] == 1
    assert not any(p['successful_defense'] or p['final_accepted'] for p in crashes)
    xml = ET.parse(ROOT / 'logs/09_pytest_final.junit.xml')
    cases = xml.findall('.//testcase')
    assert len(cases) == summary['unit_tests']['tests']
    failures = sum(c.find('failure') is not None for c in cases)
    errors = sum(c.find('error') is not None for c in cases)
    skipped = sum(c.find('skipped') is not None for c in cases)
    assert summary['unit_tests'] == dict(tests=len(cases), failures=failures, errors=errors,
                                       skipped=skipped, passed=len(cases)-failures-errors-skipped)
    assert int((ROOT / 'logs/09_pytest_final.exitcode.txt').read_text(encoding='utf-8-sig')) == 0
    catalog = json.loads((ROOT / 'examples/catalog.json').read_text(encoding='utf-8'))
    assert len(catalog) == 10
    assert len(list((ROOT / 'examples').glob('[0-9][0-9]_*.json'))) == 10
    report = (ROOT / 'REPORT.md').read_text(encoding='utf-8')
    assert f"{summary['unit_tests']['passed']}/{summary['unit_tests']['tests']}" in report
    for group in ('valid_cases', 'invalid_contracts', 'invalid_inputs', 'controls'):
        assert f"{summary[group]['numerator']}/{summary[group]['denominator']}" in report
    hashes = {}
    excluded_dirs = {'.venv', '__pycache__', '.pytest_cache'}
    for path in sorted(ROOT.rglob('*')):
        rel = path.relative_to(ROOT)
        if (not path.is_file() or excluded_dirs.intersection(rel.parts) or
                path.name in {'SHA256SUMS.json', 'audit.json'} or
                rel.as_posix().startswith('logs/13_audit.')):
            continue
        hashes[rel.as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    (ROOT / 'SHA256SUMS.json').write_text(json.dumps(hashes, indent=2), encoding='utf-8')
    # Verify after writing, rather than merely emit a proposed manifest.
    manifest = json.loads((ROOT / 'SHA256SUMS.json').read_text(encoding='utf-8'))
    for name, expected in manifest.items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
    result = dict(status='PASS', files_hashed=len(hashes), source_hashes_checked=len(pins['sources_sha256']),
                  original_guide_unchanged=True, contract_examples=10,
                  independently_counted_unit_tests=len(cases), independent_arithmetic=True,
                  exclusions='venv/cache files and self-referential manifest/audit files/logs')
    (ROOT / 'audit.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
