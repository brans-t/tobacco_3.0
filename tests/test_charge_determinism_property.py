"""
Property-based tests for charge determinism.

Feature: tobacco-refactoring, Property 3: Charge Determinism
Validates: Requirements 4.1, 4.2, 4.3

Tests that same seed produces identical charges across multiple runs.
"""

import sys
from pathlib import Path
import pytest
from hypothesis import given, strategies as st, settings
import numpy as np

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.charge_generator import (
    initialize_charge_generator,
    generate_charge_adjustment,
    get_seed_from_config,
    DEFAULT_SEED
)
from src.utils.remove_net_charge import fix_charges


class TestChargeDeterminism:
    """
    Property 3: Charge Determinism
    
    For any MOF structure and random seed, generating charges twice with the same seed
    should produce identical charge values for all atoms.
    """
    
    @given(seed=st.integers(min_value=0, max_value=1000000))
    @settings(max_examples=100)
    def test_initialize_charge_generator_determinism(self, seed):
        """
        Test that initializing with same seed produces identical RNG sequences.
        
        Property: For any seed value, two RNGs initialized with the same seed
        should produce identical sequences of random numbers.
        """
        # Initialize two RNGs with the same seed
        rng1 = initialize_charge_generator(seed)
        rng2 = initialize_charge_generator(seed)
        
        # Generate sequences of random numbers
        sequence1 = [rng1.random() for _ in range(10)]
        sequence2 = [rng2.random() for _ in range(10)]
        
        # Property: Sequences should be identical
        assert sequence1 == sequence2, \
            f"RNGs with same seed {seed} produced different sequences"
    
    @given(
        seed=st.integers(min_value=0, max_value=1000000),
        num_atoms=st.integers(min_value=1, max_value=1000)
    )
    @settings(max_examples=100)
    def test_generate_charge_adjustment_determinism(self, seed, num_atoms):
        """
        Test that charge adjustment selection is deterministic with same seed.
        
        Property: For any seed and number of atoms, generating charge adjustment
        indices multiple times with the same seed should produce identical results.
        """
        # Initialize two RNGs with the same seed
        rng1 = initialize_charge_generator(seed)
        rng2 = initialize_charge_generator(seed)
        
        # Generate charge adjustment indices
        indices1 = [generate_charge_adjustment(num_atoms, rng1) for _ in range(5)]
        indices2 = [generate_charge_adjustment(num_atoms, rng2) for _ in range(5)]
        
        # Property: Indices should be identical
        assert indices1 == indices2, \
            f"Charge adjustments with same seed {seed} produced different indices"
        
        # Property: All indices should be valid (within range)
        for idx in indices1:
            assert 0 <= idx < num_atoms, \
                f"Generated index {idx} out of range [0, {num_atoms})"
    
    @given(seed=st.integers(min_value=0, max_value=1000000))
    @settings(max_examples=100)
    def test_fix_charges_determinism(self, seed):
        """
        Test that fix_charges produces deterministic results with same seed.
        
        Property: For any atom configuration and seed, calling fix_charges
        multiple times with the same seed should produce identical charge values.
        """
        # Create a simple test atom configuration
        # Format: [element, x, y, z, charge, original_element, index, bbtype]
        placed_all = [
            ['C1', '0.0', '0.0', '0.0', '0.1', 'C', '0', 'node'],
            ['C2', '1.0', '0.0', '0.0', '0.2', 'C', '1', 'node'],
            ['C3', '0.0', '1.0', '0.0', '-0.15', 'C', '2', 'edge'],
            ['C4', '0.0', '0.0', '1.0', '0.05', 'C', '3', 'edge'],
            ['H1', '1.0', '1.0', '0.0', '0.0', 'H', '4', 'node'],
        ]
        
        # Initialize two RNGs with the same seed
        rng1 = initialize_charge_generator(seed)
        rng2 = initialize_charge_generator(seed)
        
        # Fix charges with both RNGs
        fc_placed_all1, netcharge1, onetcharge1, rcb1 = fix_charges(placed_all.copy(), rng1)
        fc_placed_all2, netcharge2, onetcharge2, rcb2 = fix_charges(placed_all.copy(), rng2)
        
        # Property: Results should be identical
        assert netcharge1 == netcharge2, \
            f"Net charges differ: {netcharge1} != {netcharge2}"
        assert onetcharge1 == onetcharge2, \
            f"Original net charges differ: {onetcharge1} != {onetcharge2}"
        assert rcb1 == rcb2, \
            f"Charge adjustments differ: {rcb1} != {rcb2}"
        
        # Property: Charge values should be identical for all atoms
        for i, (atom1, atom2) in enumerate(zip(fc_placed_all1, fc_placed_all2)):
            assert atom1[4] == atom2[4], \
                f"Charge for atom {i} differs: {atom1[4]} != {atom2[4]}"
    
    @given(
        seed=st.integers(min_value=0, max_value=1000000),
        num_atoms=st.integers(min_value=1, max_value=100)
    )
    @settings(max_examples=100)
    def test_complete_charge_workflow_determinism(self, seed, num_atoms):
        """
        Test that complete charge generation workflow is deterministic.
        
        Property: For any seed, the complete workflow of fixing charges and
        removing net charge should produce identical results across runs.
        """
        # Create random atom configuration
        placed_all = []
        for i in range(num_atoms):
            # Random charge between -0.5 and 0.5
            charge = (i % 10) * 0.1 - 0.5
            atom = [f'C{i}', str(float(i)), '0.0', '0.0', str(charge), 'C', str(i), 'node']
            placed_all.append(atom)
        
        # Run workflow twice with same seed
        rng1 = initialize_charge_generator(seed)
        fc_placed_all1, netcharge1, _, _ = fix_charges(placed_all.copy(), rng1)
        remove_net1 = generate_charge_adjustment(len(fc_placed_all1), rng1)
        fc_placed_all1[remove_net1][4] -= np.round(netcharge1, 4)
        
        rng2 = initialize_charge_generator(seed)
        fc_placed_all2, netcharge2, _, _ = fix_charges(placed_all.copy(), rng2)
        remove_net2 = generate_charge_adjustment(len(fc_placed_all2), rng2)
        fc_placed_all2[remove_net2][4] -= np.round(netcharge2, 4)
        
        # Property: Selected atoms should be the same
        assert remove_net1 == remove_net2, \
            f"Different atoms selected for net charge removal: {remove_net1} != {remove_net2}"
        
        # Property: Final charges should be identical
        for i, (atom1, atom2) in enumerate(zip(fc_placed_all1, fc_placed_all2)):
            assert atom1[4] == atom2[4], \
                f"Final charge for atom {i} differs: {atom1[4]} != {atom2[4]}"
    
    def test_default_seed_usage(self):
        """
        Test that default seed is used when no seed is provided.
        
        Property: When no seed is provided, the system should use DEFAULT_SEED (42).
        """
        # Initialize without seed
        rng1 = initialize_charge_generator()
        rng2 = initialize_charge_generator(DEFAULT_SEED)
        
        # Generate sequences
        sequence1 = [rng1.random() for _ in range(10)]
        sequence2 = [rng2.random() for _ in range(10)]
        
        # Property: Should produce identical sequences
        assert sequence1 == sequence2, \
            "RNG without seed should use DEFAULT_SEED"
    
    def test_get_seed_from_config(self):
        """
        Test that seed is correctly extracted from configuration.
        
        Property: get_seed_from_config should return the seed from config
        or DEFAULT_SEED if not present.
        """
        # Test with seed in config
        config_with_seed = {'RANDOM_SEED': 123}
        seed = get_seed_from_config(config_with_seed)
        assert seed == 123, f"Expected 123, got {seed}"
        
        # Test with no seed in config
        config_without_seed = {}
        seed = get_seed_from_config(config_without_seed)
        assert seed == DEFAULT_SEED, f"Expected {DEFAULT_SEED}, got {seed}"
        
        # Test with None config
        seed = get_seed_from_config(None)
        assert seed == DEFAULT_SEED, f"Expected {DEFAULT_SEED}, got {seed}"
    
    @given(
        seed1=st.integers(min_value=0, max_value=1000000),
        seed2=st.integers(min_value=0, max_value=1000000)
    )
    @settings(max_examples=100)
    def test_different_seeds_produce_different_results(self, seed1, seed2):
        """
        Test that different seeds produce different results (usually).
        
        Property: For most pairs of different seeds, the generated sequences
        should be different. This validates that the seed actually affects output.
        """
        # Skip if seeds are the same
        if seed1 == seed2:
            return
        
        # Initialize RNGs with different seeds
        rng1 = initialize_charge_generator(seed1)
        rng2 = initialize_charge_generator(seed2)
        
        # Generate sequences
        sequence1 = [rng1.random() for _ in range(10)]
        sequence2 = [rng2.random() for _ in range(10)]
        
        # Property: Sequences should be different (with very high probability)
        # We allow for the extremely rare case where they might be the same
        # by checking multiple values
        differences = sum(1 for a, b in zip(sequence1, sequence2) if a != b)
        
        # At least some values should be different
        assert differences > 0, \
            f"Different seeds {seed1} and {seed2} produced identical sequences"
    
    def test_charge_adjustment_input_validation(self):
        """
        Test that generate_charge_adjustment validates inputs correctly.
        
        Property: Invalid inputs should raise appropriate exceptions.
        """
        rng = initialize_charge_generator(42)
        
        # Test with invalid num_atoms
        with pytest.raises(ValueError):
            generate_charge_adjustment(0, rng)
        
        with pytest.raises(ValueError):
            generate_charge_adjustment(-1, rng)
        
        # Test with invalid rng type
        with pytest.raises(TypeError):
            generate_charge_adjustment(10, "not_an_rng")
        
        with pytest.raises(TypeError):
            generate_charge_adjustment(10, None)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
