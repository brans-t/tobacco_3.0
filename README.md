# ToBaCCo 3.0 - Topologically Based Crystal Constructor

## Authors
- Ryther Anderson
- Yamil Colón
- Diego Gómez-Gualdrón

## Overview

ToBaCCo (Topologically Based Crystal Constructor) is a tool for rapidly generating molecular representations of porous crystals as crystallographic information (.cif) files for molecular simulation and materials characterization.

This refactored version maintains full backward compatibility while adding:
- Improved project organization with clear module structure
- Programmatic API for integration into other tools
- JSON database export for faster access
- Deterministic charge generation for reproducible research
- Better error handling and validation

## Quick Start

### Installation

**Requirements:** Python 3.7+, numpy, networkx, scipy

```bash
# Create conda environment (recommended)
conda create --name tobacco python=3.9
conda activate tobacco

# Install dependencies
pip install -r requirements.txt

# Optional: Export databases to JSON for faster access
python scripts/export_databases_to_json.py
```

See [docs/INSTALLATION.md](docs/INSTALLATION.md) for detailed installation instructions.

### Basic Usage

#### Command-Line Interface
```bash
python tobacco.py
```

#### Programmatic API
```python
from src.api import generate_cif

# Generate a MOF structure
result = generate_cif(
    template_name="pcu",
    node_names="6c_Cu_1_Ch",
    edge_names="btc_edge"
)

print(f"Generated: {result['cifname']}")
print(f"Saved to: {result['file_path']}")
```

## Project Structure

```
tobacco_3.0/
├── src/                    # Source code package
│   ├── api.py             # Public API interface
│   ├── core/              # Core algorithm modules
│   ├── utils/             # Utility modules
│   └── visualization/     # Visualization tools
├── data/                   # Database files
│   ├── *_database/        # CIF databases
│   └── *.json             # JSON exports (faster)
├── inputs/                 # Input building blocks (NEW)
│   ├── edges/             # Edge linkers
│   ├── nodes/             # Node building blocks
│   └── templates/         # Topology templates
├── output/                 # Generated output files
│   ├── cifs/              # Generated CIF files
│   └── check_cifs/        # Check files
├── scripts/                # Utility scripts
│   ├── export_databases_to_json.py
│   ├── reindex_building_blocks.py
│   └── ...
├── examples/               # Usage examples
├── tests/                  # Unit tests
├── docs/                   # Documentation
│   ├── INSTALLATION.md    # Installation guide
│   ├── CONFIGURATION.md   # Configuration guide
│   ├── API_DOCUMENTATION.md
│   ├── MIGRATION_GUIDE.md
│   └── tobacco_3.0_manual.pdf
├── tobacco.py              # Main entry point (CLI)
├── configuration.py        # Configuration file
└── README.md              # This file
```

## Key Features

### 1. Flexible Input Formats
```python
# Single string
generate_cif("pcu", "6c_Cu_1_Ch", "btc_edge")

# Lists for multiple combinations
generate_cif(["pcu", "dia"], ["6c_Cu_1_Ch"], ["btc_edge"])

# Dictionary for vertex-specific assignment
generate_cif("pcu", {"V": "6c_Cu_1_Ch"}, "btc_edge")
```

### 2. Multiple Return Formats
```python
# Save to file (default)
result = generate_cif(..., return_format='file')

# Return as string (no file I/O)
cif_string = generate_cif(..., return_format='string')

# Return as JSON with metadata
cif_json = generate_cif(..., return_format='json')
```

### 3. Deterministic Charge Generation
```python
# Same seed produces identical charges
result1 = generate_cif(..., random_seed=42)
result2 = generate_cif(..., random_seed=42)
assert result1['cif_content'] == result2['cif_content']
```

### 4. Batch Generation
```python
from src.api import generate_multiple_mofs

combinations = [
    {'template': 'pcu', 'nodes': '6c_Cu_1_Ch', 'edges': 'btc_edge'},
    {'template': 'dia', 'nodes': '4c_Zn_1_Ch', 'edges': 'bdc_edge'}
]

results = generate_multiple_mofs(combinations, random_seed=42)
```

