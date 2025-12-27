"""
Unit tests for input loader module.

Tests basic functionality of input loading, validation, and normalization.
"""

import sys
from pathlib import Path
import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.input_loader import (
    normalize_input_format,
    load_building_blocks,
    validate_inputs,
    InputValidationError,
    DatabaseError
)
from src.utils.paths import NODES_JSON, EDGES_JSON, TEMPLATE_JSON


class TestNormalizeInputFormat:
    """Test input format normalization."""
    
    def test_string_to_list(self):
        """Test converting single string to list."""
        result = normalize_input_format("pcu")
        assert result == ["pcu"]
    
    def test_list_preserved(self):
        """Test that list is preserved."""
        input_list = ["pcu", "dia", "sod"]
        result = normalize_input_format(input_list)
        assert result == input_list
    
    def test_dict_to_list(self):
        """Test converting dict to list of values."""
        input_dict = {"V1": "6c_Cu_1_Ch", "V2": "4c_Zn_1_Ch"}
        result = normalize_input_format(input_dict)
        assert set(result) == {"6c_Cu_1_Ch", "4c_Zn_1_Ch"}
        assert len(result) == 2
    
    def test_invalid_type_raises_error(self):
        """Test that invalid types raise InputValidationError."""
        with pytest.raises(InputValidationError):
            normalize_input_format(123)
        
        with pytest.raises(InputValidationError):
            normalize_input_format(None)
        
        with pytest.raises(InputValidationError):
            normalize_input_format((1, 2, 3))


class TestLoadBuildingBlocks:
    """Test loading building blocks from various sources."""
    
    def test_load_from_json_if_available(self):
        """Test loading from JSON database when available."""
        if not NODES_JSON.exists():
            pytest.skip("JSON database not available")
        
        # Load a node from JSON
        import json
        with open(NODES_JSON, 'r') as f:
            nodes_db = json.load(f)
        
        if len(nodes_db) == 0:
            pytest.skip("JSON database is empty")
        
        # Get first node name
        node_name = list(nodes_db.keys())[0].replace('.cif', '')
        
        # Load with auto mode (should use JSON)
        result = load_building_blocks(node_name, 'node', source='auto')
        
        assert len(result) == 1
        assert f"{node_name}.cif" in result
    
    def test_load_from_cif_explicitly(self):
        """Test loading from CIF files explicitly."""
        from src.utils.paths import LEGACY_NODES_DIR, NODES_DIR
        
        # Find a node CIF file
        node_files = []
        if NODES_DIR.exists():
            node_files.extend(list(NODES_DIR.glob("*.cif")))
        if LEGACY_NODES_DIR.exists():
            node_files.extend(list(LEGACY_NODES_DIR.glob("*.cif")))
        
        if len(node_files) == 0:
            pytest.skip("No node CIF files available")
        
        # Get first node
        node_file = node_files[0]
        node_name = node_file.stem
        
        # Load with CIF source
        result = load_building_blocks(node_name, 'node', source='cif')
        
        assert len(result) == 1
        assert f"{node_name}.cif" in result
        
        # Verify content matches file
        with open(node_file, 'r') as f:
            expected_content = f.read()
        assert result[f"{node_name}.cif"] == expected_content
    
    def test_load_multiple_blocks(self):
        """Test loading multiple building blocks at once."""
        from src.utils.paths import LEGACY_NODES_DIR, NODES_DIR
        
        # Find node CIF files
        node_files = []
        if NODES_DIR.exists():
            node_files.extend(list(NODES_DIR.glob("*.cif")))
        if LEGACY_NODES_DIR.exists():
            node_files.extend(list(LEGACY_NODES_DIR.glob("*.cif")))
        
        if len(node_files) < 2:
            pytest.skip("Need at least 2 node CIF files")
        
        # Get first two nodes
        node_names = [node_files[0].stem, node_files[1].stem]
        
        # Load both
        result = load_building_blocks(node_names, 'node', source='auto')
        
        assert len(result) == 2
        assert f"{node_names[0]}.cif" in result
        assert f"{node_names[1]}.cif" in result
    
    def test_invalid_block_type_raises_error(self):
        """Test that invalid block type raises error."""
        with pytest.raises(InputValidationError):
            load_building_blocks("test", "invalid_type", source='auto')
    
    def test_invalid_source_raises_error(self):
        """Test that invalid source raises error."""
        with pytest.raises(InputValidationError):
            load_building_blocks("test", "node", source='invalid_source')
    
    def test_nonexistent_file_raises_error(self):
        """Test that nonexistent file raises FileNotFoundError."""
        fake_name = "nonexistent_building_block_xyz123"
        
        with pytest.raises(FileNotFoundError):
            load_building_blocks(fake_name, 'node', source='cif')


