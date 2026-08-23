# Building

## Requirements

- Python 3.10+ (the reconstruction utilities are pure Python unless otherwise noted).
- A user-dumped canonical World retail `Alien vs Predator` Jaguar ROM.
- The separate `jaguar-1994-toolchain-reconstruction` repository for historical compiler/assembler/linker compatibility work.
- Preserved Atari JagCrypt inputs (`JAGCRYPT.C` and `MD5.DAT`) obtained from a lawful preservation source. They are not redistributed here.

## Asset extraction

Do not place extracted assets under version control. The provided `.gitignore` excludes the normal output directories and ROM-image extensions.

```sh
python3 tools/extract_user_assets.py \
  --retail-rom "/path/to/Alien vs. Predator.jag" \
  --out-dir user_assets
```

The extractor verifies the expected cartridge geometry and splits resource archives into local user-owned inputs.

## Exact reconstruction

```sh
python3 tools/rebuild_world_granular.py \
  --assets user_assets \
  --jagcrypt-c /path/to/JAGCRYPT.C \
  --md5-dat /path/to/MD5.DAT \
  --output build/avp_world_rebuilt.jag \
  --verify-retail "/path/to/Alien vs. Predator.jag"
```

The canonical target SHA-256 is:

`b31ca5c2415881ce50d0c076d327297547214a6240f0058b0f225a74f7ce440b`

## Publication rule

Commit source, scripts, documentation, deterministic metadata, and tests. Do **not** commit ROM dumps, extracted graphics/audio/resources, rebuilt ROM images, or other copyrighted asset payloads.
