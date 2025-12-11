#!/usr/bin/env python3
"""
Verify Run Script - Runs pipeline and computes checksums for verification

Usage:
    python verify_run.py
"""

import hashlib
import time
import subprocess
import sys
from pathlib import Path


def compute_sha256(filepath):
    """Compute SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def main():
    print("=" * 70)
    print("P4 SaaS Growth Analytics Engine - Verification Run")
    print("=" * 70)
    
    # Run the pipeline
    print("\n[1/3] Running pipeline...")
    start_time = time.time()
    
    result = subprocess.run(
        [sys.executable, "run.py"],
        capture_output=True,
        text=True
    )
    
    elapsed_time = time.time() - start_time
    
    if result.returncode != 0:
        print(f"❌ Pipeline failed with error:\n{result.stderr}")
        return 1
    
    print(f"      OK - Pipeline completed in {elapsed_time:.2f} seconds")
    
    # Compute checksums
    print("\n[2/3] Computing SHA256 checksums...")
    
    output_files = [
        "outputs/kpi_snapshot.csv",
        "outputs/base_forecast.csv",
        "outputs/scenario_summary.csv"
    ]
    
    checksums = {}
    for filepath in output_files:
        path = Path(filepath)
        if path.exists():
            checksum = compute_sha256(path)
            checksums[filepath] = checksum
            print(f"      OK - {filepath}: {checksum[:16]}...")
        else:
            print(f"      ERROR - {filepath}: NOT FOUND")
            return 1
    
    # Write checksums to file
    print("\n[3/3] Writing checksums to verify_checksums.txt...")
    
    with open("outputs_verified/verify_checksums.txt", "w") as f:
        f.write("# SHA256 Checksums - Verified Run 2025-12-12\n")
        f.write(f"# Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# Runtime: {elapsed_time:.2f} seconds\n")
        f.write(f"# Python: {sys.version.split()[0]}\n")
        f.write("\n")
        
        for filepath, checksum in checksums.items():
            f.write(f"{checksum}  {filepath}\n")
    
    print("      OK - Checksums written to outputs_verified/verify_checksums.txt")
    
    # Print summary
    print("\n" + "=" * 70)
    print("VERIFICATION COMPLETE")
    print("=" * 70)
    print(f"\nRuntime: {elapsed_time:.2f} seconds")
    print(f"Files verified: {len(checksums)}")
    print("\nTo verify outputs match:")
    print("  1. Run: python verify_run.py")
    print("  2. Compare checksums in verify_checksums.txt")
    print("=" * 70)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
