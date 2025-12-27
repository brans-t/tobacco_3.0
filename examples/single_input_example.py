#!/usr/bin/env python
"""
ToBaCCo Single Input Example

This example demonstrates basic MOF generation with single template, node, and edge inputs.
It shows all three return formats: file, string, and JSON.

Requirements: 2.1, 3.1, 3.2, 3.3
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.api import generate_cif


def example_1_file_format():
    """
    Example 1: Generate MOF and save to file (default behavior).
    
    This is the most common use case - generate a MOF and save it to the output directory.
    """
    print("\n" + "=" * 70)
    print("Example 1: File Format (Default)")
    print("=" * 70)
    
    # Generate MOF with single inputs
    result = generate_cif(
        template_name="pcb",
        node_names="4c_Cd_1_Ch",
        edge_names="1B_2CF3_Ch",
        return_format='file'  # This is the default
    )
    
    print(f"\n✓ MOF generated successfully!")
    print(f"  CIF name:  {result['cifname']}")
    print(f"  File path: {result['file_path']}")
    print(f"  File size: {result['file_path'].stat().st_size} bytes")
    
    # Display metadata
    metadata = result['metadata']
    print(f"\n📊 Metadata:")
    print(f"  Template:        {metadata['template']}")
    print(f"  Nodes:           {metadata['nodes']}")
    print(f"  Edges:           {metadata['edges']}")
    print(f"  Generation time: {metadata['generation_time']:.3f}s")
    print(f"  Random seed:     {metadata['random_seed']}")
    print(f"  Number of atoms: {metadata['num_atoms']}")
    
    # Display unit cell parameters
    uc = metadata['unit_cell_params']
    print(f"\n📐 Unit Cell:")
    print(f"  a = {uc['a']:.3f} Å")
    print(f"  b = {uc['b']:.3f} Å")
    print(f"  c = {uc['c']:.3f} Å")
    print(f"  α = {uc['alpha']:.2f}°")
    print(f"  β = {uc['beta']:.2f}°")
    print(f"  γ = {uc['gamma']:.2f}°")
    
    return result


def example_2_string_format():
    """
    Example 2: Return CIF content as a string.
    
    Useful when you want to process the CIF content in memory without writing to disk.
    """
    print("\n" + "=" * 70)
    print("Example 2: String Format")
    print("=" * 70)
    
    # Generate MOF and return as string
    result = generate_cif(
        template_name="pcb",
        node_names="4c_Cd_1_Ch",
        edge_names="1B_2CF3_Ch",
        return_format='string'
    )
    
    # String format returns (cif_content, metadata) tuple
    cif_string, metadata = result
    
    print(f"\n✓ MOF generated as string!")
    print(f"  Type:        {type(cif_string)}")
    print(f"  Length:      {len(cif_string)} characters")
    
    # Show first few lines of CIF content
    lines = cif_string.split('\n')
    print(f"\n📄 First 10 lines of CIF content:")
    for i, line in enumerate(lines[:10], 1):
        print(f"  {i:2d}: {line}")
    
    print(f"\n  ... ({len(lines)} total lines)")
    
    # Show metadata
    print(f"\n📊 Metadata:")
    print(f"  Template:        {metadata['template']}")
    print(f"  Generation time: {metadata['generation_time']:.3f}s")
    print(f"  Number of atoms: {metadata['num_atoms']}")
    
    return result


def example_3_json_format():
    """
    Example 3: Return CIF content as JSON.
    
    Useful for web APIs or when you need structured data with metadata.
    """
    print("\n" + "=" * 70)
    print("Example 3: JSON Format")
    print("=" * 70)
    
    # Generate MOF and return as JSON
    json_result = generate_cif(
        template_name="pcb",
        node_names="4c_Cd_1_Ch",
        edge_names="1B_2CF3_Ch",
        return_format='json'
    )
    
    print(f"\n✓ MOF generated as JSON!")
    print(f"  Type:        {type(json_result)}")
    print(f"  Keys:        {list(json_result.keys())}")
    
    # Get the MOF name (first key in the dict)
    mof_name = list(json_result.keys())[0]
    mof_data = json_result[mof_name]
    
    print(f"\n📦 JSON Structure:")
    print(f"  MOF name:    {mof_name}")
    print(f"  Data keys:   {list(mof_data.keys())}")
    
    # Display metadata from JSON
    metadata = mof_data['metadata']
    print(f"\n📊 Metadata from JSON:")
    print(f"  Template:        {metadata['template']}")
    print(f"  Nodes:           {metadata['nodes']}")
    print(f"  Edges:           {metadata['edges']}")
    print(f"  Generation time: {metadata['generation_time']:.3f}s")
    print(f"  Number of atoms: {metadata['num_atoms']}")
    
    # Show CIF content length
    cif_content = mof_data['cif_content']
    print(f"\n📄 CIF Content:")
    print(f"  Length:      {len(cif_content)} characters")
    print(f"  Lines:       {len(cif_content.split(chr(10)))} lines")
    
    return json_result


def example_4_with_configuration():
    """
    Example 4: Generate MOF with custom configuration.
    
    Shows how to override default configuration settings.
    """
    print("\n" + "=" * 70)
    print("Example 4: Custom Configuration")
    print("=" * 70)
    
    # Custom configuration
    custom_config = {
        'CHARGES': True,              # Include atomic charges
        'SCALING_ITERATIONS': 5,      # More optimization iterations
        'BOND_TOL': 3.0,              # Stricter bond tolerance
        'REMOVE_DUMMY_ATOMS': True    # Remove dummy atoms
    }
    
    print(f"\n⚙️  Custom Configuration:")
    for key, value in custom_config.items():
        print(f"  {key}: {value}")
    
    # Generate MOF with custom config
    result = generate_cif(
        template_name="pcb",
        node_names="4c_Cd_1_Ch",
        edge_names="1B_2CF3_Ch",
        config=custom_config,
        return_format='file'
    )
    
    print(f"\n✓ MOF generated with custom configuration!")
    print(f"  CIF name:  {result['cifname']}")
    print(f"  File path: {result['file_path']}")
    
    return result


def example_5_with_extensions():
    """
    Example 5: Input flexibility - with or without .cif extensions.
    
    Shows that ToBaCCo accepts inputs with or without .cif extensions.
    """
    print("\n" + "=" * 70)
    print("Example 5: Input Flexibility")
    print("=" * 70)
    
    # Without .cif extensions (recommended)
    print("\n📝 Without .cif extensions:")
    result1 = generate_cif(
        template_name="pcb",
        node_names="4c_Cd_1_Ch",
        edge_names="1B_2CF3_Ch",
        return_format='file'
    )
    print(f"  Generated: {result1['cifname']}")
    
    # With .cif extensions (also works)
    print("\n📝 With .cif extensions:")
    result2 = generate_cif(
        template_name="pcb.cif",
        node_names="4c_Cd_1_Ch.cif",
        edge_names="1B_2CF3_Ch.cif",
        return_format='file'
    )
    print(f"  Generated: {result2['cifname']}")
    
    print("\n✓ Both methods produce the same result!")
    print(f"  Same CIF name: {result1['cifname'] == result2['cifname']}")
    
    return result1, result2


def main():
    """
    Main function - run all examples.
    """
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║" + " " * 18 + "ToBaCCo Single Input Examples" + " " * 19 + "║")
    print("╚" + "═" * 68 + "╝")
    
    print("\nThis script demonstrates basic MOF generation with single inputs.")
    print("It shows all three return formats: file, string, and JSON.")
    
    # Run all examples
    try:
        example_1_file_format()
        example_2_string_format()
        example_3_json_format()
        example_4_with_configuration()
        example_5_with_extensions()
        
        print("\n" + "╔" + "═" * 68 + "╗")
        print("║" + " " * 22 + "All Examples Complete!" + " " * 23 + "║")
        print("╚" + "═" * 68 + "╝\n")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure the required input files exist:")
        print("  - inputs/templates/pcb.cif")
        print("  - inputs/nodes/4c_Cd_1_Ch.cif")
        print("  - inputs/edges/1B_2CF3_Ch.cif")
        print("\nOr run: python scripts/export_databases_to_json.py")
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
