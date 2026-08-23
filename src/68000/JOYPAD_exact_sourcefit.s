; AVP Jaguar joypad.o — exact readable source-fit reconstruction
; Newly reconstructed from retail machine code + Jaguar controller semantics.
; Not claimed as surviving literal Rebellion/Atari source.

        .text

readpad::
        move.l  #$f0fffffc,d1
        moveq   #-1,d2

        move.w  #$81fe,$00f14000
        move.l  $00f14000,d0
        or.l    d1,d0
        ror.l   #4,d0
        and.l   d0,d2

        move.w  #$81fd,$00f14000
        move.l  $00f14000,d0
        or.l    d1,d0
        ror.l   #8,d0
        and.l   d0,d2

        move.w  #$81fb,$00f14000
        move.l  $00f14000,d0
        or.l    d1,d0
        rol.l   #6,d0
        rol.l   #6,d0
        and.l   d0,d2

        move.w  #$81f7,$00f14000
        move.l  $00f14000,d0
        or.l    d1,d0
        rol.l   #8,d0
        and.l   d0,d2

        move.l  $0002ee68,d0
        eor.l   d2,d0
        not.l   d0
        or.l    d2,d0
        tst.b   $0002ee76
        beq.w   .store_p1
        btst    #9,d2
        bne.s   .store_p1
        bclr    #31,d2
        bclr    #31,d0
.store_p1:
        move.l  d2,$0002ee68
        move.l  d0,$0002ee60
        move.l  d2,d3

        move.l  #$0ffffff3,d1
        moveq   #-1,d2

        move.w  #$817f,$00f14000
        move.l  $00f14000,d0
        or.l    d1,d0
        rol.b   #2,d0
        ror.l   #8,d0
        and.l   d0,d2

        move.w  #$81bf,$00f14000
        move.l  $00f14000,d0
        or.l    d1,d0
        rol.b   #2,d0
        ror.l   #8,d0
        ror.l   #4,d0
        and.l   d0,d2

        move.w  #$81df,$00f14000
        move.l  $00f14000,d0
        or.l    d1,d0
        rol.b   #2,d0
        rol.l   #8,d0
        and.l   d0,d2

        move.w  #$81ef,$00f14000
        move.l  $00f14000,d0
        or.l    d1,d0
        rol.b   #2,d0
        rol.l   #4,d0
        and.l   d0,d2

        move.l  $0002ee6c,d0
        eor.l   d2,d0
        not.l   d0
        or.l    d2,d0
        tst.b   $0002ee76
        beq.w   .store_p2
        btst    #9,d2
        bne.s   .store_p2
        bclr    #31,d2
        bclr    #31,d0
.store_p2:
        move.l  d2,$0002ee6c
        move.l  d0,$0002ee64

        tst.b   $0002ee77
        beq.w   .clear_reset_latch
        and.l   d2,d3
        and.l   #$00010001,d3
        bne.s   .clear_reset_latch
        tst.w   $0002ee70
        bne.s   .test_reset_delay
        not.w   $0002ee70
        move.l  $0002ee84,$0002ee72
.test_reset_delay:
        move.l  $0002ee84,d0
        sub.l   $0002ee72,d0
        cmp.l   #12,d0
        bcs.s   .run_callback
        bra.w   reset
.clear_reset_latch:
        clr.w   $0002ee70

.run_callback:
        movem.l d0-d7/a0-a6,-(sp)
        movea.l $00030a34,a0
        jsr     (a0)
        movem.l (sp)+,d0-d7/a0-a6
        rts

initpad::
        clr.w   $0002ee70
        move.b  #-1,$0002ee77
        move.b  #-1,$0002ee76
        move.b  #-1,$0002ee78
        clr.b   $0002ee79
        clr.l   $0002ee68
        clr.l   $0002ee6c
        move.l  #$00008fa4,$00030a34
        rts
        dc.w    0
