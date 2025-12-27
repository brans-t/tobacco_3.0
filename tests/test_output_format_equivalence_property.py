"""
Property-based tests for output format equivalence.

Feature: tobacco-refactoring, Property 5: Output Format Equivalence
Validates: Requirements 3.1, 3.2, 3.3, 3.4

Tests that converting between output formats preserves CIF content.
"""

import sys
from pathlib import Path
import pytest
from hypothesis import given, strategies as st, settings, HealthCheck
import tempfile
import shutil

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.output_formatter import (
    format_as_file,
    format_as_string,
    format_as_json,
    format_results
)


# Strategy for generating valid CIF content
@st.composite
def cif_content(draw):
    """Generate valid CIF file content for testing."""
    # Generate a simple but valid CIF structure
    mof_name = draw(st.text(
        alphabet='abcdefghijklmnopqrstuvwxyz0123456789_',
        min_size=3,
        max_size=20
    ))
    
    # Generate cell parameters
    a = draw(st.floats(min_value=5.0, max_value=50.0))
    b = draw(st.floats(min_value=5.0, max_value=50.0))
    c = draw(st.floats(min_value=5.0, max_value=50.0))
    alpha = draw(st.floats(min_value=60.0, max_value=120.0))
    beta = draw(st.floats(min_value=60.0, max_value=120.0))
    gamma = draw(st.floats(min_value=60.0, max_value=120.0))
    
    # Build CIF content
    content = f"""data_{mof_name}
_audit_creation_date              2024-12-28
_audit_creation_method            'tobacco_3.0'
_symmetry_space_group_name_H-M    'P1'
_symmetry_Int_Tables_number       1
_symmetry_cell_setting            triclinic
loop_
_symmetry_equiv_pos_as_xyz
  x,y,z
_cell_length_a                    {a:.6f}
_cell_length_b                    {b:.6f}
_cell_length_c                    {c:.6f}
_cell_angle_alpha                 {alpha:.6f}
_cell_angle_beta                  {beta:.6f}
_cell_angle_gamma                 {gamma:.6f}
loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
C1      C       0.5000000000    0.5000000000    0.5000000000
N1      N       0.2500000000    0.2500000000    0.2500000000
"""
    
    return content


# Strategy for generating CIF filenames
@st.composite
def cif_filename(draw):
    """Generate valid CIF filenames."""
    name = draw(st.text(
        alphabet='abcdefghijklmnopqrstuvwxyz0123456789_-',
        min_size=3,
        max_size=30
    ))
    
    # Randomly decide whether to include .cif extension
    include_extension = draw(st.booleans())
    if include_extension:
        return f"{name}.cif"
    return name


# Strategy for generating metadata
@st.composite
def metadata_dict(draw):
    """Generate metadata dictionaries."""
    template = draw(st.text(
        alphabet='abcdefghijklmnopqrstuvwxyz',
        min_size=3,
        max_size=10
    ))
    
    generation_time = "2024-12-28"
    
    # Optionally include additional fields
    meta = {
        "template": template,
        "generation_time": generation_time
    }
    
    include_unit_cell = draw(st.booleans())
    if include_unit_cell:
        meta["unit_cell"] = {
            "a": draw(st.floats(min_value=5.0, max_value=50.0)),
            "b": draw(st.floats(min_value=5.0, max_value=50.0)),
            "c": draw(st.floats(min_value=5.0, max_value=50.0))
        }
    
    return meta


# Strategy for generating result dictionaries
@st.composite
def result_dict(draw):
    """Generate result dictionaries for testing."""
    cifname = draw(cif_filename())
    content = draw(cif_content())
    
    # Optionally include metadata
    include_metadata = draw(st.booleans())
    if include_metadata:
        meta = draw(metadata_dict())
    else:
        meta = None
    
    return {
        "cifname": cifname,
        "cif_content": content,
        "metadata": meta
    }


