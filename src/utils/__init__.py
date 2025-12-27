"""
Utility modules for ToBaCCo.

This package contains utility functions for:
- Path management
- Building block CIF property extraction
- Placing building blocks in 3D space
- Removing net charge from structures
- Removing dummy atoms
- Adjusting edge positions
- Writing CIF files
"""

# Path management is already available
from src.utils.paths import (
    PROJECT_ROOT,
    DATA_DIR,
    EDGES_DATABASE_DIR,
    NODES_DATABASE_DIR,
    TEMPLATE_DATABASE_DIR,
    TEMPLATES_DIR,
    NODES_DIR,
    EDGES_DIR,
    OUTPUT_DIR,
    OUTPUT_CIFS_DIR,
    CHECK_CIFS_DIR,
    ensure_directories,
    get_template_path,
    get_node_path,
    get_edge_path
)

# Other utility modules will be imported here once they are moved to src/utils/
# Examples:
# from src.utils.bbcif_properties import bbcif_properties
# from src.utils.place_bbs import place_bbs
# from src.utils.remove_net_charge import remove_net_charge
# from src.utils.remove_dummy_atoms import remove_dummy_atoms
# from src.utils.adjust_edges import adjust_edges
# from src.utils.write_cifs import write_cifs

__all__ = [
    'PROJECT_ROOT',
    'DATA_DIR',
    'EDGES_DATABASE_DIR',
    'NODES_DATABASE_DIR',
    'TEMPLATE_DATABASE_DIR',
    'TEMPLATES_DIR',
    'NODES_DIR',
    'EDGES_DIR',
    'OUTPUT_DIR',
    'OUTPUT_CIFS_DIR',
    'CHECK_CIFS_DIR',
    'ensure_directories',
    'get_template_path',
    'get_node_path',
    'get_edge_path'
]
