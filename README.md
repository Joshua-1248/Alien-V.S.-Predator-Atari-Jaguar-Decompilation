# Alien vs Predator (Atari Jaguar) — reconstructed source

Code-only preservation/reconstruction repository for the 1994 Atari Jaguar release of **Alien vs Predator**.

**Build dependency:** This project uses the separate [Atari Jaguar 1994 Toolchain Reconstruction](https://github.com/Joshua-1248/Atari_Jaguar_1994_Toolchain_Reconstruction) project for the reconstructed historical GCC 2.5.8 Atari ST PL1 → mit2mot → MadMac → ALN build environment.

## Important: no game assets are included

This repository intentionally does **not** distribute the retail ROM or proprietary graphics, textures, sprites, sound effects, music samples, level/resource payloads, or other retail game-data blobs. Non-code data required by the exact build is recovered locally from the user's own canonical `.jag`.

Canonical World retail image used for verification:

- Size: `4,194,304` bytes
- SHA-256: `b31ca5c2415881ce50d0c076d327297547214a6240f0058b0f225a74f7ce440b`

The reconstruction has been verified to reproduce that image byte-for-byte: **0 differing bytes**.

## One-command build

After cloning the separate toolchain repository and making the preserved JagCrypt inputs available:

```sh
./build.sh "/path/to/Alien vs. Predator.jag"
```

The script verifies the ROM, extracts required user-owned data locally, preflights the toolchain reconstruction, rebuilds the cartridge, generates authentication, verifies SHA-256 and performs the complete bytewise comparison.

See [`BUILDING.md`](BUILDING.md) for dependency setup.

## Repository layout

- `src/68000/` — reconstructed/exact-fit Motorola 68000 modules.
- `src/unzip/` — reconstructed allocator/inflate lineage work.
- `src/frozen_exact/` — exact **code/tool-output** representations where literal lost historical source text cannot be recovered.
- `include/` — reconstructed Jaguar/game interfaces.
- `tools/` — ROM-local extraction, resource repacking, compression, authentication and verification utilities.
- `metadata/` — deterministic build metadata; no proprietary audiovisual assets.
- `docs/` — engine, format and build documentation.

## Documentation

Start with [`docs/README.md`](docs/README.md) and [`STATUS.md`](STATUS.md).

## Quick start

1. Clone/download this repository.
2. Clone [Atari Jaguar 1994 Toolchain Reconstruction](https://github.com/Joshua-1248/Atari_Jaguar_1994_Toolchain_Reconstruction) next to it, or set `AVP_TOOLCHAIN_DIR`.
3. Provide your own canonical World retail `.jag`.
4. Provide lawful preserved `JAGCRYPT.C` and `MD5.DAT` inputs as described in `BUILDING.md`.
5. Run `./build.sh "/path/to/Alien vs. Predator.jag"`.

Expected final result:

```text
bytes 4194304
sha256 b31ca5c2415881ce50d0c076d327297547214a6240f0058b0f225a74f7ce440b
differing_bytes 0
RESULT BYTE-EXACT
```

Before publishing or redistributing derived work, read `LICENSE.md`, `PROVENANCE.md`, `CREDITS.md`, and `THIRD_PARTY_NOTICES.md`.
