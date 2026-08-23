# File formats

## AAFS

The canonical retail image contains an AAFS-style resource archive. The current exact path handles **63 records** and rebuilds the archive from granular user-extracted inputs.

## FILES.DAT

The canonical FILES container contains **240 records**. Each record uses a four-byte tag plus a big-endian stored size, followed by payload data and four-byte alignment. `GZIP` records are decoded/re-encoded through the historical-compatibility path.

## Compression

Modern `gzip` output is not assumed to match the historical build. The repository contains reconstruction code for the specific historical streams needed by the canonical image.

## Distribution rule

No proprietary record payloads are included. `tools/extract_user_assets.py` obtains them from the user's canonical ROM; `tools/rebuild_resource_archives.py` reconstructs the native containers.
