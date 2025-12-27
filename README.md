# ToBaCCo 3.0 - Topologically Based Crystal Constructor

## Authors
- Ryther Anderson
- Yamil Colón
- Diego Gómez-Gualdrón

## Overview

ToBaCCo (Topologically Based Crystal Constructor) is a tool for rapidly generating molecular representations of porous crystals as crystallographic information (.cif) files, which can then be used for molecular simulation or materials characterization.

This refactored version maintains full backward compatibility while adding:
- Improved project organization with clear module structure
- Programmatic API for integration into other tools
- JSON database export for faster access
- Better error handling and validation

## Project Structure

```
tobacco_3.0/
├── inputs/                      # NEW: Organized input directory
│   ├── edges/                   # Edge building blocks (CIF files)
│   ├── nodes/                   # Node building blocks (CIF files)
│   └── templates/               # Topology templates (CIF files)
├── src/                         # Source code package
│   ├── api.py                   # Public API interface (ENHANCED)
│   ├── core/                    # Core algorithm modules (unchanged)
│   ├── utils/                   # Utility modules
│   │   ├── paths.py            # Path management (updated)
│   │   ├── input_loader.py     # NEW: Input loading and validation
│   │   ├── output_formatter.py # NEW: Flexible output formatting
│   │   ├── charge_generator.py # NEW: Deterministic charge generation
│   │   ├── cif_tools.py        # CIF file utilities
│   │   └── ...                 # Other utilities
│   └── visualization/           # Visualization modules
├── scripts/                     # Utility scripts
│   ├── export_databases_to_json.py  # Database export
│   ├── reindex_building_blocks.py   # CIF reindexing
│   ├── make_topologies.py           # Topology generation
│   ├── topo_pore_analysis.py        # Pore analysis
│   └── scrape_rcsr.py               # RCSR data scraper
├── data/                        # Database files
│   ├── edges_database/          # Legacy edge database
│   ├── nodes_database/          # Legacy node database
│   ├── template_database/       # Legacy template database
│   └── *.json                   # JSON database exports (faster loading)
├── output/                      # Generated output files
│   ├── cifs/                    # Generated CIF files
│   └── check_cifs/              # Check files
├── docs/                        # Documentation
├── templates/                   # Legacy template directory (backward compat)
├── nodes/                       # Legacy nodes directory (backward compat)
├── edges/                       # Legacy edges directory (backward compat)
├── tests/                       # Unit tests and property-based tests
├── tobacco.py                   # Main entry point (CLI)
├── configuration.py             # Configuration file (ENHANCED)
└── vertex_assignment.txt        # Vertex assignment config
```

### New Directory Structure

The refactored version introduces an `inputs/` directory for better organization:

- **`inputs/edges/`**: Place your edge building block CIF files here
- **`inputs/nodes/`**: Place your node building block CIF files here  
- **`inputs/templates/`**: Place your topology template CIF files here

**Backward Compatibility:** The system automatically checks both the new `inputs/` directory and the legacy root directories (`edges/`, `nodes/`, `templates/`), so existing workflows continue to work without modification.

## Installation

### Requirements

- **Python 3.7 or higher** (recommended: Python 3.8+)
- numpy >= 1.19.0
- networkx >= 2.5
- scipy >= 1.5.0

**Note:** This version is optimized for Python 3. Python 2.7 is no longer supported.

### Setup with Conda (Recommended)

1. Create a new conda environment:
```bash
conda create --name tobacco python=3.9
```

2. Activate the environment:
```bash
conda activate tobacco
```

3. Install dependencies:
```bash
conda install numpy networkx scipy
# Or install from requirements.txt
pip install -r requirements.txt
```

### Setup with pip

