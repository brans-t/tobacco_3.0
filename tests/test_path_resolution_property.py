"""
Property-based tests for path resolution consistency.

Feature: tobacco-refactoring, Property 2: Path Resolution Consistency
Validates: Requirements 1.5, 8.3

Tests that path resolution returns the same file from new or legacy location.
"""

import sys
import tempfile
import shutil
from pathlib import Path
import pytest
from hypothesis import given, strategies as st, settings

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.paths import (
    PROJECT_ROOT,
    TEMPLATES_DIR,
    NODES_DIR,
    EDGES_DIR,
    LEGACY_TEMPLATES_DIR,
    LEGACY_NODES_DIR,
    LEGACY_EDGES_DIR,
    get_template_path,
    get_node_path,
    get_edge_path
)


# Strategy for generating valid CIF filenames
@st.composite
def cif_filename(draw):
    """Generate valid CIF filenames for testing."""
    # Generate a simple alphanumeric name with underscores
    name = draw(st.text(
        alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_',
        min_size=3,
        max_size=20
    ))
    
    # Randomly decide whether to include .cif extension
    include_extension = draw(st.booleans())
    if include_extension:
        return f"{name}.cif"
    return name


class TestPathResolutionConsistency:
    """
    Property 2: Path Resolution Consistency
    
    For any building block name, resolving its path should return the same file
    regardless of whether it's in the new inputs/ directory or the legacy root directory.
    """
    
    @given(filename=cif_filename())
    @settings(max_examples=100)
    def test_template_path_resolution_consistency(self, filename):
        """
        Test that template path resolution returns same file from new or legacy location.
        
        Property: For any template filename, if the file exists in either location,
        get_template_path should return a path that points to the same file content.
        """
        # Normalize filename to ensure it has .cif extension
        if not filename.endswith('.cif'):
            normalized_filename = f"{filename}.cif"
        else:
            normalized_filename = filename
        
        # Get the resolved path
        resolved_path = get_template_path(filename)
        
        # Check if file exists in new location
        new_location = TEMPLATES_DIR / normalized_filename
        new_exists = new_location.exists()
        
        # Check if file exists in legacy location
        legacy_location = LEGACY_TEMPLATES_DIR / normalized_filename
        legacy_exists = legacy_location.exists()
        
        # Property: If file exists in either location, resolved path should point to it
        if new_exists:
            # Should prefer new location
            assert resolved_path == new_location, \
                f"Expected {new_location}, got {resolved_path}"
        elif legacy_exists:
            # Should fall back to legacy location
            assert resolved_path == legacy_location, \
                f"Expected {legacy_location}, got {resolved_path}"
        else:
            # If file doesn't exist in either location, should return new location path
            assert resolved_path == new_location, \
                f"Expected {new_location} for non-existent file, got {resolved_path}"
        
        # Property: Resolved path should always be absolute
        assert resolved_path.is_absolute(), \
            f"Resolved path {resolved_path} is not absolute"
    
    @given(filename=cif_filename())
    @settings(max_examples=100)
    def test_node_path_resolution_consistency(self, filename):
        """
        Test that node path resolution returns same file from new or legacy location.
        
        Property: For any node filename, if the file exists in either location,
        get_node_path should return a path that points to the same file content.
        """
        # Normalize filename to ensure it has .cif extension
        if not filename.endswith('.cif'):
            normalized_filename = f"{filename}.cif"
        else:
            normalized_filename = filename
        
        # Get the resolved path
        resolved_path = get_node_path(filename)
        
        # Check if file exists in new location
        new_location = NODES_DIR / normalized_filename
        new_exists = new_location.exists()
        
        # Check if file exists in legacy location
        legacy_location = LEGACY_NODES_DIR / normalized_filename
        legacy_exists = legacy_location.exists()
        
        # Property: If file exists in either location, resolved path should point to it
        if new_exists:
            # Should prefer new location
            assert resolved_path == new_location, \
                f"Expected {new_location}, got {resolved_path}"
        elif legacy_exists:
            # Should fall back to legacy location
            assert resolved_path == legacy_location, \
                f"Expected {legacy_location}, got {resolved_path}"
        else:
            # If file doesn't exist in either location, should return new location path
            assert resolved_path == new_location, \
                f"Expected {new_location} for non-existent file, got {resolved_path}"
        
        # Property: Resolved path should always be absolute
        assert resolved_path.is_absolute(), \
            f"Resolved path {resolved_path} is not absolute"
    
    @given(filename=cif_filename())
    @settings(max_examples=100)
    def test_edge_path_resolution_consistency(self, filename):
        """
        Test that edge path resolution returns same file from new or legacy location.
        
        Property: For any edge filename, if the file exists in either location,
        get_edge_path should return a path that points to the same file content.
        """
        # Normalize filename to ensure it has .cif extension
        if not filename.endswith('.cif'):
            normalized_filename = f"{filename}.cif"
        else:
            normalized_filename = filename
        
        # Get the resolved path
        resolved_path = get_edge_path(filename)
        
        # Check if file exists in new location
        new_location = EDGES_DIR / normalized_filename
        new_exists = new_location.exists()
        
        # Check if file exists in legacy location
        legacy_location = LEGACY_EDGES_DIR / normalized_filename
        legacy_exists = legacy_location.exists()
        
        # Property: If file exists in either location, resolved path should point to it
        if new_exists:
            # Should prefer new location
            assert resolved_path == new_location, \
                f"Expected {new_location}, got {resolved_path}"
        elif legacy_exists:
            # Should fall back to legacy location
            assert resolved_path == legacy_location, \
                f"Expected {legacy_location}, got {resolved_path}"
        else:
            # If file doesn't exist in either location, should return new location path
            assert resolved_path == new_location, \
                f"Expected {new_location} for non-existent file, got {resolved_path}"
        
        # Property: Resolved path should always be absolute
        assert resolved_path.is_absolute(), \
            f"Resolved path {resolved_path} is not absolute"
    
    def test_path_resolution_with_actual_files(self):
        """
        Test path resolution with actual files that exist in the project.
        
        This test uses real files from the legacy directories to verify that
        the path resolution correctly finds them.
        """
        # Test with actual template files
        if LEGACY_TEMPLATES_DIR.exists():
            template_files = list(LEGACY_TEMPLATES_DIR.glob("*.cif"))
            if template_files:
                # Test with first available template
                template_file = template_files[0]
                template_name = template_file.stem
                
                resolved_path = get_template_path(template_name)
                assert resolved_path.exists(), \
                    f"Resolved path {resolved_path} does not exist"
                assert resolved_path.name == template_file.name, \
                    f"Resolved filename {resolved_path.name} != {template_file.name}"
        
        # Test with actual node files
        if LEGACY_NODES_DIR.exists():
            node_files = list(LEGACY_NODES_DIR.glob("*.cif"))
            if node_files:
                # Test with first available node
                node_file = node_files[0]
                node_name = node_file.stem
                
                resolved_path = get_node_path(node_name)
                assert resolved_path.exists(), \
                    f"Resolved path {resolved_path} does not exist"
                assert resolved_path.name == node_file.name, \
                    f"Resolved filename {resolved_path.name} != {node_file.name}"
        
        # Test with actual edge files
        if LEGACY_EDGES_DIR.exists():
            edge_files = list(LEGACY_EDGES_DIR.glob("*.cif"))
            if edge_files:
                # Test with first available edge
                edge_file = edge_files[0]
                edge_name = edge_file.stem
                
                resolved_path = get_edge_path(edge_name)
                assert resolved_path.exists(), \
                    f"Resolved path {resolved_path} does not exist"
                assert resolved_path.name == edge_file.name, \
                    f"Resolved filename {resolved_path.name} != {edge_file.name}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
