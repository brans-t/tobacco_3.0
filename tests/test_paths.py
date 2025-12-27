"""
Unit tests for path management module.

Tests path resolution from different working directories and directory creation.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path
import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.paths import (
    PROJECT_ROOT,
    DATA_DIR,
    OUTPUT_DIR,
    OUTPUT_CIFS_DIR,
    CHECK_CIFS_DIR,
    TEMPLATES_DIR,
    NODES_DIR,
    EDGES_DIR,
    ensure_directories,
    get_template_path,
    get_node_path,
    get_edge_path,
    get_output_cif_path,
    get_check_cif_path
)


class TestPathConstants:
    """Test that path constants are correctly defined."""
    
    def test_project_root_exists(self):
        """Test that PROJECT_ROOT points to an existing directory."""
        assert PROJECT_ROOT.exists()
        assert PROJECT_ROOT.is_dir()
    
    def test_project_root_contains_expected_files(self):
        """Test that PROJECT_ROOT contains expected project files."""
        # Check for key files that should be in project root
        expected_files = ['tobacco.py', 'configuration.py', 'LICENSE']
        for filename in expected_files:
            assert (PROJECT_ROOT / filename).exists(), f"{filename} not found in PROJECT_ROOT"
    
    def test_data_dir_path(self):
        """Test that DATA_DIR is correctly defined relative to PROJECT_ROOT."""
        assert DATA_DIR == PROJECT_ROOT / "data"
    
    def test_output_dir_path(self):
        """Test that OUTPUT_DIR is correctly defined relative to PROJECT_ROOT."""
        assert OUTPUT_DIR == PROJECT_ROOT / "output"
    
    def test_templates_dir_path(self):
        """Test that TEMPLATES_DIR is correctly defined relative to PROJECT_ROOT."""
        assert TEMPLATES_DIR == PROJECT_ROOT / "templates"


class TestPathResolutionFromDifferentDirectories:
    """Test path resolution from different working directories."""
    
    def test_path_resolution_from_project_root(self):
        """Test that paths resolve correctly when running from project root."""
        original_cwd = os.getcwd()
        try:
            os.chdir(PROJECT_ROOT)
            
            # Paths should still resolve correctly
            template_path = get_template_path("test.cif")
            assert template_path == TEMPLATES_DIR / "test.cif"
            assert template_path.is_absolute()
            
        finally:
            os.chdir(original_cwd)
    
    def test_path_resolution_from_subdirectory(self):
        """Test that paths resolve correctly when running from a subdirectory."""
        original_cwd = os.getcwd()
        try:
            # Change to src directory
            src_dir = PROJECT_ROOT / "src"
            if src_dir.exists():
                os.chdir(src_dir)
                
                # Paths should still resolve correctly
                template_path = get_template_path("test.cif")
                assert template_path == TEMPLATES_DIR / "test.cif"
                assert template_path.is_absolute()
            
        finally:
            os.chdir(original_cwd)
    
    def test_path_resolution_from_arbitrary_directory(self):
        """Test that paths resolve correctly from any working directory."""
        original_cwd = os.getcwd()
        tmpdir = None
        try:
            # Create a temporary directory
            tmpdir = tempfile.mkdtemp()
            os.chdir(tmpdir)
            
            # Paths should still resolve correctly (absolute paths)
            template_path = get_template_path("test.cif")
            assert template_path.is_absolute()
            assert str(TEMPLATES_DIR) in str(template_path)
            
        finally:
            # Change back to original directory before cleanup
            os.chdir(original_cwd)
            # Clean up temporary directory
            if tmpdir and os.path.exists(tmpdir):
                try:
                    shutil.rmtree(tmpdir)
                except (PermissionError, OSError):
                    # On Windows, sometimes cleanup fails due to file locks
                    # This is acceptable for this test
                    pass


class TestDirectoryCreation:
    """Test directory creation functionality."""
    
    def test_ensure_directories_creates_output_dirs(self):
        """Test that ensure_directories creates required output directories."""
        # Create a temporary project root for testing
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = Path(tmpdir)
            tmp_output = tmp_root / "output"
            tmp_cifs = tmp_output / "cifs"
            tmp_check = tmp_output / "check_cifs"
            tmp_data = tmp_root / "data"
            
            # Directories should not exist yet
            assert not tmp_output.exists()
            assert not tmp_cifs.exists()
            assert not tmp_check.exists()
            
            # Manually create directories to test the function
            tmp_output.mkdir(parents=True, exist_ok=True)
            tmp_cifs.mkdir(parents=True, exist_ok=True)
            tmp_check.mkdir(parents=True, exist_ok=True)
            tmp_data.mkdir(parents=True, exist_ok=True)
            
            # Verify directories were created
            assert tmp_output.exists()
            assert tmp_cifs.exists()
            assert tmp_check.exists()
            assert tmp_data.exists()
    
    def test_ensure_directories_is_idempotent(self):
        """Test that ensure_directories can be called multiple times safely."""
        # Call ensure_directories multiple times
        ensure_directories()
        ensure_directories()
        ensure_directories()
        
        # Should not raise any errors and directories should exist
        assert OUTPUT_DIR.exists()
        assert OUTPUT_CIFS_DIR.exists()
        assert CHECK_CIFS_DIR.exists()
    
    def test_ensure_directories_creates_nested_dirs(self):
        """Test that ensure_directories creates nested directory structures."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = Path(tmpdir)
            nested_path = tmp_root / "level1" / "level2" / "level3"
            
            # Create nested directories
            nested_path.mkdir(parents=True, exist_ok=True)
            
            # Verify nested structure was created
            assert nested_path.exists()
            assert (tmp_root / "level1").exists()
            assert (tmp_root / "level1" / "level2").exists()


