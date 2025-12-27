#!/usr/bin/env python
"""
ToBaCCo MOF Generation Example

This script demonstrates how to generate a MOF structure using ToBaCCo's API
by selecting specific components from the JSON databases.

Example: Generate a MOF using:
- Template: acsh (from template_database.json)
- Node: 12c_Ce_1_Ch (from nodes_database.json)
- Edge: 1B_1TrU (from edges_database.json)
"""

import sys
import json
from pathlib import Path

# Add parent directory to path to import from src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src import generate_cif


def list_available_components():
    """
    List all available templates, nodes, and edges from JSON databases.
    
    This function helps you discover what components are available
    before generating structures.
    """
    print("=" * 70)
    print("Available Components in ToBaCCo Databases")
    print("=" * 70)
    
    # Load JSON databases
    data_dir = Path(__file__).parent.parent / "data"
    
    # Load templates
    template_file = data_dir / "template_database.json"
    if template_file.exists():
        with open(template_file, 'r') as f:
            templates = json.load(f)
        print(f"\n📐 Templates ({len(templates)} available):")
        print("   " + ", ".join(sorted(list(templates.keys())[:20])))
        if len(templates) > 20:
            print(f"   ... and {len(templates) - 20} more")
    
    # Load nodes
    nodes_file = data_dir / "nodes_database.json"
    if nodes_file.exists():
        with open(nodes_file, 'r') as f:
            nodes = json.load(f)
        print(f"\n🔵 Nodes ({len(nodes)} available):")
        print("   " + ", ".join(sorted(list(nodes.keys())[:20])))
        if len(nodes) > 20:
            print(f"   ... and {len(nodes) - 20} more")
    
    # Load edges
    edges_file = data_dir / "edges_database.json"
    if edges_file.exists():
        with open(edges_file, 'r') as f:
            edges = json.load(f)
        print(f"\n🔗 Edges ({len(edges)} available):")
        print("   " + ", ".join(sorted(list(edges.keys())[:20])))
        if len(edges) > 20:
            print(f"   ... and {len(edges) - 20} more")
    
    print("\n" + "=" * 70)


def check_component_exists(component_name, database_type):
    """
    Check if a specific component exists in the database.
    
    Args:
        component_name: Name of the component (e.g., "acsh.cif")
        database_type: Type of database ("template", "nodes", or "edges")
    
    Returns:
        bool: True if component exists, False otherwise
    """
    data_dir = Path(__file__).parent.parent / "data"
    database_file = data_dir / f"{database_type}_database.json"
    
    if not database_file.exists():
        print(f"⚠️  Warning: {database_file} not found")
        return False
    
    with open(database_file, 'r') as f:
        database = json.load(f)
    
    # Ensure .cif extension
    if not component_name.endswith('.cif'):
        component_name = f"{component_name}.cif"
    
    exists = component_name in database
    
    if exists:
        print(f"✓ Found {component_name} in {database_type}_database.json")
    else:
        print(f"✗ {component_name} not found in {database_type}_database.json")
        print(f"   Available components: {len(database)}")
    
    return exists


