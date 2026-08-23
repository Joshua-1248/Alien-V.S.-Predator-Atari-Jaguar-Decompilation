# Alien vs Predator (Atari Jaguar) — reconstructed source

Code-only preservation/reconstruction repository for the 1994 Atari Jaguar release of **Alien vs Predator**.

**Build dependency:** This project uses the separate [Atari Jaguar 1994 Toolchain Reconstruction](https://github.com/Joshua-1248/Atari_Jaguar_1994_Toolchain_Reconstruction) project to reproduce the historical GCC 2.5.8 Atari ST PL1 → mit2mot → MadMac → ALN build pipeline used for the byte-exact Jaguar build.

## Important: no game assets are included

This repository intentionally does **not** distribute the retail ROM or proprietary graphics, textures, sprites, sound effects, music samples, level/resource payloads, or other audiovisual game assets.

To reproduce the game, provide your own dumped **World retail** `.jag` image and run the asset extractor. The build tooling extracts the required proprietary payloads locally and uses them only in the user's working directory.

Canonical World retail image used for verification:

- Size: `4,194,304` bytes
- SHA-256: `b31ca5c2415881ce50d0c076d327297547214a6240f0058b0f225a74f7ce440b`

The reconstruction has been verified to reproduce the canonical retail image byte-for-byte when supplied with the required user-owned asset/data inputs and compatible historical-tool inputs.

## Repository layout

- `src/68000/` — reconstructed/exact-fit Motorola 68000 modules.
- `src/unzip/` — reconstructed allocator/inflate lineage work used by the Jaguar build.
- `src/frozen_exact/` — exact assembly representations used where literal lost historical source text cannot be recovered.
- `include/` — reconstructed Jaguar/game interfaces.
- `tools/` — ROM asset extraction, resource repacking, gzip compatibility, authentication and verification utilities.
- `metadata/` — deterministic build metadata; no proprietary audiovisual assets.
- `docs/` — build, reproducibility, provenance, credits and legal notes.

## Quick start

1. Clone/download this repository.
2. Obtain/build the separate [Atari Jaguar 1994 Toolchain Reconstruction](https://github.com/Joshua-1248/Atari_Jaguar_1994_Toolchain_Reconstruction) repository.
3. Dump your own retail cartridge to `Alien vs. Predator.jag`.
4. Extract user-owned assets:

```sh
python3 tools/extract_user_assets.py --retail-rom "Alien vs. Predator.jag" --out-dir user_assets
```

5. Rebuild using the documented historical-tool inputs:

```sh
python3 tools/rebuild_world_granular.py \
  --assets user_assets \
  --jagcrypt-c /path/to/JAGCRYPT.C \
  --md5-dat /path/to/MD5.DAT \
  --output avp_world_rebuilt.jag \
  --verify-retail "Alien vs. Predator.jag"
```

Expected verification:

```text
bytes 4194304
sha256 b31ca5c2415881ce50d0c076d327297547214a6240f0058b0f225a74f7ce440b
differing_bytes 0
RESULT BYTE-EXACT
```

See `BUILDING.md`, `ASSETS.md`, `PROVENANCE.md`, `CREDITS.md`, and `THIRD_PARTY_NOTICES.md` before publishing or redistributing derived work.
