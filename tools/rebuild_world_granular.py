#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,re,zlib,struct,binascii,json,sys,tempfile,subprocess
HERE=Path(__file__).resolve().parent; ROOT=HERE.parent
sys.path.insert(0,str(HERE))
from gzip124_atari_matcher import AtariGzipMatcher
from gzip124_atari_resource import encode_old_blocks_from_tokens
from generate_jaguar_auth import generate_prefix
from rebuild_resource_archives import build_aafs,build_files
CANON='b31ca5c2415881ce50d0c076d327297547214a6240f0058b0f225a74f7ce440b'
RDBTXT_HEADER=bytes.fromhex('1f8b0800c8c16f2e0205'); RDBDTA_HEADER=bytes.fromhex('1f8b0800dcc16f2e0205')
def parse_words(name):
 t=(ROOT/'src'/'frozen_exact'/name).read_text(); vals=[int(x,16) for x in re.findall(r'\bdc\.w\s+\$([0-9A-Fa-f]{4})',t)]; return b''.join(x.to_bytes(2,'big') for x in vals)
def trailer(d): return struct.pack('<II',binascii.crc32(d)&0xffffffff,len(d)&0xffffffff)
def gzip_txt(d):
 c=zlib.compressobj(9,zlib.DEFLATED,-15,9,zlib.Z_DEFAULT_STRATEGY); return RDBTXT_HEADER+c.compress(d)+c.flush()+trailer(d)
def gzip_dta(d):
 m=AtariGzipMatcher(); toks=[]
 for x in m.tokens(d): toks.append(('L',x[2],x[1]) if x[0]=='L' else ('M',x[2],x[3],x[1]))
 raw,_,_=encode_old_blocks_from_tokens(toks); return RDBDTA_HEADER+raw+trailer(d)
def concat_segments(root,name,manifest):
 return b''.join((root/name/x['file']).read_bytes() for x in manifest[name])
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--assets',required=True); ap.add_argument('--jagcrypt-c',required=True); ap.add_argument('--md5-dat',required=True); ap.add_argument('--output',required=True); ap.add_argument('--verify-retail'); ns=ap.parse_args()
 a=Path(ns.assets); headers=json.loads((a/'gzip_headers.json').read_text()); modes=json.loads((ROOT/'metadata/files_gzip_modes.json').read_text()); seg=json.loads((a/'stage_segments.json').read_text())
 romtxt=parse_words('ROM_TEXT_frozen_exact.s'); fixed=parse_words('ROM_DTA_PREFIX_frozen_exact.s'); rtxt=parse_words('RDB_TEXT_frozen_exact.s'); rdta=parse_words('RDB_DTA_frozen_exact.s'); trig=parse_words('TRIG_TABLES_frozen_exact.s')
 romdta=fixed+gzip_txt(rtxt)+b'\0'+gzip_dta(rdta)+b'\0'*3
 if len(romtxt)!=0x13b0 or len(romdta)!=(0x14104-0x33b0) or len(trig)!=0xc08: raise SystemExit('frozen source size failure')
 aafs=build_aafs(a/'aafs',headers['AAFS']); files=build_files(a/'files',headers['FILES'],modes)
 stages={name:concat_segments(a,name,seg) for name in ('overlays_fonts','sound_music','pause_ui','creature_lcs')}
 expected={'overlays_fonts':0x16B6E8-0x16A9A8,'sound_music':0x2F55F8-0x16B6E8,'pause_ui':0x2F8178-0x2F55F8,'creature_lcs':0x3FD30C-0x3FBA34}
 for k,v in stages.items():
  if len(v)!=expected[k]: raise SystemExit(f'{k} size mismatch')
 cart=bytearray(b'\xff'*0x400000)
 cart[0x2000:0x33b0]=romtxt; cart[0x33b0:0x14104]=romdta
 cart[0x14104:0x15000]=(a/'builder_residue.bin').read_bytes(); cart[0x15000:0x15c08]=trig; cart[0x15c08:0x16008]=(a/'rom_ptrs.bin').read_bytes()
 cart[0x16008:0x16A9A8]=aafs; cart[0x16A9A8:0x16B6E8]=stages['overlays_fonts']; cart[0x16B6E8:0x2F55F8]=stages['sound_music']; cart[0x2F55F8:0x2F8178]=stages['pause_ui']; cart[0x2F8178:0x3FBA34]=files; cart[0x3FBA34:0x3FD30C]=stages['creature_lcs']
 auth,_=generate_prefix(bytes(cart),Path(ns.jagcrypt_c).read_text(errors='replace'),Path(ns.md5_dat).read_text(errors='replace')); cart[:0x2000]=auth
 Path(ns.output).write_bytes(cart); h=hashlib.sha256(cart).hexdigest(); print('bytes',len(cart)); print('sha256',h)
 if ns.verify_retail:
  r=Path(ns.verify_retail).read_bytes(); dif=sum(x!=y for x,y in zip(cart,r)); print('differing_bytes',dif); print('RESULT','BYTE-EXACT' if dif==0 and h==CANON else 'FAIL'); raise SystemExit(0 if dif==0 and h==CANON else 1)
if __name__=='__main__': main()
