/*
 * Clean-room compatibility reconstruction scaffold for the Atari Jaguar
 * Alien vs Predator / Club Drive inflate adaptation.
 *
 * NOT the original Rebellion or Club Drive source.
 * Stock DEFLATE core should be supplied from a separately licensed historical
 * Mark Adler/gzip 1.2.4 compatible baseline. This file documents only the
 * machine-code-proven Jaguar-side glue/delta currently reconstructed.
 */
typedef unsigned char  uch;
typedef unsigned short ush;
typedef unsigned long  ulg;

extern uch *inptr;
extern uch *outptr;
extern ulg outsize;
extern void *malloc(ulg);
extern void memzero(void *, ulg);
extern void loadgpu(void *);
extern unsigned char gpunzip[];

uch *slide;
unsigned wp;
ulg bb;
unsigned bk;
unsigned lbits;
unsigned dbits;
unsigned hufts;

static uch *initial_out;

static void flush(unsigned n)
{
    uch *s = slide;
    while (n--) *outptr++ = *s++;
}

static ulg m2il(const uch *p)
{
    /* Proven from AvP machine code: gzip trailer's little-endian ISIZE. */
    return ((ulg)p[0]) | ((ulg)p[1] << 8) | ((ulg)p[2] << 16) | ((ulg)p[3] << 24);
}

int init_in(void)
{
    loadgpu(gpunzip);
    slide = (uch *)malloc(0x8000UL);
    return slide == 0;
}

/*
 * Stock core insertion point:
 *   huft_build, huft_free, inflate_codes, inflate_stored,
 *   inflate_fixed, inflate_dynamic, inflate_block.
 * Keep c10p1/gzip-1.2.4 control flow and types unless an AvP oracle proves a delta.
 */

int inflate_avp_wrapper_candidate(void)
{
    int e, r;
    unsigned h;

    initial_out = outptr;
    inptr += 10;
    wp = 0; bk = 0; bb = 0;
    lbits = 9; dbits = 6;
    memzero(slide, 0x8000UL);

    h = 0;
    do {
        hufts = 0;
        /* r = inflate_block(&e); */
        r = 0; /* placeholder until stock core is inserted */
        if (r != 0) return r;
        if (hufts > h) h = hufts;
        e = 1; /* placeholder */
    } while (!e);

    flush(wp);
    outsize = (ulg)(outptr - initial_out);

    if (m2il(inptr + 4) != outsize && m2il(inptr + 3) != outsize)
        return 6;
    return 0;
}
