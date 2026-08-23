#!/usr/bin/env python3
"""
Independent Python implementation of the Atari Jaguar cartridge-auth generation
flow documented by Atari's preserved JAGCRYPT.C / RSA.C.

This script intentionally does NOT embed Atari's MD5.DAT or RSA key arrays.
Point it at a checkout of the publicly preserved JagCrypt material.

Usage:
  python3 generate_jaguar_auth.py \
      --rom retail_or_unsigned_4MiB_image.jag \
      --jagcrypt-c /path/to/JAGCRYPT.C \
      --md5-dat /path/to/MD5.DAT \
      --out-prefix generated_prefix.bin

For the AvP retail layout, the payload hashed is ROM offset 0x2000 onward.
"""
from pathlib import Path
import argparse, re

MASK=0xffffffff
INIT=[0x67452301,0xEFCDAB89,0x98BADCFE,0x10325476]
T=[
0xD76AA478,0xE8C7B756,0x242070DB,0xC1BDCEEE,0xF57C0FAF,0x4787C62A,0xA8304613,0xFD469501,
0x698098D8,0x8B44F7AF,0xFFFF5BB1,0x895CD7BE,0x6B901122,0xFD987193,0xA679438E,0x49B40821,
0xF61E2562,0xC040B340,0x265E5A51,0xE9B6C7AA,0xD62F105D,0x02441453,0xD8A1E681,0xE7D3FBC8,
0x21E1CDE6,0xC33707D6,0xF4D50D87,0x455A14ED,0xA9E3E905,0xFCEFA3F8,0x676F02D9,0x8D2A4C8A,
0xFFFA3942,0x8771F681,0x6D9D6122,0xFDE5380C,0xA4BEEA44,0x4BDECFA9,0xF6BB4B60,0xBEBFBC70,
0x289B7EC6,0xEAA127FA,0xD4EF3085,0x04881D05,0xD9D4D039,0xE6DB99E5,0x1FA27CF8,0xC4AC5665,
0xF4292244,0x432AFF97,0xAB9423A7,0xFC93A039,0x655B59C3,0x8F0CCC92,0xFFEFF47D,0x85845DD1,
0x6FA87E4F,0xFE2CE6E0,0xA3014314,0x4E0811A1,0xF7537E82,0xBD3AF235,0x2AD7D2BB,0xEB86D391]
ROTS=[7,12,17,22,5,9,14,20,4,11,16,23,6,10,15,21]
INITX=[0,4,20,0]
XINC=[4,20,12,28]
ROMCONFIG=bytes.fromhex("040404040080200000000000")

def rol(x,n):
    x &= MASK
    return ((x<<n)|(x>>(32-n))) & MASK

def md5trans(state, block):
    """Exact Atari MD5trans semantics: Getlong reads each input word big-endian."""
    a,b,c,d=state
    ti=0
    for species in range(4):
        idx=INITX[species]
        incr=XINC[species]
        ri=0
        for _ in range(16):
            if species==0:
                accum=(b&c)|((~b)&d)
            elif species==1:
                accum=(b&d)|(c&(~d))
            elif species==2:
                accum=(b^d)^c
            else:
                accum=c^(b|(~d))
            word=int.from_bytes(block[idx:idx+4],"big")
            idx=(idx+incr)&0x3f
            accum=(accum+word+T[ti]+a)&MASK
            ti+=1
            accum=rol(accum,ROTS[species*4+ri])
            ri=(ri+1)&3
            accum=(accum+b)&MASK
            a,d,c,b=d,c,b,accum
    state[0]=(state[0]+a)&MASK
    state[1]=(state[1]+b)&MASK
    state[2]=(state[2]+c)&MASK
    state[3]=(state[3]+d)&MASK

def parse_key_array(text, name):
    m=re.search(r"\bbyte\s+"+re.escape(name)+r"\s*\[\s*128\s*\]\s*=\s*\{(.*?)\};",
                text,re.S)
    if not m:
        raise ValueError(f"could not locate {name}[128] in JAGCRYPT.C")
    vals=[int(x,16) for x in re.findall(r"0x([0-9A-Fa-f]{1,2})",m.group(1))]
    if len(vals)<65:
        raise ValueError(f"{name} has only {len(vals)} explicit bytes; need >=65")
    return bytes(vals[:65])

