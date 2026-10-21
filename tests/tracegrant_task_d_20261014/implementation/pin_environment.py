"""Record the actual runtime and all installed packages without network use."""
import hashlib
import importlib.metadata as metadata
import json
from pathlib import Path
import platform
import sys

root = Path(__file__).resolve().parents[1]
required = ['pydantic', 'pydantic_core', 'annotated-types', 'typing_extensions',
            'typing-inspection', 'pytest', 'colorama', 'iniconfig', 'packaging',
            'pluggy', 'Pygments', 'pypdf']
packages = {name: metadata.version(name) for name in required}
all_packages = sorted([{'name': d.metadata['Name'], 'version': d.version}
                       for d in metadata.distributions()], key=lambda x: x['name'].lower())
sources = {}
for path in sorted((root / 'sources').glob('*')):
    if path.is_file():
        sources[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
manifest = dict(python=sys.version, executable=sys.executable, platform=platform.platform(),
                python_requirement='3.12', direct_and_transitive_dependencies=packages,
                installed_packages=all_packages, sources_sha256=sources,
                paper_url='https://arxiv.org/pdf/2608.21126v1', paper_version='v1',
                upstream_repo_url=None, upstream_commit=None,
                upstream_status='NOT DONE: no author implementation repository obtained; independent implementation',
                environment_policy='venv inherits local system packages; pytest plugin autoload disabled; no package download')
assert sys.version_info[:2] == (3, 12)
assert int(packages['pydantic'].split('.')[0]) == 2
(root / 'pins.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
(root / 'requirements.lock').write_text('\n'.join(f'{n}=={v}' for n, v in packages.items()) + '\n', encoding='utf-8')
print(json.dumps({k: v for k, v in manifest.items() if k != 'installed_packages'}, indent=2))
