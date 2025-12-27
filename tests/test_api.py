"""
Unit tests for API module.

Tests filename normalization, input validation, configuration override, and error handling.
"""

import os
import sys
from pathlib import Path
import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.api import (
    _normalize_filename,
    _validate_inputs,
    _merge_config,
    _get_default_config,
    _prepare_node_files,
    _prepare_edge_files,
    generate_cif
)
from src.utils.paths import TEMPLATES_DIR, NODES_DIR, EDGES_DIR


class TestFilenameNormalization:
    """Test filename normalization functionality."""
    
    def test_normalize_filename_without_extension(self):
        """Test that .cif extension is added when not present."""
        result = _normalize_filename("pcu")
        assert result == "pcu.cif"
    
    def test_normalize_filename_with_extension(self):
        """Test that .cif extension is not duplicated."""
        result = _normalize_filename("pcu.cif")
        assert result == "pcu.cif"
    
    def test_normalize_filename_empty_string(self):
        """Test normalization with empty string."""
        result = _normalize_filename("")
        assert result == ".cif"
    
    def test_normalize_filename_with_path(self):
        """Test normalization with path-like string."""
        result = _normalize_filename("path/to/template")
        assert result == "path/to/template.cif"
    
    def test_normalize_filename_with_multiple_dots(self):
        """Test normalization with multiple dots in filename."""
        result = _normalize_filename("my.template.name")
        assert result == "my.template.name.cif"


