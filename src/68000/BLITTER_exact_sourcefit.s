; AVP Jaguar blitter.o — exact readable source-fit reconstruction
        .text
ByteMove::
        bsr.w   WaitBlit
        move.l  #$00000018,$00f02228
        move.l  a0,d7
        and.b   #$fff8,d7
        move.l  d7,$00f02224
        move.l  a0,d7
        and.l   #$00000007,d7
        move.l  d7,$00f02230
        move.l  d7,d6
        move.l  #$00000018,$00f02204
        move.l  a1,d7
        and.b   #$fff8,d7
        move.l  d7,$00f02200
        move.l  a1,d7
        and.l   #$00000007,d7
        move.l  d7,$00f0220c
        move.l  d0,d5
        bset    #16,d5
        move.l  d5,$00f0223c
        cmp.w   d6,d7
        bge.w   .byte_move_small
        move.l  #$01800005,$00f02238
        rts
.byte_move_small:
        move.l  #$01800001,$00f02238
        rts
ByteSet::
        bsr.w   WaitBlit
        move.l  #$00000018,$00f02204
        move.l  a1,d7
        and.b   #$fff8,d7
        move.l  d7,$00f02200
        move.l  a1,d7
        and.l   #$00000007,d7
        move.l  d7,$00f0220c
        asl.l   #3,d7
        move.l  d1,d6
        ror.l   d7,d6
        move.l  d6,$00f02268
        move.l  d6,$00f0226c
        move.l  d0,d5
        bset    #16,d5
        move.l  d5,$00f0223c
        move.l  #$00010000,$00f02238
        rts
QuickMove::
        bsr.w   WaitBlit
        moveq   #40,d7
        move.l  d7,$00f02204
        move.l  #$00000000,$00f0220c
        move.l  a1,$00f02200
        move.l  d7,$00f02228
        move.l  #$00000000,$00f02230
        move.l  a0,$00f02224
        move.l  d0,d7
        addq.l  #7,d7
        and.b   #$fff8,d7
        lsr.l   #2,d7
        bset    #16,d7
        move.l  d7,$00f0223c
        move.l  #$01800001,$00f02238
        rts
QuickSet::
        bsr.w   WaitBlit
        move.l  #$00000028,$00f02204
        move.l  #$00000000,$00f0220c
        move.l  a1,$00f02200
        move.l  d1,$00f02268
        move.l  d1,$00f0226c
        move.l  d0,d7
        lsr.l   #3,d7
        lsl.l   #1,d7
        bset    #16,d7
        move.l  d7,$00f0223c
        move.l  #$00010000,$00f02238
        rts
QuickClear::
        bsr.w   WaitBlit
        move.l  #$00000028,$00f02204
        move.l  #$00000000,$00f0220c
        move.l  a1,$00f02200
        move.l  #$00000000,$00f02268
        move.l  #$00000000,$00f0226c
        move.l  d0,d7
        lsr.l   #3,d7
        lsl.l   #1,d7
        bset    #16,d7
        move.l  d7,$00f0223c
        move.l  #$00010000,$00f02238
        rts
WaitBlit::
        move.l  d7,-(sp)
.wait:
        move.l  $00f02238,d7
        btst    #0,d7
        beq.s   .wait
        move.l  (sp)+,d7
        rts
        dc.l    0
        dc.w    0
