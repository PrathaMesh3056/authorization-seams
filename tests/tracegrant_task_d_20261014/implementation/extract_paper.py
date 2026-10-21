"""Read-only extraction and rendering; no code from the paper is executed."""
from pathlib import Path
import json
import subprocess
import shutil
from pypdf import PdfReader

root = Path(__file__).resolve().parents[1]
pdf = root / 'sources/tracegrant-2608.21126v1.pdf'
reader = PdfReader(pdf)
pages = [{'page': i + 1, 'text': p.extract_text(extraction_mode='layout')}
         for i, p in enumerate(reader.pages)]
(root / 'sources/paper-pages.json').write_text(json.dumps(pages, indent=2), encoding='utf-8')
(root / 'sources/paper.txt').write_text('\n'.join(
    f"\n=== PAGE {p['page']} ===\n{p['text']}" for p in pages), encoding='utf-8')
print(f'Extracted {len(pages)} pages')
renderer = shutil.which('pdftoppm')
if renderer:
    # Method section pages, including Algorithm 1 and the displayed equations.
    for page in range(5, 9):
        command = [renderer, '-f', str(page), '-l', str(page), '-scale-to', '1800',
                   '-singlefile', '-png', str(pdf), str(root / f'sources/page-{page:02}')]
        print(json.dumps(command))
        subprocess.run(command, check=True)
else:
    print('NOT DONE: visual rendering; pdftoppm unavailable')
