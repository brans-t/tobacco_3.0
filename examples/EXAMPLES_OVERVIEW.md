# ToBaCCo Examples Overview

This directory contains comprehensive examples demonstrating all features of ToBaCCo 3.0.

## Quick Reference

| Example File | Purpose | Key Features |
|-------------|---------|--------------|
| `quick_start.py` | Simplest introduction | Basic MOF generation in 3 steps |
| `single_input_example.py` | Single input generation | All return formats (file, string, JSON) |
| `multiple_input_example.py` | Batch generation | Multiple inputs, combinatorial generation |
| `deterministic_charge_example.py` | Reproducible charges | Random seed usage, charge verification |
| `generate_mof_example.py` | Comprehensive demo | All features with detailed output |

## Running Examples

### 1. Quick Start (Recommended First)
```bash
python examples/quick_start.py
```
**Time:** ~10 seconds  
**Output:** 1 MOF file  
**Best for:** First-time users

### 2. Single Input Examples
```bash
python examples/single_input_example.py
```
**Time:** ~30 seconds  
**Output:** Multiple MOFs demonstrating different return formats  
**Best for:** Learning the new API features

### 3. Multiple Input Examples
```bash
python examples/multiple_input_example.py
```
**Time:** ~2 minutes  
**Output:** Many MOFs from combinatorial generation  
**Best for:** Batch processing workflows

### 4. Deterministic Charge Examples
```bash
python examples/deterministic_charge_example.py
```
**Time:** ~1 minute  
**Output:** MOFs with reproducible charges  
**Best for:** Reproducible research

### 5. Comprehensive Examples
```bash
python examples/generate_mof_example.py
```
**Time:** ~30 seconds  
**Output:** Detailed generation with component discovery  
**Best for:** Understanding all features

## What's New in ToBaCCo 3.0

### 1. Flexible Input Formats
```python
# Old: Always required lists
generate_cif("pcu", ["6c_Cu_1_Ch"], ["btc_edge"])

# New: Single strings supported
generate_cif("pcu", "6c_Cu_1_Ch", "btc_edge")
```

### 2. Multiple Return Formats
```python
# Return as file (default)
result = generate_cif(..., return_format='file')

# Return as string
cif_string = generate_cif(..., return_format='string')

# Return as JSON
json_data = generate_cif(..., return_format='json')
```

### 3. Deterministic Charges
```python
# Reproducible results with random seed
result = generate_cif(..., random_seed=42)

# Same seed → identical charges
```

### 4. Organized Inputs
```
inputs/
├── templates/  # Topology templates
├── nodes/      # Node building blocks
└── edges/      # Edge linkers
```

### 5. Enhanced Metadata
```python
metadata = result['metadata']
# - generation_time
# - random_seed
# - unit_cell_params
# - num_atoms, num_bonds
# - bond_check_passed
```

## Example Progression

### Beginner Path
1. `quick_start.py` - Learn the basics
2. `single_input_example.py` - Explore return formats
3. `generate_mof_example.py` - See all features

### Advanced Path
1. `multiple_input_example.py` - Batch generation
2. `deterministic_charge_example.py` - Reproducible research
3. Custom scripts using the API

## Common Use Cases

### Use Case 1: Generate a Single MOF
**Example:** `quick_start.py` or `single_input_example.py`
```python
result = generate_cif("pcu", "6c_Cu_1_Ch", "btc_edge")
```

### Use Case 2: Generate Many MOFs
**Example:** `multiple_input_example.py`
```python
results = generate_cif(
    template_name=["pcu", "dia"],
    node_names=["6c_Cu_1_Ch", "6c_Zn_1_Ch"],
    edge_names="btc_edge"
)
```

### Use Case 3: Reproducible Research
**Example:** `deterministic_charge_example.py`
```python
result = generate_cif(..., random_seed=42)
```

### Use Case 4: Web API Integration
**Example:** `single_input_example.py` (Example 3)
```python
json_result = generate_cif(..., return_format='json')
```

### Use Case 5: In-Memory Processing
**Example:** `single_input_example.py` (Example 2)
```python
cif_string = generate_cif(..., return_format='string')
```

## Prerequisites

### Required Files
All examples require input files in one of these locations:
- `inputs/templates/`, `inputs/nodes/`, `inputs/edges/` (preferred)
- `data/template_database.json`, `data/nodes_database.json`, `data/edges_database.json` (fallback)

### Generate JSON Databases
If JSON databases don't exist:
```bash
python scripts/export_databases_to_json.py
```

### Check Installation
```bash
python check_installation.py
```

## Troubleshooting

### Error: Component not found
**Solution:** Ensure input files exist in `inputs/` directory or JSON databases

### Error: Import failed
**Solution:** Run examples from project root: `python examples/quick_start.py`

### Error: No module named 'src'
**Solution:** Make sure you're in the project root directory

## Next Steps

After running the examples:
1. Read `examples/README.md` for detailed documentation
2. Check `docs/API_DOCUMENTATION.md` for API reference
3. Review `docs/MIGRATION_GUIDE.md` for migration from old API
4. Start building your own MOF generation scripts!

## Support

- **Documentation:** `README.md`, `docs/`
- **Configuration:** `CONFIGURATION_GUIDE.md`
- **API Reference:** `docs/API_DOCUMENTATION.md`
- **Manual:** `docs/tobacco_3.0_manual.pdf`

---

**Happy MOF Generation!** 🔬✨
