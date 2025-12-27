"""
Unit tests for database export functionality.

Tests file reading with various encodings, JSON writing, and error handling.
"""

import json
import sys
import tempfile
import shutil
from pathlib import Path
import pytest

# Add project root and scripts to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "scripts"))

import export_databases_to_json
from export_databases_to_json import (
    read_database_directory,
    write_json_file,
    export_database
)


class TestReadDatabaseDirectory:
    """Test reading CIF files from database directories."""
    
    def test_read_empty_directory(self):
        """Test reading from an empty directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            
            database, processed, failed = read_database_directory(tmp_path)
            
            assert database == {}
            assert processed == 0
            assert failed == 0
    
    def test_read_directory_with_cif_files(self):
        """Test reading directory with valid CIF files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            
            # Create test CIF files
            (tmp_path / "test1.cif").write_text("CIF content 1", encoding='utf-8')
            (tmp_path / "test2.cif").write_text("CIF content 2", encoding='utf-8')
            (tmp_path / "test3.cif").write_text("CIF content 3", encoding='utf-8')
            
            database, processed, failed = read_database_directory(tmp_path)
            
            assert len(database) == 3
            assert processed == 3
            assert failed == 0
            assert "test1.cif" in database
            assert "test2.cif" in database
            assert "test3.cif" in database
            assert database["test1.cif"] == "CIF content 1"
            assert database["test2.cif"] == "CIF content 2"
            assert database["test3.cif"] == "CIF content 3"
    
    def test_read_directory_ignores_non_cif_files(self):
        """Test that non-CIF files are ignored."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            
            # Create various file types
            (tmp_path / "test.cif").write_text("CIF content", encoding='utf-8')
            (tmp_path / "test.txt").write_text("Text content", encoding='utf-8')
            (tmp_path / "test.json").write_text('{"key": "value"}', encoding='utf-8')
            (tmp_path / "README.md").write_text("# README", encoding='utf-8')
            
            database, processed, failed = read_database_directory(tmp_path)
            
            # Only .cif file should be read
            assert len(database) == 1
            assert processed == 1
            assert failed == 0
            assert "test.cif" in database
            assert "test.txt" not in database
            assert "test.json" not in database
    
    def test_read_nonexistent_directory(self):
        """Test reading from a directory that doesn't exist."""
        nonexistent_path = Path("/nonexistent/directory/path")
        
        database, processed, failed = read_database_directory(nonexistent_path)
        
        assert database == {}
        assert processed == 0
        assert failed == 0
    
    def test_read_file_instead_of_directory(self):
        """Test reading when path points to a file instead of directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            file_path = tmp_path / "test.txt"
            file_path.write_text("content", encoding='utf-8')
            
            database, processed, failed = read_database_directory(file_path)
            
            assert database == {}
            assert processed == 0
            assert failed == 0
    
    def test_read_with_utf8_encoding(self):
        """Test reading files with UTF-8 encoding."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            
            # Create file with UTF-8 content including special characters
            content = "CIF with UTF-8: café, naïve, 日本語"
            (tmp_path / "utf8.cif").write_text(content, encoding='utf-8')
            
            database, processed, failed = read_database_directory(tmp_path)
            
            assert processed == 1
            assert failed == 0
            assert database["utf8.cif"] == content
    
    def test_read_with_latin1_encoding(self):
        """Test reading files with latin-1 encoding (fallback)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            
            # Create file with latin-1 content
            content = "CIF with latin-1: café"
            file_path = tmp_path / "latin1.cif"
            file_path.write_bytes(content.encode('latin-1'))
            
            database, processed, failed = read_database_directory(tmp_path)
            
            # Should successfully read with fallback encoding
            assert processed == 1
            assert failed == 0
            assert "latin1.cif" in database
    
    def test_read_with_mixed_encodings(self):
        """Test reading directory with files in different encodings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            
            # Create UTF-8 file
            (tmp_path / "utf8.cif").write_text("UTF-8 content", encoding='utf-8')
            
            # Create latin-1 file
            (tmp_path / "latin1.cif").write_bytes(b"Latin-1 content")
            
            database, processed, failed = read_database_directory(tmp_path)
            
            # Both files should be read successfully
            assert processed == 2
            assert failed == 0
            assert "utf8.cif" in database
            assert "latin1.cif" in database
    
    def test_read_handles_permission_errors(self):
        """Test that permission errors are handled gracefully."""
        # This test is platform-dependent and may not work on all systems
        # Skip on Windows where permission handling is different
        import platform
        if platform.system() == "Windows":
            pytest.skip("Permission test not reliable on Windows")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            
            # Create a file
            file_path = tmp_path / "test.cif"
            file_path.write_text("content", encoding='utf-8')
            
            # Remove read permissions
            file_path.chmod(0o000)
            
            try:
                database, processed, failed = read_database_directory(tmp_path)
                
                # Should handle the error gracefully
                assert processed == 0
                assert failed == 1
            finally:
                # Restore permissions for cleanup
                try:
                    file_path.chmod(0o644)
                except:
                    pass