Install dependencies using pip:
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install numpy>=1.19.0 networkx>=2.5 scipy>=1.5.0
```

### Verify Installation

Test your installation:
```bash
python -c "import numpy, networkx, scipy; print('All dependencies installed successfully!')"
```

### Tested Versions

**Python 3.7+:**
- numpy: 1.19.0 - 1.24.0
- networkx: 2.5 - 3.0
- scipy: 1.5.0 - 1.10.0

**Python 3.9+ (Recommended):**
- numpy: 1.21.0+
- networkx: 2.6+
- scipy: 1.7.0+

### Optional: Export Databases to JSON

For faster database access, export CIF databases to JSON format:
```bash
python scripts/export_databases_to_json.py
```

This creates JSON files in the `data/` directory that can be loaded more quickly than reading individual CIF files.

## Usage

### Command-Line Interface (Original Method)

Execute the tobacco.py file to run ToBaCCo interactively:
```bash
python tobacco.py
```

This maintains full backward compatibility with the original ToBaCCo interface.

### Programmatic API (New)

Use the API for integration into other Python tools:

#### Basic Usage

```python
from src.api import generate_cif

# Generate a single MOF structure
result = generate_cif(
    template_name="pcu",
    node_names="6c_Cu_1_Ch",
    edge_names="btc_edge"
)

# Access the generated CIF file path
print(f"Generated: {result['cifname']}")
print(f"File saved to: {result['file_path']}")
```

#### Multiple Input Formats

The API accepts flexible input formats:

```python
from src.api import generate_cif

# Single string inputs (simplest)
result = generate_cif("pcu", "6c_Cu_1_Ch", "btc_edge")

# List inputs (generate multiple combinations)
result = generate_cif(
    template_name=["pcu", "dia"],
    node_names=["6c_Cu_1_Ch", "4c_Zn_1_Ch"],
    edge_names=["btc_edge", "bdc_edge"]
)

# Dictionary mapping for vertex types
result = generate_cif(
    template_name="pcu",
    node_names={"V": "6c_Cu_1_Ch"},  # Map vertex type to node
    edge_names="btc_edge"
)
```

#### Return Format Options

Control how results are returned:

```python
from src.api import generate_cif

# Return as file path (default - backward compatible)
result = generate_cif("pcu", "6c_Cu_1_Ch", "btc_edge", return_format='file')
print(result['file_path'])  # Path to saved CIF file

# Return as string (no file I/O)
cif_string = generate_cif("pcu", "6c_Cu_1_Ch", "btc_edge", return_format='string')
print(cif_string)  # CIF content as string

# Return as JSON (structured data)
cif_json = generate_cif("pcu", "6c_Cu_1_Ch", "btc_edge", return_format='json')
print(cif_json.keys())  # {'pcu_v1-6c_Cu_1_Ch_1-btc_edge': {...}}
print(cif_json['pcu_v1-6c_Cu_1_Ch_1-btc_edge']['cif_content'])
print(cif_json['pcu_v1-6c_Cu_1_Ch_1-btc_edge']['metadata'])
```

#### Deterministic Charge Generation

Generate reproducible structures with seeded random charges:

```python
from src.api import generate_cif

# Use a specific random seed for reproducibility
result1 = generate_cif("pcu", "6c_Cu_1_Ch", "btc_edge", random_seed=42)
result2 = generate_cif("pcu", "6c_Cu_1_Ch", "btc_edge", random_seed=42)

# Both results will have identical atomic charges
assert result1['cif_content'] == result2['cif_content']

# Different seed produces different charges
result3 = generate_cif("pcu", "6c_Cu_1_Ch", "btc_edge", random_seed=123)
assert result1['cif_content'] != result3['cif_content']
```

#### Advanced Usage with Custom Configuration

```python
from src.api import generate_cif

# Override default configuration
custom_config = {
    "CHARGES": False,
    "SCALING_ITERATIONS": 5,
    "BOND_TOL": 3.0,
    "REMOVE_DUMMY_ATOMS": True
}

result = generate_cif(
    template_name="pcu",
    node_names={"V": "6c_Cu_1_Ch"},  # Dictionary mapping vertex types
    edge_names=["btc_edge"],
    config=custom_config
)

# Access metadata
metadata = result["metadata"]
print(f"Generation time: {metadata['generation_time']:.2f}s")
print(f"Unit cell: a={metadata['unit_cell_params']['a']:.3f} Å")
print(f"Number of atoms: {metadata['num_atoms']}")
print(f"Random seed used: {metadata['random_seed']}")
```

#### Generating Multiple Structures

```python
from src.api import generate_cif, generate_multiple_mofs

