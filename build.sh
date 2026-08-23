#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CANON="b31ca5c2415881ce50d0c076d327297547214a6240f0058b0f225a74f7ce440b"
usage(){ echo 'Usage: ./build.sh "/path/to/Alien vs. Predator.jag"' >&2; echo 'Optional: AVP_TOOLCHAIN_DIR, JAGCRYPT_C, MD5_DAT' >&2; exit 2; }
[[ $# -eq 1 ]] || usage
ROM="$1"
[[ -f "$ROM" ]] || { echo "ERROR: ROM not found: $ROM" >&2; exit 2; }
command -v python3 >/dev/null || { echo "ERROR: python3 is required" >&2; exit 2; }
read -r size actual < <(python3 -c 'import hashlib,os,sys; p=sys.argv[1]; print(os.path.getsize(p),hashlib.sha256(open(p,"rb").read()).hexdigest())' "$ROM")
[[ "$size" == "4194304" ]] || { echo "ERROR: expected 4,194,304-byte World retail ROM; got $size" >&2; exit 1; }
[[ "$actual" == "$CANON" ]] || { echo "ERROR: ROM SHA-256 is not the canonical World retail image" >&2; echo "got: $actual" >&2; exit 1; }
echo "[1/6] Canonical retail ROM verified"
TOOLCHAIN="${AVP_TOOLCHAIN_DIR:-}"
if [[ -z "$TOOLCHAIN" ]]; then for cand in "$ROOT/../Atari_Jaguar_1994_Toolchain_Reconstruction" "$ROOT/../jaguar-1994-toolchain-reconstruction"; do [[ -d "$cand" ]] && TOOLCHAIN="$cand" && break; done; fi
[[ -n "$TOOLCHAIN" && -d "$TOOLCHAIN" ]] || { echo "ERROR: toolchain repo not found; set AVP_TOOLCHAIN_DIR" >&2; exit 2; }
[[ -f "$TOOLCHAIN/tools/mit2mot_compat.py" ]] || { echo "ERROR: toolchain checkout is incomplete" >&2; exit 2; }
python3 "$TOOLCHAIN/tools/mit2mot_compat.py" --help >/dev/null
if [[ -f "$TOOLCHAIN/tests/mit2mot_cases.actual.s" && -f "$TOOLCHAIN/tests/mit2mot_cases.expected.s" ]]; then cmp -s "$TOOLCHAIN/tests/mit2mot_cases.actual.s" "$TOOLCHAIN/tests/mit2mot_cases.expected.s" || { echo "ERROR: toolchain regression fixture mismatch" >&2; exit 1; }; fi
echo "[2/6] Toolchain reconstruction preflight passed"
JAGCRYPT="${JAGCRYPT_C:-$TOOLCHAIN/external/JAGCRYPT.C}"
MD5="${MD5_DAT:-$TOOLCHAIN/external/MD5.DAT}"
[[ -f "$JAGCRYPT" ]] || { echo "ERROR: JAGCRYPT.C not found; set JAGCRYPT_C" >&2; exit 2; }
[[ -f "$MD5" ]] || { echo "ERROR: MD5.DAT not found; set MD5_DAT" >&2; exit 2; }
echo "[3/6] JagCrypt historical inputs found"
WORK="$ROOT/build"; ASSETS="$WORK/user_assets"; OUT="$WORK/avp_world_rebuilt.jag"
rm -rf "$WORK"; mkdir -p "$WORK"
python3 "$ROOT/tools/extract_user_assets.py" --retail-rom "$ROM" --out-dir "$ASSETS"
echo "[4/6] User-owned asset/data inputs extracted locally"
python3 "$ROOT/tools/rebuild_world_granular.py" --assets "$ASSETS" --jagcrypt-c "$JAGCRYPT" --md5-dat "$MD5" --output "$OUT" --verify-retail "$ROM"
echo "[5/6] Cartridge reconstruction completed"
python3 "$ROOT/tools/verify_canonical_rom.py" "$OUT"
python3 "$ROOT/tools/publication_audit.py"
echo "[6/6] Final verification passed"
echo "SUCCESS: byte-exact World retail reconstruction"
echo "Output: $OUT"
echo "SHA-256: $CANON"
