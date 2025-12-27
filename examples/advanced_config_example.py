#!/usr/bin/env python
"""
ToBaCCo Advanced Configuration Example

This example demonstrates how to use configuration options to customize
MOF generation, including USER_SPECIFIED_NODE_ASSIGNMENT and SCALING_ITERATIONS.

Usage:
    python examples/advanced_config_example.py
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.api import generate_cif


print("=" * 70)
print("ToBaCCo Advanced Configuration Example")
print("=" * 70)


# ============================================================================
# Example 1: Basic generation with default settings
# ============================================================================
print("\n" + "─" * 70)
print("Example 1: Default Configuration")
print("─" * 70)

result1 = generate_cif(
    template_name="pcu",
    node_names="6c_Cu_1_Ch",
    edge_names="1B_1TrU"
)

print(f"✓ Generated: {result1['cifname']}")
print(f"  Scaling iterations: 1 (default)")
print(f"  Node assignment: User-specified (API default)")


# ============================================================================
# Example 2: Custom scaling iterations
# ============================================================================
print("\n" + "─" * 70)
print("Example 2: Multiple Scaling Iterations")
print("─" * 70)

config_scaling = {
    'SCALING_ITERATIONS': 3,  # Increase for better unit cell optimization
}

result2 = generate_cif(
    template_name="pcu",
    node_names="6c_Cu_1_Ch",
    edge_names="1B_1TrU",
    config=config_scaling
)

print(f"✓ Generated: {result2['cifname']}")
print(f"  Scaling iterations: 3")
print(f"  Unit cell: a={result2['metadata']['unit_cell_params']['a']:.3f} Å")


# ============================================================================
# Example 3: User-specified node assignment
# ============================================================================
print("\n" + "─" * 70)
print("Example 3: User-Specified Node Assignment")
print("─" * 70)

config_nodes = {
    'USER_SPECIFIED_NODE_ASSIGNMENT': True,  # Only use specified nodes
}

result3 = generate_cif(
    template_name="pcu",
    node_names="6c_Cu_1_Ch",
    edge_names="1B_1TrU",
    config=config_nodes
)

print(f"✓ Generated: {result3['cifname']}")
print(f"  Node assignment: User-specified only")
print(f"  Nodes used: {result3['metadata']['nodes']}")


# ============================================================================
# Example 4: Combined configuration options
# ============================================================================
print("\n" + "─" * 70)
print("Example 4: Combined Configuration")
print("─" * 70)

config_combined = {
    'USER_SPECIFIED_NODE_ASSIGNMENT': True,
    'SCALING_ITERATIONS': 2,
    'CHARGES': True,              # Enable charge assignment
    'REMOVE_DUMMY_ATOMS': True,   # Remove dummy atoms
    'MIN_CELL_LENGTH': 10.0,      # Minimum cell length (Å)
    'RANDOM_SEED': 42,            # Deterministic charge generation
}

result4 = generate_cif(
    template_name="pcu",
    node_names="6c_Cu_1_Ch",
    edge_names="1B_1TrU",
    config=config_combined
)

print(f"✓ Generated: {result4['cifname']}")
print(f"  Scaling iterations: 2")
print(f"  Min cell length: 10.0 Å")
print(f"  Charges: Enabled")
print(f"  Random seed: 42")
print(f"  Atoms: {result4['metadata']['num_atoms']}")
print(f"  Bonds: {result4['metadata']['num_bonds']}")


# ============================================================================
# Example 5: Disable charges and dummy atom removal
# ============================================================================
print("\n" + "─" * 70)
print("Example 5: Custom Charge and Atom Settings")
print("─" * 70)

config_no_charges = {
    'CHARGES': False,             # Disable charge assignment
    'REMOVE_DUMMY_ATOMS': False,  # Keep dummy atoms (Fr)
}

result5 = generate_cif(
    template_name="pcu",
    node_names="6c_Cu_1_Ch",
    edge_names="1B_1TrU",
    config=config_no_charges
)

print(f"✓ Generated: {result5['cifname']}")
print(f"  Charges: Disabled")
print(f"  Dummy atoms: Kept")


# ============================================================================
# Summary
# ============================================================================
print("\n" + "=" * 70)
print("Summary of Available Configuration Options:")
print("=" * 70)
print("""
Key Configuration Options:
  
  • USER_SPECIFIED_NODE_ASSIGNMENT (bool)
    - True: Only use nodes specified in node_names parameter
    - False: Consider all available nodes in database
    - Default: False (True in API mode)
  
  • SCALING_ITERATIONS (int)
    - Number of iterations for unit cell optimization
    - Higher values may improve cell parameters
    - Default: 1
  
  • CHARGES (bool)
    - Enable/disable atomic charge assignment
    - Default: True
  
  • REMOVE_DUMMY_ATOMS (bool)
    - Remove dummy atoms (Fr) from final structure
    - Default: True
  
  • MIN_CELL_LENGTH (float)
    - Minimum unit cell length in Angstroms
    - Default: 5.0
  
  • RANDOM_SEED (int)
    - Seed for deterministic charge generation
    - Same seed produces identical charges
    - Default: 42
  
  • OPT_METHOD (str)
    - Optimization method for scaling
    - Options: 'L-BFGS-B', 'SLSQP', etc.
    - Default: 'L-BFGS-B'

For complete list, see configuration.py
""")

print("=" * 70)
print(f"All structures saved to: output/cifs/")
print("=" * 70)
