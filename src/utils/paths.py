"""
Path management module for ToBaCCo.

This module provides centralized path management to ensure correct file paths
regardless of where the code is executed from.
"""

import os
from pathlib import Path


# Detect project root (3 levels up from this file: src/utils/paths.py -> src/utils -> src -> root)
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
EDGES_DATABASE_DIR = DATA_DIR / "edges_database"
NODES_DATABASE_DIR = DATA_DIR / "nodes_database"
TEMPLATE_DATABASE_DIR = DATA_DIR / "template_database"
TEMPLATE_2D_DATABASE_DIR = DATA_DIR / "template_2D_database"
TEMPLATE_DATABASE_OLD_DIR = DATA_DIR / "template_database_old"

# Working directories (in project root for runtime use)
TEMPLATES_DIR = PROJECT_ROOT / "templates"
NODES_DIR = PROJECT_ROOT / "nodes"
EDGES_DIR = PROJECT_ROOT / "edges"

# Output directories
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_CIFS_DIR = OUTPUT_DIR / "cifs"
CHECK_CIFS_DIR = OUTPUT_DIR / "check_cifs"

# JSON database files
EDGES_JSON = DATA_DIR / "edges_database.json"
NODES_JSON = DATA_DIR / "nodes_database.json"
TEMPLATE_JSON = DATA_DIR / "template_database.json"

# Documentation directory
DOCS_DIR = PROJECT_ROOT / "docs"


def ensure_directories():
    """
    Create all required directories if they don't exist.
    
    This function ensures that output directories are created automatically
    when needed, preventing FileNotFoundError during file writing operations.
    """
    directories = [
        OUTPUT_DIR,
        OUTPUT_CIFS_DIR,
        CHECK_CIFS_DIR,
        DATA_DIR
    ]
    
    for dir_path in directories:
        dir_path.mkdir(parents=True, exist_ok=True)


def get_template_path(filename):
    """
    Get full path to template file.
    
    Args:
        filename (str): Template filename (with or without .cif extension)
        
    Returns:
        Path: Full path to template file
    """
    if not filename.endswith('.cif'):
        filename = f"{filename}.cif"
    return TEMPLATES_DIR / filename


def get_node_path(filename):
    """
    Get full path to node file.
    
    Args:
        filename (str): Node filename (with or without .cif extension)
        
    Returns:
        Path: Full path to node file
    """
    if not filename.endswith('.cif'):
        filename = f"{filename}.cif"
    return NODES_DIR / filename


def get_edge_path(filename):
    """
    Get full path to edge file.
    
    Args:
        filename (str): Edge filename (with or without .cif extension)
        
    Returns:
        Path: Full path to edge file
    """
    if not filename.endswith('.cif'):
        filename = f"{filename}.cif"
    return EDGES_DIR / filename


def get_output_cif_path(filename):
    """
    Get full path for output CIF file.
    
    Args:
        filename (str): Output CIF filename
        
    Returns:
        Path: Full path for output CIF file
    """
    if not filename.endswith('.cif'):
        filename = f"{filename}.cif"
    return OUTPUT_CIFS_DIR / filename


def get_check_cif_path(filename):
    """
    Get full path for check CIF file.
    
    Args:
        filename (str): Check CIF filename
        
    Returns:
        Path: Full path for check CIF file
    """
    return CHECK_CIFS_DIR / filename
