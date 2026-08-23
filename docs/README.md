# Documentation index

This directory is the contributor-facing technical reference for the reconstructed Jaguar source.

- [Engine overview](engine_overview.md) — execution domains, timing and subsystem boundaries.
- [Rendering](rendering.md) — Jaguar rendering responsibilities and preservation rules.
- [Collision](collision.md) — collision-system preservation notes.
- [AI](ai.md) — actor behavior and timing rules.
- [Weapons](weapons.md) — weapon-state and timing preservation.
- [Player](player.md) — player/character-control architecture.
- [Levels](levels.md) — native level/maze data and SDK round-trip goals.
- [File formats](file_formats.md) — AAFS, FILES.DAT and compression.
- [JagPEG](jagpeg.md) — native picture data and corrected color interpretation.
- [Audio](audio.md) — SFX and FullSynth music behavior.
- [GPU](gpu.md) — Jaguar GPU code responsibilities.
- [DSP](dsp.md) — DSP/FullSynth behavior.
- [Cartridge layout](cartridge_layout.md) — canonical image composition and auth.
- [Build pipeline](build_pipeline.md) — source + user ROM + toolchain → byte-exact `.jag`.

Also see [`../STATUS.md`](../STATUS.md), [`../BUILDING.md`](../BUILDING.md), and [`../REPRODUCIBILITY.md`](../REPRODUCIBILITY.md).