class TestOutputFormatEquivalence:
    """
    Property 5: Output Format Equivalence
    
    For any generated MOF, converting between output formats (file → string → JSON)
    should preserve the CIF content exactly.
    """
    
    @given(content=cif_content(), filename=cif_filename())
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    def test_file_to_string_preserves_content(self, content, filename):
        """
        Test that writing to file and reading back preserves CIF content.
        
        Property: For any CIF content, writing to file and reading back
        should produce identical content.
        
        Validates: Requirements 3.1, 3.6 - File output preserves content
        """
        # Create temporary directory for test
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            
            # Write to file
            file_path = format_as_file(content, filename, output_dir=tmpdir_path)
            
            # Read back from file
            with open(file_path, 'r') as f:
                read_content = f.read()
            
            # Property: Content should be identical
            assert read_content == content, \
                f"File content differs from original"
    
    @given(content=cif_content(), meta=st.one_of(st.none(), metadata_dict()))
    @settings(max_examples=100)
    def test_string_format_preserves_content(self, content, meta):
        """
        Test that string formatting preserves CIF content.
        
        Property: For any CIF content, format_as_string should return
        the exact same content (with optional metadata).
        
        Validates: Requirement 3.1 - String return preserves content
        """
        result = format_as_string(content, metadata=meta)
        
        if meta is None:
            # Property: Result should be the content itself
            assert result == content, \
                f"String format altered content"
        else:
            # Property: Result should be tuple with content and metadata
            assert isinstance(result, tuple), \
                f"Expected tuple when metadata provided, got {type(result)}"
            assert len(result) == 2, \
                f"Expected tuple of length 2, got {len(result)}"
            assert result[0] == content, \
                f"String format altered content in tuple"
            assert result[1] == meta, \
                f"Metadata not preserved correctly"
    
    @given(results=st.lists(result_dict(), min_size=1, max_size=5))
    @settings(max_examples=100)
    def test_json_format_preserves_content(self, results):
        """
        Test that JSON formatting preserves CIF content.
        
        Property: For any list of results, format_as_json should preserve
        all CIF content in the JSON structure.
        
        When duplicate cifnames exist, they are automatically given unique
        suffixes (e.g., "mof", "mof_2", "mof_3").
        
        Validates: Requirements 3.2, 3.3, 3.4 - JSON format preserves content
        """
        json_output = format_as_json(results)
        
        # Property: JSON output should be a dict
        assert isinstance(json_output, dict), \
            f"Expected dict, got {type(json_output)}"
        
        # Property: Should have same number of entries as results (duplicates get suffixes)
        assert len(json_output) == len(results), \
            f"Expected {len(results)} entries, got {len(json_output)}"
        
        # Property: All CIF content should be preserved (check by content, not by name)
        result_contents = [r['cif_content'] for r in results]
        json_contents = [entry['cif_content'] for entry in json_output.values()]
        
        # Sort both lists to compare regardless of order
        assert sorted(result_contents) == sorted(json_contents), \
            f"CIF contents not preserved in JSON output"
    
    @given(results=st.lists(result_dict(), min_size=1, max_size=5))
    @settings(max_examples=100)
    def test_format_results_file_preserves_content(self, results):
        """
        Test that format_results with 'file' format preserves content.
        
        Property: For any results, format_results with return_format='file'
        should write files that contain the exact CIF content.
        
        When duplicate filenames exist, they are automatically given unique
        suffixes (e.g., "mof.cif", "mof_2.cif", "mof_3.cif").
        
        Validates: Requirement 3.6, 10.2 - File format preserves content
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            
            # Format as files
            file_paths = format_results(results, return_format='file', output_dir=tmpdir_path)
            
            # Property: Should return list of paths
            assert isinstance(file_paths, list), \
                f"Expected list, got {type(file_paths)}"
            assert len(file_paths) == len(results), \
                f"Expected {len(results)} paths, got {len(file_paths)}"
            
            # Property: All files should exist
            for file_path in file_paths:
                assert file_path.exists(), \
                    f"File {file_path} does not exist"
            
            # Property: All CIF content should be preserved (check by content)
            result_contents = sorted([r['cif_content'] for r in results])
            file_contents = []
            for file_path in file_paths:
                with open(file_path, 'r') as f:
                    file_contents.append(f.read())
            file_contents = sorted(file_contents)
            
            assert result_contents == file_contents, \
                f"File contents differ from original results"
    
    @given(results=st.lists(result_dict(), min_size=1, max_size=5))
    @settings(max_examples=100)
    def test_format_results_string_preserves_content(self, results):
        """
        Test that format_results with 'string' format preserves content.
        
        Property: For any results, format_results with return_format='string'
        should return strings (or tuples) with exact CIF content.
        
        Validates: Requirement 3.1, 10.3 - String format preserves content
        """
        strings = format_results(results, return_format='string')
        
        # Property: Should return list
        assert isinstance(strings, list), \
            f"Expected list, got {type(strings)}"
        assert len(strings) == len(results), \
            f"Expected {len(results)} strings, got {len(strings)}"
        
        # Property: Each string should contain the correct content
        for result, string_result in zip(results, strings):
            if result['metadata'] is None:
                # Should be just the string
                assert isinstance(string_result, str), \
                    f"Expected str, got {type(string_result)}"
                assert string_result == result['cif_content'], \
                    f"String content differs from original"
            else:
                # Should be tuple
                assert isinstance(string_result, tuple), \
                    f"Expected tuple, got {type(string_result)}"
                assert string_result[0] == result['cif_content'], \
                    f"String content in tuple differs from original"
                assert string_result[1] == result['metadata'], \
                    f"Metadata in tuple differs from original"
    
    @given(results=st.lists(result_dict(), min_size=1, max_size=5))
    @settings(max_examples=100)
    def test_format_results_json_preserves_content(self, results):
        """
        Test that format_results with 'json' format preserves content.
        
        Property: For any results, format_results with return_format='json'
        should return JSON with exact CIF content.
        
        When duplicate cifnames exist, they are automatically given unique
        suffixes (e.g., "mof", "mof_2", "mof_3").
        
        Validates: Requirements 3.2, 3.3, 3.4, 10.4 - JSON format preserves content
        """
        json_output = format_results(results, return_format='json')
        
        # Property: Should return dict
        assert isinstance(json_output, dict), \
            f"Expected dict, got {type(json_output)}"
        
        # Property: Should have same number of entries as results
        assert len(json_output) == len(results), \
            f"Expected {len(results)} entries, got {len(json_output)}"
        
        # Property: All CIF content should be preserved (check by content)
        result_contents = sorted([r['cif_content'] for r in results])
        json_contents = sorted([entry['cif_content'] for entry in json_output.values()])
        
        assert result_contents == json_contents, \
            f"CIF contents not preserved in JSON output"
    
    @given(results=st.lists(result_dict(), min_size=1, max_size=3))
    @settings(max_examples=50)
    def test_multiple_formats_preserve_content(self, results):
        """
        Test that requesting multiple formats preserves content in all formats.
        
        Property: For any results, format_results with multiple return_formats
        should preserve content in all requested formats.
        
        When duplicate names exist, they are automatically given unique suffixes.
        
        Validates: Requirements 3.7, 10.6, 10.7 - Multiple formats preserve content
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            
            # Request all three formats
            multi_output = format_results(
                results,
                return_format=['file', 'string', 'json'],
                output_dir=tmpdir_path
            )
            
            # Property: Should return dict with all format keys
            assert isinstance(multi_output, dict), \
                f"Expected dict, got {type(multi_output)}"
            assert set(multi_output.keys()) == {'file', 'string', 'json'}, \
                f"Expected keys ['file', 'string', 'json'], got {list(multi_output.keys())}"
            
            # Get all original contents
            result_contents = sorted([r['cif_content'] for r in results])
            
            # Property: File format should preserve all content
            file_contents = []
            for file_path in multi_output['file']:
                with open(file_path, 'r') as f:
                    file_contents.append(f.read())
            file_contents = sorted(file_contents)
            assert result_contents == file_contents, \
                f"File format content differs"
            
            # Property: String format should preserve all content
            string_contents = []
            for string_result in multi_output['string']:
                if isinstance(string_result, tuple):
                    string_contents.append(string_result[0])
                else:
                    string_contents.append(string_result)
            string_contents = sorted(string_contents)
            assert result_contents == string_contents, \
                f"String format content differs"
            
            # Property: JSON format should preserve all content
            json_contents = sorted([entry['cif_content'] for entry in multi_output['json'].values()])
            assert result_contents == json_contents, \
                f"JSON format content differs"
    
    @given(content=cif_content(), filename=cif_filename())
    @settings(max_examples=50)
    def test_round_trip_file_string_equivalence(self, content, filename):
        """
        Test round-trip equivalence: file → read → string should equal original.
        
        Property: Writing to file and reading back should produce the same
        content as format_as_string.
        
        This is a round-trip property testing format equivalence.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            
            # Format as file
            file_path = format_as_file(content, filename, output_dir=tmpdir_path)
            
            # Read back
            with open(file_path, 'r') as f:
                file_content = f.read()
            
            # Format as string
            string_content = format_as_string(content)
            
            # Property: Both should be identical to original
            assert file_content == content, \
                f"File round-trip altered content"
            assert string_content == content, \
                f"String format altered content"
            assert file_content == string_content, \
                f"File and string formats differ"
    
    def test_empty_results_raises_error(self):
        """
        Test that empty results list raises ValueError.
        
        Edge case: The system should reject empty results.
        """
        with pytest.raises(ValueError) as exc_info:
            format_results([])
        
        assert "cannot be empty" in str(exc_info.value).lower()
    
    def test_invalid_return_format_raises_error(self):
        """
        Test that invalid return_format raises ValueError.
        
        Edge case: The system should reject invalid format specifications.
        """
        results = [{
            "cifname": "test.cif",
            "cif_content": "data_test\n",
            "metadata": None
        }]
        
        with pytest.raises(ValueError) as exc_info:
            format_results(results, return_format='invalid')
        
        assert "invalid return_format" in str(exc_info.value).lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
