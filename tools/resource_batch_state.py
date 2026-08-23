#!/usr/bin/env python3
"""Reconstructed gzip-1.2.4 Atari resource batch-state model.

The 1994 matcher keeps its static 64 KiB `window` contents across files inside
one process/invocation. `lm_init()` clears `head[]`, but not `window[]`.

This module models only window-state transfer; each file's dictionary/hash
state still starts fresh exactly as gzip does.
"""
WINDOW=65536
HALF=32768

def update_persistent_window(window: bytearray, data: bytes):
    n=len(data)
    if n < WINDOW:
        # Initial read overwrites only bytes belonging to the new file.
        # gzip 1.2.4 does not clear the remainder at EOF.
        window[:n]=data
        return

    # Initial read fills the complete 64 KiB window.
    window[:WINDOW]=data[:WINDOW]
    pos=WINDOW

    # At EOF/low-lookahead, 1.2.4 slides whenever local strstart reaches
    # WSIZE+MAX_DIST. For a complete memory input this produces this count.
    slides=(n-65535 + HALF-1)//HALF
    for _ in range(slides):
        # memcpy(window, window+WSIZE, WSIZE); upper half intentionally remains.
        window[:HALF]=window[HALF:WINDOW]
        take=min(HALF,n-pos)
        if take:
            window[HALF:HALF+take]=data[pos:pos+take]
            pos+=take

# Reconstructed semantic batch lineages sufficient for every historical
# final-distance case.  These are compatibility/reconstruction evidence, not
# a claim that the lost batch script used this exact textual representation.
RESOURCE_BATCH_PRIORS={
    134:[133],                 # pulse_a -> pulse_b
    136:[],                    # flash_1 batch start
    138:[136,137],             # flash_1, flash_2a -> flash_2b
    141:[],                    # flame_puff_a batch start
    142:[141],                 # flame_puff_a -> flame_puff_b
    152:[149,150,151],         # shotgun_1..3 -> shotgun_4
    166:[],                    # alien_tail1 is state-insensitive here
    178:[173,174,175,177],     # Predator disc frames + punch1 -> punch2
    181:[173,174,175,177,178,179,180],       # pred_combi3
    182:[173,174,175,177,178,179,180,181],   # pred_combi4
    186:[155,185],             # fullscreen/HUD large-image stale high window
}
