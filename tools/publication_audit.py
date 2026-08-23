#!/usr/bin/env python3
from pathlib import Path
import sys
root=Path(__file__).resolve().parents[1]
blocked={'.jag','.j64','.rom','.wav','.png','.bmp','.tga','.jpg','.jpeg','.mp3','.flac'}
bad=[]
for p in root.rglob('*'):
    if p.is_file() and p.suffix.lower() in blocked:
        bad.append(p.relative_to(root))
if bad:
    print('FAIL: prohibited publication payloads found:')
    for x in bad: print(x)
    sys.exit(1)
print('PASS: no ROM/media asset payloads found')
