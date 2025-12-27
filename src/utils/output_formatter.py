"""
Output formatter module for ToBaCCo.

This module provides flexible output formatting options for generated CIF files,
supporting file output, string return, and JSON format.
"""

from pathlib import Path
from typing import Union, Dict, List, Optional, Any
from src.utils.paths import OUTPUT_CIFS_DIR, ensure_directories


def format_as_file(cif_content: str, filename: str, output_dir: Optional[Path] = None) -> Path:
    """
    Save CIF content to file in output directory.
    
    If a file with the same name already exists, a numeric suffix is automatically
    appended to make it unique (e.g., "mof.cif", "mof_2.cif", "mof_3.cif").
    
    Args:
        cif_content: CIF file content as string
        filename: Output filename (with or without .cif extension)
        output_dir: Output directory path (defaults to OUTPUT_CIFS_DIR)
    
    Returns:
        Path: Path to saved file
    
    Raises:
        ValueError: If filename is empty or invalid
        IOError: If file cannot be written
    
    Examples:
        >>> content = "data_mof\\n_cell_length_a 10.0\\n"
        >>> path = format_as_file(content, "test_mof.cif")
        >>> print(path)
        .../output/cifs/test_mof.cif
    """
    if not filename:
        raise ValueError("Filename cannot be empty")
    
    # Ensure .cif extension
    if not filename.endswith('.cif'):
        filename = f"{filename}.cif"
    
    # Use default output directory if not specified
    if output_dir is None:
        output_dir = OUTPUT_CIFS_DIR
    
    # Ensure output directory exists
    ensure_directories()
    
    # Create full path
    file_path = output_dir / filename
    
    # Handle duplicate filenames by appending a suffix
    if file_path.exists():
        # Extract base name and extension
        base_name = filename[:-4]  # Remove .cif
        counter = 2
        
        while file_path.exists():
            new_filename = f"{base_name}_{counter}.cif"
            file_path = output_dir / new_filename
            counter += 1
    
    # Write CIF content to file
    try:
        with open(file_path, 'w') as f:
            f.write(cif_content)
    except IOError as e:
        raise IOError(f"Failed to write CIF file to {file_path}: {e}")
    
    return file_path


def format_as_string(cif_content: str, metadata: Optional[Dict[str, Any]] = None) -> Union[str, tuple]:
    """
    Return CIF content as string with optional metadata.
    
    Args:
        cif_content: CIF file content as string
        metadata: Optional metadata dictionary to include with the CIF content
    
    Returns:
        str: CIF content if metadata is None
        tuple: (cif_content, metadata) if metadata is provided
    
    Examples:
        >>> content = "data_mof\\n_cell_length_a 10.0\\n"
        >>> result = format_as_string(content)
        >>> print(result)
        data_mof
        _cell_length_a 10.0
        
        >>> meta = {"generation_time": "2024-12-28", "template": "pcu"}
        >>> result = format_as_string(content, meta)
        >>> print(result[0])
        data_mof
        _cell_length_a 10.0
        >>> print(result[1])
        {'generation_time': '2024-12-28', 'template': 'pcu'}
    """
    if metadata is None:
        return cif_content
    else:
        return (cif_content, metadata)


