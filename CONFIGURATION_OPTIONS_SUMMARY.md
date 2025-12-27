# Configuration Options Summary

This document provides a quick reference for the most commonly used configuration options in ToBaCCo's `generate_cif()` API function.

## Quick Reference

### Basic Usage

```python
from src.api import generate_cif

config = {
    'USER_SPECIFIED_NODE_ASSIGNMENT': False,
    'SCALING_ITERATIONS': 1,
}

result = generate_cif(
    template_name="pcu",
    node_names="6c_Cu_1_Ch",
    edge_names="1B_1TrU",
    config=config  # Pass configuration dictionary
)
```

## Most Important Options

### 1. USER_SPECIFIED_NODE_ASSIGNMENT (bool)
**Default:** `False` (global), `True` (API mode)

Controls which nodes are considered during vertex assignment:
- `True`: Only use nodes specified in `node_names` parameter
- `False`: Consider all available nodes in database

**When to use:**
- Set to `True` when you want precise control over which nodes are used
- Set to `False` to allow the algorithm to explore all compatible nodes

```python
config = {'USER_SPECIFIED_NODE_ASSIGNMENT': True}
```

### 2. SCALING_ITERATIONS (int)
**Default:** `1`

Number of iterations for unit cell optimization.

**When to use:**
- Increase (e.g., 2-5) for better unit cell parameter optimization
- Higher values increase computation time but may improve results
- Use 1 for quick generation

```python
config = {'SCALING_ITERATIONS': 3}  # More optimization
```

### 3. CHARGES (bool)
**Default:** `True`

Enable/disable atomic charge assignment.

```python
config = {'CHARGES': False}  # Disable charges
```

### 4. RANDOM_SEED (int)
**Default:** `42`

Seed for deterministic charge generation. Same seed produces identical charges.

```python
config = {'RANDOM_SEED': 123}  # Custom seed
```

### 5. MIN_CELL_LENGTH (float)
**Default:** `5.0`

Minimum unit cell length in Angstroms. Prevents unit cell collapse.

```python
config = {'MIN_CELL_LENGTH': 10.0}  # Larger minimum
```

### 6. REMOVE_DUMMY_ATOMS (bool)
**Default:** `True`

Remove dummy atoms (Fr) from final structure.

```python
config = {'REMOVE_DUMMY_ATOMS': False}  # Keep dummy atoms
```

## Complete Example

```python
from src.api import generate_cif

# Comprehensive configuration
config = {
    # Structure generation
    'USER_SPECIFIED_NODE_ASSIGNMENT': True,
    'SCALING_ITERATIONS': 2,
    
    # Unit cell
    'MIN_CELL_LENGTH': 10.0,
    'PRE_SCALE': 1.1,
    
    # Charges
    'CHARGES': True,
    'RANDOM_SEED': 42,
    
    # Atoms and bonds
    'REMOVE_DUMMY_ATOMS': True,
    'CONNECTION_SITE_BOND_LENGTH': 1.54,
    'BOND_TOL': 3.0,
    
    # Optimization
    'OPT_METHOD': 'L-BFGS-B',
    
    # Filtering
    'SINGLE_METAL_MOFS_ONLY': True,
    'MOFS_ONLY': True,
}

result = generate_cif(
    template_name="pcu",
    node_names="6c_Cu_1_Ch",
    edge_names="1B_1TrU",
    config=config
)

print(f"Generated: {result['cifname']}")
print(f"Atoms: {result['metadata']['num_atoms']}")
print(f"Unit cell: {result['metadata']['unit_cell_params']}")
```

## All Available Options

For a complete list of all configuration options, see:
- `configuration.py` - All options with default values
- `examples/CONFIG_OPTIONS.md` - Detailed documentation
- `CONFIGURATION_GUIDE.md` - Global configuration file guide

## Examples

See these example files for practical demonstrations:
- `examples/quick_start.py` - Basic usage with config options
- `examples/advanced_config_example.py` - Comprehensive examples
- `test_config_options.py` - Test suite for config options

## Configuration File vs. API Parameter

You can configure ToBaCCo in two ways:

### 1. Global Configuration File (`configuration.py`)
Affects all MOF generations unless overridden:

```python
# In configuration.py
SCALING_ITERATIONS = 3
USER_SPECIFIED_NODE_ASSIGNMENT = True
```

### 2. API Parameter (Recommended)
Override configuration for specific generation:

```python
# In your script
config = {
    'SCALING_ITERATIONS': 3,
    'USER_SPECIFIED_NODE_ASSIGNMENT': True
}

result = generate_cif(..., config=config)
```

**Recommendation:** Use API parameter for flexibility and reproducibility.

## Tips

1. **Start Simple:** Begin with default settings, then adjust as needed
2. **Increase Iterations:** Use `SCALING_ITERATIONS: 2-3` for better optimization
3. **Control Nodes:** Set `USER_SPECIFIED_NODE_ASSIGNMENT: True` for precise control
4. **Reproducibility:** Always set `RANDOM_SEED` for reproducible results
5. **Cell Size:** Adjust `MIN_CELL_LENGTH` if unit cell collapses
6. **Performance:** Lower `SCALING_ITERATIONS` for faster generation

## See Also

- [API Documentation](docs/API_DOCUMENTATION.md)
- [Configuration Guide](CONFIGURATION_GUIDE.md)
- [Examples README](examples/README.md)
- [Quick Start Example](examples/quick_start.py)
