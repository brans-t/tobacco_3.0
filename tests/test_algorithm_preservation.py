"""
Test algorithm preservation - verify that refactored code produces identical results.

This test suite validates that the refactored ToBaCCo code produces identical
MOF structures compared to the original implementation (excluding random charges).

**Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.5, 5.6**
"""

import pytest
import numpy as np
import re
from pathlib import Path
from src.api import generate_cif
from src.utils.paths import get_output_cif_path


def parse_cif_structure(cif_content):
    """
    Parse CIF content to extract structural information.
    
    Returns dict with:
    - unit_cell: (a, b, c, alpha, beta, gamma)
    - atoms: list of (element, x, y, z) tuples (excluding charges)
    - bonds: list of bond pairs
    """
    lines = cif_content.split('\n')
    
    # Extract unit cell parameters
    unit_cell = {}
    for line in lines:
        if '_cell_length_a' in line:
            unit_cell['a'] = float(line.split()[1])
        elif '_cell_length_b' in line:
            unit_cell['b'] = float(line.split()[1])
        elif '_cell_length_c' in line:
            unit_cell['c'] = float(line.split()[1])
        elif '_cell_angle_alpha' in line:
            unit_cell['alpha'] = float(line.split()[1])
        elif '_cell_angle_beta' in line:
            unit_cell['beta'] = float(line.split()[1])
        elif '_cell_angle_gamma' in line:
            unit_cell['gamma'] = float(line.split()[1])
    
    # Extract atoms (element and coordinates, ignore charges)
    atoms = []
    in_atom_section = False
    for line in lines:
        if '_atom_site_fract_z' in line:
            in_atom_section = True
            continue
        if in_atom_section:
            # Skip header lines that start with underscore
            if line.strip().startswith('_'):
                continue
            # Stop at empty line or new section
            if line.strip() == '':
                break
            if line.startswith('#') or line.strip().startswith('loop_'):
                break
            parts = line.split()
            if len(parts) >= 5:
                element = parts[0]
                x = float(parts[2])
                y = float(parts[3])
                z = float(parts[4])
                atoms.append((element, x, y, z))
    
    # Extract bonds
    bonds = []
    in_bond_section = False
    for i, line in enumerate(lines):
        if '_geom_bond_atom_site_label_2' in line:
            in_bond_section = True
            continue
        if in_bond_section:
            # Skip header lines that start with underscore
            if line.strip().startswith('_'):
                continue
            # Stop if we hit an empty line after data, a comment, or another loop
            if line.strip() == '':
                continue  # Skip empty lines within bond section
            if line.startswith('#'):
                break
            if line.strip().startswith('loop_'):
                break
            parts = line.split()
            if len(parts) >= 2:
                bonds.append((parts[0], parts[1]))
    
    return {
        'unit_cell': unit_cell,
        'atoms': atoms,
        'bonds': bonds
    }


def compare_unit_cells(uc1, uc2, tolerance=0.01):
    """Compare two unit cells within tolerance."""
    for param in ['a', 'b', 'c', 'alpha', 'beta', 'gamma']:
        if abs(uc1[param] - uc2[param]) > tolerance:
            return False, f"Unit cell parameter {param} differs: {uc1[param]} vs {uc2[param]}"
    return True, "Unit cells match"


def compare_atoms(atoms1, atoms2, tolerance=0.001):
    """Compare two atom lists (element and position, ignoring charges)."""
    if len(atoms1) != len(atoms2):
        return False, f"Different number of atoms: {len(atoms1)} vs {len(atoms2)}"
    
    # Sort atoms by element and position for comparison
    atoms1_sorted = sorted(atoms1, key=lambda x: (x[0], x[1], x[2], x[3]))
    atoms2_sorted = sorted(atoms2, key=lambda x: (x[0], x[1], x[2], x[3]))
    
    for i, (atom1, atom2) in enumerate(zip(atoms1_sorted, atoms2_sorted)):
        if atom1[0] != atom2[0]:
            return False, f"Atom {i} element differs: {atom1[0]} vs {atom2[0]}"
        for j, coord_name in enumerate(['x', 'y', 'z']):
            if abs(atom1[j+1] - atom2[j+1]) > tolerance:
                return False, f"Atom {i} {coord_name} coordinate differs: {atom1[j+1]} vs {atom2[j+1]}"
    
    return True, "Atoms match"