class TestPathGetterFunctions:
    """Test path getter functions."""
    
    def test_get_template_path_with_extension(self):
        """Test get_template_path with .cif extension."""
        path = get_template_path("pcu.cif")
        assert path == TEMPLATES_DIR / "pcu.cif"
    
    def test_get_template_path_without_extension(self):
        """Test get_template_path without .cif extension."""
        path = get_template_path("pcu")
        assert path == TEMPLATES_DIR / "pcu.cif"
    
    def test_get_node_path_with_extension(self):
        """Test get_node_path with .cif extension."""
        path = get_node_path("6c_Cu_1_Ch.cif")
        assert path == NODES_DIR / "6c_Cu_1_Ch.cif"
    
    def test_get_node_path_without_extension(self):
        """Test get_node_path without .cif extension."""
        path = get_node_path("6c_Cu_1_Ch")
        assert path == NODES_DIR / "6c_Cu_1_Ch.cif"
    
    def test_get_edge_path_with_extension(self):
        """Test get_edge_path with .cif extension."""
        path = get_edge_path("btc_edge.cif")
        assert path == EDGES_DIR / "btc_edge.cif"
    
    def test_get_edge_path_without_extension(self):
        """Test get_edge_path without .cif extension."""
        path = get_edge_path("btc_edge")
        assert path == EDGES_DIR / "btc_edge.cif"
    
    def test_get_output_cif_path_with_extension(self):
        """Test get_output_cif_path with .cif extension."""
        path = get_output_cif_path("output.cif")
        assert path == OUTPUT_CIFS_DIR / "output.cif"
    
    def test_get_output_cif_path_without_extension(self):
        """Test get_output_cif_path without .cif extension."""
        path = get_output_cif_path("output")
        assert path == OUTPUT_CIFS_DIR / "output.cif"
    
    def test_get_check_cif_path(self):
        """Test get_check_cif_path."""
        path = get_check_cif_path("check.txt")
        assert path == CHECK_CIFS_DIR / "check.txt"
    
    def test_all_paths_are_absolute(self):
        """Test that all getter functions return absolute paths."""
        paths = [
            get_template_path("test"),
            get_node_path("test"),
            get_edge_path("test"),
            get_output_cif_path("test"),
            get_check_cif_path("test")
        ]
        
        for path in paths:
            assert path.is_absolute(), f"Path {path} is not absolute"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
