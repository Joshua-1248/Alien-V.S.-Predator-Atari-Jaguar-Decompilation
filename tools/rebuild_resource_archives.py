#!/usr/bin/env python3
from pathlib import Path
import argparse,json,csv,struct,zlib,binascii,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import gzip124_atari_resource as old
from deflate_tokens import modern_tokens
from gzip124_atari_matcher import AtariGzipMatcher
from resource_batch_state import update_persistent_window

def trailer(data):
    return struct.pack("<II",binascii.crc32(data)&0xffffffff,len(data)&0xffffffff)

def old_from_modern_tokens(data):
    toks,_=modern_tokens(data)
    raw,_,_=old.encode_old_blocks_from_tokens(toks)
    return raw

def matcher_raw(data,prior_payloads):
    win=bytearray(65536)
    for p in prior_payloads:
        update_persistent_window(win,p)
    m=AtariGzipMatcher(); m.window[:]=win
    toks=[]
    for x in m.tokens(data):
        if x[0]=="L": toks.append(("L",x[2],x[1]))
        else: toks.append(("M",x[2],x[3],x[1]))
    raw,_,_=old.encode_old_blocks_from_tokens(toks)
    return raw

def member(data,header,raw):
    return header+raw+trailer(data)

def build_aafs(sprite_root,headers):
    meta=json.loads((sprite_root/"metadata.json").read_text())
    dirs={int(p.name[:3]):p for p in sprite_root.iterdir()
          if p.is_dir() and p.name[:3].isdigit()}
    out=bytearray()
    for i,r in enumerate(meta):
        data=(dirs[i]/"payload.aaf").read_bytes()
        if i<58:
            tag=b"NONE"; stored=data
        else:
            tag=b"GZIP"
            raw=old_from_modern_tokens(data)
            stored=member(data,bytes.fromhex(headers[str(i)]),raw)
        out += tag+struct.pack(">I",len(stored))+stored
        out += b"\0"*((-len(out))%4)
    out += b"\0"*4
    return bytes(out)

def build_files(files_root,headers,modes):
    rows=list(csv.DictReader(open(files_root/"metadata/files_inventory.csv",newline="")))
    payloads={int(r["index"]):(files_root/r["output"]).read_bytes() for r in rows}
    out=bytearray()
    for r in rows:
        i=int(r["index"]); data=payloads[i]; tag=r["tag"].encode()
        if tag!=b"GZIP":
            stored=data
        else:
            md=modes[str(i)]
            if md["mode"]=="modern_raw_exact":
                c=zlib.compressobj(9,zlib.DEFLATED,-15,int(md["memLevel"]),zlib.Z_DEFAULT_STRATEGY)
                raw=c.compress(data)+c.flush()
            elif md["mode"]=="old_encoder_modern_tokens":
                raw=old_from_modern_tokens(data)
            elif md["mode"]=="persistent_matcher":
                raw=matcher_raw(data,[payloads[j] for j in md["priors"]])
            else:
                raise ValueError(md)
            stored=member(data,bytes.fromhex(headers[str(i)]),raw)
        out += tag+struct.pack(">I",len(stored))+stored
        out += b"\0"*((-len(out))%4)
    out += b"\0"*4
    return bytes(out)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--sprites",required=True)
    ap.add_argument("--files-root",required=True)
    ap.add_argument("--headers",required=True)
    ap.add_argument("--modes",required=True)
    ap.add_argument("--out-aafs",required=True)
    ap.add_argument("--out-files",required=True)
    ns=ap.parse_args()
    h=json.loads(Path(ns.headers).read_text())
    modes=json.loads(Path(ns.modes).read_text())
    Path(ns.out_aafs).write_bytes(build_aafs(Path(ns.sprites),h["AAFS"]))
    Path(ns.out_files).write_bytes(build_files(Path(ns.files_root),h["FILES"],modes))
if __name__=="__main__": main()
