; AVP Jaguar joyed.o — exact source-fit reconstruction
; Newly reconstructed from retail machine code. Not surviving historical source.
; Deliberately preserves displacement forms needed for byte identity.

        .text

MoveData::
        move.w  #13,d2
        cmpa.l  #$000203f8,a1
        bne.s   .not_edit_obj
        move.w  #19,d2
.not_edit_obj:
        clr.l   d0
        move.w  8(a3),d0
        moveq   #6,d1
        sub.b   0(a3,d2.w),d1
        lsr.l   d1,d0
        lsl.l   #3,d0
        move.l  $0002ee60,d3
        move.l  0(a3),d1

        btst    #20,d3
        bne.s   .no_dec_coarse
        sub.l   d0,d1
.no_dec_coarse:
        btst    #21,d3
        bne.s   .no_inc_coarse
        add.l   d0,d1
.no_inc_coarse:
        btst    #22,d3
        bne.s   .no_dec_fine
        subq.l  #1,d1
.no_dec_fine:
        btst    #23,d3
        bne.s   .no_inc_fine
        addq.l  #1,d1
.no_inc_fine:
        move.l  d1,0(a3)
        rts

MoveXYFromJoy_reconstructed:
        move.l  $0002ee68,d4
        move.w  4(a3),d0
        move.w  6(a3),d1
        btst    #20,d4
        bne.s   .no_y_dec
        subq.w  #1,d1
.no_y_dec:
        btst    #21,d4
        bne.s   .no_y_inc
        addq.w  #1,d1
.no_y_inc:
        btst    #22,d4
        bne.s   .no_x_dec
        subq.w  #1,d0
.no_x_dec:
        btst    #23,d4
        bne.s   .no_x_inc
        addq.w  #1,d0
.no_x_inc:
        move.w  d0,4(a3)
        move.w  d1,6(a3)
        rts
