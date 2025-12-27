"""
Property-based tests for input format normalization.

Feature: tobacco-refactoring, Property 1: Input Format Normalization
Validates: Requirements 2.1, 2.2, 2.3, 2.4

Tests that all input formats normalize to consistent list format.
"""

import sys
from pathlib import Path
import pytest
from hypothesis import given, strategies as st, settings, assume

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.input_loader import normalize_input_format, InputValidationError


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


# Strategy for generating lists of building block names
def building_block_list(min_size=1, max_size=10):
    """Generate lists of building block names."""
    return st.lists(
        building_block_name(),
        min_size=min_size,
        max_size=max_size
    )


# Strategy for generating dicts mapping vertex types to building block names
@st.composite
def building_block_dict(draw, min_size=1, max_size=10):
    """Generate dicts mapping vertex types to building block names."""
    size = draw(st.integers(min_value=min_size, max_value=max_size))
    
    # Generate unique vertex type keys (V1, V2, V3, etc.)
    keys = [f"V{i}" for i in range(1, size + 1)]
    
    # Generate building block names for each key
    values = [draw(building_block_name()) for _ in range(size)]
    
    return dict(zip(keys, values))


class TestInputFormatNormalization:
    """
    Property 1: Input Format Normalization
    
    For any valid input format (string, list, or dict), normalizing the input
    should produce a consistent list format that can be processed by the core algorithms.
    """
    
    @given(name=building_block_name())
    @settings(max_examples=100)
    def test_single_string_normalizes_to_list(self, name):
        """
        Test that a single string input normalizes to a list with one element.
        
        Property: For any string input, normalize_input_format should return
        a list containing exactly that string.
        
        Validates: Requirement 2.1 - Accept single node/edge/template inputs as strings
        """
        result = normalize_input_format(name)
        
        # Property: Result should be a list
        assert isinstance(result, list), \
            f"Expected list, got {type(result).__name__}"
        
        # Property: List should contain exactly one element
        assert len(result) == 1, \
            f"Expected list of length 1, got length {len(result)}"
        
        # Property: The element should be the original string
        assert result[0] == name, \
            f"Expected [{name}], got {result}"
    
    @given(names=building_block_list(min_size=1, max_size=10))
    @settings(max_examples=100)
    def test_list_input_preserved(self, names):
        """
        Test that a list input is preserved as-is.
        
        Property: For any list input, normalize_input_format should return
        the same list unchanged.
        
        Validates: Requirements 2.2, 2.3, 2.4 - Accept multiple inputs as lists
        """
        result = normalize_input_format(names)
        
        # Property: Result should be a list
        assert isinstance(result, list), \
            f"Expected list, got {type(result).__name__}"
        
        # Property: List should have same length as input
        assert len(result) == len(names), \
            f"Expected list of length {len(names)}, got length {len(result)}"
        
        # Property: List should contain same elements in same order
        assert result == names, \
            f"Expected {names}, got {result}"
    
    @given(mapping=building_block_dict(min_size=1, max_size=10))
    @settings(max_examples=100)
    def test_dict_input_extracts_values(self, mapping):
        """
        Test that a dict input extracts values as a list.
        
        Property: For any dict input, normalize_input_format should return
        a list containing all the values from the dict.
        
        Validates: Requirement 2.4 - Accept dict mapping vertex types to nodes
        """
        result = normalize_input_format(mapping)
        
        # Property: Result should be a list
        assert isinstance(result, list), \
            f"Expected list, got {type(result).__name__}"
        
        # Property: List should have same length as dict
        assert len(result) == len(mapping), \
            f"Expected list of length {len(mapping)}, got length {len(result)}"
        
        # Property: List should contain all values from dict
        expected_values = list(mapping.values())
        assert set(result) == set(expected_values), \
            f"Expected values {expected_values}, got {result}"
    
    @given(
        input_data=st.one_of(
            building_block_name(),
            building_block_list(min_size=1, max_size=10),
            building_block_dict(min_size=1, max_size=10)
        )
    )
    @settings(max_examples=100)
    def test_all_formats_produce_list(self, input_data):
        """
        Test that all input formats produce a list output.
        
        Property: For any valid input format (str, list, or dict),
        normalize_input_format should always return a list.
        
        Validates: Requirements 2.1, 2.2, 2.3, 2.4 - All input formats normalize to list
        """
        result = normalize_input_format(input_data)
        
        # Property: Result should always be a list
        assert isinstance(result, list), \
            f"Expected list for input {type(input_data).__name__}, got {type(result).__name__}"
        
        # Property: List should not be empty (since we generate non-empty inputs)
        assert len(result) > 0, \
            f"Expected non-empty list, got empty list"
    
    @given(
        input_data=st.one_of(
            building_block_name(),
            building_block_list(min_size=1, max_size=10),
            building_block_dict(min_size=1, max_size=10)
        )
    )
    @settings(max_examples=100)
    def test_normalization_is_idempotent(self, input_data):
        """
        Test that normalizing twice produces the same result as normalizing once.
        
        Property: For any input, normalize_input_format(normalize_input_format(x))
        should equal normalize_input_format(x).
        
        This tests idempotence - applying the operation multiple times has the
        same effect as applying it once.
        """
        # Normalize once
        result_once = normalize_input_format(input_data)
        
        # Normalize twice (normalize the result)
        result_twice = normalize_input_format(result_once)
        
        # Property: Results should be identical
        assert result_once == result_twice, \
            f"Normalization is not idempotent: {result_once} != {result_twice}"
    
    @given(invalid_input=st.one_of(
        st.integers(),
        st.floats(),
        st.booleans(),
        st.none(),
        st.tuples(building_block_name(), building_block_name())
    ))
    @settings(max_examples=50)
    def test_invalid_input_raises_error(self, invalid_input):
        """
        Test that invalid input types raise InputValidationError.
        
        Property: For any input that is not str, list, or dict,
        normalize_input_format should raise InputValidationError.
        """
        with pytest.raises(InputValidationError) as exc_info:
            normalize_input_format(invalid_input)
        
        # Property: Error message should mention the invalid type
        error_message = str(exc_info.value)
        assert "must be str, list, or dict" in error_message.lower(), \
            f"Error message should mention valid types: {error_message}"
    
    def test_empty_list_preserved(self):
        """
        Test that an empty list is preserved (edge case).
        
        While the system may reject empty lists during validation,
        the normalization function itself should preserve them.
        """
        result = normalize_input_format([])
        
        assert isinstance(result, list)
        assert len(result) == 0
    
    def test_empty_dict_produces_empty_list(self):
        """
        Test that an empty dict produces an empty list (edge case).
        
        While the system may reject empty dicts during validation,
        the normalization function itself should handle them.
        """
        result = normalize_input_format({})
        
        assert isinstance(result, list)
        assert len(result) == 0
    
    def test_dict_with_duplicate_values(self):
        """
        Test that a dict with duplicate values preserves all values.
        
        This tests that the normalization doesn't deduplicate values,
        which could be important for certain use cases.
        """
        mapping = {
            "V1": "node_a",
            "V2": "node_a",  # Duplicate value
            "V3": "node_b"
        }
        
        result = normalize_input_format(mapping)
        
        assert isinstance(result, list)
        assert len(result) == 3
        assert result.count("node_a") == 2
        assert result.count("node_b") == 1
    
    def test_list_with_mixed_extensions(self):
        """
        Test that a list with mixed .cif extensions is preserved.
        
        The normalization function should not modify the strings,
        including whether they have .cif extensions or not.
        """
        names = ["node1", "node2.cif", "node3", "node4.cif"]
        
        result = normalize_input_format(names)
        
        assert result == names
        assert result[0] == "node1"
        assert result[1] == "node2.cif"
        assert result[2] == "node3"
        assert result[3] == "node4.cif"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