# Method 1: Use lists for combinatorial generation
results = generate_cif(
    template_name="pcu",
    node_names=["6c_Cu_1_Ch"],
    edge_names=["btc_edge", "bdc_edge"],
    config={"COMBINATORIAL_EDGE_ASSIGNMENT": True}
)

# Results is a list when multiple structures are generated
for result in results:
    print(f"Structure: {result['cifname']}")

# Method 2: Use generate_multiple_mofs for explicit combinations
combinations = [
    {'template': 'pcu', 'nodes': ['6c_Cu_1_Ch'], 'edges': ['btc_edge']},
    {'template': 'dia', 'nodes': ['4c_Zn_1_Ch'], 'edges': ['bdc_edge']}
]

results = generate_multiple_mofs(combinations, random_seed=42)
print(f"Generated {len(results)} MOFs")
```

#### Error Handling

```python
from src.api import generate_cif

try:
    result = generate_cif(
        template_name="my_template",
        node_names=["6c_Cu_1_Ch"],
        edge_names=["btc_edge"]
    )
except FileNotFoundError as e:
    print(f"File not found: {e}")
except ValueError as e:
    print(f"Invalid input: {e}")
```

### API Reference

#### `generate_cif(template_name, node_names, edge_names, config=None, return_format='file', random_seed=None)`

Generate CIF file content from template, nodes, and edges.

**Parameters:**
- `template_name` (str or list): Template filename(s) without .cif extension (e.g., "pcu")
  - Single string: `"pcu"`
  - List of strings: `["pcu", "dia", "sod"]`
- `node_names` (str, list, or dict): Node filename(s) or vertex type mapping
  - Single string: `"6c_Cu_1_Ch"`
  - List of strings: `["6c_Cu_1_Ch", "4c_Zn_1_Ch"]`
  - Dict mapping vertex types: `{"V": "6c_Cu_1_Ch", "V2": "4c_Zn_1_Ch"}`
- `edge_names` (str or list): Edge filename(s) without .cif extension
  - Single string: `"btc_edge"`
  - List of strings: `["btc_edge", "bdc_edge"]`
- `config` (dict, optional): Configuration overrides (see Configuration section)
- `return_format` (str or list, optional): Output format specification
  - `'file'`: Save to file and return path (default, backward compatible)
  - `'string'`: Return CIF content as string
  - `'json'`: Return as JSON object with metadata
  - List of formats: `['file', 'string']` returns dict with both
- `random_seed` (int, optional): Seed for deterministic charge generation
  - If None, uses `RANDOM_SEED` from configuration (default: 42)
  - Same seed produces identical atomic charges

**Returns:**
- **When `return_format='file'`** (default):
  - Single result: dict with keys `'file_path'`, `'cifname'`, `'cif_content'`, `'metadata'`
  - Multiple results: list of dicts
- **When `return_format='string'`**:
  - Single result: string (CIF content)
  - Multiple results: list of strings
- **When `return_format='json'`**:
  - dict: `{"mof_name": {"cif_content": "...", "metadata": {...}}, ...}`
- **When `return_format` is a list**:
  - dict mapping format names to their respective outputs

**Raises:**
- `FileNotFoundError`: If template, node, or edge file not found
- `ValueError`: If assignments are incompatible or inputs are invalid

**Examples:**
```python
# Basic usage
result = generate_cif("pcu", "6c_Cu_1_Ch", "btc_edge")

# Multiple inputs
result = generate_cif(
    template_name=["pcu", "dia"],
    node_names=["6c_Cu_1_Ch"],
    edge_names=["btc_edge"]
)

# Return as string
cif_string = generate_cif("pcu", "6c_Cu_1_Ch", "btc_edge", return_format='string')

