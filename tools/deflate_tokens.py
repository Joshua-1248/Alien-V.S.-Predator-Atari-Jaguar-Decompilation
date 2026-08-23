#!/usr/bin/env python3
import zlib
from gzip124_atari_resource import LEN_BASE,LEN_EXTRA,DIST_BASE,DIST_EXTRA,BL_ORDER

class BR:
    def __init__(self,b): self.b=b; self.p=0
    def bits(self,n):
        v=0
        for i in range(n):
            v|=((self.b[self.p>>3]>>(self.p&7))&1)<<i
            self.p+=1
        return v
    def align(self): self.p=(self.p+7)&~7

def rev(x,n):
    r=0
    for _ in range(n): r=(r<<1)|(x&1); x>>=1
    return r

def table(lens):
    m=max(lens) if lens else 0
    cnt=[0]*(m+1)
    for L in lens:
        if L: cnt[L]+=1
    nxt=[0]*(m+1); c=0
    for b in range(1,m+1):
        c=(c+cnt[b-1])<<1; nxt[b]=c
    d={}
    for sym,L in enumerate(lens):
        if L:
            d[(rev(nxt[L],L),L)]=sym
            nxt[L]+=1
    return d,m

def getsym(br,t):
    d,m=t; v=0
    for n in range(1,m+1):
        v|=br.bits(1)<<(n-1)
        if (v,n) in d: return d[(v,n)]
    raise ValueError("bad Huffman code")

def parse_raw(raw):
    br=BR(raw); tokens=[]; out=bytearray(); blocks=[]
    while True:
        final=br.bits(1); typ=br.bits(2)
        if typ==0:
            br.align(); n=br.bits(16); nn=br.bits(16)
            assert (n^0xffff)==nn
            for _ in range(n):
                x=br.bits(8); tokens.append(("L",x,len(out))); out.append(x)
        else:
            if typ==1:
                ll=[0]*288
                for i in range(0,144): ll[i]=8
                for i in range(144,256): ll[i]=9
                for i in range(256,280): ll[i]=7
                for i in range(280,288): ll[i]=8
                dd=[5]*32
            elif typ==2:
                hl=br.bits(5)+257; hd=br.bits(5)+1; hc=br.bits(4)+4
                bl=[0]*19
                for i in range(hc): bl[BL_ORDER[i]]=br.bits(3)
                bt=table(bl); arr=[]
                while len(arr)<hl+hd:
                    q=getsym(br,bt)
                    if q<=15: arr.append(q)
                    elif q==16: arr.extend([arr[-1]]*(br.bits(2)+3))
                    elif q==17: arr.extend([0]*(br.bits(3)+3))
                    else: arr.extend([0]*(br.bits(7)+11))
                ll=arr[:hl]+[0]*(288-hl)
                dd=arr[hl:hl+hd]+[0]*(32-hd)
            else:
                raise ValueError("reserved block")
            lt=table(ll); dt=table(dd)
            while True:
                q=getsym(br,lt)
                if q<256:
                    tokens.append(("L",q,len(out))); out.append(q)
                elif q==256:
                    break
                else:
                    li=q-257
                    L=LEN_BASE[li]+(br.bits(LEN_EXTRA[li]) if LEN_EXTRA[li] else 0)
                    ds=getsym(br,dt)
                    D=DIST_BASE[ds]+(br.bits(DIST_EXTRA[ds]) if DIST_EXTRA[ds] else 0)
                    p=len(out); tokens.append(("M",L,D,p))
                    for _ in range(L): out.append(out[-D])
        blocks.append((len(tokens),len(out),typ))
        if final: break
    return tokens,bytes(out),blocks

def modern_tokens(data,mem_level=8):
    c=zlib.compressobj(9,zlib.DEFLATED,-15,mem_level,zlib.Z_DEFAULT_STRATEGY)
    raw=c.compress(data)+c.flush()
    toks,out,blocks=parse_raw(raw)
    assert out==data
    return toks,blocks
