#!/usr/bin/env python
"""
ToBaCCo Quick Start Example

This is the simplest way to generate a MOF structure using ToBaCCo.

Usage:
    python examples/quick_start.py

Note: This example uses the new inputs/ directory structure.
      Input files should be in inputs/templates/, inputs/nodes/, and inputs/edges/
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.api import generate_cif


# ============================================================================
# QUICK START: Generate a MOF structure with 3 simple steps
# ============================================================================

print("=" * 70)
print("ToBaCCo Quick Start - Generate MOF Structure")
print("=" * 70)

# Step 1: Choose your components
# ─────────────────────────────────────────────────────────────────────────
# Components are loaded from the JSON database in data/ directory:
#   - data/template_database.json
#   - data/nodes_database.json
#   - data/edges_database.json

template = "pcu"            # Topology template (6-connected)
node = "6c_Cu_1_Ch"         # Node building block (6-connected, compatible with pcu)
edge = "1B_1TrU"            # Edge building block

print(f"\n📋 Components:")
print(f"   Template: {template}")
print(f"   Node:     {node}")
print(f"   Edge:     {edge}")


# Step 2: Generate the structure
# ─────────────────────────────────────────────────────────────────────────
print(f"\n🔨 Generating structure...")

# Optional: Configure generation parameters
# You can override any configuration option from configuration.py
config = {
    'USER_SPECIFIED_NODE_ASSIGNMENT': False,  # Use only user-specified nodes (True) or all available nodes (False)
    'SCALING_ITERATIONS': 1,                  # Number of scaling iterations (default: 1)
    # 'CHARGES': True,                        # Enable/disable charge assignment
    # 'REMOVE_DUMMY_ATOMS': True,             # Remove dummy atoms (Fr)
    # 'MIN_CELL_LENGTH': 5.0,                 # Minimum unit cell length
}

result = generate_cif(
    template_name=template,
    node_names=node,    # Single string input (new API supports this)
    edge_names=edge,    # Single string input (new API supports this)
    config=config       # Optional: Pass configuration overrides
)

# The new API returns a dict with 'file_path', 'cifname', 'cif_content', and 'metadata'
# File is automatically saved to output/cifs/ directory


# Step 3: Display the results
# ─────────────────────────────────────────────────────────────────────────
print(f"\n✓ Success!")
print(f"   Generated: {result['cifname']}")
print(f"   Saved to:  {result['file_path']}")
print(f"   File size: {result['file_path'].stat().st_size} bytes")

# Display metadata
metadata = result.get('metadata', {})
if 'generation_time' in metadata:
    print(f"   Time:      {metadata['generation_time']:.2f}s")
if 'num_atoms' in metadata:
    print(f"   Atoms:     {metadata['num_atoms']}")

# Display unit cell parameters
if 'unit_cell_params' in metadata:
    uc = metadata['unit_cell_params']
    print(f"\n📐 Unit Cell:")
    print(f"   a = {uc['a']:.3f} Å")
    print(f"   b = {uc['b']:.3f} Å")
    print(f"   c = {uc['c']:.3f} Å")

print("\n" + "=" * 70)
print("Done! Check the output/cifs/ directory for your MOF structure.")
print("=" * 70)
