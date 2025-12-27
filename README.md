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
├── src/                          # Source code package
│   ├── api.py                   # Public API interface
│   ├── core/                    # Core algorithm modules
│   ├── utils/                   # Utility modules
│   │   ├── paths.py            # Path management
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
│   ├── edges_database/
│   ├── nodes_database/
│   ├── template_database/
│   └── *.json                   # JSON database exports
├── output/                      # Generated output files
│   ├── cifs/                    # Generated CIF files
│   └── check_cifs/              # Check files
├── docs/                        # Documentation
├── templates/                   # Working template directory
├── nodes/                       # Working nodes directory
├── edges/                       # Working edges directory
├── tests/                       # Unit tests
├── tobacco.py                   # Main entry point (CLI)
├── configuration.py             # Configuration file
└── vertex_assignment.txt        # Vertex assignment config
```

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
from src import generate_cif

# Generate a MOF structure
result = generate_cif(
    template_name="pcu",
    node_names=["6c_Cu_1_Ch"],
    edge_names=["btc_edge"]
)

# Access the generated CIF content
print(result["cif_content"])
print(f"Generated: {result['cifname']}")

# Save to file
with open(f"output/{result['cifname']}", "w") as f:
    f.write(result["cif_content"])
```

#### Advanced Usage with Custom Configuration

```python
from src import generate_cif

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
```

#### Generating Multiple Structures

```python
from src import generate_cif

# Enable combinatorial edge assignment
config = {"COMBINATORIAL_EDGE_ASSIGNMENT": True}

results = generate_cif(
    template_name="pcu",
    node_names=["6c_Cu_1_Ch"],
    edge_names=["btc_edge", "bdc_edge"],
    config=config
)

# Results is a list when multiple structures are generated
for i, result in enumerate(results):
    print(f"Structure {i+1}: {result['cifname']}")
    with open(f"output/structure_{i}.cif", "w") as f:
        f.write(result["cif_content"])
```

#### Error Handling

```python
from src import generate_cif

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

#### `generate_cif(template_name, node_names, edge_names, config=None)`

Generate CIF file content from template, nodes, and edges.

**Parameters:**
- `template_name` (str): Template filename without .cif extension (e.g., "pcu")
- `node_names` (list or dict): 
  - List of node filenames: `["6c_Cu_1_Ch"]`
  - Dict mapping vertex types to filenames: `{"V": "6c_Cu_1_Ch"}`
- `edge_names` (list): List of edge filenames without .cif extension
- `config` (dict, optional): Configuration overrides

**Returns:**
- dict or list: Single result dict or list of dicts if multiple structures generated
  - `"cif_content"` (str): The CIF file content
  - `"cifname"` (str): Generated filename
  - `"metadata"` (dict): Generation metadata (timing, parameters, unit cell, etc.)

**Raises:**
- `FileNotFoundError`: If template, node, or edge file not found
- `ValueError`: If assignments are incompatible or inputs are invalid

## Configuration

Configuration options are defined in `configuration.py`. Key options include:

- `CHARGES`: Include atomic charges in output
- `SCALING_ITERATIONS`: Number of unit cell optimization iterations
- `BOND_TOL`: Bond distance tolerance for connectivity
- `REMOVE_DUMMY_ATOMS`: Remove dummy atoms (Fr) from output
- `ALL_NODE_COMBINATIONS`: Try all node combinations
- `COMBINATORIAL_EDGE_ASSIGNMENT`: Generate all edge assignment combinations

See `configuration.py` for the complete list of options and their descriptions.

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

The refactored version is fully backward compatible:

1. **Command-line usage**: No changes required - `python tobacco.py` works exactly as before
2. **File locations**: Working directories (`templates/`, `nodes/`, `edges/`) remain in the same location
3. **Configuration**: `configuration.py` remains in the same location
4. **Output**: Enhanced output directory structure (`output/cifs/`) but compatible

**New features** (optional):
- Use the programmatic API for integration
- Export databases to JSON for faster access
- Access generation metadata and timing information

See `CHANGES.md` for a complete list of changes and migration details.

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
