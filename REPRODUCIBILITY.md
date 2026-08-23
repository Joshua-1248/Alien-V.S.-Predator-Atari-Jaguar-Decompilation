# Reproducibility

Canonical target: World retail **Alien vs Predator** Atari Jaguar image.

- Size: `4,194,304` bytes
- SHA-256: `b31ca5c2415881ce50d0c076d327297547214a6240f0058b0f225a74f7ce440b`

Run `./build.sh "/path/to/Alien vs. Predator.jag"`.

A successful canonical build must report `bytes 4194304`, the SHA-256 above, `differing_bytes 0`, and `RESULT BYTE-EXACT`.

The build obtains proprietary audiovisual/resource data and non-code retail data only from the user's locally supplied ROM.

See [`STATUS.md`](STATUS.md) for the precise meaning and provenance boundary of the byte-exact/100% claim.
