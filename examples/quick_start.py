#!/usr/bin/env python
"""
ToBaCCo Quick Start Example

This is the simplest way to generate a MOF structure using ToBaCCo.

Usage:
    python examples/quick_start.py
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src import generate_cif


# ============================================================================
# QUICK START: Generate a MOF structure with 3 simple steps
# ============================================================================

print("=" * 70)
print("ToBaCCo Quick Start - Generate MOF Structure")
print("=" * 70)

# Step 1: Choose your components
# ─────────────────────────────────────────────────────────────────────────
template = "acsh"           # Topology template
node = "12c_Ce_1_Ch"        # Node building block
edge = "1B_1TrU"            # Edge building block

print(f"\n📋 Components:")
print(f"   Template: {template}")
print(f"   Node:     {node}")
print(f"   Edge:     {edge}")


# Step 2: Generate the structure
# ─────────────────────────────────────────────────────────────────────────
print(f"\n🔨 Generating structure...")

result = generate_cif(
    template_name=template,
    node_names=[node],
    edge_names=[edge]
)

# Handle multiple results (if any)
if isinstance(result, list):
    result = result[0]


# Step 3: Save the output
# ─────────────────────────────────────────────────────────────────────────
output_file = Path("output") / "cifs" / result['cifname']
output_file.parent.mkdir(parents=True, exist_ok=True)

with open(output_file, 'w') as f:
    f.write(result['cif_content'])

print(f"\n✓ Success!")
print(f"   Generated: {result['cifname']}")
print(f"   Saved to:  {output_file}")
print(f"   File size: {len(result['cif_content'])} bytes")

# Display some metadata
metadata = result.get('metadata', {})
if 'generation_time' in metadata:
    print(f"   Time:      {metadata['generation_time']:.2f}s")

print("\n" + "=" * 70)
print("Done! Check the output/cifs/ directory for your MOF structure.")
print("=" * 70)
