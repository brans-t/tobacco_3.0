IGNORE_ALL_ERRORS = False
PRINT = False
CONNECTION_SITE_BOND_LENGTH = 1.54
WRITE_CHECK_FILES = False
WRITE_CIF = True
ALL_NODE_COMBINATIONS = False
USER_SPECIFIED_NODE_ASSIGNMENT = False
COMBINATORIAL_EDGE_ASSIGNMENT = True
CHARGES = True
SYMMETRY_TOL = {2:0.10, 3:0.12, 4:0.35, 5:0.25, 6:0.45, 7:0.35, 8:0.40, 9:0.60, 10:0.60, 12:0.60}
BOND_TOL = 5.0
ORIENTATION_DEPENDENT_NODES = False
PLACE_EDGES_BETWEEN_CONNECTION_POINTS = True
RECORD_CALLBACK = False
OUTPUT_SCALING_DATA = True
FIX_UC = (0,0,0,0,0,0)
MIN_CELL_LENGTH = 5.0
OPT_METHOD = 'L-BFGS-B'
PRE_SCALE = 1.00
SCALING_ITERATIONS = 1
SINGLE_METAL_MOFS_ONLY = True
MOFS_ONLY = True
MERGE_CATENATED_NETS = True
RUN_PARALLEL = False
REMOVE_DUMMY_ATOMS = True

# ============================================================================
# New Configuration Options (ToBaCCo 3.0 Refactoring)
# ============================================================================

# RANDOM_SEED: Seed for deterministic charge generation
# Type: int
# Default: 42
# Description: Controls the random number generator used for charge assignment.
#              Using the same seed with identical inputs will produce identical
#              atomic charges, enabling reproducible simulation results.
RANDOM_SEED = 42

# INPUT_SOURCE: Source for loading building blocks
# Type: str
# Default: 'auto'
# Options: 'json', 'cif', 'auto'
# Description: Specifies where to load building blocks (nodes, edges, templates).
#              - 'json': Load from JSON database files (data/*.json)
#              - 'cif': Load from CIF files in inputs/ directories
#              - 'auto': Try JSON first, fallback to CIF if unavailable
INPUT_SOURCE = 'auto'

# DEFAULT_RETURN_FORMAT: Default format for API return values
# Type: str
# Default: 'file'
# Options: 'file', 'string', 'json'
# Description: Controls how generated CIF content is returned from API functions.
#              - 'file': Save to output/cifs/ directory and return file path
#              - 'string': Return CIF content as a string
#              - 'json': Return structured JSON with CIF content and metadata
DEFAULT_RETURN_FORMAT = 'file'