def generate_mof_structure(template_name, node_name, edge_name, output_dir=None):
    """
    Generate a MOF structure using specified components.
    
    Args:
        template_name: Template topology name (e.g., "acsh")
        node_name: Node building block name (e.g., "12c_Ce_1_Ch")
        edge_name: Edge building block name (e.g., "1B_1TrU")
        output_dir: Optional output directory (default: output/cifs/)
    
    Returns:
        dict: Result dictionary with CIF content and metadata
    """
    print("\n" + "=" * 70)
    print("Generating MOF Structure")
    print("=" * 70)
    
    # Display selected components
    print(f"\n📋 Selected Components:")
    print(f"   Template: {template_name}")
    print(f"   Node:     {node_name}")
    print(f"   Edge:     {edge_name}")
    
    # Check if components exist
    print(f"\n🔍 Checking component availability...")
    template_exists = check_component_exists(template_name, "template")
    node_exists = check_component_exists(node_name, "nodes")
    edge_exists = check_component_exists(edge_name, "edges")
    
    if not all([template_exists, node_exists, edge_exists]):
        print("\n❌ Error: One or more components not found in databases")
        print("   Run list_available_components() to see available options")
        return None
    
    # Configure generation settings
    config = {
        "CHARGES": True,              # Include atomic charges
        "SCALING_ITERATIONS": 3,      # Number of optimization iterations
        "BOND_TOL": 5.0,              # Bond tolerance
        "REMOVE_DUMMY_ATOMS": True,   # Remove dummy atoms from output
    }
    
    print(f"\n⚙️  Configuration:")
    for key, value in config.items():
        print(f"   {key}: {value}")
    
    # Generate the structure
    print(f"\n🔨 Generating structure...")
    try:
        result = generate_cif(
            template_name=template_name,
            node_names=[node_name],
            edge_names=[edge_name],
            config=config
        )
        
        # Handle multiple results (if combinatorial edge assignment is enabled)
        if isinstance(result, list):
            print(f"\n✓ Successfully generated {len(result)} structure(s)")
            result = result[0]  # Use first result for this example
        else:
            print(f"\n✓ Successfully generated structure")
        
        # Display metadata
        print(f"\n📊 Structure Metadata:")
        metadata = result.get('metadata', {})
        print(f"   CIF filename:     {result['cifname']}")
        print(f"   Generation time:  {metadata.get('generation_time', 'N/A'):.2f}s")
        
        if 'unit_cell_params' in metadata:
            uc = metadata['unit_cell_params']
            print(f"   Unit cell:")
            print(f"      a = {uc.get('a', 'N/A'):.3f} Å")
            print(f"      b = {uc.get('b', 'N/A'):.3f} Å")
            print(f"      c = {uc.get('c', 'N/A'):.3f} Å")
            print(f"      α = {uc.get('alpha', 'N/A'):.2f}°")
            print(f"      β = {uc.get('beta', 'N/A'):.2f}°")
            print(f"      γ = {uc.get('gamma', 'N/A'):.2f}°")
        
        if 'num_atoms' in metadata:
            print(f"   Number of atoms:  {metadata['num_atoms']}")
        
        # Save to file
        if output_dir is None:
            output_dir = Path(__file__).parent.parent / "output" / "cifs"
        else:
            output_dir = Path(output_dir)
        
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / result['cifname']
        
        with open(output_file, 'w') as f:
            f.write(result['cif_content'])
        
        print(f"\n💾 Saved to: {output_file}")
        print(f"   File size: {len(result['cif_content'])} bytes")
        
        return result
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: File not found - {e}")
        print("   Make sure the component files exist in the database directories")
        return None
    except ValueError as e:
        print(f"\n❌ Error: Invalid input - {e}")
        return None
    except Exception as e:
        print(f"\n❌ Error: {type(e).__name__}: {e}")
        return None


def generate_multiple_structures():
    """
    Example: Generate multiple MOF structures with different combinations.
    """
    print("\n" + "=" * 70)
    print("Generating Multiple MOF Structures")
    print("=" * 70)
    
    # Define multiple structure combinations
    structures = [
        {
            "name": "Structure 1",
            "template": "acsh",
            "node": "12c_Ce_1_Ch",
            "edge": "1B_1TrU"
        },
        {
            "name": "Structure 2",
            "template": "pcu",
            "node": "6c_Cu_1_Ch",
            "edge": "btc_edge"
        },
        {
            "name": "Structure 3",
            "template": "dia",
            "node": "4c_Cd_1_Ch",
            "edge": "bdc_edge"
        }
    ]
    
    results = []
    
    for i, struct in enumerate(structures, 1):
        print(f"\n{'─' * 70}")
        print(f"Structure {i}/{len(structures)}: {struct['name']}")
        print(f"{'─' * 70}")
        
        result = generate_mof_structure(
            template_name=struct['template'],
            node_name=struct['node'],
            edge_name=struct['edge']
        )
        
        if result:
            results.append(result)
    
    print("\n" + "=" * 70)
    print(f"Summary: Successfully generated {len(results)}/{len(structures)} structures")
    print("=" * 70)
    
    return results


def main():
    """
    Main function demonstrating different usage patterns.
    """
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║" + " " * 20 + "ToBaCCo MOF Generation Example" + " " * 18 + "║")
    print("╚" + "═" * 68 + "╝")
    
    # Example 1: List available components
    print("\n" + "─" * 70)
    print("Example 1: List Available Components")
    print("─" * 70)
    list_available_components()
    
    # Example 2: Generate a single structure
    print("\n" + "─" * 70)
    print("Example 2: Generate Single MOF Structure")
    print("─" * 70)
    result = generate_mof_structure(
        template_name="acsh",
        node_name="12c_Ce_1_Ch",
        edge_name="1B_1TrU"
    )
    
    # Example 3: Generate multiple structures (commented out by default)
    # Uncomment the lines below to generate multiple structures
    """
    print("\n" + "─" * 70)
    print("Example 3: Generate Multiple MOF Structures")
    print("─" * 70)
    results = generate_multiple_structures()
    """
    
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║" + " " * 25 + "Examples Complete!" + " " * 24 + "║")
    print("╚" + "═" * 68 + "╝\n")


if __name__ == "__main__":
    main()
