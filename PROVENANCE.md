# Provenance

This repository combines several clearly separated provenance classes:

1. **Reconstructed AvP program source** — derived through reverse engineering of the retail Jaguar program and comparison with surviving historical/source material where available. These files do not claim to be the literal lost 1994 source text unless explicitly marked as surviving source.
2. **Exact/frozen assembly** — mechanical source representations of verified executable/code bytes, used where original source spelling cannot be recovered. Non-code retail data required by the build is extracted locally from the user’s ROM rather than published as frozen source.
3. **Independent build/reconstruction utilities** — modern scripts written for this preservation effort.
4. **Historical/open-source lineage references** — GNU GCC 2.5.8 Atari ST Patchlevel 1, Atari Jaguar MadMac/ALN-era tools, Eric R. Smith's `mit2mot`/unzip lineage, gzip 1.2.4 behavior, and Atari JagCrypt behavior. Third-party code is not silently relicensed.
5. **User-owned proprietary assets** — never distributed here; extracted locally from the user's retail `.jag`.

The M1–M92 research milestones are archival evidence and are intentionally not dumped into this publication tree. The public tree contains the consolidated final code paths and documentation.
