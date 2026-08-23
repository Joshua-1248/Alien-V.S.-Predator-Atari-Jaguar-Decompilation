# Cartridge layout

Canonical World retail image:

- Size: `0x400000` / `4,194,304` bytes
- SHA-256: `b31ca5c2415881ce50d0c076d327297547214a6240f0058b0f225a74f7ce440b`

The exact-rebuild tooling composes the cartridge from reconstructed program regions plus resource/data inputs extracted locally from the user's canonical ROM.

AAFS and FILES.DAT are rebuilt from granular records rather than copied as opaque multi-megabyte slices. Non-code RDB/data-table inputs are also recovered locally from the user ROM in the public code-only package.

The Jaguar authentication prefix is generated through the reconstructed JagCrypt-compatible path. Historical JagCrypt inputs are not silently relicensed or embedded.

The final acceptance test is a complete bytewise comparison of all `4,194,304` bytes plus the canonical SHA-256.
