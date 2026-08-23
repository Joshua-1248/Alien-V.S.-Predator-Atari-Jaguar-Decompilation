# Build pipeline

```text
reconstructed/decompiled code
            +
user-owned canonical World retail .jag
      |  (extract assets/non-code data locally)
      v
local build/user_assets/
            +
Atari Jaguar 1994 Toolchain Reconstruction
            +
lawfully obtained JagCrypt historical inputs
      |
      v
reconstructed cartridge image
      |
      +--> size: 4,194,304 bytes
      +--> SHA-256 verification
      +--> full bytewise comparison
      |
      v
RESULT BYTE-EXACT / differing_bytes 0
```

## One-command front end

```sh
./build.sh "/path/to/Alien vs. Predator.jag"
```

The script verifies the input ROM, checks the separate toolchain checkout, extracts the user's required data locally, rebuilds the resource containers/cartridge, generates authentication and performs the final verification.

The exact closure deliberately uses exact assembly representations where literal historical source text is unavailable. The toolchain checkout is therefore preflighted/integrated without falsely claiming that every exact assembly module is regenerated from a lost original C/assembly file.
