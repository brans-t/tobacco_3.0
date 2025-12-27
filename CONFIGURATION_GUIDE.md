# ToBaCCo Configuration Guide

## Overview

The `configuration.py` file contains all the global settings that control how ToBaCCo generates MOF (Metal-Organic Framework) structures. These settings affect everything from output format to optimization parameters.

## Configuration File Location

```
tobacco_3.0/
└── configuration.py    # Main configuration file
```

## How Configuration Works

### 1. Default Configuration
All settings in `configuration.py` serve as default values for ToBaCCo operations.

### 2. Command-Line Usage
When running `tobacco.py`, these settings are loaded automatically:
```python
import configuration
CHARGES = configuration.CHARGES
SCALING_ITERATIONS = configuration.SCALING_ITERATIONS
# ... etc
```

### 3. API Usage
When using the programmatic API, you can override any setting:
```python
from src import generate_cif

# Override default configuration
custom_config = {
    "CHARGES": False,
    "SCALING_ITERATIONS": 5,
    "BOND_TOL": 3.0
}

result = generate_cif(
    template_name="pcu",
    node_names=["6c_Cu_1_Ch"],
    edge_names=["btc_edge"],
    config=custom_config  # Override defaults
)
```

## Configuration Options

### Error Handling

#### `IGNORE_ALL_ERRORS`
- **Type:** Boolean
- **Default:** `False`
- **Description:** If `True`, ToBaCCo will continue execution even when errors occur
- **Use case:** Batch processing where you want to skip problematic structures

#### `PRINT`
- **Type:** Boolean
- **Default:** `False`
- **Description:** Enable verbose output for debugging
- **Use case:** Troubleshooting structure generation issues

---

### Output Control

#### `WRITE_CHECK_FILES`
- **Type:** Boolean
- **Default:** `False`
- **Description:** Write intermediate check files for debugging
- **Output location:** `output/check_cifs/`
- **Use case:** Debugging structure generation process

#### `WRITE_CIF`
- **Type:** Boolean
- **Default:** `True`
- **Description:** Write final CIF files
- **Output location:** `output/cifs/`
- **Use case:** Disable if you only want to test without generating files

#### `CHARGES`
- **Type:** Boolean
- **Default:** `True`
- **Description:** Include atomic charges in output CIF files
- **Use case:** Disable for simpler output or when charges are not needed

#### `REMOVE_DUMMY_ATOMS`
- **Type:** Boolean
- **Default:** `True`
- **Description:** Remove dummy atoms (Fr) from final output
- **Use case:** Dummy atoms are used internally for alignment but usually removed from final structures

---

### Structure Generation

#### `ALL_NODE_COMBINATIONS`
- **Type:** Boolean
- **Default:** `False`
- **Description:** Try all possible combinations of node assignments
- **Use case:** Enable for exhaustive search of possible structures
- **Warning:** Can significantly increase computation time

#### `USER_SPECIFIED_NODE_ASSIGNMENT`
- **Type:** Boolean
- **Default:** `False`
- **Description:** Use user-specified node assignments from `vertex_assignment.txt`
- **Use case:** When you want precise control over which nodes go where

#### `COMBINATORIAL_EDGE_ASSIGNMENT`
- **Type:** Boolean
- **Default:** `True`
- **Description:** Generate all possible edge assignment combinations
- **Use case:** Explore different edge configurations for the same topology
- **Result:** Multiple output structures when enabled

#### `ORIENTATION_DEPENDENT_NODES`
- **Type:** Boolean
- **Default:** `False`
- **Description:** Consider node orientation during placement
- **Use case:** For asymmetric nodes where orientation matters

#### `PLACE_EDGES_BETWEEN_CONNECTION_POINTS`
- **Type:** Boolean
- **Default:** `True`
- **Description:** Place edges between node connection points
- **Use case:** Standard MOF generation; disable for special cases

---

### Geometric Parameters

#### `CONNECTION_SITE_BOND_LENGTH`
- **Type:** Float (Angstroms)
- **Default:** `1.54`
- **Description:** Target bond length at connection sites
- **Use case:** Adjust for different types of bonds (C-C, C-N, etc.)

#### `BOND_TOL`
- **Type:** Float (Angstroms)
- **Default:** `5.0`
- **Description:** Tolerance for bond distance detection
- **Use case:** Increase for loose structures, decrease for tight validation

#### `SYMMETRY_TOL`
- **Type:** Dictionary
- **Default:** `{2:0.10, 3:0.12, 4:0.35, 5:0.25, 6:0.45, 7:0.35, 8:0.40, 9:0.60, 10:0.60, 12:0.60}`
- **Description:** Symmetry tolerance for different coordination numbers
- **Format:** `{coordination_number: tolerance}`
- **Use case:** Fine-tune symmetry detection for different node types

#### `MIN_CELL_LENGTH`
- **Type:** Float (Angstroms)
- **Default:** `5.0`
- **Description:** Minimum unit cell length
- **Use case:** Prevent generation of unrealistically small unit cells

---

### Optimization Parameters

#### `SCALING_ITERATIONS`
- **Type:** Integer
- **Default:** `1`
- **Description:** Number of unit cell optimization iterations
- **Use case:** Increase for better optimized structures (slower)
- **Typical range:** 1-10

#### `OPT_METHOD`
- **Type:** String
- **Default:** `'L-BFGS-B'`
- **Description:** Optimization method for unit cell scaling
- **Options:** Any scipy.optimize method ('L-BFGS-B', 'SLSQP', etc.)
- **Use case:** Change if default optimizer has convergence issues