## Configuration

Configuration options can be set in `configuration.py` or passed to the API:

```python
config = {
    'CHARGES': True,                          # Include atomic charges
    'RANDOM_SEED': 42,                        # Seed for reproducibility
    'SCALING_ITERATIONS': 3,                  # Optimization iterations
    'USER_SPECIFIED_NODE_ASSIGNMENT': True,   # Use only specified nodes
    'MIN_CELL_LENGTH': 10.0,                  # Minimum cell length (Å)
    'BOND_TOL': 3.0,                         # Bond tolerance (Å)
    'INPUT_SOURCE': 'auto'                    # 'auto', 'json', or 'cif'
}

result = generate_cif(..., config=config)
```

See [docs/CONFIGURATION.md](docs/CONFIGURATION.md) for complete configuration guide.

## Examples

```bash
# Quick start example
python examples/quick_start.py

# Single input example
python examples/single_input_example.py

# Multiple inputs example
python examples/multiple_input_example.py

# Deterministic charges example
python examples/deterministic_charge_example.py

# Advanced configuration example
python examples/advanced_config_example.py
```

See [examples/README.md](examples/README.md) for detailed examples.

## Utility Scripts

```bash
# Export databases to JSON (recommended for faster access)
python scripts/export_databases_to_json.py

# Reindex building blocks
python scripts/reindex_building_blocks.py

# Generate topologies from RCSR
python scripts/make_topologies.py

# Analyze pore structures
python scripts/topo_pore_analysis.py
```

See [scripts/README.md](scripts/README.md) for script documentation.

## Documentation

- **[Installation Guide](docs/INSTALLATION.md)** - Detailed installation instructions
- **[Configuration Guide](docs/CONFIGURATION.md)** - Complete configuration reference
- **[API Documentation](docs/API_DOCUMENTATION.md)** - API reference and examples
- **[Migration Guide](docs/MIGRATION_GUIDE.md)** - Migrating from older versions
- **[Examples](examples/README.md)** - Usage examples and tutorials
- **[ToBaCCo Manual](docs/tobacco_3.0_manual.pdf)** - Complete user manual

## Migration from Original Version

The refactored version is **fully backward compatible**:

✅ Command-line interface unchanged  
✅ Configuration file location unchanged  
✅ Working directories supported  
✅ Output format unchanged  
✅ All algorithms preserved  

### What's New (Optional)

1. **Organized inputs**: New `inputs/` directory structure
2. **Enhanced API**: Programmatic interface with flexible options
3. **New configuration options**:
   - `RANDOM_SEED`: Control charge generation (default: 42)
   - `INPUT_SOURCE`: Choose database source (default: 'auto')
   - `DEFAULT_RETURN_FORMAT`: Set output format (default: 'file')
4. **JSON database support**: Faster loading from pre-exported databases

See [docs/MIGRATION_GUIDE.md](docs/MIGRATION_GUIDE.md) for migration details.

## Testing

```bash
# Run all tests
pytest tests/

# Run specific test
pytest tests/test_api.py

# Check installation
python check_installation.py
```

## Troubleshooting

### Component not found
```bash
# Export databases to JSON
python scripts/export_databases_to_json.py

# Check available components
python -c "import json; print(list(json.load(open('data/template_database.json')).keys()))"
```

### Generation fails
- Check node coordination matches template requirements
- Try different node/edge combinations
- Increase `BOND_TOL` in configuration

### Different results each time
- Set `RANDOM_SEED` to a fixed value for reproducibility

## License

GNU General Public License (see LICENSE file)

## Citation

If you use ToBaCCo in your research, please cite:

```
Anderson, R., Gómez-Gualdrón, D. A., et al. (2019)
ToBaCCo: Topologically Based Crystal Constructor
```

## Support

- **Documentation**: See `docs/` directory
- **Examples**: See `examples/` directory
- **Issues**: Check existing issues or create a new one
- **Manual**: See `docs/tobacco_3.0_manual.pdf`

---

**Version:** 3.0  
**Python Support:** 3.7+  
**Last Updated:** December 2024
