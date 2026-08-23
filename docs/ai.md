# AI

Enemy and creature behavior is driven by the original game-state and level systems on the 68000 side.

Preservation rules:

- retain original state-transition ordering;
- retain original timing against the simulation tick;
- do not normalize historical quirks that affect encounters;
- expose AI values to modding tools only with a reversible mapping to native data.

Retail executable behavior remains the authority.
