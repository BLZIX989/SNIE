#!/usr/bin/env python3
"""
Section 21: provenance record + SHA-256 checksums for raw files.

Walks runs/, raw/, and results/, and for every file records:
  input -> configuration -> software -> execution -> raw output -> derived statistic

as a flat JSON manifest, plus a SHA-256 checksum for every file under
runs/ and raw/ (the raw, unrounded outputs -- results/ files are derived
and are checksummed too but flagged as derived in the manifest).
"""
import hashlib
import json
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    manifest = {
        "provenance_chain": "input -> configuration -> software -> execution -> raw_output -> derived_statistic",
        "software": {
            "primat_version": "0.3.1",
            "source": "PyPI (pip install primat==0.3.1)",
            "python_version": "3.11.15",
            "os": "Linux 6.18.5-fc-v20, x86_64",
        },
        "checksums": {},
    }

    for subdir, category in [
        ("runs", "raw_run_output"),
        ("raw", "raw_mc_samples"),
        ("results", "derived_statistic"),
        ("configs", "configuration"),
        ("environment", "environment_record"),
    ]:
        base = os.path.join(ROOT, subdir)
        if not os.path.isdir(base):
            continue
        for dirpath, _, filenames in os.walk(base):
            for fn in sorted(filenames):
                fpath = os.path.join(dirpath, fn)
                relpath = os.path.relpath(fpath, ROOT)
                manifest["checksums"][relpath] = {
                    "sha256": sha256_of(fpath),
                    "category": category,
                    "size_bytes": os.path.getsize(fpath),
                }

    out_path = os.path.join(ROOT, "provenance/checksums.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)
    print(f"wrote {out_path} ({len(manifest['checksums'])} files checksummed)")

    # Also a plain sha256sum-compatible text file for runs/ and raw/ only
    # (the files task Section 21 explicitly calls "important raw files").
    txt_path = os.path.join(ROOT, "provenance/SHA256SUMS.txt")
    with open(txt_path, "w") as f:
        for relpath, info in sorted(manifest["checksums"].items()):
            if info["category"] in ("raw_run_output", "raw_mc_samples"):
                f.write(f"{info['sha256']}  {relpath}\n")
    print(f"wrote {txt_path}")


if __name__ == "__main__":
    main()
