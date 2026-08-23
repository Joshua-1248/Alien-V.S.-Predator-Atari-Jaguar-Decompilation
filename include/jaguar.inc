; AvP reconstructed Jaguar hardware interface subset
; NOT original Atari/Rebellion include text.
BASE            equ     $F00000
HC              equ     BASE+$0004
VC              equ     BASE+$0006
OLP             equ     BASE+$0020
VMODE           equ     BASE+$0028
BG              equ     BASE+$0058
INT1            equ     BASE+$00E0
CLUT            equ     BASE+$0400
GPU_FLAGS       equ     $F02100
GPU_END         equ     $F0210C
GPU_PC          equ     $F02110
GPU_CTRL        equ     $F02114
GPU_RAM         equ     $F03000
JOYIN           equ     $F14000
CONFIG          equ     $F14002
DSP_RAM         equ     $F1B000
VMODE_CRY16     equ     $0000
VMODE_RGB24     equ     $0002
VMODE_RGB16     equ     $0006
