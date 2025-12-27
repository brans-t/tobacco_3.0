#!/usr/bin/env python
"""
Test script to verify configuration options work correctly.

This script tests USER_SPECIFIED_NODE_ASSIGNMENT and SCALING_ITERATIONS
configuration options with the generate_cif API.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.api import generate_cif


def test_user_specified_node_assignment():
    """Test USER_SPECIFIED_NODE_ASSIGNMENT configuration option."""
    print("=" * 70)
    print("Testing USER_SPECIFIED_NODE_ASSIGNMENT")
    print("=" * 70)
    
    # Test with USER_SPECIFIED_NODE_ASSIGNMENT = True
    print("\n1. Testing with USER_SPECIFIED_NODE_ASSIGNMENT = True")
    config_true = {'USER_SPECIFIED_NODE_ASSIGNMENT': True}
    
    try:
        result = generate_cif(
            template_name="pcu",
            node_names="6c_Cu_1_Ch",
            edge_names="1B_1TrU",
            config=config_true
        )
        print(f"   ✓ Success: {result['cifname']}")
        print(f"   Nodes used: {result['metadata']['nodes']}")
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        return False
    
    # Test with USER_SPECIFIED_NODE_ASSIGNMENT = False
    print("\n2. Testing with USER_SPECIFIED_NODE_ASSIGNMENT = False")
    config_false = {'USER_SPECIFIED_NODE_ASSIGNMENT': False}
    
    try:
        result = generate_cif(
            template_name="pcu",
            node_names="6c_Cu_1_Ch",
            edge_names="1B_1TrU",
            config=config_false
        )
        print(f"   ✓ Success: {result['cifname']}")
        print(f"   Nodes used: {result['metadata']['nodes']}")
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        return False
    
    return True


def test_scaling_iterations():
    """Test SCALING_ITERATIONS configuration option."""
    print("\n" + "=" * 70)
    print("Testing SCALING_ITERATIONS")
    print("=" * 70)
    
    # Test with different scaling iterations
    for iterations in [1, 2, 3]:
        print(f"\n{iterations}. Testing with SCALING_ITERATIONS = {iterations}")
        config = {'SCALING_ITERATIONS': iterations}
        
        try:
            result = generate_cif(
                template_name="pcu",
                node_names="6c_Cu_1_Ch",
                edge_names="1B_1TrU",
                config=config
            )
            print(f"   ✓ Success: {result['cifname']}")
            uc = result['metadata']['unit_cell_params']
            print(f"   Unit cell: a={uc['a']:.3f}, b={uc['b']:.3f}, c={uc['c']:.3f} Å")
            print(f"   Generation time: {result['metadata']['generation_time']:.2f}s")
        except Exception as e:
            print(f"   ✗ Failed: {e}")
            return False
    
    return True


def test_combined_options():
    """Test combined configuration options."""
    print("\n" + "=" * 70)
    print("Testing Combined Configuration Options")
    print("=" * 70)
    
    config = {
        'USER_SPECIFIED_NODE_ASSIGNMENT': True,
        'SCALING_ITERATIONS': 2,
        'CHARGES': True,
        'REMOVE_DUMMY_ATOMS': True,
        'MIN_CELL_LENGTH': 10.0,
        'RANDOM_SEED': 42
    }
    
    print("\nConfiguration:")
    for key, value in config.items():
        print(f"   {key}: {value}")
    
    try:
        result = generate_cif(
            template_name="pcu",
            node_names="6c_Cu_1_Ch",
            edge_names="1B_1TrU",
            config=config
        )
        print(f"\n✓ Success: {result['cifname']}")
        print(f"   Atoms: {result['metadata']['num_atoms']}")
        print(f"   Bonds: {result['metadata']['num_bonds']}")
        print(f"   Random seed: {result['metadata']['random_seed']}")
        uc = result['metadata']['unit_cell_params']
        print(f"   Unit cell: a={uc['a']:.3f}, b={uc['b']:.3f}, c={uc['c']:.3f} Å")
    except Exception as e:
        print(f"\n✗ Failed: {e}")
        return False
    
    return True


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("ToBaCCo Configuration Options Test Suite")
    print("=" * 70)
    
    results = []
    
    # Test USER_SPECIFIED_NODE_ASSIGNMENT
    results.append(("USER_SPECIFIED_NODE_ASSIGNMENT", test_user_specified_node_assignment()))
    
    # Test SCALING_ITERATIONS
    results.append(("SCALING_ITERATIONS", test_scaling_iterations()))
    
    # Test combined options
    results.append(("Combined Options", test_combined_options()))
    
    # Print summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{status}: {test_name}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n✓ All tests passed!")
        return 0
    else:
        print("\n✗ Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
