# Asset policy

No retail game assets are distributed in this repository.

Users must provide their own dumped `.jag` cartridge image. `tools/extract_user_assets.py` extracts the proprietary resource payloads into a local working directory. Those files are inputs to reconstruction and must remain outside the repository.

This includes, without limitation:

- textures and wall/floor/ceiling artwork;
- sprites and first-person overlays;
- fonts and front-end artwork;
- sound effects, music samples and score/resource payloads;
- level/resource archives and other copyrighted cartridge content.

The repository may contain reconstructed program constants/tables and exact assembly representations required to express program behavior. Those are kept separate from user-extracted audiovisual/resource payloads.

## Code-only repository rule

Non-code build data, including the retail RDB data payload and trigger/data tables needed for exact reconstruction, is extracted locally from the user's canonical ROM. It is intentionally not carried as frozen retail data under `src/`.
