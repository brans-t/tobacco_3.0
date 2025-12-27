"""
ToBaCCo (Topologically Based Crystal Constructor)

A tool for rapidly generating molecular representations of porous crystals.

This package provides a unified API for generating CIF files from templates,
nodes, and edges.
"""

# Import the main API function
from src.api import generate_cif

__all__ = ['generate_cif']

__version__ = '3.0.0'
