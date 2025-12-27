"""
Input loader module for ToBaCCo.

This module provides functions for loading building blocks from various sources
(JSON databases or CIF files) and validating inputs.
"""

import json
from pathlib import Path
from typing import Union, List, Dict, Tuple

from src.utils.paths import (
    get_template_path, get_node_path, get_edge_path,
    NODES_JSON, EDGES_JSON, TEMPLATE_JSON,
    TEMPLATES_DIR, NODES_DIR, EDGES_DIR
)


class InputValidationError(ValueError):
    """Raised when inputs are invalid or incompatible."""
    pass


class DatabaseError(Exception):
    """Raised when JSON database is corrupted or invalid."""
    pass


def normalize_input_format(input_data: Union[str, List[str], Dict[str, str]]) -> List[str]:
    """
    Convert single string, list, or dict to standardized list format.
    
    This function normalizes various input formats into a consistent list format
    that can be processed by the core algorithms.
    
    Args:
        input_data: Input in one of three formats:
                   - str: Single building block name
                   - list: List of building block names
                   - dict: Mapping of vertex types to building block names
    
    Returns:
        list: Normalized list of building block names
        
    Examples:
        >>> normalize_input_format("pcu")
        ['pcu']
        
        >>> normalize_input_format(["pcu", "dia"])
        ['pcu', 'dia']
        
        >>> normalize_input_format({"V1": "6c_Cu_1_Ch", "V2": "4c_Zn_1_Ch"})
        ['6c_Cu_1_Ch', '4c_Zn_1_Ch']
    """
    if isinstance(input_data, str):
        # Single string -> list with one element
        return [input_data]
    elif isinstance(input_data, list):
        # Already a list -> return as is
        return input_data
    elif isinstance(input_data, dict):
        # Dict -> extract values as list
        return list(input_data.values())
    else:
        raise InputValidationError(
            f"Input must be str, list, or dict. Got {type(input_data).__name__}"
        )


def _normalize_filename(filename: str) -> str:
    """
    Add .cif extension to filename if not present.
    
    Args:
        filename: Filename with or without .cif extension
        
    Returns:
        str: Filename with .cif extension
    """
    if not filename.endswith('.cif'):
        return f"{filename}.cif"
    return filename


def _load_from_json(names: List[str], block_type: str) -> Dict[str, str]:
    """
    Load building blocks from JSON database.
    
    Args:
        names: List of building block names (with or without .cif extension)
        block_type: Type of building block ('node', 'edge', or 'template')
        
    Returns:
        dict: {name: cif_content} for successfully loaded blocks
        
    Raises:
        DatabaseError: If JSON database is corrupted or invalid
        FileNotFoundError: If JSON database file doesn't exist
    """
    # Map block type to JSON file path
    json_paths = {
        'node': NODES_JSON,
        'edge': EDGES_JSON,
        'template': TEMPLATE_JSON
    }
    
    if block_type not in json_paths:
        raise ValueError(f"Invalid block_type: {block_type}. Must be 'node', 'edge', or 'template'")
    
    json_path = json_paths[block_type]
    
    # Check if JSON file exists
    if not json_path.exists():
        raise FileNotFoundError(f"JSON database not found: {json_path}")
    
    # Load JSON database
    try:
        with open(json_path, 'r') as f:
            database = json.load(f)
    except json.JSONDecodeError as e:
        raise DatabaseError(f"Corrupted JSON database {json_path}: {e}")
    except Exception as e:
        raise DatabaseError(f"Error reading JSON database {json_path}: {e}")
    
    # Validate database format
    if not isinstance(database, dict):
        raise DatabaseError(f"Invalid JSON database format in {json_path}: expected dict, got {type(database).__name__}")
    
    # Load requested building blocks
    results = {}
    for name in names:
        # Normalize filename
        filename = _normalize_filename(name)
        
        # Check if building block exists in database
        if filename in database:
            results[filename] = database[filename]
        else:
            # Building block not found in database
            # This is not an error - caller will handle fallback to CIF
            pass
    
    return results


def _load_from_cif(names: List[str], block_type: str) -> Dict[str, str]:
    """
    Load building blocks from CIF files.
    
    Args:
        names: List of building block names (with or without .cif extension)
        block_type: Type of building block ('node', 'edge', or 'template')
        
    Returns:
        dict: {name: cif_content} for successfully loaded blocks
        
    Raises:
        FileNotFoundError: If CIF file doesn't exist
    """
    # Map block type to path getter function
    path_getters = {
        'node': get_node_path,
        'edge': get_edge_path,
        'template': get_template_path
    }
    
    if block_type not in path_getters:
        raise ValueError(f"Invalid block_type: {block_type}. Must be 'node', 'edge', or 'template'")
    
    path_getter = path_getters[block_type]
    
    # Load requested building blocks
    results = {}
    for name in names:
        # Normalize filename
        filename = _normalize_filename(name)
        
        # Get path to CIF file
        cif_path = path_getter(filename)
        
        # Check if file exists
        if not cif_path.exists():
            raise FileNotFoundError(
                f"{block_type.capitalize()} file '{filename}' not found. "
                f"Searched in: {cif_path.parent}"
            )
        
        # Read CIF content
        try:
            with open(cif_path, 'r') as f:
                cif_content = f.read()
            results[filename] = cif_content
        except Exception as e:
            raise IOError(f"Error reading {block_type} file {cif_path}: {e}")
    
    return results