#### `PRE_SCALE`
- **Type:** Float
- **Default:** `1.00`
- **Description:** Pre-scaling factor for unit cell
- **Use case:** Start optimization from a scaled initial guess

#### `FIX_UC`
- **Type:** Tuple of 6 integers (0 or 1)
- **Default:** `(0,0,0,0,0,0)`
- **Description:** Fix unit cell parameters during optimization
- **Format:** `(a, b, c, alpha, beta, gamma)` where 1 = fixed, 0 = free
- **Example:** `(1,1,0,0,0,0)` fixes a and b, optimizes c and angles

#### `OUTPUT_SCALING_DATA`
- **Type:** Boolean
- **Default:** `True`
- **Description:** Output scaling optimization data
- **Use case:** Debugging optimization process

---

### Structure Filtering

#### `SINGLE_METAL_MOFS_ONLY`
- **Type:** Boolean
- **Default:** `True`
- **Description:** Only generate structures with a single metal type
- **Use case:** Disable to allow mixed-metal MOFs

#### `MOFS_ONLY`
- **Type:** Boolean
- **Default:** `True`
- **Description:** Only generate MOF structures (require metal nodes)
- **Use case:** Disable to generate purely organic frameworks

#### `MERGE_CATENATED_NETS`
- **Type:** Boolean
- **Default:** `True`
- **Description:** Merge interpenetrated/catenated networks
- **Use case:** Disable to keep separate networks

---

### Performance

#### `RUN_PARALLEL`
- **Type:** Boolean
- **Default:** `False`
- **Description:** Enable parallel processing for batch operations
- **Use case:** Enable for faster batch generation (requires multiprocessing)
- **Note:** May not work on all systems

#### `RECORD_CALLBACK`
- **Type:** Boolean
- **Default:** `False`
- **Description:** Record callback data during optimization
- **Use case:** Advanced debugging of optimization process

---

## Common Configuration Scenarios

### 1. Quick Testing (Fast, Minimal Output)
```python
WRITE_CHECK_FILES = False
WRITE_CIF = True
CHARGES = False
SCALING_ITERATIONS = 1
COMBINATORIAL_EDGE_ASSIGNMENT = False
```

### 2. High-Quality Production (Slow, Optimized)
```python
WRITE_CHECK_FILES = False
WRITE_CIF = True
CHARGES = True
SCALING_ITERATIONS = 5
BOND_TOL = 3.0
COMBINATORIAL_EDGE_ASSIGNMENT = True
```

### 3. Debugging (Verbose, All Files)
```python
PRINT = True
WRITE_CHECK_FILES = True
WRITE_CIF = True
OUTPUT_SCALING_DATA = True
IGNORE_ALL_ERRORS = False
```

### 4. Batch Processing (Robust, Continue on Errors)
```python
IGNORE_ALL_ERRORS = True
WRITE_CHECK_FILES = False
WRITE_CIF = True
RUN_PARALLEL = True
```

### 5. Exploring Structures (All Combinations)
```python
ALL_NODE_COMBINATIONS = True
COMBINATORIAL_EDGE_ASSIGNMENT = True
SCALING_ITERATIONS = 3
```

---

## Modifying Configuration

### Method 1: Edit configuration.py Directly
```python
# configuration.py
CHARGES = False
SCALING_ITERATIONS = 5
BOND_TOL = 3.0
```

### Method 2: Override in API Call
```python
from src import generate_cif

result = generate_cif(
    template_name="pcu",
    node_names=["6c_Cu_1_Ch"],
    edge_names=["btc_edge"],
    config={
        "CHARGES": False,
        "SCALING_ITERATIONS": 5,
        "BOND_TOL": 3.0
    }
)
```

### Method 3: Modify at Runtime (Command-Line)
```python
# In tobacco.py or custom script
import configuration
configuration.CHARGES = False
configuration.SCALING_ITERATIONS = 5
```

---

## Best Practices

1. **Start with Defaults** - The default settings work well for most cases
2. **Test Changes** - Always test configuration changes on a small example first
3. **Document Changes** - Keep notes on why you changed specific settings
4. **Use API Overrides** - For one-off changes, use API config parameter instead of editing file
5. **Backup Original** - Keep a copy of the original configuration.py

---

## Troubleshooting

### Problem: Structures look distorted
**Solution:** Increase `SCALING_ITERATIONS` to 3-5

### Problem: Generation is too slow
**Solution:** 
- Set `COMBINATORIAL_EDGE_ASSIGNMENT = False`
- Set `ALL_NODE_COMBINATIONS = False`
- Reduce `SCALING_ITERATIONS` to 1

### Problem: Bond detection issues
**Solution:** Adjust `BOND_TOL` (increase for loose detection, decrease for strict)

### Problem: Symmetry errors
**Solution:** Adjust `SYMMETRY_TOL` values for specific coordination numbers

### Problem: Unit cell too small/large
**Solution:** 
- Adjust `MIN_CELL_LENGTH`
- Modify `PRE_SCALE`
- Use `FIX_UC` to constrain specific parameters

---

## Related Files

- `tobacco.py` - Main entry point that loads configuration
- `src/api.py` - API that allows configuration overrides
- `vertex_assignment.txt` - Used when `USER_SPECIFIED_NODE_ASSIGNMENT = True`

---

**Last Updated:** December 27, 2024
