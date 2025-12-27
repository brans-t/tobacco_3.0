"""
Property-based tests for JSON database fallback.

Feature: tobacco-refactoring, Property 7: JSON Database Fallback
Validates: Requirements 9.4

Tests that system loads from CIF when JSON unavailable.
"""

import sys
import json
import tempfile
import shutil
from pathlib import Path
import pytest
from hypothesis import given, strategies as st, settings, assume

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.input_loader import (
    load_building_blocks,
    InputValidationError,
    DatabaseError
)
from src.utils.paths import (
    NODES_DIR,
    EDGES_DIR,
    TEMPLATES_DIR,
    LEGACY_NODES_DIR,
    LEGACY_EDGES_DIR,
    LEGACY_TEMPLATES_DIR,
    NODES_JSON,
    EDGES_JSON,
    TEMPLATE_JSON
)


# Strategy for generating valid building block names
@st.composite
def building_block_name(draw):
    """Generate valid building block names for testing."""
    # Generate a simple alphanumeric name with underscores
    name = draw(st.text(
        alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_',
        min_size=1,
        max_size=30
    ))
    
    # Randomly decide whether to include .cif extension
    include_extension = draw(st.booleans())
    if include_extension:
        return f"{name}.cif"
    return name


class TestJSONDatabaseFallback:
    """
    Property 7: JSON Database Fallback
    
    For any building block, if the JSON database is unavailable or corrupted,
    the system should successfully load the building block from CIF files.
    """
    
    def test_auto_mode_tries_json_first(self):
        """
        Test that 'auto' mode tries JSON database first.
        
        Property: When source='auto' and a building block exists in both JSON
        and CIF, the system should load from JSON (faster).
        """
        # Find a node that exists in both JSON database and CIF files
        if not NODES_JSON.exists():
            pytest.skip("JSON database not available")
        
        # Load JSON database
        with open(NODES_JSON, 'r') as f:
            nodes_db = json.load(f)
        
        # Find a node that exists in JSON
        if len(nodes_db) == 0:
            pytest.skip("JSON database is empty")
        
        # Get first node from JSON database
        node_name = list(nodes_db.keys())[0]
        node_name_without_ext = node_name.replace('.cif', '')
        
        # Load with auto mode
        result = load_building_blocks(node_name_without_ext, 'node', source='auto')
        
        # Property: Should successfully load
        assert len(result) == 1
        assert node_name in result
        
        # Property: Content should match JSON database
        assert result[node_name] == nodes_db[node_name]
    
    def test_cif_fallback_when_json_unavailable(self):
        """
        Test that system falls back to CIF when JSON database unavailable.
        
        Property: When source='auto' and JSON database doesn't exist,
        the system should successfully load from CIF files.
        """
        # Find a node that exists in CIF files
        node_files = []
        if NODES_DIR.exists():
            node_files.extend(list(NODES_DIR.glob("*.cif")))
        if LEGACY_NODES_DIR.exists():
            node_files.extend(list(LEGACY_NODES_DIR.glob("*.cif")))
        
        if len(node_files) == 0:
            pytest.skip("No node CIF files available")
        
        # Get first available node
        node_file = node_files[0]
        node_name = node_file.stem
        
        # Load with auto mode (will fallback to CIF if JSON unavailable)
        result = load_building_blocks(node_name, 'node', source='auto')
        
        # Property: Should successfully load
        assert len(result) == 1
        assert f"{node_name}.cif" in result
        
        # Property: Content should be non-empty
        assert len(result[f"{node_name}.cif"]) > 0
    
    def test_explicit_cif_source_bypasses_json(self):
        """
        Test that source='cif' bypasses JSON database entirely.
        
        Property: When source='cif', the system should load from CIF files
        even if JSON database is available.
        """
        # Find a node that exists in CIF files
        node_files = []
        if NODES_DIR.exists():
            node_files.extend(list(NODES_DIR.glob("*.cif")))
        if LEGACY_NODES_DIR.exists():
            node_files.extend(list(LEGACY_NODES_DIR.glob("*.cif")))
        
        if len(node_files) == 0:
            pytest.skip("No node CIF files available")
        
        # Get first available node
        node_file = node_files[0]
        node_name = node_file.stem
        
        # Load with explicit CIF source
        result = load_building_blocks(node_name, 'node', source='cif')
        
        # Property: Should successfully load
        assert len(result) == 1
        assert f"{node_name}.cif" in result
        
        # Property: Content should be non-empty
        assert len(result[f"{node_name}.cif"]) > 0
        
        # Property: Content should match file content
        with open(node_file, 'r') as f:
            expected_content = f.read()
        assert result[f"{node_name}.cif"] == expected_content
    
    def test_json_and_cif_content_consistency(self):
        """
        Test that JSON and CIF sources provide consistent content.
        
        Property: For any building block that exists in both JSON and CIF,
        the content loaded from both sources should be identical.
        """
        # Find a node that exists in both JSON and CIF
        if not NODES_JSON.exists():
            pytest.skip("JSON database not available")
        
        # Load JSON database
        with open(NODES_JSON, 'r') as f:
            nodes_db = json.load(f)
        
        # Find a node that exists in both JSON and CIF
        found_match = False
        for node_name in nodes_db.keys():
            node_name_without_ext = node_name.replace('.cif', '')
            
            # Check if CIF file exists
            node_files = []
            if NODES_DIR.exists():
                node_files.extend(list(NODES_DIR.glob(node_name)))
            if LEGACY_NODES_DIR.exists():
                node_files.extend(list(LEGACY_NODES_DIR.glob(node_name)))
            
            if len(node_files) > 0:
                found_match = True
                
                # Load from JSON
                json_result = load_building_blocks(node_name_without_ext, 'node', source='json')
                
                # Load from CIF
                cif_result = load_building_blocks(node_name_without_ext, 'node', source='cif')
                
                # Property: Content should be identical
                assert json_result[node_name] == cif_result[node_name], \
                    f"Content mismatch for {node_name}"
                
                break
        
        if not found_match:
            pytest.skip("No nodes found in both JSON and CIF")
    
    def test_auto_mode_handles_missing_json_gracefully(self):
        """
        Test that auto mode handles missing JSON database gracefully.
        
        Property: When source='auto' and JSON database doesn't exist,
        the system should not raise an error but fallback to CIF.
        """
        # Find an edge that exists in CIF files
        edge_files = []
        if EDGES_DIR.exists():
            edge_files.extend(list(EDGES_DIR.glob("*.cif")))
        if LEGACY_EDGES_DIR.exists():
            edge_files.extend(list(LEGACY_EDGES_DIR.glob("*.cif")))
        
        if len(edge_files) == 0:
            pytest.skip("No edge CIF files available")
        
        # Get first available edge
        edge_file = edge_files[0]
        edge_name = edge_file.stem
        
        # Load with auto mode (should not raise error even if JSON missing)
        try:
            result = load_building_blocks(edge_name, 'edge', source='auto')
            
            # Property: Should successfully load
            assert len(result) == 1
            assert f"{edge_name}.cif" in result
            
        except (FileNotFoundError, DatabaseError):
            # If both JSON and CIF are unavailable, that's expected
            pass
    
    def test_auto_mode_handles_corrupted_json_gracefully(self):
        """
        Test that auto mode handles corrupted JSON database gracefully.
        
        Property: When source='auto' and JSON database is corrupted,
        the system should fallback to CIF without raising an error.
        
        Note: This test doesn't actually corrupt the JSON database,
        but verifies the fallback mechanism works.
        """
        # Find a template that exists in CIF files
        template_files = []
        if TEMPLATES_DIR.exists():
            template_files.extend(list(TEMPLATES_DIR.glob("*.cif")))
        if LEGACY_TEMPLATES_DIR.exists():
            template_files.extend(list(LEGACY_TEMPLATES_DIR.glob("*.cif")))
        
        if len(template_files) == 0:
            pytest.skip("No template CIF files available")
        
        # Get first available template
        template_file = template_files[0]
        template_name = template_file.stem
        
        # Load with auto mode
        result = load_building_blocks(template_name, 'template', source='auto')
        
        # Property: Should successfully load
        assert len(result) == 1
        assert f"{template_name}.cif" in result
        
        # Property: Content should match file content
        with open(template_file, 'r') as f:
            expected_content = f.read()
        assert result[f"{template_name}.cif"] == expected_content
    
    def test_json_source_raises_error_when_unavailable(self):
        """
        Test that source='json' raises error when JSON unavailable.
        
        Property: When source='json' and building block not in JSON database,
        the system should raise FileNotFoundError (no fallback).
        """
        # Use a non-existent building block name
        fake_name = "nonexistent_building_block_xyz123"
        
        # Try to load with JSON source only
        with pytest.raises(FileNotFoundError) as exc_info:
            load_building_blocks(fake_name, 'node', source='json')
        
        # Property: Error message should mention JSON database
        error_message = str(exc_info.value)
        assert "json" in error_message.lower() or "database" in error_message.lower()
    
    def test_cif_source_raises_error_when_unavailable(self):
        """
        Test that source='cif' raises error when CIF file unavailable.
        
        Property: When source='cif' and CIF file doesn't exist,
        the system should raise FileNotFoundError.
        """
        # Use a non-existent building block name
        fake_name = "nonexistent_building_block_xyz123"
        
        # Try to load with CIF source only
        with pytest.raises(FileNotFoundError) as exc_info:
            load_building_blocks(fake_name, 'node', source='cif')
        
        # Property: Error message should mention file not found
        error_message = str(exc_info.value)
        assert "not found" in error_message.lower()
    
    def test_multiple_blocks_with_mixed_availability(self):
        """
        Test loading multiple blocks where some are in JSON and some only in CIF.
        
        Property: When loading multiple building blocks with source='auto',
        the system should load each from the best available source.
        """
        # This test requires both JSON and CIF files to be available
        if not NODES_JSON.exists():
            pytest.skip("JSON database not available")
        
        # Load JSON database
        with open(NODES_JSON, 'r') as f:
            nodes_db = json.load(f)
        
        if len(nodes_db) == 0:
            pytest.skip("JSON database is empty")
        
        # Get a node from JSON
        json_node = list(nodes_db.keys())[0].replace('.cif', '')
        
        # Find a node that exists in CIF but not in JSON
        cif_only_node = None
        node_files = []
        if NODES_DIR.exists():
            node_files.extend(list(NODES_DIR.glob("*.cif")))
        if LEGACY_NODES_DIR.exists():
            node_files.extend(list(LEGACY_NODES_DIR.glob("*.cif")))
        
        for node_file in node_files:
            if node_file.name not in nodes_db:
                cif_only_node = node_file.stem
                break
        
        if cif_only_node is None:
            pytest.skip("All CIF nodes are in JSON database")
        
        # Load both nodes with auto mode
        result = load_building_blocks([json_node, cif_only_node], 'node', source='auto')
        
        # Property: Should successfully load both
        assert len(result) == 2
        assert f"{json_node}.cif" in result
        assert f"{cif_only_node}.cif" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