def load_building_blocks(
    names: Union[str, List[str], Dict[str, str]],
    block_type: str,
    source: str = 'auto'
) -> Dict[str, str]:
    """
    Load building blocks from JSON database or CIF files.
    
    This function provides flexible loading of building blocks with support for
    multiple input formats and automatic fallback from JSON to CIF files.
    
    Args:
        names: Building block name(s) in one of three formats:
              - str: Single building block name
              - list: List of building block names
              - dict: Mapping of vertex types to building block names
              Extensions (.cif) are optional and will be added automatically.
        block_type: Type of building block to load:
                   - 'node': Node building blocks
                   - 'edge': Edge building blocks
                   - 'template': Template topologies
        source: Source to load from:
               - 'json': Load from JSON database only (raises error if not found)
               - 'cif': Load from CIF files only
               - 'auto': Try JSON first, fallback to CIF if not found (default)
    
    Returns:
        dict: Dictionary mapping filenames to CIF content
              Format: {filename: cif_content_string}
              
    Raises:
        InputValidationError: If input format is invalid
        FileNotFoundError: If building block file not found
        DatabaseError: If JSON database is corrupted
        
    Examples:
        >>> # Load single node from JSON (with auto fallback to CIF)
        >>> blocks = load_building_blocks("6c_Cu_1_Ch", "node")
        >>> print(blocks.keys())
        dict_keys(['6c_Cu_1_Ch.cif'])
        
        >>> # Load multiple edges from CIF only
        >>> blocks = load_building_blocks(["btc_edge", "bdc_edge"], "edge", source="cif")
        
        >>> # Load nodes with vertex mapping
        >>> blocks = load_building_blocks({"V1": "6c_Cu_1_Ch", "V2": "4c_Zn_1_Ch"}, "node")
    """
    # Normalize input format
    names_list = normalize_input_format(names)
    
    # Validate block_type
    valid_types = ['node', 'edge', 'template']
    if block_type not in valid_types:
        raise InputValidationError(
            f"Invalid block_type: '{block_type}'. Must be one of {valid_types}"
        )
    
    # Validate source
    valid_sources = ['json', 'cif', 'auto']
    if source not in valid_sources:
        raise InputValidationError(
            f"Invalid source: '{source}'. Must be one of {valid_sources}"
        )
    
    # Load based on source
    if source == 'cif':
        # Load from CIF files only
        return _load_from_cif(names_list, block_type)
    
    elif source == 'json':
        # Load from JSON database only (no fallback)
        results = _load_from_json(names_list, block_type)
        
        # Check if all requested blocks were found
        normalized_names = [_normalize_filename(name) for name in names_list]
        missing = set(normalized_names) - set(results.keys())
        if missing:
            raise FileNotFoundError(
                f"Building blocks not found in JSON database: {', '.join(missing)}"
            )
        
        return results
    
    else:  # source == 'auto'
        # Try JSON first, fallback to CIF for missing blocks
        results = {}
        
        # Try loading from JSON
        try:
            json_results = _load_from_json(names_list, block_type)
            results.update(json_results)
        except (FileNotFoundError, DatabaseError):
            # JSON database not available or corrupted, will use CIF fallback
            json_results = {}
        
        # Identify blocks not found in JSON
        normalized_names = [_normalize_filename(name) for name in names_list]
        missing_from_json = [
            name for name in names_list
            if _normalize_filename(name) not in results
        ]
        
        # Load missing blocks from CIF
        if missing_from_json:
            cif_results = _load_from_cif(missing_from_json, block_type)
            results.update(cif_results)
        
        return results



def validate_inputs(
    template_names: Union[str, List[str]],
    node_names: Union[str, List[str], Dict[str, str]],
    edge_names: Union[str, List[str]]
) -> Tuple[bool, str]:
    """
    Validate that all required inputs exist and are compatible.
    
    This function checks that all specified building blocks exist and can be
    loaded successfully. It provides clear error messages to help users fix
    input problems.
    
    Args:
        template_names: Template name(s) - str or list of str
        node_names: Node name(s) - str, list of str, or dict mapping vertices to nodes
        edge_names: Edge name(s) - str or list of str
        
    Returns:
        tuple: (valid, error_message)
              - valid (bool): True if all inputs are valid, False otherwise
              - error_message (str): Empty string if valid, error description if invalid
              
    Examples:
        >>> valid, error = validate_inputs("pcu", ["6c_Cu_1_Ch"], ["btc_edge"])
        >>> if not valid:
        ...     print(f"Validation failed: {error}")
        
        >>> # Check multiple templates
        >>> valid, error = validate_inputs(["pcu", "dia"], {"V1": "6c_Cu_1_Ch"}, ["btc_edge"])
    """
    try:
        # Normalize all inputs
        template_list = normalize_input_format(template_names)
        node_list = normalize_input_format(node_names)
        edge_list = normalize_input_format(edge_names)
        
        # Validate that lists are not empty
        if len(template_list) == 0:
            return False, "Template list cannot be empty"
        
        if len(node_list) == 0:
            return False, "Node list cannot be empty"
        
        if len(edge_list) == 0:
            return False, "Edge list cannot be empty"
        
        # Try loading templates
        try:
            load_building_blocks(template_list, 'template', source='auto')
        except FileNotFoundError as e:
            return False, f"Template validation failed: {e}"
        except Exception as e:
            return False, f"Template loading error: {e}"
        
        # Try loading nodes
        try:
            load_building_blocks(node_list, 'node', source='auto')
        except FileNotFoundError as e:
            return False, f"Node validation failed: {e}"
        except Exception as e:
            return False, f"Node loading error: {e}"
        
        # Try loading edges
        try:
            load_building_blocks(edge_list, 'edge', source='auto')
        except FileNotFoundError as e:
            return False, f"Edge validation failed: {e}"
        except Exception as e:
            return False, f"Edge loading error: {e}"
        
        # All validations passed
        return True, ""
        
    except InputValidationError as e:
        return False, f"Input format error: {e}"
    except Exception as e:
        return False, f"Unexpected validation error: {e}"
