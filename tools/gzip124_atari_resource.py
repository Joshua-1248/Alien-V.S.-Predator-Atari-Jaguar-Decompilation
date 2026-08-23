#!/usr/bin/env python3
import argparse, binascii, struct, hashlib
from pathlib import Path

WSIZE=32768; MAX_MATCH=258; MIN_MATCH=3
MAX_DIST=WSIZE-MAX_MATCH-MIN_MATCH-1
HASH_BITS=15; HASH_SIZE=1<<HASH_BITS; HASH_MASK=HASH_SIZE-1
WMASK=WSIZE-1; H_SHIFT=(HASH_BITS+MIN_MATCH-1)//MIN_MATCH
TOO_FAR=4096
LEN_BASE=[3,4,5,6,7,8,9,10,11,13,15,17,19,23,27,31,35,43,51,59,67,83,99,115,131,163,195,227,258]
LEN_EXTRA=[0,0,0,0,0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,0]
DIST_BASE=[1,2,3,4,5,7,9,13,17,25,33,49,65,97,129,193,257,385,513,769,1025,1537,2049,3073,4097,6145,8193,12289,16385,24577]
DIST_EXTRA=[0,0,0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,11,11,12,12,13,13]
BL_ORDER=[16,17,18,0,8,7,9,6,10,5,11,4,12,3,13,2,14,1,15]
HEAP_SIZE=573

def len_symbol(L):
    if L==258:return 285
    for i,(b,e) in enumerate(zip(LEN_BASE,LEN_EXTRA)):
        top=b+((1<<e)-1 if e else 0)
        if i==27: top=257
        if L<=top:return 257+i
    raise ValueError(L)

def dist_symbol(d):
    for i,(b,e) in enumerate(zip(DIST_BASE,DIST_EXTRA)):
        if d<=b+((1<<e)-1 if e else 0): return i
    raise ValueError(d)

def tokenize(data):
    n=len(data)
    win=bytearray(data+b"\0"*(65536+MAX_MATCH+16-len(data)))
    prev=[0]*WSIZE; head=[0]*HASH_SIZE
    ins_h=0
    for j in range(2): ins_h=((ins_h<<H_SHIFT)^win[j])&HASH_MASK
    strstart=0; lookahead=n; match_start=0
    match_length=2; match_available=False; out=[]

    def insert(s):
        nonlocal ins_h
        ins_h=((ins_h<<H_SHIFT)^win[s+2])&HASH_MASK
        mh=head[ins_h]
        prev[s&WMASK]=mh&0xffff
        head[ins_h]=s&0xffff
        return mh

    def longest(cur, prev_length):
        nonlocal match_start
        chain=4096; best=prev_length
        limit=strstart-MAX_DIST if strstart>MAX_DIST else 0
        if prev_length>=32: chain>>=2
        chain-=1
        scan_start=(win[strstart]<<8)|win[strstart+1]
        scan_end=(win[strstart+best-1]<<8)|win[strstart+best]
        cm=cur&0xffff
        while True:
            test_end=(win[cm+best-1]<<8)|win[cm+best]
            test_start=(win[cm]<<8)|win[cm+1]
            if test_end==scan_end and test_start==scan_start:
                k=3
                while k<258 and win[cm+k]==win[strstart+k]: k+=1
                if k>best:
                    best=k; match_start=cm
                    scan_end=(win[strstart+best-1]<<8)|win[strstart+best]
                    if best>=258:return best
            cm=prev[cm&WMASK]&0xffff
            if cm <= (limit&0xffff): return best
            chain=(chain-1)&0xffffffff
            if (chain&0xffff)==0xffff:return best

    while lookahead:
        hash_head=insert(strstart)
        prev_length=match_length; prev_match=match_start
        match_length=2
        if hash_head and prev_length<258 and strstart-hash_head<=MAX_DIST:
            match_length=longest(hash_head,prev_length)
            if match_length>lookahead:match_length=lookahead
            if match_length==3 and strstart-match_start>TOO_FAR:match_length-=1
        if prev_length>=3 and match_length<=prev_length:
            out.append(("M",prev_length,(strstart-1)-prev_match,strstart-1))
            lookahead-=prev_length-1
            pl=prev_length-2
            while True:
                strstart+=1; insert(strstart); pl-=1
                if pl==0:break
            match_available=False;match_length=2;strstart+=1
        elif match_available:
            out.append(("L",win[strstart-1],strstart-1))
            strstart+=1;lookahead-=1
        else:
            match_available=True;strstart+=1;lookahead-=1
    if match_available:out.append(("L",win[strstart-1],strstart-1))
    return out