# Deterministic charges
result = generate_cif("pcu", "6c_Cu_1_Ch", "btc_edge", random_seed=42)
```

#### `generate_multiple_mofs(combinations, config=None, return_format='file', random_seed=None)`

Generate multiple MOFs from a list of explicit combinations.

**Parameters:**
- `combinations` (list): List of combination dictionaries, each containing:
  - `'template'`: Template name (str or list)
  - `'nodes'`: Node name(s) (str, list, or dict)
  - `'edges'`: Edge name(s) (str or list)
- `config` (dict, optional): Configuration overrides applied to all generations
- `return_format` (str or list, optional): Output format (same as `generate_cif`)
- `random_seed` (int, optional): Seed for deterministic charge generation

**Returns:**
- **When `return_format='file'`**: list of result dicts
- **When `return_format='string'`**: list of CIF strings
- **When `return_format='json'`**: single dict with all MOFs
- **When `return_format` is a list**: dict mapping format names to outputs

**Raises:**
- `ValueError`: If combinations list is empty or has invalid structure
- `FileNotFoundError`: If any template, node, or edge file not found

**Examples:**
```python
combinations = [
    {'template': 'pcu', 'nodes': ['6c_Cu_1_Ch'], 'edges': ['btc_edge']},
    {'template': 'dia', 'nodes': ['4c_Zn_1_Ch'], 'edges': ['bdc_edge']}
]

results = generate_multiple_mofs(combinations, random_seed=42)
print(f"Generated {len(results)} MOFs")

