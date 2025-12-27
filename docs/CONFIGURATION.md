# ToBaCCo Configuration Guide

### Overview

The `configuration.py` file contains all global settings that control how ToBaCCo generates MOF structures. These settings affect everything from output format to optimization parameters.

### Configuration Methods

#### Method 1: Global Configuration File
Edit `configuration.py` to set defaults for all generations:

```python
# configuration.py
CHARGES = True
SCALING_ITERATIONS = 3
RANDOM_SEED = 42
```

#### Method 2: API Parameter (Recommended)
Override configuration for specific generations:

```python
from src.api import generate_cif

config = {
    'CHARGES': True,
    'SCALING_ITERATIONS': 3,
    'RANDOM_SEED': 42
}

result = generate_cif(
    template_name="pcu",
    node_names="6c_Cu_1_Ch",
    edge_names="btc_edge",
    config=config
)
```

### Key Configuration Options

#### Input/Output Control

**INPUT_SOURCE** (String, default: `'auto'`)
- `'auto'`: Try JSON database first, fallback to CIF files (recommended)
- `'json'`: Load only from JSON databases (faster)
- `'cif'`: Load only from CIF files

**DEFAULT_RETURN_FORMAT** (String, default: `'file'`)
- `'file'`: Save to file and return path
- `'string'`: Return CIF content as string
- `'json'`: Return as JSON object with metadata

**WRITE_CIF** (Boolean, default: `True`)
- Write final CIF files to `output/cifs/`

**WRITE_CHECK_FILES** (Boolean, default: `False`)
- Write intermediate check files for debugging

#### Charge Generation

**CHARGES** (Boolean, default: `True`)
- Include atomic charges in output CIF files

**RANDOM_SEED** (Integer, default: `42`)
- Seed for deterministic charge generation
- Same seed produces identical charges
- Essential for reproducible research

**REMOVE_DUMMY_ATOMS** (Boolean, default: `True`)
- Remove dummy atoms (Fr) from final output

#### Structure Generation

**USER_SPECIFIED_NODE_ASSIGNMENT** (Boolean, default: `False`)
- `True`: Only use nodes specified in `node_names` parameter
- `False`: Consider all available nodes in database

**SCALING_ITERATIONS** (Integer, default: `1`)
- Number of unit cell optimization iterations
- Higher values improve optimization but increase time

**ALL_NODE_COMBINATIONS** (Boolean, default: `False`)
- Try all possible combinations of node assignments

**COMBINATORIAL_EDGE_ASSIGNMENT** (Boolean, default: `True`)
- Generate all possible edge assignment combinations

**ORIENTATION_DEPENDENT_NODES** (Boolean, default: `False`)
- Consider node orientation during placement

#### Geometric Parameters

**CONNECTION_SITE_BOND_LENGTH** (Float, default: `1.54` Å)
- Target bond length at connection sites

**BOND_TOL** (Float, default: `5.0` Å)
- Tolerance for bond distance detection

**MIN_CELL_LENGTH** (Float, default: `5.0` Å)
- Minimum unit cell length

**SYMMETRY_TOL** (Dictionary)
- Symmetry tolerance for different coordination numbers
- Format: `{coordination_number: tolerance}`

#### Optimization Parameters

**OPT_METHOD** (String, default: `'L-BFGS-B'`)
- Optimization method for unit cell scaling

**PRE_SCALE** (Float, default: `1.00`)
- Pre-scaling factor for unit cell

**FIX_UC** (Tuple, default: `(0,0,0,0,0,0)`)
- Fix unit cell parameters during optimization
- Format: `(a, b, c, alpha, beta, gamma)` where 1=fixed, 0=free

#### Structure Filtering

**SINGLE_METAL_MOFS_ONLY** (Boolean, default: `True`)
- Only generate structures with a single metal type

**MOFS_ONLY** (Boolean, default: `True`)
- Only generate MOF structures (require metal nodes)

**MERGE_CATENATED_NETS** (Boolean, default: `True`)
- Merge interpenetrated/catenated networks

### Common Configuration Scenarios

#### Quick Testing
```python
config = {
    'CHARGES': False,
    'SCALING_ITERATIONS': 1,
    'COMBINATORIAL_EDGE_ASSIGNMENT': False,
    'INPUT_SOURCE': 'auto'
}
```

#### High-Quality Production
```python
config = {
    'CHARGES': True,
    'RANDOM_SEED': 42,
    'SCALING_ITERATIONS': 5,
    'BOND_TOL': 3.0,
    'INPUT_SOURCE': 'json'
}
```

#### Reproducible Research
```python
config = {
    'RANDOM_SEED': 42,
    'CHARGES': True,
    'SCALING_ITERATIONS': 3,
    'INPUT_SOURCE': 'json'
}
```

### Quick Reference

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `CHARGES` | bool | `True` | Include atomic charges |
| `RANDOM_SEED` | int | `42` | Seed for charge generation |
| `SCALING_ITERATIONS` | int | `1` | Optimization iterations |
| `USER_SPECIFIED_NODE_ASSIGNMENT` | bool | `False` | Use only specified nodes |
| `MIN_CELL_LENGTH` | float | `5.0` | Minimum cell length (Å) |
| `BOND_TOL` | float | `5.0` | Bond tolerance (Å) |
| `INPUT_SOURCE` | str | `'auto'` | Database source |
| `DEFAULT_RETURN_FORMAT` | str | `'file'` | Output format |

---

## See Also

- Main README: `README.md`
- API Documentation: `docs/API_DOCUMENTATION.md`
- Installation Guide: `docs/INSTALLATION.md`
- Migration Guide: `docs/MIGRATION_GUIDE.md`
- Examples: `examples/README.md`