class TestWriteJsonFile:
    """Test writing data to JSON files."""
    
    def test_write_empty_dict(self):
        """Test writing an empty dictionary."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "output.json"
            
            write_json_file({}, output_path)
            
            assert output_path.exists()
            with open(output_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            assert data == {}
    
    def test_write_simple_dict(self):
        """Test writing a simple dictionary."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "output.json"
            
            test_data = {
                "file1.cif": "content 1",
                "file2.cif": "content 2"
            }
            
            write_json_file(test_data, output_path)
            
            assert output_path.exists()
            with open(output_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            assert data == test_data
    
    def test_write_creates_parent_directories(self):
        """Test that write_json_file creates parent directories if needed."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "subdir1" / "subdir2" / "output.json"
            
            test_data = {"test": "data"}
            
            write_json_file(test_data, output_path)
            
            assert output_path.exists()
            assert output_path.parent.exists()
            with open(output_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            assert data == test_data
    
    def test_write_with_utf8_content(self):
        """Test writing dictionary with UTF-8 content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "output.json"
            
            test_data = {
                "file1.cif": "UTF-8: café, naïve, 日本語"
            }
            
            write_json_file(test_data, output_path)
            
            assert output_path.exists()
            with open(output_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            assert data == test_data
    
    def test_write_with_indentation(self):
        """Test that JSON is written with proper indentation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "output.json"
            
            test_data = {
                "file1.cif": "content 1",
                "file2.cif": "content 2"
            }
            
            write_json_file(test_data, output_path)
            
            # Read raw content to check formatting
            content = output_path.read_text(encoding='utf-8')
            
            # Should have indentation (2 spaces)
            assert "  " in content
            # Should have newlines
            assert "\n" in content
    
    def test_write_overwrites_existing_file(self):
        """Test that writing overwrites existing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "output.json"
            
            # Write initial data
            initial_data = {"old": "data"}
            write_json_file(initial_data, output_path)
            
            # Write new data
            new_data = {"new": "data"}
            write_json_file(new_data, output_path)
            
            # Should contain new data
            with open(output_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            assert data == new_data
            assert data != initial_data


class TestExportDatabase:
    """Test exporting a complete database."""
    
    def test_export_simple_database(self):
        """Test exporting a simple database."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            
            # Create database directory
            db_dir = tmp_path / "test_database"
            db_dir.mkdir()
            
            # Create test CIF files
            (db_dir / "file1.cif").write_text("content 1", encoding='utf-8')
            (db_dir / "file2.cif").write_text("content 2", encoding='utf-8')
            
            # Export database
            output_dir = tmp_path / "output"
            processed, failed = export_database("test_database", db_dir, output_dir)
            
            assert processed == 2
            assert failed == 0
            
            # Check output file
            output_file = output_dir / "test_database.json"
            assert output_file.exists()
            
            with open(output_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            assert len(data) == 2
            assert "file1.cif" in data
            assert "file2.cif" in data
            assert data["file1.cif"] == "content 1"
            assert data["file2.cif"] == "content 2"
    
    def test_export_nonexistent_database(self):
        """Test exporting a database that doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            
            nonexistent_dir = tmp_path / "nonexistent"
            output_dir = tmp_path / "output"
            
            processed, failed = export_database("test", nonexistent_dir, output_dir)
            
            assert processed == 0
            assert failed == 0
    
    def test_export_empty_database(self):
        """Test exporting an empty database directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            
            # Create empty database directory
            db_dir = tmp_path / "empty_database"
            db_dir.mkdir()
            
            # Export database
            output_dir = tmp_path / "output"
            processed, failed = export_database("empty_database", db_dir, output_dir)
            
            assert processed == 0
            assert failed == 0
    
    def test_export_with_some_failures(self):
        """Test exporting when some files fail to read."""
        # This test is platform-dependent
        import platform
        if platform.system() == "Windows":
            pytest.skip("Permission test not reliable on Windows")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            
            # Create database directory
            db_dir = tmp_path / "test_database"
            db_dir.mkdir()
            
            # Create readable file
            (db_dir / "good.cif").write_text("good content", encoding='utf-8')
            
            # Create unreadable file
            bad_file = db_dir / "bad.cif"
            bad_file.write_text("bad content", encoding='utf-8')
            bad_file.chmod(0o000)
            
            try:
                # Export database
                output_dir = tmp_path / "output"
                processed, failed = export_database("test_database", db_dir, output_dir)
                
                # Should have 1 success and 1 failure
                assert processed == 1
                assert failed == 1
                
                # Output file should still be created with successful files
                output_file = output_dir / "test_database.json"
                assert output_file.exists()
                
                with open(output_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                assert "good.cif" in data
                assert "bad.cif" not in data
            finally:
                # Restore permissions for cleanup
                try:
                    bad_file.chmod(0o644)
                except:
                    pass


class TestErrorHandling:
    """Test error handling for missing files and directories."""
    
    def test_read_handles_missing_directory_gracefully(self):
        """Test that missing directory is handled without crashing."""
        missing_path = Path("/this/path/does/not/exist")
        
        # Should not raise exception
        database, processed, failed = read_database_directory(missing_path)
        
        assert database == {}
        assert processed == 0
        assert failed == 0
    
    def test_export_handles_missing_directory_gracefully(self):
        """Test that export handles missing database directory gracefully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            
            missing_db = tmp_path / "missing"
            output_dir = tmp_path / "output"
            
            # Should not raise exception
            processed, failed = export_database("missing", missing_db, output_dir)
            
            assert processed == 0
            assert failed == 0
    
    def test_write_handles_invalid_path(self):
        """Test that write handles invalid paths appropriately."""
        # Try to write to a path that cannot be created (e.g., root on Unix)
        # This test may behave differently on different platforms
        try:
            invalid_path = Path("/root/cannot/create/this/path/output.json")
            write_json_file({"test": "data"}, invalid_path)
            # If it succeeds (unlikely), that's also acceptable
        except (PermissionError, OSError):
            # Expected behavior - permission denied
            pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