# Return as JSON
json_results = generate_multiple_mofs(combinations, return_format='json')
```

## Configuration

Configuration options are defined in `configuration.py`. Key options include:

### Core Options
- `CHARGES`: Include atomic charges in output (default: `True`)
- `RANDOM_SEED`: Seed for deterministic charge generation (default: `42`)
- `SCALING_ITERATIONS`: Number of unit cell optimization iterations (default: `1`)
- `BOND_TOL`: Bond distance tolerance for connectivity (default: `5.0` Å)
- `REMOVE_DUMMY_ATOMS`: Remove dummy atoms (Fr) from output (default: `True`)

### Input/Output Options
- `INPUT_SOURCE`: Source for building blocks - `'auto'`, `'json'`, or `'cif'` (default: `'auto'`)
  - `'auto'`: Try JSON database first, fallback to CIF files
  - `'json'`: Load only from JSON databases
  - `'cif'`: Load only from CIF files
- `DEFAULT_RETURN_FORMAT`: Default output format - `'file'`, `'string'`, or `'json'` (default: `'file'`)
- `WRITE_CIF`: Write final CIF files (default: `True`)
- `WRITE_CHECK_FILES`: Write intermediate check files for debugging (default: `False`)

### Generation Options
- `ALL_NODE_COMBINATIONS`: Try all node combinations (default: `False`)
- `COMBINATORIAL_EDGE_ASSIGNMENT`: Generate all edge assignment combinations (default: `True`)
- `ORIENTATION_DEPENDENT_NODES`: Consider node orientation (default: `False`)
- `PLACE_EDGES_BETWEEN_CONNECTION_POINTS`: Place edges between node connection points (default: `True`)

### Filtering Options
- `SINGLE_METAL_MOFS_ONLY`: Only generate structures with a single metal type (default: `True`)
- `MOFS_ONLY`: Only generate MOF structures (require metal nodes) (default: `True`)
- `MERGE_CATENATED_NETS`: Merge interpenetrated/catenated networks (default: `True`)

See `CONFIGURATION_GUIDE.md` for the complete list of options and detailed explanations.

## Utility Scripts

ToBaCCo includes several utility scripts in the `scripts/` directory for database management and analysis:

- **export_databases_to_json.py** - Export CIF databases to JSON format
- **reindex_building_blocks.py** - Reindex building block CIF files
- **make_topologies.py** - Generate topology CIF files from RCSR data
- **topo_pore_analysis.py** - Analyze pore structures using Voronoi tessellation
- **scrape_rcsr.py** - Scrape topology data from RCSR website

For detailed usage information, see `scripts/README.md`.

## Documentation

For detailed information about ToBaCCo's algorithms, inputs, and outputs, see:
- `docs/tobacco_3.0_manual.pdf` - Complete user manual
- `CHANGES.md` - Refactoring changes and migration guide

## Migration from Original Version

The refactored version is fully backward compatible with enhanced features:

### What Stays the Same
1. **Command-line usage**: No changes required - `python tobacco.py` works exactly as before
2. **File locations**: Legacy directories (`templates/`, `nodes/`, `edges/`) are still supported
3. **Configuration**: `configuration.py` remains in the same location with all original options
4. **Output**: CIF files are still saved to `output/cifs/` by default
5. **Algorithms**: All core algorithms are preserved - identical structures are generated

### What's New (Optional)
1. **Organized inputs**: New `inputs/` directory structure for better organization
   - Place files in `inputs/edges/`, `inputs/nodes/`, `inputs/templates/`
   - System checks new location first, then falls back to legacy directories
   
2. **Enhanced API**: Programmatic interface with flexible options
   - Multiple input formats (string, list, dict)
   - Multiple return formats (file, string, JSON)
   - Deterministic charge generation with random seeds
   - Batch generation with `generate_multiple_mofs()`

3. **New configuration options**:
   - `RANDOM_SEED`: Control charge generation for reproducibility (default: 42)
   - `INPUT_SOURCE`: Choose between JSON databases and CIF files (default: 'auto')
   - `DEFAULT_RETURN_FORMAT`: Set default output format (default: 'file')

4. **JSON database support**: Faster loading from pre-exported JSON databases
   - Run `python scripts/export_databases_to_json.py` to create JSON databases
   - System automatically uses JSON when available

### Migration Steps

#### Option 1: No Changes Required
Continue using ToBaCCo exactly as before - everything works without modification.

#### Option 2: Adopt New Directory Structure
1. Create the `inputs/` directory structure:
   ```bash
   mkdir -p inputs/edges inputs/nodes inputs/templates
   ```

2. Move or copy your building blocks:
   ```bash
   # Move files (or use copy to keep originals)
   mv edges/* inputs/edges/
   mv nodes/* inputs/nodes/
   mv templates/* inputs/templates/
   ```

3. (Optional) Export databases to JSON for faster loading:
   ```bash
   python scripts/export_databases_to_json.py
   ```

#### Option 3: Use the New API
Integrate ToBaCCo into your Python scripts:

```python
from src.api import generate_cif

# Old way: Run tobacco.py and read output files
# New way: Call API directly
result = generate_cif(
    template_name="pcu",
    node_names="6c_Cu_1_Ch",
    edge_names="btc_edge",
    return_format='string',  # Get content directly
    random_seed=42  # Reproducible results
)

# Process CIF content directly
print(result)  # CIF content as string
```

#### Option 4: Enable Deterministic Charges
For reproducible simulations:

1. Edit `configuration.py`:
   ```python
   RANDOM_SEED = 42  # Or any integer seed
   ```

2. Or specify in API calls:
   ```python
   result = generate_cif("pcu", "6c_Cu_1_Ch", "btc_edge", random_seed=42)
   ```

### Troubleshooting Migration

**Problem**: "File not found" errors after moving files
- **Solution**: System checks both new and legacy locations. Ensure files are in either `inputs/` or root directories.

**Problem**: Want to use both old and new directory structures
- **Solution**: System supports both simultaneously. Files in `inputs/` take precedence.

**Problem**: Need to verify identical results
- **Solution**: Use the same random seed for charge generation:
  ```python
  # Set in configuration.py
  RANDOM_SEED = 42
  ```

For detailed migration information, see `CHANGES.md`.

## Examples

ToBaCCo includes several example scripts in the `examples/` directory:

### Quick Start Example
```bash
python examples/quick_start.py
```
The simplest way to generate a MOF structure.

### Specific MOF Generation
```bash
python examples/generate_acsh_ce_mof.py
```
Demonstrates how to generate a MOF using specific components:
- Template: acsh
- Node: 12c_Ce_1_Ch  
- Edge: 1B_1TrU

### Comprehensive Example
```bash
python examples/generate_mof_example.py
```
Shows all features including component listing, validation, and batch generation.

For detailed documentation, see `examples/README.md`.

# License
GNU General Public License (can be viewed in the LICENSE file included in this repository)