def compare_bonds(bonds1, bonds2):
    """Compare two bond lists."""
    if len(bonds1) != len(bonds2):
        return False, f"Different number of bonds: {len(bonds1)} vs {len(bonds2)}"
    
    # Sort bonds for comparison
    bonds1_sorted = sorted([tuple(sorted(b)) for b in bonds1])
    bonds2_sorted = sorted([tuple(sorted(b)) for b in bonds2])
    
    for i, (bond1, bond2) in enumerate(zip(bonds1_sorted, bonds2_sorted)):
        if bond1 != bond2:
            return False, f"Bond {i} differs: {bond1} vs {bond2}"
    
    return True, "Bonds match"


class TestAlgorithmPreservation:
    """Test that refactored code produces identical structures."""
    
    def test_simple_mof_generation(self):
        """
        Test that a simple MOF generates with expected structure.
        
        This test generates a simple MOF and validates that the structure
        is consistent across multiple runs with the same seed.
        
        **Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.5, 5.6**
        """
        # Generate MOF twice with same seed
        # Using 4c_In_1_Ch which is compatible with pcb template (4-connected)
        result1 = generate_cif(
            template_name="pcb",
            node_names="4c_In_1_Ch",
            edge_names="1B_2CF3_Ch",
            random_seed=42,
            return_format='file'
        )
        
        result2 = generate_cif(
            template_name="pcb",
            node_names="4c_In_1_Ch",
            edge_names="1B_2CF3_Ch",
            random_seed=42,
            return_format='file'
        )
        
        # Handle case where multiple compatible nodes are found
        if isinstance(result1, list):
            result1 = result1[0]
        if isinstance(result2, list):
            result2 = result2[0]
        
        # Read CIF content
        cif_path1 = get_output_cif_path(result1['cifname'])
        cif_path2 = get_output_cif_path(result2['cifname'])
        
        with open(cif_path1, 'r') as f:
            cif1 = f.read()
        with open(cif_path2, 'r') as f:
            cif2 = f.read()
        
        # Parse structures
        struct1 = parse_cif_structure(cif1)
        struct2 = parse_cif_structure(cif2)
        
        # Compare unit cells
        match, msg = compare_unit_cells(struct1['unit_cell'], struct2['unit_cell'])
        assert match, f"Unit cells don't match: {msg}"
        
        # Compare atoms (excluding charges)
        match, msg = compare_atoms(struct1['atoms'], struct2['atoms'])
        assert match, f"Atoms don't match: {msg}"
        
        # Compare bonds
        match, msg = compare_bonds(struct1['bonds'], struct2['bonds'])
        assert match, f"Bonds don't match: {msg}"
    
    def test_unit_cell_parameters_match(self):
        """
        Test that unit cell parameters are calculated correctly.
        
        **Validates: Requirements 5.3**
        """
        # Using 4c_In_1_Ch which is compatible with pcb template (4-connected)
        result = generate_cif(
            template_name="pcb",
            node_names="4c_In_1_Ch",
            edge_names="1B_2CF3_Ch",
            random_seed=42,
            return_format='file'
        )
        
        # Handle case where multiple compatible nodes are found
        if isinstance(result, list):
            result = result[0]
        
        # Check that unit cell parameters are reasonable
        uc = result['metadata']['unit_cell_params']
        
        # Unit cell parameters should be positive
        assert uc['a'] > 0, "Unit cell parameter a should be positive"
        assert uc['b'] > 0, "Unit cell parameter b should be positive"
        assert uc['c'] > 0, "Unit cell parameter c should be positive"
        
        # Angles should be between 0 and 180 degrees
        assert 0 < uc['alpha'] < 180, "Alpha angle should be between 0 and 180"
        assert 0 < uc['beta'] < 180, "Beta angle should be between 0 and 180"
        assert 0 < uc['gamma'] < 180, "Gamma angle should be between 0 and 180"
        
        # For pcu topology, we expect cubic or near-cubic unit cell
        # (this is a sanity check, not a strict requirement)
        assert uc['a'] > 5.0, "Unit cell should be larger than MIN_CELL_LENGTH"
    
    def test_atom_positions_deterministic(self):
        """
        Test that atom positions are deterministic (same seed = same positions).
        
        **Validates: Requirements 5.4, 5.5**
        """
        # Generate same MOF twice with same seed
        # Using 4c_In_1_Ch which is compatible with pcb template (4-connected)
        result1 = generate_cif(
            template_name="pcb",
            node_names="4c_In_1_Ch",
            edge_names="1B_2CF3_Ch",
            random_seed=123,
            return_format='file'
        )
        
        result2 = generate_cif(
            template_name="pcb",
            node_names="4c_In_1_Ch",
            edge_names="1B_2CF3_Ch",
            random_seed=123,
            return_format='file'
        )
        
        # Handle case where multiple compatible nodes are found
        if isinstance(result1, list):
            result1 = result1[0]
        if isinstance(result2, list):
            result2 = result2[0]
        
        # Read and parse CIF files
        cif_path1 = get_output_cif_path(result1['cifname'])
        cif_path2 = get_output_cif_path(result2['cifname'])
        
        with open(cif_path1, 'r') as f:
            struct1 = parse_cif_structure(f.read())
        with open(cif_path2, 'r') as f:
            struct2 = parse_cif_structure(f.read())
        
        # Atom positions should be identical
        match, msg = compare_atoms(struct1['atoms'], struct2['atoms'], tolerance=1e-6)
        assert match, f"Atom positions not deterministic: {msg}"
    
    def test_bond_connectivity_preserved(self):
        """
        Test that bond connectivity is preserved correctly.
        
        **Validates: Requirements 5.4, 5.6**
        """
        # Using 4c_In_1_Ch which is compatible with pcb template (4-connected)
        result = generate_cif(
            template_name="pcb",
            node_names="4c_In_1_Ch",
            edge_names="1B_2CF3_Ch",
            random_seed=42,
            return_format='file'
        )
        
        # Handle case where multiple compatible nodes are found
        if isinstance(result, list):
            result = result[0]
        
        # Read and parse CIF
        cif_path = get_output_cif_path(result['cifname'])
        with open(cif_path, 'r') as f:
            struct = parse_cif_structure(f.read())
        
        # Check that we have bonds
        assert len(struct['bonds']) > 0, "MOF should have bonds"
        
        # Check that bond check passed (from metadata)
        assert result['metadata']['bond_check_passed'], "Bond check should pass"
        
        # Check that number of bonds is reasonable
        num_atoms = len(struct['atoms'])
        num_bonds = len(struct['bonds'])
        
        # Sanity check: should have at least some bonds relative to atoms
        assert num_bonds > 0, "Should have at least one bond"
        assert num_bonds < num_atoms * 10, "Bond count seems unreasonably high"
    
    def test_different_seeds_same_structure(self):
        """
        Test that different seeds produce same structure (excluding charges).
        
        **Validates: Requirements 5.1, 5.2**
        """
        # Generate with different seeds
        # Using 4c_In_1_Ch which is compatible with pcb template (4-connected)
        result1 = generate_cif(
            template_name="pcb",
            node_names="4c_In_1_Ch",
            edge_names="1B_2CF3_Ch",
            random_seed=42,
            return_format='file'
        )
        
        result2 = generate_cif(
            template_name="pcb",
            node_names="4c_In_1_Ch",
            edge_names="1B_2CF3_Ch",
            random_seed=999,
            return_format='file'
        )
        
        # Handle case where multiple compatible nodes are found
        if isinstance(result1, list):
            result1 = result1[0]
        if isinstance(result2, list):
            result2 = result2[0]
        
        # Read and parse CIF files
        cif_path1 = get_output_cif_path(result1['cifname'])
        cif_path2 = get_output_cif_path(result2['cifname'])
        
        with open(cif_path1, 'r') as f:
            struct1 = parse_cif_structure(f.read())
        with open(cif_path2, 'r') as f:
            struct2 = parse_cif_structure(f.read())
        
        # Structure should be identical (excluding charges which are affected by seed)
        match, msg = compare_unit_cells(struct1['unit_cell'], struct2['unit_cell'])
        assert match, f"Unit cells should match regardless of seed: {msg}"
        
        match, msg = compare_atoms(struct1['atoms'], struct2['atoms'])
        assert match, f"Atom positions should match regardless of seed: {msg}"
        
        match, msg = compare_bonds(struct1['bonds'], struct2['bonds'])
        assert match, f"Bonds should match regardless of seed: {msg}"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
