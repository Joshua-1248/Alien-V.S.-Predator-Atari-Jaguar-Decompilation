# Building

## Requirements

- Python 3.10+.
- A user-dumped canonical World retail **Alien vs Predator** Jaguar ROM.
- The separate [Atari Jaguar 1994 Toolchain Reconstruction](https://github.com/Joshua-1248/Atari_Jaguar_1994_Toolchain_Reconstruction) checkout.
- Preserved Atari JagCrypt inputs (`JAGCRYPT.C` and `MD5.DAT`) obtained from a lawful preservation source. They are not redistributed here.

## Recommended directory layout

```text
projects/
  Alien-V.S.-Predator-Atari-Jaguar-Decompilation/
  Atari_Jaguar_1994_Toolchain_Reconstruction/
```

Place `JAGCRYPT.C` and `MD5.DAT` under an untracked `external/` directory in the toolchain checkout, or set `JAGCRYPT_C` and `MD5_DAT`. If the toolchain checkout is elsewhere, set `AVP_TOOLCHAIN_DIR`.

## One-command exact build

```sh
./build.sh "/path/to/Alien vs. Predator.jag"
```

The command verifies the canonical ROM, preflights the separate toolchain, extracts proprietary/non-code inputs locally, rebuilds AAFS/FILES.DAT and the cartridge, generates Jaguar authentication, and performs final SHA-256 plus bytewise verification.

A successful build ends with `RESULT BYTE-EXACT`, `differing_bytes 0`, and the canonical SHA-256.

## Publication rule

Commit code, scripts, documentation, deterministic metadata and tests. Do **not** commit ROM dumps, extracted graphics/audio/resources, non-code retail data extracted for the build, rebuilt ROM images, or other copyrighted game payloads.