class TestInputValidation:
    """Test input validation functionality."""
    
    def test_validate_inputs_with_valid_list_inputs(self):
        """Test validation with valid list inputs (should not raise)."""
        # This test requires actual files to exist
        # We'll test the validation logic without file existence checks
        pass
    
    def test_validate_inputs_empty_template_name(self):
        """Test that empty template_name raises ValueError."""
        with pytest.raises(ValueError, match="template_name must be a non-empty string"):
            _validate_inputs("", ["node1"], ["edge1"])
    
    def test_validate_inputs_none_template_name(self):
        """Test that None template_name raises ValueError."""
        with pytest.raises(ValueError, match="template_name must be a non-empty string"):
            _validate_inputs(None, ["node1"], ["edge1"])
    
    def test_validate_inputs_invalid_node_names_type(self):
        """Test that invalid node_names type raises ValueError."""
        with pytest.raises(ValueError, match="node_names must be"):
            _validate_inputs("template", 12345, ["edge1"])
    
    def test_validate_inputs_empty_node_names_list(self):
        """Test that empty node_names list raises ValueError."""
        with pytest.raises(ValueError, match="node_names list cannot be empty"):
            _validate_inputs("template", [], ["edge1"])
    
    def test_validate_inputs_empty_node_names_dict(self):
        """Test that empty node_names dict raises ValueError."""
        with pytest.raises(ValueError, match="node_names dict cannot be empty"):
            _validate_inputs("template", {}, ["edge1"])
    
    def test_validate_inputs_invalid_edge_names_type(self):
        """Test that invalid edge_names type raises ValueError."""
        with pytest.raises(ValueError, match="edge_names must be"):
            _validate_inputs("template", ["node1"], 12345)
    
    def test_validate_inputs_empty_edge_names_list(self):
        """Test that empty edge_names list raises ValueError."""
        with pytest.raises(ValueError, match="edge_names list cannot be empty"):
            _validate_inputs("template", ["node1"], [])
    
    def test_validate_inputs_nonexistent_template(self):
        """Test that nonexistent template file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError, match="Template file.*not found"):
            _validate_inputs("nonexistent_template_xyz123", ["node1"], ["edge1"])
    
    def test_validate_inputs_nonexistent_node(self):
        """Test that nonexistent node file raises FileNotFoundError."""
        # First, we need a valid template
        # Check if any template exists
        if TEMPLATES_DIR.exists() and list(TEMPLATES_DIR.glob("*.cif")):
            template = list(TEMPLATES_DIR.glob("*.cif"))[0].stem
            with pytest.raises(FileNotFoundError, match="Node file.*not found"):
                _validate_inputs(template, ["nonexistent_node_xyz123"], ["edge1"])
    
    def test_validate_inputs_nonexistent_edge(self):
        """Test that nonexistent edge file raises FileNotFoundError."""
        # First, we need valid template and node
        if TEMPLATES_DIR.exists() and list(TEMPLATES_DIR.glob("*.cif")):
            template = list(TEMPLATES_DIR.glob("*.cif"))[0].stem
            if NODES_DIR.exists() and list(NODES_DIR.glob("*.cif")):
                node = list(NODES_DIR.glob("*.cif"))[0].stem
                with pytest.raises(FileNotFoundError, match="Edge file.*not found"):
                    _validate_inputs(template, [node], ["nonexistent_edge_xyz123"])


class TestConfigurationMerging:
    """Test configuration merging functionality."""
    
    def test_merge_config_with_none(self):
        """Test that None user_config returns copy of default config."""
        default = {"key1": "value1", "key2": "value2"}
        result = _merge_config(None, default)
        
        assert result == default
        assert result is not default  # Should be a copy
    
    def test_merge_config_with_empty_dict(self):
        """Test that empty user_config returns copy of default config."""
        default = {"key1": "value1", "key2": "value2"}
        result = _merge_config({}, default)
        
        assert result == default
    
    def test_merge_config_override_single_value(self):
        """Test that user config overrides single default value."""
        default = {"key1": "value1", "key2": "value2"}
        user = {"key1": "new_value"}
        result = _merge_config(user, default)
        
        assert result["key1"] == "new_value"
        assert result["key2"] == "value2"
    
    def test_merge_config_override_multiple_values(self):
        """Test that user config overrides multiple default values."""
        default = {"key1": "value1", "key2": "value2", "key3": "value3"}
        user = {"key1": "new1", "key3": "new3"}
        result = _merge_config(user, default)
        
        assert result["key1"] == "new1"
        assert result["key2"] == "value2"
        assert result["key3"] == "new3"
    
    def test_merge_config_add_new_key(self):
        """Test that user config can add new keys."""
        default = {"key1": "value1"}
        user = {"key2": "value2"}
        result = _merge_config(user, default)
        
        assert result["key1"] == "value1"
        assert result["key2"] == "value2"
    
    def test_merge_config_does_not_modify_default(self):
        """Test that merging does not modify the default config."""
        default = {"key1": "value1", "key2": "value2"}
        user = {"key1": "new_value"}
        
        original_default = default.copy()
        result = _merge_config(user, default)
        
        assert default == original_default  # Default should be unchanged


class TestDefaultConfig:
    """Test default configuration retrieval."""
    
    def test_get_default_config_returns_dict(self):
        """Test that _get_default_config returns a dictionary."""
        config = _get_default_config()
        assert isinstance(config, dict)
    
    def test_get_default_config_has_required_keys(self):
        """Test that default config has all required keys."""
        config = _get_default_config()
        
        required_keys = [
            'CHARGES', 'CONNECTION_SITE_BOND_LENGTH', 'SYMMETRY_TOL',
            'BOND_TOL', 'SCALING_ITERATIONS', 'MIN_CELL_LENGTH',
            'OPT_METHOD', 'REMOVE_DUMMY_ATOMS'
        ]
        
        for key in required_keys:
            assert key in config, f"Required key '{key}' not in default config"
    
    def test_get_default_config_values_are_correct_types(self):
        """Test that default config values have correct types."""
        config = _get_default_config()
        
        # Test some key types
        assert isinstance(config['CHARGES'], bool)
        assert isinstance(config['CONNECTION_SITE_BOND_LENGTH'], (int, float))
        assert isinstance(config['SYMMETRY_TOL'], dict)
        assert isinstance(config['BOND_TOL'], (int, float))
        assert isinstance(config['SCALING_ITERATIONS'], int)
        assert isinstance(config['OPT_METHOD'], str)


class TestPrepareNodeFiles:
    """Test node files preparation."""
    
    def test_prepare_node_files_from_list(self):
        """Test preparing node files from a list."""
        node_names = ["node1", "node2.cif", "node3"]
        result = _prepare_node_files(node_names)
        
        assert result == ["node1.cif", "node2.cif", "node3.cif"]
    
    def test_prepare_node_files_from_dict(self):
        """Test preparing node files from a dictionary."""
        node_names = {"V": "node1", "W": "node2.cif"}
        result = _prepare_node_files(node_names)
        
        assert "node1.cif" in result
        assert "node2.cif" in result
        assert len(result) == 2
    
    def test_prepare_node_files_empty_list(self):
        """Test preparing node files from empty list."""
        result = _prepare_node_files([])
        assert result == []


class TestPrepareEdgeFiles:
    """Test edge files preparation."""
    
    def test_prepare_edge_files_basic(self):
        """Test preparing edge files from a list."""
        edge_names = ["edge1", "edge2.cif", "edge3"]
        result = _prepare_edge_files(edge_names)
        
        assert result == ["edge1.cif", "edge2.cif", "edge3.cif"]
    
    def test_prepare_edge_files_empty_list(self):
        """Test preparing edge files from empty list."""
        result = _prepare_edge_files([])
        assert result == []



class TestGenerateCifErrorHandling:
    """Test error handling in generate_cif function."""
    
    def test_generate_cif_invalid_template(self):
        """Test that generate_cif raises error for invalid template."""
        with pytest.raises(ValueError, match="Input validation failed"):
            generate_cif("nonexistent_template_xyz", ["node1"], ["edge1"])
    
    def test_generate_cif_invalid_node(self):
        """Test that generate_cif raises error for invalid node."""
        # Need a valid template
        if TEMPLATES_DIR.exists() and list(TEMPLATES_DIR.glob("*.cif")):
            template = list(TEMPLATES_DIR.glob("*.cif"))[0].stem
            with pytest.raises(ValueError, match="Input validation failed"):
                generate_cif(template, ["nonexistent_node_xyz"], ["edge1"])
    
    def test_generate_cif_invalid_edge(self):
        """Test that generate_cif raises error for invalid edge."""
        # Need valid template and node
        if TEMPLATES_DIR.exists() and list(TEMPLATES_DIR.glob("*.cif")):
            template = list(TEMPLATES_DIR.glob("*.cif"))[0].stem
            if NODES_DIR.exists() and list(NODES_DIR.glob("*.cif")):
                node = list(NODES_DIR.glob("*.cif"))[0].stem
                with pytest.raises(ValueError, match="Input validation failed"):
                    generate_cif(template, [node], ["nonexistent_edge_xyz"])
    
    def test_generate_cif_empty_template_name(self):
        """Test that generate_cif raises error for empty template name."""
        with pytest.raises(ValueError):
            generate_cif("", ["node1"], ["edge1"])
    
    def test_generate_cif_empty_node_list(self):
        """Test that generate_cif raises error for empty node list."""
        with pytest.raises(ValueError):
            generate_cif("template", [], ["edge1"])
    
    def test_generate_cif_empty_edge_list(self):
        """Test that generate_cif raises error for empty edge list."""
        with pytest.raises(ValueError):
            generate_cif("template", ["node1"], [])


class TestGenerateCifConfigOverride:
    """Test configuration override in generate_cif function."""
    
    def test_generate_cif_accepts_config_parameter(self):
        """Test that generate_cif accepts config parameter without error."""
        # This is a basic test that the parameter is accepted
        # Full integration test would require valid files
        config = {"CHARGES": False, "SCALING_ITERATIONS": 5}
        
        # We can't run a full test without valid files, but we can verify
        # the function signature accepts the parameter
        import inspect
        sig = inspect.signature(generate_cif)
        assert 'config' in sig.parameters
        assert sig.parameters['config'].default is None


class TestGenerateCifReturnValue:
    """Test return value structure of generate_cif function."""
    
    def test_generate_cif_return_structure(self):
        """Test that generate_cif returns expected structure."""
        # This test would require valid template, node, and edge files
        # For now, we document the expected structure
        
        # Expected return structure:
        # {
        #     "cif_content": str,
        #     "cifname": str,
        #     "metadata": {
        #         "template": str,
        #         "nodes": list,
        #         "edges": list,
        #         "generation_time": float,
        #         "unit_cell_params": dict,
        #         "num_atoms": int,
        #         "num_bonds": int,
        #         "bond_check_passed": bool
        #     }
        # }
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
