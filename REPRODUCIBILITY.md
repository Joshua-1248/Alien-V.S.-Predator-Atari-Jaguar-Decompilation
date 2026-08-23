# Reproducibility

Canonical verification target:

```text
Platform: Atari Jaguar
Title: Alien vs Predator
Region/release: World retail
Size: 4,194,304 bytes
SHA-256: b31ca5c2415881ce50d0c076d327297547214a6240f0058b0f225a74f7ce440b
```

The reconstruction workflow was closed with a zero-difference comparison against that image. The public repository is deliberately code-only: proprietary cartridge assets are re-extracted from the user's own ROM rather than redistributed.

Exact historical source wording, comments, local labels, and the precise binaries installed on Rebellion's 1994 workstation cannot be proven where those primary artifacts do not survive. Where necessary, `src/frozen_exact/` preserves exact machine-code/source representations so the build oracle remains deterministic.
