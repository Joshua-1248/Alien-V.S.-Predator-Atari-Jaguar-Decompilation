# JagPEG

AvP uses Jaguar-specific compressed picture data (identified during reverse engineering as JP80/JagPEG-related content) for several front-end/presentation images.

The verified practical decode uses the corrected chroma-component interpretation that produces the intended warmer/less-blue appearance seen in retail reference imagery.

Keep two things separate:

- **stored native data** — byte-exact user-owned payload extracted from the ROM;
- **decoded presentation image** — host-friendly output using the verified color interpretation.

The extractor/tooling should never replace the native stored bytes with a “corrected” image representation.