def dcode(d): return dist_symbol(d)

def boundaries(tokens):
    result=[]; count=dist_count=0; df=[0]*30
    block_start=0; last_end=0
    for absolute,t in enumerate(tokens,1):
        if t[0]=="M":
            L,d,pos=t[1],t[2],t[3]; dist_count+=1;df[dcode(d)]+=1;end=pos+L
        else:end=t[2]+1
        count+=1;last_end=end;flush=False
        if (count&0xfff)==0:
            estimate=count*8
            for i in range(30):estimate+=df[i]*(5+DIST_EXTRA[i])
            estimate>>=3
            if dist_count<count/2 and estimate<(end-block_start)/2:flush=True
        if count==0x7fff:flush=True
        if flush:
            result.append((absolute,end));count=dist_count=0;df=[0]*30;block_start=end
    if not result or result[-1][0]!=len(tokens):result.append((len(tokens),last_end))
    return result

def tree_lengths(freq, elems, max_length):
    f=list(freq)+[0]*(HEAP_SIZE-len(freq)); ln=[0]*HEAP_SIZE
    dad=[0]*HEAP_SIZE;depth=[0]*HEAP_SIZE;heap=[0]*HEAP_SIZE
    hlen=0;hmax=HEAP_SIZE;max_code=-1
    for n in range(elems):
        if f[n]:
            hlen+=1;heap[hlen]=n;max_code=n
    while hlen<2:
        if max_code<2:max_code+=1;node=max_code
        else:node=0
        hlen+=1;heap[hlen]=node;f[node]=1
    def smaller(n,m):return f[n]<f[m] or (f[n]==f[m] and depth[n]<=depth[m])
    def down(k):
        nonlocal hlen
        v=heap[k];j=k*2
        while j<=hlen:
            if j<hlen and smaller(heap[j+1],heap[j]):j+=1
            if smaller(v,heap[j]):break
            heap[k]=heap[j];k=j;j*=2
        heap[k]=v
    for n in range(hlen//2,0,-1):down(n)
    node=elems
    while hlen>=2:
        n=heap[1];heap[1]=heap[hlen];hlen-=1;down(1);m=heap[1]
        hmax-=1;heap[hmax]=n;hmax-=1;heap[hmax]=m
        f[node]=f[n]+f[m];depth[node]=max(depth[n],depth[m])+1
        dad[n]=dad[m]=node;heap[1]=node;node+=1;down(1)
    hmax-=1;heap[hmax]=heap[1]
    bl=[0]*(max_length+1);overflow=0;ln[heap[hmax]]=0
    for h in range(hmax+1,HEAP_SIZE):
        n=heap[h];bits=ln[dad[n]]+1
        if bits>max_length:bits=max_length;overflow+=1
        ln[n]=bits
        if n<=max_code:bl[bits]+=1
    # gzip 1.2.4 trees.c gen_bitlen(): if no overflow occurred, the
    # initially assigned lengths are already final.  Return immediately.
    if overflow==0:
        return ln[:elems],max_code
    while overflow>0:
        bits=max_length-1
        while bl[bits]==0:bits-=1
        bl[bits]-=1;bl[bits+1]+=2;bl[max_length]-=1;overflow-=2
    h=HEAP_SIZE
    for bits in range(max_length,0,-1):
        cnt=bl[bits]
        while cnt:
            h-=1;m=heap[h]
            if m>max_code:continue
            ln[m]=bits;cnt-=1
    return ln[:elems],max_code

def scan_freq(lens,max_code):
    f=[0]*19;ext=lens[:max_code+1]+[0xffff]
    prevlen=-1;nextlen=ext[0];count=0;mx=7;mn=4
    if nextlen==0:mx=138;mn=3
    for n in range(max_code+1):
        cur=nextlen;nextlen=ext[n+1];count+=1
        if count<mx and cur==nextlen:continue
        if count<mn:f[cur]+=count
        elif cur:
            if cur!=prevlen:f[cur]+=1
            f[16]+=1
        elif count<=10:f[17]+=1
        else:f[18]+=1
        count=0;prevlen=cur
        if nextlen==0:mx,mn=138,3
        elif cur==nextlen:mx,mn=6,3
        else:mx,mn=7,4
    return f

def reverse(c,n):
    r=0
    for _ in range(n):r=(r<<1)|(c&1);c>>=1
    return r

def make_codes(lens,maxbits):
    cnt=[0]*(maxbits+1)
    for n in lens:
        if n:cnt[n]+=1
    nxt=[0]*(maxbits+1);code=0
    for b in range(1,maxbits+1):code=(code+cnt[b-1])<<1;nxt[b]=code
    out=[0]*len(lens)
    for i,L in enumerate(lens):
        if L:out[i]=reverse(nxt[L],L);nxt[L]+=1
    return out

class BW:
    def __init__(self):self.o=bytearray();self.v=0;self.n=0
    def bits(self,v,n):
        self.v|=(v&((1<<n)-1))<<self.n;self.n+=n
        while self.n>=8:self.o.append(self.v&255);self.v>>=8;self.n-=8
    def done(self):
        if self.n:self.o.append(self.v&255)
        return bytes(self.o)

def send_tree(w,lens,max_code,bl,bc):
    ext=lens[:max_code+1]+[0xffff]
    prev=-1;nxt=ext[0];cnt=0;mx=7;mn=4
    if nxt==0:mx,mn=138,3
    def sc(s):w.bits(bc[s],bl[s])
    for i in range(max_code+1):
        cur=nxt;nxt=ext[i+1];cnt+=1
        if cnt<mx and cur==nxt:continue
        if cnt<mn:
            for _ in range(cnt):sc(cur)
        elif cur:
            if cur!=prev:sc(cur);cnt-=1
            sc(16);w.bits(cnt-3,2)
        elif cnt<=10:sc(17);w.bits(cnt-3,3)
        else:sc(18);w.bits(cnt-11,7)
        cnt=0;prev=cur
        if nxt==0:mx,mn=138,3
        elif cur==nxt:mx,mn=6,3
        else:mx,mn=7,4

def dynamic_block(w,toks,final):
    lf=[0]*286;df=[0]*30
    for t in toks:
        if t[0]=="L":lf[t[1]]+=1
        else:lf[len_symbol(t[1])]+=1;df[dist_symbol(t[2])]+=1
    lf[256]+=1
    ll,mc=tree_lengths(lf,286,15);dd,md=tree_lengths(df,30,15)
    bf=scan_freq(ll,mc);q=scan_freq(dd,md);bf=[a+b for a,b in zip(bf,q)]
    bl,_=tree_lengths(bf,19,7);mi=18
    while mi>=3 and bl[BL_ORDER[mi]]==0:mi-=1
    lc=make_codes(ll,15);dc=make_codes(dd,15);bc=make_codes(bl,7)
    w.bits(5 if final else 4,3);w.bits(mc+1-257,5);w.bits(md,5);w.bits(mi+1-4,4)
    for i in range(mi+1):w.bits(bl[BL_ORDER[i]],3)
    send_tree(w,ll,mc,bl,bc);send_tree(w,dd,md,bl,bc)
    for t in toks:
        if t[0]=="L":w.bits(lc[t[1]],ll[t[1]])
        else:
            L,d=t[1],t[2];s=len_symbol(L);w.bits(lc[s],ll[s]);li=s-257
            if LEN_EXTRA[li]:w.bits(L-LEN_BASE[li],LEN_EXTRA[li])
            ds=dist_symbol(d);w.bits(dc[ds],dd[ds])
            if DIST_EXTRA[ds]:w.bits(d-DIST_BASE[ds],DIST_EXTRA[ds])
    w.bits(lc[256],ll[256])

def raw_deflate(data):
    toks=tokenize(data);bs=boundaries(toks);w=BW();st=0
    for i,(en,_) in enumerate(bs):
        dynamic_block(w,toks[st:en],i==len(bs)-1);st=en
    return w.done()

def gzip124_atari(data,header10):
    raw=raw_deflate(data)
    return header10+raw+struct.pack("<II",binascii.crc32(data)&0xffffffff,len(data)&0xffffffff)

# ---------------------------------------------------------------------------
# M54: gzip 1.2.4 STATIC-vs-DYNAMIC block selection
# ---------------------------------------------------------------------------
_FIXED_LL=[0]*288
for _i in range(0,144): _FIXED_LL[_i]=8
for _i in range(144,256): _FIXED_LL[_i]=9
for _i in range(256,280): _FIXED_LL[_i]=7
for _i in range(280,288): _FIXED_LL[_i]=8
_FIXED_DD=[5]*32
_FIXED_LC=make_codes(_FIXED_LL,9)
_FIXED_DC=make_codes(_FIXED_DD,5)

def static_block(w,toks,final):
    # LSB-first: BFINAL plus BTYPE=01.
    w.bits(3 if final else 2,3)
    for t in toks:
        if t[0]=="L":
            sym=t[1]
            w.bits(_FIXED_LC[sym],_FIXED_LL[sym])
        else:
            L,d=t[1],t[2]
            ls=len_symbol(L)
            w.bits(_FIXED_LC[ls],_FIXED_LL[ls])
            li=ls-257
            if LEN_EXTRA[li]:
                w.bits(L-LEN_BASE[li],LEN_EXTRA[li])
            ds=dist_symbol(d)
            w.bits(_FIXED_DC[ds],5)
            if DIST_EXTRA[ds]:
                w.bits(d-DIST_BASE[ds],DIST_EXTRA[ds])
    w.bits(_FIXED_LC[256],_FIXED_LL[256])

class CountBW:
    def __init__(self): self.nbits=0
    def bits(self,v,n): self.nbits+=n

def block_costs(toks):
    d=CountBW(); dynamic_block(d,toks,False)
    s=CountBW(); static_block(s,toks,False)
    # gzip's flush_block compares byte-rounded opt_len/static_len (+3 header).
    return {
        "dynamic_bits":d.nbits,
        "static_bits":s.nbits,
        "dynamic_bytes":(d.nbits+7)//8,
        "static_bytes":(s.nbits+7)//8,
    }

def chosen_block(w,toks,final):
    c=block_costs(toks)
    # gzip 1.2.4 chooses static on equality.
    if c["static_bytes"] <= c["dynamic_bytes"]:
        static_block(w,toks,final)
        return "static"
    dynamic_block(w,toks,final)
    return "dynamic"

def encode_old_blocks_from_tokens(tokens):
    bs=boundaries(tokens)
    w=BW(); st=0; kinds=[]
    for i,(en,endpos) in enumerate(bs):
        kinds.append(chosen_block(w,tokens[st:en],i==len(bs)-1))
        st=en
    return w.done(),bs,kinds

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--header",default="1f8b0800dcc16f2e0205")
    ns=ap.parse_args()
    data=Path(ns.input).read_bytes()
    out=gzip124_atari(data,bytes.fromhex(ns.header))
    Path(ns.output).write_bytes(out)
    print("bytes",len(out))
    print("sha256",hashlib.sha256(out).hexdigest())

if __name__=="__main__":main()
