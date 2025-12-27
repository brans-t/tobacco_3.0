# ToBaCCo 3.0 API Documentation

## Overview

The ToBaCCo 3.0 API provides a programmatic interface for generating Metal-Organic Framework (MOF) structures. This document describes all public API functions, their parameters, return values, and usage examples.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Core Functions](#core-functions)
   - [generate_cif()](#generate_cif)
   - [generate_multiple_mofs()](#generate_multiple_mofs)
3. [Input Formats](#input-formats)
4. [Return Formats](#return-formats)
5. [Configuration](#configuration)
6. [Error Handling](#error-handling)
7. [Advanced Usage](#advanced-usage)
8. [Examples](#examples)

---

## Quick Start

```python
from src.api import generate_cif

# Generate a single MOF
result = generate_cif(
    template_name="pcu",
    node_names="6c_Cu_1_Ch",
    edge_names="btc_edge"
)

print(f"Generated: {result['cifname']}")
print(f"Saved to: {result['file_path']}")
```

---

## Core Functions

### generate_cif()

Generate CIF file(s) from template, nodes, and edges.

#### Signature

```python
def generate_cif(
    template_name,
    node_names,
    edge_names,
    config=None,
    return_format='file',
    random_seed=None
)
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `template_name` | str or list | Yes | Template filename(s) without .cif extension (e.g., "pcu") |
| `node_names` | str, list, or dict | Yes | Node filename(s) or vertex type mapping |
| `edge_names` | str or list | Yes | Edge filename(s) without .cif extension |
| `config` | dict | No | Configuration overrides (see [Configuration](#configuration)) |
| `return_format` | str or list | No | Output format: 'file', 'string', or 'json' (default: 'file') |
| `random_seed` | int | No | Seed for deterministic charge generation (default: from config) |

#### Input Format Details

**template_name:**
- Single string: `"pcu"`
- List of strings: `["pcu", "dia", "sod"]`
- Extensions (.cif) are optional

**node_names:**
- Single string: `"6c_Cu_1_Ch"`
- List of strings: `["6c_Cu_1_Ch", "4c_Zn_1_Ch"]`
- Dict mapping vertex types: `{"V": "6c_Cu_1_Ch", "V2": "4c_Zn_1_Ch"}`
- Extensions (.cif) are optional

**edge_names:**
- Single string: `"btc_edge"`
- List of strings: `["btc_edge", "bdc_edge"]`
- Extensions (.cif) are optional

#### Return Values

The return value depends on the `return_format` parameter:

**When `return_format='file'` (default):**
- Single result: dict with keys:
  - `'file_path'`: Path object to saved CIF file
  - `'cifname'`: Generated filename (str)
  - `'cif_content'`: CIF file content (str)
  - `'metadata'`: Generation metadata (dict)
- Multiple results: list of dicts

**When `return_format='string'`:**
- Single result: CIF content as string
- Multiple results: list of strings

**When `return_format='json'`:**
- dict: `{"mof_name": {"cif_content": "...", "metadata": {...}}, ...}`

**When `return_format` is a list (e.g., `['file', 'string']`):**
- dict mapping format names to their respective outputs

#### Metadata Structure

The `metadata` dict contains:

```python
{
    "template": "pcu.cif",
    "nodes": ["6c_Cu_1_Ch.cif"],
    "edges": ["btc_edge.cif"],
    "generation_time": 1.23,  # seconds
    "random_seed": 42,
    "unit_cell_params": {
        "a": 10.5,  # Angstroms
        "b": 10.5,
        "c": 10.5,
        "alpha": 90.0,  # degrees
        "beta": 90.0,
        "gamma": 90.0
    },
    "num_atoms": 156,
    "num_bonds": 180,
    "bond_check_passed": True
}
```

#### Exceptions

| Exception | When Raised |
|-----------|-------------|
| `FileNotFoundError` | Template, node, or edge file not found |
| `ValueError` | Invalid input format or incompatible assignments |

#### Examples

**Basic usage:**
```python
result = generate_cif("pcu", "6c_Cu_1_Ch", "btc_edge")
```

**Multiple templates:**
```python
results = generate_cif(
    template_name=["pcu", "dia"],
    node_names="6c_Cu_1_Ch",
    edge_names="btc_edge"
)
# Returns list of results
```

**Vertex type mapping:**
```python
result = generate_cif(
    template_name="pcu",
    node_names={"V": "6c_Cu_1_Ch"},
    edge_names="btc_edge"
)
```

**Return as string:**
```python
cif_string = generate_cif(
    template_name="pcu",
    node_names="6c_Cu_1_Ch",
    edge_names="btc_edge",
    return_format='string'
)
print(cif_string)  # CIF content
```

**Return as JSON:**
```python
cif_json = generate_cif(
    template_name="pcu",
    node_names="6c_Cu_1_Ch",
    edge_names="btc_edge",
    return_format='json'
)
print(cif_json.keys())  # MOF names
```

**Deterministic charges:**
```python
result1 = generate_cif("pcu", "6c_Cu_1_Ch", "btc_edge", random_seed=42)
result2 = generate_cif("pcu", "6c_Cu_1_Ch", "btc_edge", random_seed=42)
# result1 and result2 have identical charges
```

**Custom configuration:**
```python
result = generate_cif(
    template_name="pcu",
    node_names="6c_Cu_1_Ch",
    edge_names="btc_edge",
    config={
        "CHARGES": False,
        "SCALING_ITERATIONS": 5,
        "BOND_TOL": 3.0
    }
)
```

---

### generate_multiple_mofs()

Generate multiple MOFs from a list of explicit combinations.

#### Signature

```python
def generate_multiple_mofs(
    combinations,
    config=None,
    return_format='file',
    random_seed=None
)
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `combinations` | list | Yes | List of combination dicts (see below) |
| `config` | dict | No | Configuration overrides applied to all generations |
| `return_format` | str or list | No | Output format: 'file', 'string', or 'json' (default: 'file') |
| `random_seed` | int | No | Seed for deterministic charge generation |

#### Combinations Format

Each combination dict must contain:

```python
{
    'template': 'pcu',  # str or list
    'nodes': ['6c_Cu_1_Ch'],  # str, list, or dict
    'edges': ['btc_edge']  # str or list
}
```

Example:
```python
combinations = [
    {'template': 'pcu', 'nodes': ['6c_Cu_1_Ch'], 'edges': ['btc_edge']},
    {'template': 'dia', 'nodes': ['4c_Zn_1_Ch'], 'edges': ['bdc_edge']},
    {'template': 'sod', 'nodes': {'V': '6c_Cu_1_Ch'}, 'edges': ['btc_edge']}
]
```

#### Return Values

**When `return_format='file'`:**
- list of result dicts (same structure as `generate_cif`)

**When `return_format='string'`:**
- list of CIF content strings

**When `return_format='json'`:**
- Single dict with all MOFs: `{"mof1": {...}, "mof2": {...}, ...}`

**When `return_format` is a list:**
- dict mapping format names to their outputs

#### Exceptions

| Exception | When Raised |
|-----------|-------------|
| `ValueError` | Empty combinations list or invalid structure |
| `FileNotFoundError` | Any template, node, or edge file not found |

#### Examples

**Basic usage:**
```python
from src.api import generate_multiple_mofs

combinations = [
    {'template': 'pcu', 'nodes': ['6c_Cu_1_Ch'], 'edges': ['btc_edge']},
    {'template': 'dia', 'nodes': ['4c_Zn_1_Ch'], 'edges': ['bdc_edge']}
]

results = generate_multiple_mofs(combinations)
print(f"Generated {len(results)} MOFs")

for result in results:
    print(f"- {result['cifname']}")
```

**With JSON output:**
```python
json_results = generate_multiple_mofs(
    combinations,
    return_format='json'
)

for mof_name, mof_data in json_results.items():
    print(f"{mof_name}: {mof_data['metadata']['num_atoms']} atoms")
```

**With deterministic charges:**
```python
results = generate_multiple_mofs(
    combinations,
    random_seed=42,
    config={"CHARGES": True}
)
```

---

## Input Formats

### Template Names

Templates define the topological network structure.

**Accepted formats:**
- Single string: `"pcu"`
- List of strings: `["pcu", "dia", "sod"]`
- With or without .cif extension: `"pcu"` or `"pcu.cif"`

**File locations:**
- Primary: `inputs/templates/`
- Fallback: `templates/` (legacy)

### Node Names

Nodes are building blocks representing vertices in the network.

**Accepted formats:**
- Single string: `"6c_Cu_1_Ch"`
- List of strings: `["6c_Cu_1_Ch", "4c_Zn_1_Ch"]`
- Dict mapping vertex types: `{"V": "6c_Cu_1_Ch", "V2": "4c_Zn_1_Ch"}`
- With or without .cif extension

**File locations:**
- Primary: `inputs/nodes/`
- Fallback: `nodes/` (legacy)

**Vertex type mapping:**
When using a dict, keys should match vertex types in the template:
```python
node_names = {
    "V": "6c_Cu_1_Ch",  # Vertex type V
    "V2": "4c_Zn_1_Ch"  # Vertex type V2
}
```

### Edge Names

Edges are building blocks representing connections between nodes.

**Accepted formats:**
- Single string: `"btc_edge"`
- List of strings: `["btc_edge", "bdc_edge"]`
- With or without .cif extension

**File locations:**
- Primary: `inputs/edges/`
- Fallback: `edges/` (legacy)

---

## Return Formats

### File Format (default)

Saves CIF files to `output/cifs/` and returns file paths.

```python
result = generate_cif("pcu", "6c_Cu_1_Ch", "btc_edge", return_format='file')

# Single result
print(result['file_path'])  # Path object
print(result['cifname'])    # Filename string
print(result['cif_content']) # CIF content string
print(result['metadata'])   # Metadata dict

# Multiple results
for res in results:
    print(res['file_path'])
```

**Use when:**
- You want to save CIF files for later use
- You need backward compatibility with existing workflows
- You want both file and content access

### String Format

Returns CIF content as strings without file I/O.

```python
cif_string = generate_cif("pcu", "6c_Cu_1_Ch", "btc_edge", return_format='string')

# Single result
print(cif_string)  # CIF content as string

# Multiple results
for cif in cif_strings:
    print(cif)
```

**Use when:**
- You want to process CIF content directly
- You don't need to save files
- You're integrating with other tools that accept strings

### JSON Format

Returns structured JSON with CIF content and metadata.

```python
cif_json = generate_cif("pcu", "6c_Cu_1_Ch", "btc_edge", return_format='json')

# Structure
{
    "pcu_v1-6c_Cu_1_Ch_1-btc_edge": {
        "cif_content": "data_pcu...",
        "metadata": {
            "template": "pcu.cif",
            "nodes": ["6c_Cu_1_Ch.cif"],
            "edges": ["btc_edge.cif"],
            "generation_time": 1.23,
            "random_seed": 42,
            "unit_cell_params": {...},
            "num_atoms": 156,
            "num_bonds": 180,
            "bond_check_passed": True
        }
    }
}

# Access
for mof_name, mof_data in cif_json.items():
    print(f"MOF: {mof_name}")
    print(f"Atoms: {mof_data['metadata']['num_atoms']}")
    print(f"Content: {mof_data['cif_content'][:100]}...")
```

**Use when:**
- You need structured data with metadata
- You're building web APIs or services
- You want to serialize results to JSON files

### Multiple Formats

Request multiple formats simultaneously.

```python
results = generate_cif(
    "pcu", "6c_Cu_1_Ch", "btc_edge",
    return_format=['file', 'string', 'json']
)

# Structure
{
    'file': [Path('output/cifs/pcu_v1-6c_Cu_1_Ch_1-btc_edge.cif')],
    'string': ["data_pcu..."],
    'json': {"pcu_v1-6c_Cu_1_Ch_1-btc_edge": {...}}
}

# Access
file_paths = results['file']
cif_strings = results['string']
cif_json = results['json']
```

**Use when:**
- You need results in multiple formats
- You want to save files and process content
- You're building flexible pipelines

---

## Configuration

Configuration options can be overridden via the `config` parameter.

### Common Configuration Options

```python
config = {
    # Charge generation
    "CHARGES": True,  # Include atomic charges
    "RANDOM_SEED": 42,  # Seed for deterministic charges
    
    # Optimization
    "SCALING_ITERATIONS": 1,  # Unit cell optimization iterations
    "BOND_TOL": 5.0,  # Bond distance tolerance (Angstroms)
    
    # Generation options
    "COMBINATORIAL_EDGE_ASSIGNMENT": True,  # All edge combinations
    "ALL_NODE_COMBINATIONS": False,  # All node combinations
    
    # Output options
    "REMOVE_DUMMY_ATOMS": True,  # Remove Fr atoms
    "WRITE_CIF": True,  # Write CIF files
    
    # Filtering
    "SINGLE_METAL_MOFS_ONLY": True,  # Only single-metal MOFs
    "MOFS_ONLY": True  # Only MOFs (require metal nodes)
}

result = generate_cif(
    "pcu", "6c_Cu_1_Ch", "btc_edge",
    config=config
)
```

### Configuration Categories

**Charge Generation:**
- `CHARGES` (bool): Include atomic charges
- `RANDOM_SEED` (int): Seed for reproducibility

**Optimization:**
- `SCALING_ITERATIONS` (int): Optimization iterations (1-10)
- `OPT_METHOD` (str): Scipy optimizer ('L-BFGS-B', 'SLSQP', etc.)
- `PRE_SCALE` (float): Pre-scaling factor
- `FIX_UC` (tuple): Fix unit cell parameters (a,b,c,α,β,γ)

**Geometric Parameters:**
- `CONNECTION_SITE_BOND_LENGTH` (float): Target bond length (Å)
- `BOND_TOL` (float): Bond detection tolerance (Å)
- `MIN_CELL_LENGTH` (float): Minimum unit cell length (Å)
- `SYMMETRY_TOL` (dict): Symmetry tolerances by coordination

**Generation Options:**
- `ALL_NODE_COMBINATIONS` (bool): Try all node combinations
- `COMBINATORIAL_EDGE_ASSIGNMENT` (bool): All edge combinations
- `ORIENTATION_DEPENDENT_NODES` (bool): Consider node orientation
- `PLACE_EDGES_BETWEEN_CONNECTION_POINTS` (bool): Edge placement

**Output Options:**
- `WRITE_CIF` (bool): Write CIF files
- `WRITE_CHECK_FILES` (bool): Write debug files
- `REMOVE_DUMMY_ATOMS` (bool): Remove Fr atoms
- `OUTPUT_SCALING_DATA` (bool): Output optimization data

**Filtering:**
- `SINGLE_METAL_MOFS_ONLY` (bool): Only single-metal MOFs
- `MOFS_ONLY` (bool): Require metal nodes
- `MERGE_CATENATED_NETS` (bool): Merge interpenetrated nets

**Error Handling:**
- `IGNORE_ALL_ERRORS` (bool): Continue on errors
- `PRINT` (bool): Verbose output

See `CONFIGURATION_GUIDE.md` for complete documentation.

---

## Error Handling

### Common Exceptions

#### FileNotFoundError

Raised when input files are not found.

```python
try:
    result = generate_cif("nonexistent", "6c_Cu_1_Ch", "btc_edge")
except FileNotFoundError as e:
    print(f"File not found: {e}")
    # Error message includes searched locations
```

**Solutions:**
- Check file exists in `inputs/templates/`, `inputs/nodes/`, or `inputs/edges/`
- Check legacy directories: `templates/`, `nodes/`, `edges/`
- Verify filename spelling and extension

#### ValueError

Raised for invalid inputs or incompatible assignments.

```python
try:
    result = generate_cif("pcu", [], "btc_edge")  # Empty list
except ValueError as e:
    print(f"Invalid input: {e}")
```

**Common causes:**
- Empty input lists
- Invalid input types
- Incompatible node/edge assignments
- Invalid return_format
- No valid vertex assignments found

**Solutions:**
- Validate inputs before calling API
- Check node coordination numbers match template
- Verify edge types are compatible

### Error Handling Best Practices

```python
from src.api import generate_cif

def safe_generate_mof(template, nodes, edges):
    """
    Safely generate MOF with error handling.
    """
    try:
        result = generate_cif(
            template_name=template,
            node_names=nodes,
            edge_names=edges
        )
        return result, None
    
    except FileNotFoundError as e:
        return None, f"File not found: {e}"
    
    except ValueError as e:
        return None, f"Invalid input: {e}"
    
    except Exception as e:
        return None, f"Unexpected error: {e}"

# Usage
result, error = safe_generate_mof("pcu", "6c_Cu_1_Ch", "btc_edge")
if error:
    print(f"Error: {error}")
else:
    print(f"Success: {result['cifname']}")
```

---

## Advanced Usage

### Batch Generation

Generate multiple MOFs efficiently:

```python
from src.api import generate_multiple_mofs

# Define all combinations
combinations = []
templates = ["pcu", "dia", "sod"]
nodes = ["6c_Cu_1_Ch", "4c_Zn_1_Ch"]
edges = ["btc_edge", "bdc_edge"]

for template in templates:
    for node in nodes:
        for edge in edges:
            combinations.append({
                'template': template,
                'nodes': [node],
                'edges': [edge]
            })

# Generate all at once
results = generate_multiple_mofs(
    combinations,
    random_seed=42,
    return_format='json'
)

print(f"Generated {len(results)} MOFs")
```

### Reproducible Research

Ensure reproducible results with random seeds:

```python
# Set seed for reproducibility
SEED = 42

# Generate MOF
result1 = generate_cif(
    "pcu", "6c_Cu_1_Ch", "btc_edge",
    random_seed=SEED
)

# Later, regenerate with same seed
result2 = generate_cif(
    "pcu", "6c_Cu_1_Ch", "btc_edge",
    random_seed=SEED
)

# Verify identical charges
assert result1['cif_content'] == result2['cif_content']
```

### Custom Workflows

Build custom workflows with different return formats:

```python
# Generate and save to file
result = generate_cif(
    "pcu", "6c_Cu_1_Ch", "btc_edge",
    return_format='file'
)

# Process CIF content
cif_content = result['cif_content']
# ... custom processing ...

# Get metadata
metadata = result['metadata']
print(f"Unit cell: {metadata['unit_cell_params']}")
print(f"Atoms: {metadata['num_atoms']}")
print(f"Generation time: {metadata['generation_time']:.2f}s")
```

### Integration with Other Tools

```python
import json
from src.api import generate_cif

# Generate MOF as JSON
mof_json = generate_cif(
    "pcu", "6c_Cu_1_Ch", "btc_edge",
    return_format='json'
)

# Save to JSON file
with open('mof_data.json', 'w') as f:
    json.dump(mof_json, f, indent=2)

# Send to web API
import requests
response = requests.post(
    'https://api.example.com/mofs',
    json=mof_json
)
```

---

## Examples

### Example 1: Basic MOF Generation

```python
from src.api import generate_cif

result = generate_cif(
    template_name="pcu",
    node_names="6c_Cu_1_Ch",
    edge_names="btc_edge"
)

print(f"Generated: {result['cifname']}")
print(f"Saved to: {result['file_path']}")
print(f"Atoms: {result['metadata']['num_atoms']}")
```

### Example 2: Multiple Templates

```python
results = generate_cif(
    template_name=["pcu", "dia", "sod"],
    node_names="6c_Cu_1_Ch",
    edge_names="btc_edge"
)

for result in results:
    print(f"Template: {result['metadata']['template']}")
    print(f"File: {result['cifname']}")
    print()
```

### Example 3: Vertex Type Mapping

```python
result = generate_cif(
    template_name="pcu",
    node_names={
        "V": "6c_Cu_1_Ch",
        "V2": "4c_Zn_1_Ch"
    },
    edge_names="btc_edge"
)
```

### Example 4: String Output

```python
cif_string = generate_cif(
    template_name="pcu",
    node_names="6c_Cu_1_Ch",
    edge_names="btc_edge",
    return_format='string'
)

# Process string directly
lines = cif_string.split('\n')
print(f"CIF has {len(lines)} lines")
```

### Example 5: JSON Output with Metadata

```python
cif_json = generate_cif(
    template_name="pcu",
    node_names="6c_Cu_1_Ch",
    edge_names="btc_edge",
    return_format='json'
)

for mof_name, mof_data in cif_json.items():
    print(f"MOF: {mof_name}")
    print(f"Atoms: {mof_data['metadata']['num_atoms']}")
    print(f"Unit cell a: {mof_data['metadata']['unit_cell_params']['a']:.3f} Å")
```

### Example 6: Deterministic Charges

```python
# Generate with specific seed
result1 = generate_cif(
    "pcu", "6c_Cu_1_Ch", "btc_edge",
    random_seed=42
)

# Regenerate with same seed
result2 = generate_cif(
    "pcu", "6c_Cu_1_Ch", "btc_edge",
    random_seed=42
)

# Verify identical
assert result1['cif_content'] == result2['cif_content']
print("Charges are identical!")
```

### Example 7: Custom Configuration

```python
result = generate_cif(
    template_name="pcu",
    node_names="6c_Cu_1_Ch",
    edge_names="btc_edge",
    config={
        "CHARGES": False,
        "SCALING_ITERATIONS": 5,
        "BOND_TOL": 3.0,
        "REMOVE_DUMMY_ATOMS": True
    }
)
```

### Example 8: Batch Generation

```python
from src.api import generate_multiple_mofs

combinations = [
    {'template': 'pcu', 'nodes': ['6c_Cu_1_Ch'], 'edges': ['btc_edge']},
    {'template': 'dia', 'nodes': ['4c_Zn_1_Ch'], 'edges': ['bdc_edge']},
    {'template': 'sod', 'nodes': ['6c_Cu_1_Ch'], 'edges': ['btc_edge']}
]

results = generate_multiple_mofs(
    combinations,
    random_seed=42,
    return_format='json'
)

print(f"Generated {len(results)} MOFs")
for mof_name in results.keys():
    print(f"- {mof_name}")
```

### Example 9: Error Handling

```python
from src.api import generate_cif

def generate_with_fallback(template, nodes, edges):
    """Generate MOF with fallback options."""
    try:
        # Try primary generation
        return generate_cif(template, nodes, edges)
    
    except FileNotFoundError:
        # Try alternative nodes
        print(f"File not found, trying alternative...")
        return generate_cif(template, "default_node", edges)
    
    except ValueError as e:
        print(f"Invalid input: {e}")
        return None

result = generate_with_fallback("pcu", "nonexistent", "btc_edge")
```

### Example 10: Multiple Return Formats

```python
results = generate_cif(
    "pcu", "6c_Cu_1_Ch", "btc_edge",
    return_format=['file', 'string', 'json']
)

# Access different formats
file_path = results['file'][0]
cif_string = results['string'][0]
cif_json = results['json']

print(f"File: {file_path}")
print(f"String length: {len(cif_string)}")
print(f"JSON keys: {list(cif_json.keys())}")
```

---

## See Also

- [Configuration Guide](../CONFIGURATION_GUIDE.md) - Detailed configuration options
- [README](../README.md) - General usage and installation
- [Migration Guide](MIGRATION_GUIDE.md) - Migrating from original version
- [Examples](../examples/) - Complete example scripts

---

**Last Updated:** December 28, 2024  
**Version:** 3.0
