# Audio

The retail audio system includes ordinary sound effects plus Atari/Jaguar FullSynth music executed through DSP-side code/tables.

## Sound effects

The extraction work identifies and decodes retail SFX without distributing those payloads. Known ambient tracks are `amb2x`, `amb4x`, `amb11` and `lowam`.

## Music

The shipping patch banks use the FullSynth module types observed as:

- `0x04` — FM + envelope
- `0x20` — compressed sampler
- `0x2C` — compressed sampler + envelope

The reconstructed interpreter covers the module behavior used by the shipping music: note-on/off, interpolation, envelopes, sample loops and pan.

Compressed sample decoding uses sign bit 7 and a squared 7-bit magnitude, with adjacent-sample interpolation from an 8.8 phase accumulator.

Score-jump behavior includes signed relative displacement, repeat state and an infinite-loop flag. Voice retrigger behavior turns the active voice off, retries the event, and starts the replacement note on the next programmable-timer tick.
