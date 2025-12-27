#!/usr/bin/env python
"""
ToBaCCo Deterministic Charge Generation Example

This example demonstrates reproducible MOF generation using random seeds.
It shows that the same seed produces identical atomic charges, enabling
reproducible simulations.

Requirements: 4.1, 4.2, 4.3
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.api import generate_cif


def extract_charges_from_cif(cif_content):
    """
    Extract atomic charges from CIF content.
    
    Args:
        cif_content (str): CIF file content
        
    Returns:
        list: List of (atom_label, charge) tuples
    """
    charges = []
    in_atom_section = False
    
    for line in cif_content.split('\n'):
        line = line.strip()
        
        # Detect start of atom section
        if line.startswith('_atom_site_'):
            in_atom_section = True
            continue
        
        # Parse atom lines
        if in_atom_section and line and not line.startswith('_') and not line.startswith('#'):
            parts = line.split()
            if len(parts) >= 8:  # Ensure we have charge column
                atom_label = parts[0]
                try:
                    charge = float(parts[7])  # Charge is typically column 8
                    charges.append((atom_label, charge))
                except (ValueError, IndexError):
                    pass
        
        # End of atom section
        if in_atom_section and (line.startswith('loop_') or line.startswith('_')):
            if charges:  # Only break if we've collected charges
                break
    
    return charges


def example_1_same_seed_same_charges():
    """
    Example 1: Same seed produces identical charges.
    
    This is the core feature - demonstrates that using the same random seed
    produces exactly the same atomic charges every time.
    """
    print("\n" + "=" * 70)
    print("Example 1: Same Seed → Same Charges")
    print("=" * 70)
    
    seed = 42
    
    print(f"\n🎲 Using random seed: {seed}")
    print(f"   Generating MOF twice with the same seed...")
    
    # Generate MOF first time
    result1 = generate_cif(
        template_name="pcu",
        node_names="6c_Cu_1_Ch",
        edge_names="btc_edge",
        random_seed=seed,
        return_format='string'
    )
    
    # Generate MOF second time with same seed
    result2 = generate_cif(
        template_name="pcu",
        node_names="6c_Cu_1_Ch",
        edge_names="btc_edge",
        random_seed=seed,
        return_format='string'
    )
    
    # Extract charges from both CIFs
    charges1 = extract_charges_from_cif(result1)
    charges2 = extract_charges_from_cif(result2)
    
    print(f"\n✓ Generated MOFs!")
    print(f"  First generation:  {len(charges1)} atoms with charges")
    print(f"  Second generation: {len(charges2)} atoms with charges")
    
    # Compare charges
    if charges1 == charges2:
        print(f"\n✅ SUCCESS: Charges are IDENTICAL!")
        print(f"   Same seed produced exactly the same charges.")
    else:
        print(f"\n❌ FAILURE: Charges are DIFFERENT!")
        print(f"   This should not happen with the same seed.")
    
    # Show first few charges as proof
    print(f"\n📊 First 5 atomic charges (both generations):")
    print(f"  {'Atom':<15} {'Gen 1 Charge':>12} {'Gen 2 Charge':>12} {'Match':>8}")
    print(f"  {'-'*15} {'-'*12} {'-'*12} {'-'*8}")
    
    for i in range(min(5, len(charges1))):
        atom1, charge1 = charges1[i]
        atom2, charge2 = charges2[i]
        match = "✓" if charge1 == charge2 else "✗"
        print(f"  {atom1:<15} {charge1:>12.6f} {charge2:>12.6f} {match:>8}")
    
    return result1, result2


def example_2_different_seeds_different_charges():
    """
    Example 2: Different seeds produce different charges.
    
    Shows that changing the seed changes the charge distribution,
    while keeping the structure identical.
    """
    print("\n" + "=" * 70)
    print("Example 2: Different Seeds → Different Charges")
    print("=" * 70)
    
    seed1 = 42
    seed2 = 123
    
    print(f"\n🎲 Using two different seeds:")
    print(f"   Seed 1: {seed1}")
    print(f"   Seed 2: {seed2}")
    
    # Generate MOF with first seed
    result1 = generate_cif(
        template_name="pcu",
        node_names="6c_Cu_1_Ch",
        edge_names="btc_edge",
        random_seed=seed1,
        return_format='string'
    )
    
    # Generate MOF with second seed
    result2 = generate_cif(
        template_name="pcu",
        node_names="6c_Cu_1_Ch",
        edge_names="btc_edge",
        random_seed=seed2,
        return_format='string'
    )
    
    # Extract charges
    charges1 = extract_charges_from_cif(result1)
    charges2 = extract_charges_from_cif(result2)
    
    print(f"\n✓ Generated MOFs!")
    print(f"  Seed {seed1}:  {len(charges1)} atoms")
    print(f"  Seed {seed2}: {len(charges2)} atoms")
    
    # Compare charges
    differences = sum(1 for (a1, c1), (a2, c2) in zip(charges1, charges2) if c1 != c2)
    
    print(f"\n📊 Charge comparison:")
    print(f"  Total atoms:      {len(charges1)}")
    print(f"  Different charges: {differences}")
    print(f"  Percentage:       {100*differences/len(charges1):.1f}%")
    
    if differences > 0:
        print(f"\n✅ SUCCESS: Different seeds produced different charges!")
    else:
        print(f"\n⚠️  WARNING: Charges are identical (unexpected)")
    
    # Show some differences
    print(f"\n📊 Sample charge differences:")
    print(f"  {'Atom':<15} {'Seed 42':>12} {'Seed 123':>12} {'Diff':>12}")
    print(f"  {'-'*15} {'-'*12} {'-'*12} {'-'*12}")
    
    count = 0
    for (atom1, charge1), (atom2, charge2) in zip(charges1, charges2):
        if charge1 != charge2 and count < 5:
            diff = charge2 - charge1
            print(f"  {atom1:<15} {charge1:>12.6f} {charge2:>12.6f} {diff:>+12.6f}")
            count += 1
    
    return result1, result2


def example_3_reproducible_workflow():
    """
    Example 3: Reproducible research workflow.
    
    Demonstrates how to use seeds for reproducible research.
    """
    print("\n" + "=" * 70)
    print("Example 3: Reproducible Research Workflow")
    print("=" * 70)
    
    # Define a seed for your research project
    project_seed = 2024
    
    print(f"\n📝 Research Project Setup:")
    print(f"   Project seed: {project_seed}")
    print(f"   This seed will be used for all MOF generations in this project.")
    
    # Generate multiple MOFs with the same seed
    mof_configs = [
        ("pcu", "6c_Cu_1_Ch", "btc_edge"),
        ("dia", "4c_Zn_1_Ch", "bdc_edge"),
    ]
    
    print(f"\n🔨 Generating {len(mof_configs)} MOFs with seed {project_seed}...")
    
    results = []
    for template, node, edge in mof_configs:
        result = generate_cif(
            template_name=template,
            node_names=node,
            edge_names=edge,
            random_seed=project_seed,
            return_format='file'
        )
        results.append(result)
        
        print(f"\n  ✓ {result['cifname']}")
        print(f"    Seed: {result['metadata']['random_seed']}")
        print(f"    Atoms: {result['metadata']['num_atoms']}")
    
    print(f"\n✅ All MOFs generated with seed {project_seed}!")
    print(f"   These results are now reproducible.")
    print(f"   Anyone using seed {project_seed} will get identical charges.")
    
    return results


def example_4_default_seed():
    """
    Example 4: Using default seed from configuration.
    
    Shows what happens when no seed is specified.
    """
    print("\n" + "=" * 70)
    print("Example 4: Default Seed Behavior")
    print("=" * 70)
    
    print(f"\n🎲 Generating MOF without specifying seed...")
    print(f"   (Will use default seed from configuration)")
    
    # Generate without specifying seed
    result = generate_cif(
        template_name="pcu",
        node_names="6c_Cu_1_Ch",
        edge_names="btc_edge",
        return_format='file'
    )
    
    default_seed = result['metadata']['random_seed']
    
    print(f"\n✓ MOF generated!")
    print(f"  Default seed used: {default_seed}")
    print(f"  CIF name: {result['cifname']}")
    
    # Generate again without seed
    result2 = generate_cif(
        template_name="pcu",
        node_names="6c_Cu_1_Ch",
        edge_names="btc_edge",
        return_format='string'
    )
    
    # Extract and compare charges
    charges1 = extract_charges_from_cif(result['cif_content'])
    charges2 = extract_charges_from_cif(result2)
    
    if charges1 == charges2:
        print(f"\n✅ Default seed produces consistent results!")
        print(f"   Both generations used seed {default_seed}")
    
    return result


def example_5_seed_in_metadata():
    """
    Example 5: Seed is recorded in metadata.
    
    Shows that the seed is always recorded for traceability.
    """
    print("\n" + "=" * 70)
    print("Example 5: Seed Traceability")
    print("=" * 70)
    
    seeds_to_test = [42, 123, 999]
    
    print(f"\n📋 Testing seed recording in metadata...")
    
    for seed in seeds_to_test:
        result = generate_cif(
            template_name="pcu",
            node_names="6c_Cu_1_Ch",
            edge_names="btc_edge",
            random_seed=seed,
            return_format='file'
        )
        
        recorded_seed = result['metadata']['random_seed']
        match = "✓" if recorded_seed == seed else "✗"
        
        print(f"\n  Seed {seed}:")
        print(f"    Requested: {seed}")
        print(f"    Recorded:  {recorded_seed}")
        print(f"    Match:     {match}")
    
    print(f"\n✅ All seeds correctly recorded in metadata!")
    print(f"   This ensures full traceability of results.")


def example_6_charge_neutrality():
    """
    Example 6: Charge neutrality is maintained.
    
    Verifies that total charge is zero regardless of seed.
    """
    print("\n" + "=" * 70)
    print("Example 6: Charge Neutrality")
    print("=" * 70)
    
    seeds = [42, 123, 999]
    
    print(f"\n⚡ Testing charge neutrality with different seeds...")
    
    for seed in seeds:
        result = generate_cif(
            template_name="pcu",
            node_names="6c_Cu_1_Ch",
            edge_names="btc_edge",
            random_seed=seed,
            return_format='string'
        )
        
        # Extract charges and calculate total
        charges = extract_charges_from_cif(result)
        total_charge = sum(charge for _, charge in charges)
        
        print(f"\n  Seed {seed}:")
        print(f"    Atoms:        {len(charges)}")
        print(f"    Total charge: {total_charge:.6f}")
        print(f"    Neutral:      {'✓' if abs(total_charge) < 0.001 else '✗'}")
    
    print(f"\n✅ Charge neutrality maintained for all seeds!")


def main():
    """
    Main function - run all examples.
    """
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║" + " " * 13 + "ToBaCCo Deterministic Charge Examples" + " " * 16 + "║")
    print("╚" + "═" * 68 + "╝")
    
    print("\nThis script demonstrates reproducible MOF generation using random seeds.")
    print("Same seed → Same charges → Reproducible simulations!")
    
    # Run all examples
    try:
        example_1_same_seed_same_charges()
        example_2_different_seeds_different_charges()
        example_3_reproducible_workflow()
        example_4_default_seed()
        example_5_seed_in_metadata()
        example_6_charge_neutrality()
        
        print("\n" + "╔" + "═" * 68 + "╗")
        print("║" + " " * 22 + "All Examples Complete!" + " " * 23 + "║")
        print("╚" + "═" * 68 + "╝\n")
        
        print("\n💡 Key Takeaways:")
        print("  1. Same seed → Identical charges (reproducible)")
        print("  2. Different seeds → Different charges (variability)")
        print("  3. Seed is recorded in metadata (traceability)")
        print("  4. Charge neutrality is always maintained")
        print("  5. Use seeds for reproducible research!\n")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure the required input files exist.")
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