class TestValidateInputs:
    """Test input validation."""
    
    def test_valid_inputs(self):
        """Test validation with valid inputs."""
        from src.utils.paths import LEGACY_NODES_DIR, LEGACY_EDGES_DIR, LEGACY_TEMPLATES_DIR
        from src.utils.paths import NODES_DIR, EDGES_DIR, TEMPLATES_DIR
        
        # Find available files
        template_files = []
        if TEMPLATES_DIR.exists():
            template_files.extend(list(TEMPLATES_DIR.glob("*.cif")))
        if LEGACY_TEMPLATES_DIR.exists():
            template_files.extend(list(LEGACY_TEMPLATES_DIR.glob("*.cif")))
        
        node_files = []
        if NODES_DIR.exists():
            node_files.extend(list(NODES_DIR.glob("*.cif")))
        if LEGACY_NODES_DIR.exists():
            node_files.extend(list(LEGACY_NODES_DIR.glob("*.cif")))
        
        edge_files = []
        if EDGES_DIR.exists():
            edge_files.extend(list(EDGES_DIR.glob("*.cif")))
        if LEGACY_EDGES_DIR.exists():
            edge_files.extend(list(LEGACY_EDGES_DIR.glob("*.cif")))
        
        if len(template_files) == 0 or len(node_files) == 0 or len(edge_files) == 0:
            pytest.skip("Need at least one template, node, and edge file")
        
        # Get first available files
        template_name = template_files[0].stem
        node_name = node_files[0].stem
        edge_name = edge_files[0].stem
        
        # Validate
        valid, error = validate_inputs(template_name, [node_name], [edge_name])
        
        assert valid is True
        assert error == ""
    
    def test_invalid_template_returns_error(self):
        """Test validation with invalid template."""
        from src.utils.paths import LEGACY_NODES_DIR, LEGACY_EDGES_DIR
        from src.utils.paths import NODES_DIR, EDGES_DIR
        
        # Find available files
        node_files = []
        if NODES_DIR.exists():
            node_files.extend(list(NODES_DIR.glob("*.cif")))
        if LEGACY_NODES_DIR.exists():
            node_files.extend(list(LEGACY_NODES_DIR.glob("*.cif")))
        
        edge_files = []
        if EDGES_DIR.exists():
            edge_files.extend(list(EDGES_DIR.glob("*.cif")))
        if LEGACY_EDGES_DIR.exists():
            edge_files.extend(list(LEGACY_EDGES_DIR.glob("*.cif")))
        
        if len(node_files) == 0 or len(edge_files) == 0:
            pytest.skip("Need at least one node and edge file")
        
        node_name = node_files[0].stem
        edge_name = edge_files[0].stem
        
        # Validate with fake template
        valid, error = validate_inputs("nonexistent_template", [node_name], [edge_name])
        
        assert valid is False
        assert "template" in error.lower()
    
    def test_empty_lists_return_error(self):
        """Test validation with empty lists."""
        valid, error = validate_inputs("pcu", [], ["btc_edge"])
        assert valid is False
        assert "empty" in error.lower()
        
        valid, error = validate_inputs("pcu", ["6c_Cu_1_Ch"], [])
        assert valid is False
        assert "empty" in error.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
