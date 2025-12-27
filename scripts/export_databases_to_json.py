#!/usr/bin/env python
"""
Database Export Script for ToBaCCo

This script exports CIF database files to JSON format for faster programmatic access.
It reads all .cif files from the edges_database, nodes_database, and template_database
directories and creates corresponding JSON files in the data/ directory.

Usage:
    python export_databases_to_json.py
"""

import json
import sys
from pathlib import Path
from typing import Dict, Tuple


def read_database_directory(directory_path: Path) -> Tuple[Dict[str, str], int, int]:
    """
    Read all .cif files from a directory.
    
    This function reads all .cif files in the specified directory and returns
    a dictionary mapping filenames to their content. It handles encoding errors
    gracefully by trying UTF-8 first, then falling back to latin-1.
    
    Args:
        directory_path (Path): Path to database directory
        
    Returns:
        tuple: A tuple containing:
            - dict: Mapping of filename (without path) to file content as string
            - int: Number of files successfully processed
            - int: Number of files that failed to process
    """
    database = {}
    files_processed = 0
    files_failed = 0
    
    if not directory_path.exists():
        print(f"Warning: Directory {directory_path} does not exist")
        return database, files_processed, files_failed
    
    if not directory_path.is_dir():
        print(f"Warning: {directory_path} is not a directory")
        return database, files_processed, files_failed
    
    # Get all .cif files in the directory
    cif_files = sorted(directory_path.glob("*.cif"))
    
    for file_path in cif_files:
        try:
            # Try UTF-8 encoding first
            try:
                content = file_path.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                # Fallback to latin-1 if UTF-8 fails
                content = file_path.read_text(encoding='latin-1')
            
            # Store with just the filename (not the full path)
            database[file_path.name] = content
            files_processed += 1
            
        except Exception as e:
            print(f"Warning: Failed to read {file_path.name}: {e}")
            files_failed += 1
    
    return database, files_processed, files_failed


def write_json_file(data: Dict[str, str], output_path: Path) -> None:
    """
    Write dictionary to JSON file.
    
    This function writes the provided dictionary to a JSON file with UTF-8
    encoding and 2-space indentation for readability.
    
    Args:
        data (dict): Data to write (mapping of filenames to content)
        output_path (Path): Output file path
        
    Raises:
        IOError: If the file cannot be written
    """
    # Ensure the parent directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write JSON with nice formatting
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def export_database(db_name: str, db_path: Path, output_dir: Path) -> Tuple[int, int]:
    """
    Export a single database to JSON.
    
    This function reads all .cif files from the specified database directory
    and exports them to a single JSON file in the output directory.
    
    Args:
        db_name (str): Database name (used for output filename, e.g., "edges_database")
        db_path (Path): Database directory path
        output_dir (Path): Output directory for JSON file
        
    Returns:
        tuple: (files_processed, files_failed)
    """
    print(f"\nExporting {db_name}...")
    print(f"  Source: {db_path}")
    
    if not db_path.exists():
        print(f"  Error: Database directory does not exist")
        return 0, 0
    
    # Read all files from the database directory
    database, files_processed, files_failed = read_database_directory(db_path)
    
    if not database:
        print(f"  Warning: No .cif files found in {db_path}")
        return files_processed, files_failed
    
    # Write to JSON file
    output_path = output_dir / f"{db_name}.json"
    try:
        write_json_file(database, output_path)
        print(f"  Output: {output_path}")
        print(f"  Success: {files_processed} files processed")
        if files_failed > 0:
            print(f"  Failed: {files_failed} files")
    except Exception as e:
        print(f"  Error: Failed to write JSON file: {e}")
        return files_processed, files_processed + files_failed
    
    return files_processed, files_failed


def main():
    """
    Main entry point - exports all three databases.
    
    This function exports the edges_database, nodes_database, and template_database
    directories to JSON files in the data/ directory. It provides progress reporting
    and summary statistics.
    """
    print("=" * 70)
    print("ToBaCCo Database Export to JSON")
    print("=" * 70)
    
    # Detect project root (same directory as this script)
    project_root = Path(__file__).parent
    
    # Define database directories (now in data/ subdirectory)
    data_dir = project_root / "data"
    databases = [
        ("edges_database", data_dir / "edges_database"),
        ("nodes_database", data_dir / "nodes_database"),
        ("template_database", data_dir / "template_database"),
    ]
    
    # Output directory
    output_dir = project_root / "data"
    
    # Track overall statistics
    total_processed = 0
    total_failed = 0
    
    # Export each database
    for db_name, db_path in databases:
        processed, failed = export_database(db_name, db_path, output_dir)
        total_processed += processed
        total_failed += failed
    
    # Print summary
    print("\n" + "=" * 70)
    print("Export Summary")
    print("=" * 70)
    print(f"Total files processed: {total_processed}")
    print(f"Total files failed: {total_failed}")
    print(f"Output directory: {output_dir}")
    
    if total_failed > 0:
        print("\nWarning: Some files failed to process. Check the output above for details.")
        sys.exit(1)
    else:
        print("\nAll databases exported successfully!")
        sys.exit(0)


if __name__ == "__main__":
    main()
