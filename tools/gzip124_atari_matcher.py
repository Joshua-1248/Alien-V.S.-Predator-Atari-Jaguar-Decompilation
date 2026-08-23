WSIZE=32768; WINDOW_SIZE=65536; MAX_MATCH=258; MIN_MATCH=3; MIN_LOOKAHEAD=262
MAX_DIST=WSIZE-MIN_LOOKAHEAD; HASH_BITS=15; HASH_SIZE=1<<HASH_BITS; HASH_MASK=HASH_SIZE-1; H_SHIFT=5; WMASK=WSIZE-1
GOOD=32; MAX_LAZY=258; NICE=258; MAX_CHAIN=4096; TOO_FAR=4096

class AtariGzipMatcher:
    def __init__(self, int_size=4):
        self.window=bytearray(WINDOW_SIZE)
        self.int_size=int_size
    def tokens(self,data):
        n=len(data); srcpos=0
        head=[0]*HASH_SIZE; prev=[0]*WSIZE
        strstart=0; block_start=0; match_start=0; lookahead=0; eofile=False; ins_h=0
        # initial read
        amt=WSIZE if self.int_size<=2 else 2*WSIZE
        take=min(amt,n-srcpos); self.window[:take]=data[srcpos:srcpos+take]; srcpos+=take; lookahead=take
        if take==0: eofile=True
        def fill_window():
            nonlocal strstart,block_start,match_start,lookahead,eofile,srcpos,head,prev
            more=(WINDOW_SIZE-lookahead-strstart) & 0xffffffffffffffff
            # Source uses unsigned, but on 32-bit Atari host this is ordinary 32-bit. no weird EOF case needed.
            if strstart >= WSIZE+MAX_DIST:
                self.window[:WSIZE]=self.window[WSIZE:2*WSIZE]
                match_start-=WSIZE; strstart-=WSIZE; block_start-=WSIZE
                for i,m in enumerate(head): head[i]=m-WSIZE if m>=WSIZE else 0
                for i,m in enumerate(prev): prev[i]=m-WSIZE if m>=WSIZE else 0
                more += WSIZE
            if not eofile:
                take=min(more,n-srcpos)
                if take:
                    st=strstart+lookahead;self.window[st:st+take]=data[srcpos:srcpos+take];srcpos+=take;lookahead+=take
                else:
                    # gzip 1.2.4 fill_window(): EOF only sets eofile.  It does
                    # NOT clear bytes following the logical end of this file, so
                    # the static window retains prior-file contents there.
                    eofile=True
        if lookahead==0:return []
        while lookahead<MIN_LOOKAHEAD and not eofile: fill_window()
        # init hash first two window bytes
        for j in range(MIN_MATCH-1):ins_h=((ins_h<<H_SHIFT)^self.window[j])&HASH_MASK
        tokens=[];match_length=MIN_MATCH-1;match_available=False
        def insert(s):
            nonlocal ins_h
            ins_h=((ins_h<<H_SHIFT)^self.window[s+MIN_MATCH-1])&HASH_MASK
            mh=head[ins_h];prev[s&WMASK]=mh;head[ins_h]=s;return mh
        def longest(cur,prev_length,old_ms):
            nonlocal match_start
            chain=MAX_CHAIN;best=prev_length;ms=old_ms
            limit=strstart-MAX_DIST if strstart>MAX_DIST else 0
            if prev_length>=GOOD:chain >>=2
            chain=(chain-1)&0xffffffff
            scan_ini=strstart+MIN_MATCH;match_ini=MIN_MATCH
            scan_start=(self.window[scan_ini-MIN_MATCH]<<8)|self.window[scan_ini-MIN_MATCH+1]
            scan_end=(self.window[scan_ini+best-MIN_MATCH-1]<<8)|self.window[scan_ini+best-MIN_MATCH]
            while True:
                match=match_ini+cur
                cand_end=(self.window[match+best-MIN_MATCH-1]<<8)|self.window[match+best-MIN_MATCH]
                cand_start=(self.window[match-MIN_MATCH]<<8)|self.window[match-MIN_MATCH+1]
                if cand_end==scan_end and cand_start==scan_start:
                    lc=255;si=scan_ini;mi=match
                    while True:
                        eq=self.window[mi]==self.window[si];mi+=1;si+=1
                        if not eq:break
                        lo=(lc-1)&0xffff;lc=(lc&0xffff0000)|lo
                        if lo==0xffff:break
                    length=(si-scan_ini)+(MIN_MATCH-1)
                    if length>best:
                        best=length;ms=cur;match_start=cur
                        if best>=NICE:return best,ms
                        scan_end=(self.window[scan_ini+best-MIN_MATCH-1]<<8)|self.window[scan_ini+best-MIN_MATCH]
                cur=prev[cur&WMASK]
                if (cur&0xffff)<=(limit&0xffff):break
                lo=(chain-1)&0xffff;chain=(chain&0xffff0000)|lo
                if lo==0xffff:break
            return best,ms
        abs_base=0 # number of input bytes slid out; for reporting token positions
        # To report absolute output positions, track consumed output independent of local strstart.
        outpos=0
        while lookahead!=0:
            hh=insert(strstart)
            prev_length=match_length;prev_match=match_start;match_length=MIN_MATCH-1
            if hh!=0 and prev_length<MAX_LAZY and strstart-hh<=MAX_DIST:
                match_length,match_start=longest(hh,prev_length,match_start)
                if match_length>lookahead:match_length=lookahead
                if match_length==MIN_MATCH and strstart-match_start>TOO_FAR:match_length-=1
            if prev_length>=MIN_MATCH and match_length<=prev_length:
                dist=(strstart-1)-prev_match
                tokens.append(('M',outpos,prev_length,dist));outpos+=prev_length
                lookahead-=prev_length-1
                k=prev_length-2
                while k:
                    strstart+=1;insert(strstart);k-=1
                match_available=False;match_length=MIN_MATCH-1;strstart+=1
            elif match_available:
                tokens.append(('L',outpos,self.window[strstart-1]));outpos+=1;strstart+=1;lookahead-=1
            else:
                match_available=True;strstart+=1;lookahead-=1
            while lookahead<MIN_LOOKAHEAD and not eofile:fill_window()
        if match_available:
            tokens.append(('L',outpos,self.window[strstart-1]));outpos+=1
        assert outpos==n,(outpos,n)
        return tokens