def parse_md5_dat(text):
    vals=[int(x,16) for x in re.findall(r"0x([0-9A-Fa-f]{2})",text)]
    if len(vals)<648:
        raise ValueError(f"MD5.DAT decoded to {len(vals)} bytes; expected >=648")
    return bytes(vals)

def putlong(buf,off,x):
    buf[off:off+4]=(x&MASK).to_bytes(4,"big")

def compute_state(rom):
    if len(rom)<0x2000 or len(rom)%64:
        raise ValueError("ROM must include 0x2000-byte prefix and be 64-byte aligned")
    state=INIT.copy()
    prefix=bytearray([0xff])*0x2000
    prefix[0x400:0x40c]=ROMCONFIG
    for off in range(0x2c0,0x2000,64):
        md5trans(state,prefix[off:off+64])
    for off in range(0x2000,len(rom),64):
        md5trans(state,rom[off:off+64])
    # JagCrypt pads the cartridge address space to the next power of two with FF.
    pow2=2
    while pow2<len(rom):
        pow2*=2
    ff=bytes([0xff])*64
    cur=len(rom)
    while cur<pow2:
        md5trans(state,ff)
        cur+=64
    return state,pow2

def build_rsa_source(boot,state,romsize):
    # boot_orig begins with an 8-byte load header; signing starts at boot+8.
    a0=bytearray(boot[8:])
    if len(a0)<0x280:
        raise ValueError("MD5.DAT boot payload too short")
    putlong(a0,0x20,~state[0])
    putlong(a0,0x44,~state[1])
    a3=0x24
    d1=0xbc
    d3=0
    for _ in range(8):
        old=int.from_bytes(a0[d1:d1+4],"big")
        putlong(a0,a3,old)
        a3+=4
        putlong(a0,d1,state[d3//4])
        d3=(d3+4)&0x0f
        d1+=0x40
    putlong(a0,0x56,0x02c00080)
    endaddr=romsize+0x800000
    wordswapped=((endaddr>>16)|((endaddr&0xffff)<<16))&MASK
    putlong(a0,0x5c,wordswapped)

    # Dave Staugas' byte-difference transform, exactly as portable JagCrypt.
    original=bytes(a0[:0x280])
    prev=0
    for i,x in enumerate(original):
        a0[i]=(x-prev)&0xff
        prev=x
    return bytes(a0[:0x280])

def mult_rsa(src, private65, public65, blocks=10):
    # RSA.C uses KEYSIZE=66, prepending a zero to each 65-byte key, then
    # reverses the arrays for BSAFE's little-endian big-number representation.
    exponent=int.from_bytes(b"\x00"+private65,"big")
    modulus=int.from_bytes(b"\x00"+public65,"big")
    dest=bytearray([(0x100-blocks)&0xff])
    for n in range(blocks):
        chunk=src[n*64:(n+1)*64]
        if len(chunk)!=64:
            raise ValueError("RSA source shorter than requested block count")
        B=chunk+b"\x15\x00"
        value=int.from_bytes(B,"little")
        result=pow(value,exponent,modulus).to_bytes(66,"little")
        dest+=result[:65]
    return bytes(dest)

def generate_prefix(rom,jagcrypt_text,md5_text):
    priv=parse_key_array(jagcrypt_text,"privateK")
    pub=parse_key_array(jagcrypt_text,"publicK")
    boot=parse_md5_dat(md5_text)
    state,romsize=compute_state(rom)
    rsa_src=build_rsa_source(boot,state,romsize)
    sig=mult_rsa(rsa_src,priv,pub,10)
    if len(sig)!=651:
        raise AssertionError(len(sig))
    prefix=bytearray([0xff])*0x2000
    prefix[:651]=sig
    prefix[0x400:0x40c]=ROMCONFIG
    return bytes(prefix),state

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--rom",required=True)
    ap.add_argument("--jagcrypt-c",required=True)
    ap.add_argument("--md5-dat",required=True)
    ap.add_argument("--out-prefix",required=True)
    args=ap.parse_args()
    rom=Path(args.rom).read_bytes()
    p,state=generate_prefix(
        rom,
        Path(args.jagcrypt_c).read_text(errors="replace"),
        Path(args.md5_dat).read_text(errors="replace"))
    Path(args.out_prefix).write_bytes(p)
    print("MD5 state:", " ".join(f"{x:08x}" for x in state))
    print("prefix bytes:",len(p))
    print("signature bytes:",651)

if __name__=="__main__":
    main()