def format_as_json(cif_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Format CIF results as JSON object.
    
    Args:
        cif_results: List of result dictionaries, each containing:
            - 'cifname': Name of the MOF/CIF file
            - 'cif_content': CIF file content as string
            - 'metadata': Optional metadata dictionary
    
    Returns:
        dict: JSON object with format {"mof_name": {"cif_content": "...", "metadata": {...}}}
    
    Raises:
        ValueError: If cif_results is empty or has invalid structure
    
    Notes:
        If duplicate cifnames are encountered, a numeric suffix is automatically
        appended to make them unique (e.g., "mof", "mof_2", "mof_3").
    
    Examples:
        >>> results = [
        ...     {
        ...         "cifname": "pcu_mof.cif",
        ...         "cif_content": "data_pcu\\n_cell_length_a 10.0\\n",
        ...         "metadata": {"template": "pcu", "generation_time": "2024-12-28"}
        ...     }
        ... ]
        >>> json_output = format_as_json(results)
        >>> print(json_output.keys())
        dict_keys(['pcu_mof'])
        >>> print(json_output['pcu_mof']['cif_content'])
        data_pcu
        _cell_length_a 10.0
    """
    if not cif_results:
        raise ValueError("cif_results cannot be empty")
    
    json_output = {}
    name_counts = {}  # Track how many times each name has been used
    
    for result in cif_results:
        if not isinstance(result, dict):
            raise ValueError(f"Each result must be a dictionary, got {type(result)}")
        
        if 'cifname' not in result:
            raise ValueError("Each result must contain 'cifname' key")
        
        if 'cif_content' not in result:
            raise ValueError("Each result must contain 'cif_content' key")
        
        # Remove .cif extension from name for JSON key
        cifname = result['cifname']
        if cifname.endswith('.cif'):
            base_name = cifname[:-4]
        else:
            base_name = cifname
        
        # Handle duplicate names by appending a suffix
        if base_name in name_counts:
            name_counts[base_name] += 1
            mof_name = f"{base_name}_{name_counts[base_name]}"
        else:
            name_counts[base_name] = 1
            mof_name = base_name
        
        # Build JSON entry
        json_entry = {
            'cif_content': result['cif_content']
        }
        
        # Include metadata if present
        if 'metadata' in result and result['metadata'] is not None:
            json_entry['metadata'] = result['metadata']
        
        json_output[mof_name] = json_entry
    
    return json_output


def format_results(results: List[Dict[str, Any]], 
                   return_format: Union[str, List[str]] = 'file', 
                   output_dir: Optional[Path] = None) -> Union[List[Path], List[str], List[tuple], Dict[str, Any], Dict[str, Union[List[Path], List[str], List[tuple], Dict[str, Any]]]]:
    """
    Format results according to specified format(s).
    
    This function dispatches to appropriate formatter based on return_format parameter.
    Supports single format or multiple formats simultaneously.
    
    Args:
        results: List of result dictionaries, each containing:
            - 'cifname': Name of the MOF/CIF file
            - 'cif_content': CIF file content as string
            - 'metadata': Optional metadata dictionary
        return_format: Format specification, one of:
            - 'file': Save to file and return paths
            - 'string': Return CIF content as strings
            - 'json': Return as JSON object
            - List of formats: Return dict with results for each format
        output_dir: Output directory for file format (defaults to OUTPUT_CIFS_DIR)
    
    Returns:
        Formatted results according to return_format:
        - 'file': List of Path objects
        - 'string': List of strings (or tuples if metadata present)
        - 'json': Dict with MOF names as keys
        - List of formats: Dict mapping format names to their respective outputs
    
    Raises:
        ValueError: If return_format is invalid or results are empty
    
    Examples:
        >>> results = [
        ...     {
        ...         "cifname": "test_mof.cif",
        ...         "cif_content": "data_test\\n_cell_length_a 10.0\\n",
        ...         "metadata": {"template": "pcu"}
        ...     }
        ... ]
        >>> 
        >>> # Single format
        >>> paths = format_results(results, return_format='file')
        >>> print(type(paths[0]))
        <class 'pathlib.Path'>
        >>> 
        >>> # Multiple formats
        >>> multi = format_results(results, return_format=['file', 'json'])
        >>> print(multi.keys())
        dict_keys(['file', 'json'])
    """
    if not results:
        raise ValueError("results cannot be empty")
    
    # Validate return_format
    valid_formats = {'file', 'string', 'json'}
    
    # Handle multiple formats
    if isinstance(return_format, list):
        if not return_format:
            raise ValueError("return_format list cannot be empty")
        
        # Validate all formats
        for fmt in return_format:
            if fmt not in valid_formats:
                raise ValueError(f"Invalid return_format: '{fmt}'. Must be one of {valid_formats}")
        
        # Process each format and return dict
        output = {}
        for fmt in return_format:
            output[fmt] = format_results(results, return_format=fmt, output_dir=output_dir)
        
        return output
    
    # Handle single format
    if return_format not in valid_formats:
        raise ValueError(f"Invalid return_format: '{return_format}'. Must be one of {valid_formats}")
    
    # Dispatch to appropriate formatter
    if return_format == 'file':
        file_paths = []
        for result in results:
            path = format_as_file(
                cif_content=result['cif_content'],
                filename=result['cifname'],
                output_dir=output_dir
            )
            file_paths.append(path)
        return file_paths
    
    elif return_format == 'string':
        strings = []
        for result in results:
            metadata = result.get('metadata', None)
            string_result = format_as_string(
                cif_content=result['cif_content'],
                metadata=metadata
            )
            strings.append(string_result)
        return strings
    
    elif return_format == 'json':
        return format_as_json(results)
    
    else:
        # Should never reach here due to validation above
        raise ValueError(f"Unexpected return_format: '{return_format}'")
