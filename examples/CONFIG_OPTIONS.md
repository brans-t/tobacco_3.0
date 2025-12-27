# ToBaCCo Configuration Options Guide

This guide explains how to use configuration options with the `generate_cif()` API function.

## Basic Usage

```python
from src.api import generate_cif

# Pass configuration options via the config parameter
config = {
    'USER_SPECIFIED_NODE_ASSIGNMENT': False,
    'SCALING_ITERATIONS': 1,
}

result = generate_cif(
    template_name="pcu",
    node_names="6c_Cu_1_Ch",
    edge_names="1B_1TrU",
    config=config  # Optional configuration overrides
)
```

## Key Configuration Options

### Structure Generation

#### `USER_SPECIFIED_NODE_ASSIGNMENT` (bool)
- **Default**: `False` (global), `True` (API mode)
- **Description**: Controls which nodes are considered during vertex assignment
  - `True`: Only use nodes specified in the `node_names` parameter
  - `False`: Consider all available nodes in the database
- **Use case**: Set to `True` when you want precise control over which nodes are used

```python
config = {'USER_SPECIFIED_NODE_ASSIGNMENT': True}
```

#### `SCALING_ITERATIONS` (int)
- **Default**: `1`
- **Description**: Number of iterations for unit cell optimization
- **Use case**: Increase for better unit cell parameter optimization (may increase computation time)

```python
config = {'SCALING_ITERATIONS': 3}  # More iterations for better optimization
```

### Unit Cell Parameters

#### `MIN_CELL_LENGTH` (float)
- **Default**: `5.0`
- **Description**: Minimum unit cell length in Angstroms
- **Use case**: Prevent unit cell collapse during scaling

```python
config = {'MIN_CELL_LENGTH': 10.0}  # Larger minimum cell size
```

#### `FIX_UC` (tuple)
- **Default**: `(0, 0, 0, 0, 0, 0)`
- **Description**: Fix specific unit cell parameters (a, b, c, alpha, beta, gamma)
  - `0`: Allow parameter to vary during optimization
  - Non-zero value: Fix parameter to that value
- **Use case**: Constrain specific cell parameters

```python
config = {'FIX_UC': (0, 0, 20.0, 90, 90, 90)}  # Fix c=20Å and angles
```

#### `PRE_SCALE` (float)
- **Default**: `1.00`
- **Description**: Pre-scaling factor applied before optimization
- **Use case**: Adjust initial unit cell size

```python
config = {'PRE_SCALE': 1.2}  # Start with 20% larger cell
```

### Charge Assignment

#### `CHARGES` (bool)
- **Default**: `True`
- **Description**: Enable/disable atomic charge assignment
- **Use case**: Disable for structures that don't need charges

```python
config = {'CHARGES': False}  # No charge assignment
```

#### `RANDOM_SEED` (int)
- **Default**: `42`
- **Description**: Seed for deterministic charge generation
- **Use case**: Ensure reproducible charge assignments

```python
config = {'RANDOM_SEED': 123}  # Custom seed for reproducibility
```

### Atom and Bond Settings

#### `REMOVE_DUMMY_ATOMS` (bool)
- **Default**: `True`
- **Description**: Remove dummy atoms (Fr) from final structure
- **Use case**: Keep dummy atoms for debugging or visualization

```python
config = {'REMOVE_DUMMY_ATOMS': False}  # Keep dummy atoms
```

#### `CONNECTION_SITE_BOND_LENGTH` (float)
- **Default**: `1.54`
- **Description**: Bond length for connection sites in Angstroms
- **Use case**: Adjust connection geometry

```python
config = {'CONNECTION_SITE_BOND_LENGTH': 1.6}
```

#### `BOND_TOL` (float)
- **Default**: `5.0`
- **Description**: Bond tolerance for distance-based bonding
- **Use case**: Adjust bonding criteria

```python
config = {'BOND_TOL': 3.0}  # Stricter bonding criteria
```

### Node and Edge Placement

#### `ORIENTATION_DEPENDENT_NODES` (bool)
- **Default**: `False`
- **Description**: Consider node orientation during placement
- **Use case**: Enable for nodes with specific directional properties

```python
config = {'ORIENTATION_DEPENDENT_NODES': True}
```

#### `PLACE_EDGES_BETWEEN_CONNECTION_POINTS` (bool)
- **Default**: `True`
- **Description**: Adjust edge placement between connection points
- **Use case**: Control edge positioning

```python
config = {'PLACE_EDGES_BETWEEN_CONNECTION_POINTS': False}
```

### Optimization Settings

#### `OPT_METHOD` (str)
- **Default**: `'L-BFGS-B'`
- **Description**: Optimization method for unit cell scaling
- **Options**: `'L-BFGS-B'`, `'SLSQP'`, `'Powell'`, etc. (scipy.optimize methods)
- **Use case**: Try different optimizers for better convergence

```python
config = {'OPT_METHOD': 'SLSQP'}  # Alternative optimizer
```

### Filtering Options

#### `SINGLE_METAL_MOFS_ONLY` (bool)
- **Default**: `True`
- **Description**: Only generate MOFs with a single metal type
- **Use case**: Allow multi-metal MOFs

```python
config = {'SINGLE_METAL_MOFS_ONLY': False}  # Allow multiple metals
```

#### `MOFS_ONLY` (bool)
- **Default**: `True`
- **Description**: Only generate structures containing metals (MOFs)
- **Use case**: Allow non-metal structures (COFs)

```python
config = {'MOFS_ONLY': False}  # Allow COFs
```

### Edge Assignment

#### `COMBINATORIAL_EDGE_ASSIGNMENT` (bool)
- **Default**: `True`
- **Description**: Try all combinations of edge assignments
- **Use case**: Disable for faster generation with sequential edge assignment

```python
config = {'COMBINATORIAL_EDGE_ASSIGNMENT': False}  # Sequential assignment
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
print(f"Unit cell: {result['metadata']['unit_cell_params']}")
```

## See Also

- `configuration.py` - Complete list of all configuration options
- `examples/quick_start.py` - Basic usage example
- `examples/advanced_config_example.py` - Advanced configuration examples
- `CONFIGURATION_GUIDE.md` - Detailed configuration documentation
