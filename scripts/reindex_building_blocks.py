#!/usr/bin/env python
"""
Reindex Building Block CIF Files

This script reindexes atoms in building block CIF files (nodes and edges)
with sequential numbering and updates all bond references.

Usage:
    python scripts/reindex_building_blocks.py [--charges]
"""

import glob
import os
import sys
from pathlib import Path

# Add parent directory to path to import from src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.cif_tools import reindex_cif
from src.utils.paths import NODES_DIR, EDGES_DIR


def apply_reindex(charges: bool = False):
    """
    Apply reindexing to all edge and node CIF files.
    
    This function:
    1. Reindexes all CIF files in edges/ and nodes/ directories
    2. Removes original files
    3. Renames reindexed files (removes '_ri' suffix)
    
    Args:
        charges: Whether to include charge information in output
    """
    print("Reindexing building block CIF files...")
    print(f"  Edges directory: {EDGES_DIR}")
    print(f"  Nodes directory: {NODES_DIR}")
    
    ecifs = glob.glob(str(EDGES_DIR / '*.cif'))
    ncifs = glob.glob(str(NODES_DIR / '*.cif'))
    
    print(f"\nFound {len(ecifs)} edge files and {len(ncifs)} node files")
    
    # Reindex all files
    print("\nReindexing files...")
    for e in ecifs:
        reindex_cif(e, charges)
        print(f"  Reindexed: {Path(e).name}")
    for n in ncifs:
        reindex_cif(n, charges)
        print(f"  Reindexed: {Path(n).name}")
    
    # Remove original files
    print("\nRemoving original files...")
    for e in ecifs:
        os.remove(e)
    for n in ncifs:
        os.remove(n)
    
    # Rename reindexed files
    print("\nRenaming reindexed files...")
    ri_ecifs = glob.glob(str(EDGES_DIR / '*.cif_ri'))
    ri_ncifs = glob.glob(str(NODES_DIR / '*.cif_ri'))
    
    for e in ri_ecifs:
        new_name = e.split('.')[0] + '.cif'
        os.rename(e, new_name)
        print(f"  Renamed: {Path(new_name).name}")
    for n in ri_ncifs:
        new_name = n.split('.')[0] + '.cif'
        os.rename(n, new_name)
        print(f"  Renamed: {Path(new_name).name}")
    
    print(f"\nReindexing complete! Processed {len(ecifs) + len(ncifs)} files")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Reindex building block CIF files')
    parser.add_argument('--charges', action='store_true', 
                        help='Include charge information in output')
    
    args = parser.parse_args()
    
    apply_reindex(charges=args.charges)
