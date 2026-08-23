# Engine overview

The retail game is a heterogeneous Atari Jaguar program. The Motorola 68000 coordinates game state, resource loading, input, AI, player logic, level logic and hardware setup, while specialized Jaguar hardware handles time-critical graphics/audio work.

## Major execution domains

- **68000** — high-level game/runtime control, player and AI state, resource management, level logic, UI and Jaguar setup.
- **GPU** — specialized graphics/data-conversion routines used by the retail renderer/resource path.
- **DSP** — FullSynth-driven music/audio execution and associated tables.
- **Object Processor / Blitter** — Jaguar hardware used by the presentation path and sprite/screen operations.

The reconstruction keeps these domains distinct rather than flattening them into a modern engine abstraction.

## Timing

The preservation baseline retains the original simulation behavior. A future PC port may render at higher rates, but simulation timing, AI timing, movement, weapon cadence and other gameplay rules should remain decoupled from optional presentation-rate improvements.

## Source policy

Surviving historical source remains historical source. Missing source is represented by reconstructed readable source where possible and exact assembly where necessary. The canonical retail executable is the acceptance oracle.
