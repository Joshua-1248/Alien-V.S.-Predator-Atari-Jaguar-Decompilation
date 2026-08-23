# Rendering

AvP uses the Jaguar's mixed CPU/hardware graphics model rather than a conventional PC-style renderer.

The reconstructed source preserves the original division of work among 68000 setup/control code, GPU helper programs, the Blitter and the Object Processor. Exact-source-fit work is retained where instruction form, branch width, operand size or padding matters to byte identity.

## Fidelity rules

- Preserve native coordinate systems and fixed-point behavior.
- Preserve original palette/color conversion behavior.
- Preserve the baseline simulation/presentation relationship.
- Do not silently smooth, reinterpret or “fix” original rendering behavior.
- Put PC-port enhancements behind optional paths.

JagPEG-backed imagery is documented in [`jagpeg.md`](jagpeg.md).
