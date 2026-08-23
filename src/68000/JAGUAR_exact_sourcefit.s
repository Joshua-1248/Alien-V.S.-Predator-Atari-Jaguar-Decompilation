; AVP Jaguar jaguar.o — exact readable source-fit reconstruction
; Newly reconstructed from the retail linked instruction stream.
; This is not claimed to be the literal missing historical source text.

        .text

InitJaguar::
        clr.l   $7f80.w
        move.l  #$00070007,$00f0210c.l
        move.l  #$00070007,$00f1a10c.l
        bsr.w   WaitBlit
        move.l  #$00000000,$00f02208.l
        move.l  #$00000000,$0000.w
        move.l  #$00000004,$0004.w
        clr.l   $00f00020.l
        move.l  #$00009020,$0002ee80.l
        clr.w   $00f000e0.l
        move.l  #$00000008,$00f02114.l
        move.l  #$00000000,$00f02100.l
        move.l  #$00000008,$00f1a114.l
        move.l  #$00000000,$00f1a100.l
        bsr.w   initpad
        rts

InitVideo::
        move.w  $00f14002.l,d0
        and.w   #$0010,d0
        bne.s   .pal_constants

        move.w  #$0144,$0002ee8c.l
        move.w  #$034b,$0002ee8a.l
        move.w  #$0008,$0002eea2.l
        move.w  #$0001,$0002eea4.l
        move.l  #$00000032,$0002ee9c.l
        move.w  #$0004,$0002eea0.l
        bra.s   .video_constants_done

.pal_constants:
        move.w  #$010c,$0002ee8c.l
        move.w  #$0337,$0002ee8a.l
        move.w  #$0004,$0002eea2.l
        move.w  #$0004,$0002eea4.l
        move.l  #$0000003c,$0002ee9c.l
        move.w  #$0005,$0002eea0.l

.video_constants_done:
        move.l  #$00000140,d0
        move.l  #$000000e4,d1
        bsr.w   SetScreen
        move.w  #$0000,$00f00058.l
        move.l  #$00000000,$00f0002a.l
        bsr.w   InitPal
        bsr.w   InitObjL
        bsr.w   InitInts
        move.w  #$06c1,$00f00028.l
        rts

SetScreen::
        lsr.w   #1,d0
        lsr.w   #1,d1
        move.w  d0,$0002ee8e.l
        move.w  d1,$0002ee90.l
        lsl.w   #1,d0
        lsl.w   #1,d1

        move.w  $0002ee8c.l,d2
        move.w  d2,d3
        sub.w   d1,d2
        move.w  d2,$00f00046.l
        move.w  d2,$0002ee94.l
        lsr.w   #1,d2
        move.w  d2,$0002ee92.l

        add.w   d1,d3
        move.w  d3,$0002ee98.l
        lsr.w   #1,d3
        move.w  d3,$0002ee96.l

        move.w  #$ffff,$00f00048.l
        move.w  #$0004,d2
        move.w  $0002eea2.l,d5
        mulu.w  d2,d5
        move.w  d2,d4
        mulu.w  d0,d2
        lsr.w   #1,d2
        move.w  d2,d3
        neg.w   d2
        add.w   $0002ee8a.l,d2
        add.w   d4,d2
        add.w   d5,d2
        move.w  d2,$00f00038.l
        move.w  d2,$00f0003a.l

        clr.w   $0002ee9a.l
        or.w    #$0400,d3
        mulu.w  $0002eea4.l,d4
        sub.w   d4,d3
        add.w   d5,d3
        move.w  d3,$00f0003c.l

        bsr.s   VideoHelper_91A2
        bsr.w   BuildPre
        rts

; External targets resolved from RDB.SYM / linked control flow:
; WaitBlit         = $008dd8
; initpad          = $008f6a
; InitPal          = $009164
; InitObjL         = $00929e
; InitInts         = $00917e
; VideoHelper_91A2 = $0091a2   ; no global DRI name survives
; BuildPre         = $009210
