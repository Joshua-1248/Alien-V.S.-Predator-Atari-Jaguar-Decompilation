# Project status

## v1.0 status

The Atari Jaguar **Alien vs Predator** reconstruction is complete at the project's reproducibility target.

- Canonical target: World retail cartridge image
- Size: `4,194,304` bytes
- SHA-256: `b31ca5c2415881ce50d0c076d327297547214a6240f0058b0f225a74f7ce440b`
- Verified final comparison: **0 differing bytes**
- Ordinary 68000 semantic/source coverage: **100%**
- Jaguar GPU/DSP products required by the retail build: represented in the reproducible build closure
- Proprietary audiovisual/resource assets and non-code retail data: **not distributed**; recovered locally from the user's own retail `.jag`

## What “byte-exact” means

For the canonical World retail image, the reconstruction pipeline can produce a `4,194,304`-byte Jaguar image whose SHA-256 is exactly the value above and whose bytewise comparison against the supplied canonical retail dump reports zero differences.

Byte-exact does **not** mean that every lost 1994 source line, comment, identifier spelling, compiler executable, or developer-workstation file has been recovered. Where historical source text no longer survives, the repository uses documented reconstructed source or exact assembly representations that preserve the verified machine code.

## Historical toolchain limitation

The build lineage is pinned to GNU C 2.5.8 Atari ST Patchlevel 1, `mit2mot`, MadMac-era assembly, and ALN-era linking, with AvP-required behavior reconstructed in the separate toolchain project.

What cannot presently be proven is that any surviving compiler/assembler/linker executable is byte-for-byte the exact file installed on Rebellion's workstation for the final 1994 build. That would require an authenticated copy of the original workstation/tool directory.

This is a provenance limitation, not an unresolved game-code or retail-ROM mismatch.
