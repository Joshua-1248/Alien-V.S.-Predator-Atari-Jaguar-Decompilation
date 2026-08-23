; AvP reconstructed MESSAGE.INC API
; Declarations derived from surviving HUD_MSG.S global definitions.
; NOT original source text.
MSG_STOP        equ     0
MSG_NEW         equ     $FF

extern          InitHUDMsg
extern          UpdtHUDMsg
extern          ShowHUDMsg
extern          msg_dead
extern          msg_pressure
extern          msg_notsecure
extern          msg_airlocked
extern          msg_jlift
extern          msg_jammed
extern          msg_acdenied
extern          ac2
extern          clm_card
extern          clm_shot
extern          clm_sammo
extern          clm_pulse
extern          clm_pammo
extern          clm_flame
extern          clm_fammo
extern          clm_smart
extern          clm_smammo
extern          clm_mtrack
extern          clm_food
extern          clm_medaid
extern          chmsg_on
extern          chmsg_off
extern          msg_stun
extern          msg_cocooned
extern          msg_ccnfail
extern          msg_usecocoon
extern          msg_newduct
extern          msg_newlevel
extern          msg_escape
extern          duct_ids
extern          gain_combi
extern          lose_combi
extern          gain_disc
extern          lose_disc
extern          gain_cannon
extern          lose_cannon
extern          msg_countdown
extern          cdm_stop
extern          cdm1
extern          cdm2
extern          cdm
extern          font_desc
extern          font_trans
extern          ac2_copy
extern          cm1_copy
extern          msg1_data
extern          msg2_data
extern          msg3_data
extern          msg_ptr
extern          new_message
extern          msg1_on
extern          msg2_on
extern          msg3_on
extern          msg_status
