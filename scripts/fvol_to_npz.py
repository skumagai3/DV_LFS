"""Convert .fvol grids to compressed .npz without changing any value.

Each .npz holds the values (uint8 for masks whose values are all whole
numbers 0..3, float32 otherwise), the original 256-byte .fvol header, and a
JSON header readable by deepvoid.io.load_volume. The original file can be
rebuilt byte for byte as header + values as float32; the script checks that
the rebuilt bytes have the SHA-256 recorded by Git LFS for the original.

Run from the repository root after `git lfs pull`:  python scripts/fvol_to_npz.py
"""
import hashlib, json, subprocess, sys
from pathlib import Path
import numpy as np

repo = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
boxes = {"TNG": 205.0, "Bolshoi": 250.0}
oids = {}
for line in subprocess.run(["git", "lfs", "ls-files", "-l"], cwd=repo, capture_output=True,
                           text=True, check=True).stdout.splitlines():
    oid, _, path = line.split(" ", 2)
    oids[path] = oid

rows = []
for rel, oid in sorted(oids.items()):
    src = repo / rel
    raw = src.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == oid, rel
    head = raw[:256]
    nx, ny, nz = np.frombuffer(head[12:24], dtype="<i4")
    values = np.frombuffer(raw, dtype="<f4", offset=256)
    assert values.size == nx * ny * nz, rel
    values = values.reshape(nx, ny, nz)
    is_mask = "mask" in src.name
    if is_mask:
        assert np.all(np.isin(values, [0, 1, 2, 3])), rel
        data = values.astype(np.uint8)
    else:
        data = values
    meta = {"source_file": src.name, "source_sha256": oid,
            "field": "mask" if is_mask else "density"}
    header = json.dumps({"box_size": boxes[rel.split("/")[0]], "meta": meta})
    dst = src.with_suffix(".npz")
    np.savez_compressed(dst, data=data, header=np.array(header),
                        fvol_header=np.frombuffer(head, dtype=np.uint8))
    # Rebuild the original from the .npz alone and compare checksums.
    with np.load(dst) as f:
        rebuilt = f["fvol_header"].tobytes() + f["data"].astype("<f4").tobytes()
    assert hashlib.sha256(rebuilt).hexdigest() == oid, f"{rel}: rebuilt file differs"
    rows.append((rel, len(raw), dst.stat().st_size, str(data.dtype)))
    print(f"{rel}: {len(raw)/1e6:.0f} MB -> {dst.stat().st_size/1e6:.1f} MB ({data.dtype}), identical on rebuild",
          flush=True)
print("all files converted; every original rebuilds byte for byte")
