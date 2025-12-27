"""
Charge generator module for deterministic charge assignment.

This module provides functions for generating deterministic atomic charges
using seeded random number generators. This ensures reproducibility of
MOF structures when the same random seed is used.
"""

import random
import numpy as np


# Default random seed for deterministic charge generation
DEFAULT_SEED = 42


def initialize_charge_generator(seed=None):
    """
    Initialize random number generator with seed for deterministic charge generation.
    
    This function creates a seeded random number generator that can be used
    for reproducible charge adjustments. Using the same seed will produce
    identical charge assignments across multiple runs.
    
    Args:
        seed (int or None): Random seed for the generator.
                           If None, uses DEFAULT_SEED (42).
                           The seed value will be documented in output metadata.
    
    Returns:
        random.Random: Seeded random number generator instance.
                      This generator should be passed to charge adjustment functions.
    
    Examples:
        >>> rng = initialize_charge_generator(seed=123)
        >>> # Use rng for deterministic charge adjustments
        
        >>> # Using default seed
        >>> rng = initialize_charge_generator()
        >>> # Will use seed=42 by default
    
    Notes:
        - The default seed (42) is used when no seed is provided
        - The same seed will always produce the same sequence of random numbers
        - Different seeds will produce different (but still deterministic) sequences
        - The seed value should be documented in MOF generation metadata
    """
    if seed is None:
        seed = DEFAULT_SEED
    
    # Create a new Random instance with the specified seed
    rng = random.Random(seed)
    
    return rng


def generate_charge_adjustment(num_atoms, rng):
    """
    Generate charge adjustment index using seeded random number generator.
    
    This function selects a random atom index for charge adjustment while
    maintaining determinism through the seeded RNG. The charge neutrality
    algorithm from the original implementation is preserved.
    
    Args:
        num_atoms (int): Total number of atoms in the structure.
                        Must be a positive integer.
        rng (random.Random): Seeded random number generator from initialize_charge_generator().
                            This ensures deterministic selection.
    
    Returns:
        int: Index of the atom to adjust (0-based indexing).
            The returned index is in the range [0, num_atoms-1].
    
    Raises:
        ValueError: If num_atoms is not a positive integer.
        TypeError: If rng is not a random.Random instance.
    
    Examples:
        >>> rng = initialize_charge_generator(seed=42)
        >>> atom_index = generate_charge_adjustment(100, rng)
        >>> # atom_index will always be the same for seed=42 and num_atoms=100
        
        >>> # Multiple calls with same RNG produce different indices
        >>> rng = initialize_charge_generator(seed=42)
        >>> idx1 = generate_charge_adjustment(100, rng)
        >>> idx2 = generate_charge_adjustment(100, rng)
        >>> # idx1 != idx2 (usually), but sequence is deterministic
    
    Notes:
        - Uses the seeded RNG to ensure reproducibility
        - Preserves the original charge assignment algorithm logic
        - The selected atom will have its charge adjusted to maintain neutrality
        - This function should be called after fix_charges() in the workflow
    """
    # Validate inputs
    if not isinstance(num_atoms, int) or num_atoms <= 0:
        raise ValueError(f"num_atoms must be a positive integer, got {num_atoms}")
    
    if not isinstance(rng, random.Random):
        raise TypeError(f"rng must be a random.Random instance, got {type(rng)}")
    
    # Use the seeded RNG to select a random atom index
    # This replaces the non-deterministic choice() call in the original code
    atom_index = rng.randrange(num_atoms)
    
    return atom_index


def get_seed_from_config(config=None):
    """
    Get random seed from configuration.
    
    Helper function to extract the random seed from configuration dictionary
    or use the default seed if not specified.
    
    Args:
        config (dict or None): Configuration dictionary that may contain 'RANDOM_SEED' key.
                              If None or if 'RANDOM_SEED' key is missing, returns DEFAULT_SEED.
    
    Returns:
        int: Random seed value to use for charge generation.
    
    Examples:
        >>> seed = get_seed_from_config({'RANDOM_SEED': 123})
        >>> # Returns 123
        
        >>> seed = get_seed_from_config(None)
        >>> # Returns DEFAULT_SEED (42)
        
        >>> seed = get_seed_from_config({})
        >>> # Returns DEFAULT_SEED (42)
    """
    if config is None:
        return DEFAULT_SEED
    
    return config.get('RANDOM_SEED', DEFAULT_SEED)
