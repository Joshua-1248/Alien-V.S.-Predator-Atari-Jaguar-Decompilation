#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,struct,zlib,csv,json
CANON='b31ca5c2415881ce50d0c076d327297547214a6240f0058b0f225a74f7ce440b'
STAGES={
 'builder_residue':(0x14104,0x15000),
 'rom_ptrs':(0x15C08,0x16008),
 'overlays_fonts':(0x16A9A8,0x16B6E8),
 'sound_music':(0x16B6E8,0x2F55F8),
 'pause_ui':(0x2F55F8,0x2F8178),
 'creature_lcs':(0x3FBA34,0x3FD30C),
}
def gzip_member_payload(stored): return zlib.decompress(stored,31)
def parse_archive(blob,start,end,count,outroot,is_aafs=False):
    p=start; rows=[]; headers={}
    for i in range(count):
        tag=blob[p:p+4].decode('ascii'); n=int.from_bytes(blob[p+4:p+8],'big'); s=p+8; e=s+n
        stored=blob[s:e]
        if tag=='GZIP':
            data=gzip_member_payload(stored); headers[str(i)]=stored[:10].hex()
        else: data=stored
        if is_aafs:
            d=outroot/f'{i:03d}_record'; d.mkdir(parents=True,exist_ok=True); rel=f'{i:03d}_record/payload.aaf'; (d/'payload.aaf').write_bytes(data)
        else:
            d=outroot/'payloads'; d.mkdir(parents=True,exist_ok=True); rel=f'payloads/{i:03d}.bin'; (outroot/rel).write_bytes(data)
        rows.append({'index':i,'tag':tag,'stored_size':n,'decoded_size':len(data),'output':rel,'offset':p})
        p=e; p=(p+3)&~3
    # historical final u32 zero terminator
    assert blob[p:p+4]==b'\0'*4
    p+=4
    assert p==end,(hex(p),hex(end))
    return rows,headers

def split_stage_by_ptrs(blob,ptrs,a,b,outdir):
    # Split at every valid ROM pointer into the stage, retaining prefix/suffix and exact ordering.
    cuts={a,b}
    for v in ptrs:
        if 0x800000+a <= v < 0x800000+b: cuts.add(v-0x800000)
    cuts=sorted(cuts); manifest=[]; outdir.mkdir(parents=True,exist_ok=True)
    for i,(s,e) in enumerate(zip(cuts,cuts[1:])):
        fn=f'{i:03d}_{s:06X}_{e:06X}.bin'; (outdir/fn).write_bytes(blob[s:e]); manifest.append({'file':fn,'start':s,'end':e,'size':e-s})
    return manifest

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--retail-rom',required=True); ap.add_argument('--out-dir',required=True); ns=ap.parse_args()
    b=Path(ns.retail_rom).read_bytes(); h=hashlib.sha256(b).hexdigest()
    if len(b)!=0x400000 or h!=CANON: raise SystemExit('canonical World ROM required')
    root=Path(ns.out_dir); root.mkdir(parents=True,exist_ok=True)
    # Non-code build data is recovered locally from the user's ROM rather than
    # distributed in this code-only repository.
    (root/'rom_dta_prefix.bin').write_bytes(b[0x33B0:0x3804])
    dobj=zlib.decompressobj(31)
    rdb_dta=dobj.decompress(b[0xE840:])
    if not dobj.eof:
        raise SystemExit('could not decode retail RDBDTA gzip member')
    (root/'rdb_dta.bin').write_bytes(rdb_dta)
    (root/'trig_tables.bin').write_bytes(b[0x15000:0x15C08])
    # small non-semantic/historical metadata blobs
    for name,(a,e) in STAGES.items():
        if name in ('overlays_fonts','sound_music','pause_ui','creature_lcs'): continue
        (root/f'{name}.bin').write_bytes(b[a:e])
    ptrraw=b[0x15C08:0x16008]; ptrs=[int.from_bytes(ptrraw[i:i+4],'big') for i in range(0,0x400,4)]
    # AAFS decoded per record
    aroot=root/'aafs'; rows,ah=parse_archive(b,0x16008,0x16A9A8,63,aroot,True)
    (aroot/'metadata.json').write_text(json.dumps(rows,indent=2))
    # FILES.DAT decoded per record
    froot=root/'files'; (froot/'metadata').mkdir(parents=True,exist_ok=True)
    frows,fh=parse_archive(b,0x2F8178,0x3FBA34,240,froot,False)
    with open(froot/'metadata/files_inventory.csv','w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['index','tag','stored_size','decoded_size','output','offset']); w.writeheader(); w.writerows(frows)
    headers={'AAFS':ah,'FILES':fh}; (root/'gzip_headers.json').write_text(json.dumps(headers,indent=2))
    # Other stages split by actual pointer boundaries instead of opaque megabyte copies.
    split={}
    for name in ('overlays_fonts','sound_music','pause_ui','creature_lcs'):
        a,e=STAGES[name]; split[name]=split_stage_by_ptrs(b,ptrs,a,e,root/name)
    (root/'stage_segments.json').write_text(json.dumps(split,indent=2))
    (root/'manifest.json').write_text(json.dumps({'canonical_sha256':h,'stages':STAGES,'aafs_records':63,'files_records':240},indent=2))
    print('asset extraction complete')
    print('AAFS records',len(rows),'FILES records',len(frows))
    print('granular segments',sum(len(v) for v in split.values()))
if __name__=='__main__': main()
