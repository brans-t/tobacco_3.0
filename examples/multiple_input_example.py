#!/usr/bin/env python
"""
ToBaCCo Multiple Input Example

This example demonstrates batch MOF generation with multiple templates, nodes, and edges.
It shows how to generate many MOFs efficiently using list inputs.

Requirements: 2.2, 2.3, 2.4, 2.5
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.api import generate_cif, generate_multiple_mofs


def example_1_multiple_nodes():
    """
    Example 1: Generate MOFs with multiple node types.
    
    When you provide a list of nodes, ToBaCCo generates a MOF for each node.
    """
    print("\n" + "=" * 70)
    print("Example 1: Multiple Nodes")
    print("=" * 70)
    
    # Generate MOFs with different node types
    results = generate_cif(
        template_name="pcu",
        node_names=["6c_Cu_1_Ch", "6c_Zn_1_Ch"],  # List of nodes
        edge_names="btc_edge",
        return_format='file'
    )
    
    print(f"\n✓ Generated {len(results)} MOFs with different nodes!")
    
    for i, result in enumerate(results, 1):
        print(f"\n  MOF {i}:")
        print(f"    CIF name: {result['cifname']}")
        print(f"    Nodes:    {result['metadata']['nodes']}")
        print(f"    Atoms:    {result['metadata']['num_atoms']}")
    
    return results


def example_2_multiple_edges():
    """
    Example 2: Generate MOFs with multiple edge types.
    
    When you provide a list of edges, ToBaCCo generates a MOF for each edge.
    """
    print("\n" + "=" * 70)
    print("Example 2: Multiple Edges")
    print("=" * 70)
    
    # Generate MOFs with different edge types
    results = generate_cif(
        template_name="pcu",
        node_names="6c_Cu_1_Ch",
        edge_names=["btc_edge", "bdc_edge"],  # List of edges
        return_format='file'
    )
    
    print(f"\n✓ Generated {len(results)} MOFs with different edges!")
    
    for i, result in enumerate(results, 1):
        print(f"\n  MOF {i}:")
        print(f"    CIF name: {result['cifname']}")
        print(f"    Edges:    {result['metadata']['edges']}")
        print(f"    Atoms:    {result['metadata']['num_atoms']}")
    
    return results


def example_3_multiple_templates():
    """
    Example 3: Generate MOFs with multiple templates.
    
    When you provide a list of templates, ToBaCCo generates a MOF for each template.
    """
    print("\n" + "=" * 70)
    print("Example 3: Multiple Templates")
    print("=" * 70)
    
    # Generate MOFs with different topologies
    results = generate_cif(
        template_name=["pcu", "dia"],  # List of templates
        node_names="6c_Cu_1_Ch",
        edge_names="btc_edge",
        return_format='file'
    )
    
    print(f"\n✓ Generated {len(results)} MOFs with different topologies!")
    
    for i, result in enumerate(results, 1):
        print(f"\n  MOF {i}:")
        print(f"    CIF name:  {result['cifname']}")
        print(f"    Template:  {result['metadata']['template']}")
        print(f"    Unit cell: a={result['metadata']['unit_cell_params']['a']:.2f} Å")
    
    return results


def example_4_combinatorial_generation():
    """
    Example 4: Combinatorial generation with multiple inputs.
    
    When you provide lists for multiple parameters, ToBaCCo generates all valid combinations.
    """
    print("\n" + "=" * 70)
    print("Example 4: Combinatorial Generation")
    print("=" * 70)
    
    # Define multiple options for each component
    templates = ["pcu", "dia"]
    nodes = ["6c_Cu_1_Ch", "6c_Zn_1_Ch"]
    edges = ["btc_edge"]
    
    print(f"\n📋 Input combinations:")
    print(f"  Templates: {templates} ({len(templates)} options)")
    print(f"  Nodes:     {nodes} ({len(nodes)} options)")
    print(f"  Edges:     {edges} ({len(edges)} options)")
    print(f"  Expected:  {len(templates) * len(nodes) * len(edges)} MOFs")
    
    # Generate all combinations
    results = generate_cif(
        template_name=templates,
        node_names=nodes,
        edge_names=edges,
        return_format='file'
    )
    
    print(f"\n✓ Generated {len(results)} MOFs from all combinations!")
    
    # Display summary
    for i, result in enumerate(results, 1):
        metadata = result['metadata']
        print(f"\n  MOF {i}: {result['cifname']}")
        print(f"    Template: {metadata['template']}")
        print(f"    Node:     {metadata['nodes'][0]}")
        print(f"    Edge:     {metadata['edges'][0]}")
    
    return results


def example_5_generate_multiple_mofs():
    """
    Example 5: Using generate_multiple_mofs() for batch generation.
    
    This function provides a convenient way to generate multiple MOFs with
    different combinations in a single call.
    """
    print("\n" + "=" * 70)
    print("Example 5: Batch Generation with generate_multiple_mofs()")
    print("=" * 70)
    
    # Define combinations
    combinations = [
        {
            'template': 'pcu',
            'nodes': ['6c_Cu_1_Ch'],
            'edges': ['btc_edge']
        },
        {
            'template': 'dia',
            'nodes': ['4c_Zn_1_Ch'],
            'edges': ['bdc_edge']
        },
        {
            'template': 'pcu',
            'nodes': ['6c_Zn_1_Ch'],
            'edges': ['btc_edge']
        }
    ]
    
    print(f"\n📋 Generating {len(combinations)} different MOFs:")
    for i, combo in enumerate(combinations, 1):
        print(f"  {i}. {combo['template']} + {combo['nodes'][0]} + {combo['edges'][0]}")
    
    # Generate all MOFs
    results = generate_multiple_mofs(
        combinations=combinations,
        return_format='file'
    )
    
    print(f"\n✓ Generated {len(results)} MOFs!")
    
    for i, result in enumerate(results, 1):
        print(f"\n  MOF {i}:")
        print(f"    CIF name: {result['cifname']}")
        print(f"    File:     {result['file_path']}")
    
    return results


def example_6_json_output_multiple():
    """
    Example 6: Multiple MOFs with JSON output.
    
    Shows how to get all MOFs in a single JSON object.
    """
    print("\n" + "=" * 70)
    print("Example 6: Multiple MOFs as JSON")
    print("=" * 70)
    
    # Generate multiple MOFs and return as JSON
    json_result = generate_cif(
        template_name="pcu",
        node_names=["6c_Cu_1_Ch", "6c_Zn_1_Ch"],
        edge_names="btc_edge",
        return_format='json'
    )
    
    print(f"\n✓ Generated MOFs as JSON!")
    print(f"  Type:     {type(json_result)}")
    print(f"  MOF count: {len(json_result)}")
    print(f"\n📦 MOF names in JSON:")
    
    for i, mof_name in enumerate(json_result.keys(), 1):
        mof_data = json_result[mof_name]
        metadata = mof_data['metadata']
        print(f"  {i}. {mof_name}")
        print(f"     Node: {metadata['nodes'][0]}")
        print(f"     Atoms: {metadata['num_atoms']}")
    
    return json_result


def example_7_vertex_type_mapping():
    """
    Example 7: Vertex-specific node assignment using dictionary.
    
    For templates with multiple vertex types, you can assign specific nodes
    to specific vertex types using a dictionary.
    """
    print("\n" + "=" * 70)
    print("Example 7: Vertex-Specific Node Assignment")
    print("=" * 70)
    
    # Use dictionary to map vertex types to nodes
    node_mapping = {
        "V": "6c_Cu_1_Ch"  # Assign this node to vertex type V
    }
    
    print(f"\n📋 Node mapping:")
    for vertex_type, node_name in node_mapping.items():
        print(f"  Vertex {vertex_type} → {node_name}")
    
    # Generate MOF with vertex-specific assignment
    result = generate_cif(
        template_name="pcu",
        node_names=node_mapping,  # Dictionary mapping
        edge_names="btc_edge",
        return_format='file'
    )
    
    print(f"\n✓ MOF generated with vertex-specific assignment!")
    print(f"  CIF name: {result['cifname']}")
    print(f"  Nodes:    {result['metadata']['nodes']}")
    
    return result


def example_8_large_batch():
    """
    Example 8: Large batch generation.
    
    Demonstrates efficient generation of many MOFs at once.
    """
    print("\n" + "=" * 70)
    print("Example 8: Large Batch Generation")
    print("=" * 70)
    
    # Define a larger set of combinations
    templates = ["pcu", "dia"]
    nodes = ["6c_Cu_1_Ch", "6c_Zn_1_Ch"]
    edges = ["btc_edge", "bdc_edge"]
    
    expected_count = len(templates) * len(nodes) * len(edges)
    
    print(f"\n📋 Batch parameters:")
    print(f"  Templates: {len(templates)}")
    print(f"  Nodes:     {len(nodes)}")
    print(f"  Edges:     {len(edges)}")
    print(f"  Expected:  {expected_count} MOFs")
    
    print(f"\n🔨 Generating {expected_count} MOFs...")
    
    import time
    start_time = time.time()
    
    # Generate all combinations
    results = generate_cif(
        template_name=templates,
        node_names=nodes,
        edge_names=edges,
        return_format='file'
    )
    
    elapsed_time = time.time() - start_time
    
    print(f"\n✓ Generated {len(results)} MOFs in {elapsed_time:.2f}s!")
    print(f"  Average: {elapsed_time/len(results):.3f}s per MOF")
    
    # Display summary statistics
    total_atoms = sum(r['metadata']['num_atoms'] for r in results)
    avg_atoms = total_atoms / len(results)
    
    print(f"\n📊 Statistics:")
    print(f"  Total atoms:   {total_atoms}")
    print(f"  Average atoms: {avg_atoms:.1f} per MOF")
    
    return results


def main():
    """
    Main function - run all examples.
    """
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║" + " " * 17 + "ToBaCCo Multiple Input Examples" + " " * 18 + "║")
    print("╚" + "═" * 68 + "╝")
    
    print("\nThis script demonstrates batch MOF generation with multiple inputs.")
    print("It shows how to efficiently generate many MOFs at once.")
    
    # Run all examples
    try:
        example_1_multiple_nodes()
        example_2_multiple_edges()
        example_3_multiple_templates()
        example_4_combinatorial_generation()
        example_5_generate_multiple_mofs()
        example_6_json_output_multiple()
        example_7_vertex_type_mapping()
        example_8_large_batch()
        
        print("\n" + "╔" + "═" * 68 + "╗")
        print("║" + " " * 22 + "All Examples Complete!" + " " * 23 + "║")
        print("╚" + "═" * 68 + "╝\n")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure the required input files exist in:")
        print("  - inputs/templates/")
        print("  - inputs/nodes/")
        print("  - inputs/edges/")
        print("\nOr run: python scripts/export_databases_to_json.py")
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
