#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, sys
EXPECTED='b31ca5c2415881ce50d0c076d327297547214a6240f0058b0f225a74f7ce440b'
if len(sys.argv)!=2:
    raise SystemExit('usage: verify_canonical_rom.py <Alien vs. Predator retail .jag>')
p=Path(sys.argv[1]); b=p.read_bytes(); h=hashlib.sha256(b).hexdigest()
print('bytes',len(b)); print('sha256',h); print('canonical', len(b)==4194304 and h==EXPECTED)
raise SystemExit(0 if len(b)==4194304 and h==EXPECTED else 1)
