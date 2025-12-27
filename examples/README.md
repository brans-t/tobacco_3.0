# ToBaCCo Usage Examples

This directory contains example scripts demonstrating how to use ToBaCCo to generate MOF structures.

## Quick Start

### Simplest Example: `quick_start.py`

The fastest way to generate a MOF structure:

```bash
python examples/quick_start.py
```

This script demonstrates the **3-step process**:
1. Choose components (template, node, edge)
2. Generate the structure
3. View the results

**Example output:**
```
Template: acsh
Node:     12c_Ce_1_Ch
Edge:     1B_1TrU

✓ Success!
   Generated: acsh_v1-12c_Ce_1_Ch_1-1B_1TrU.cif
   Saved to:  output/cifs/acsh_v1-12c_Ce_1_Ch_1-1B_1TrU.cif
```

---

## Configuration Options

ToBaCCo provides extensive configuration options to customize MOF generation. See `CONFIG_OPTIONS.md` for a complete guide.

### Key Configuration Parameters

#### Structure Generation
- `USER_SPECIFIED_NODE_ASSIGNMENT` (bool) - Control which nodes are considered during vertex assignment
  - `True`: Only use nodes specified in `node_names` parameter
  - `False`: Consider all available nodes in database (default)
  
- `SCALING_ITERATIONS` (int) - Number of iterations for unit cell optimization (default: 1)
  - Higher values may improve cell parameters but increase computation time

#### Unit Cell Parameters
- `MIN_CELL_LENGTH` (float) - Minimum unit cell length in Angstroms (default: 5.0)
- `FIX_UC` (tuple) - Fix specific unit cell parameters (a, b, c, alpha, beta, gamma)
- `PRE_SCALE` (float) - Pre-scaling factor applied before optimization (default: 1.0)

#### Charge Assignment
- `CHARGES` (bool) - Enable/disable atomic charge assignment (default: True)
- `RANDOM_SEED` (int) - Seed for deterministic charge generation (default: 42)

#### Atom and Bond Settings
- `REMOVE_DUMMY_ATOMS` (bool) - Remove dummy atoms (Fr) from final structure (default: True)
- `CONNECTION_SITE_BOND_LENGTH` (float) - Bond length for connection sites in Å (default: 1.54)
- `BOND_TOL` (float) - Bond tolerance for distance-based bonding (default: 5.0)

#### Optimization
- `OPT_METHOD` (str) - Optimization method for unit cell scaling (default: 'L-BFGS-B')
  - Options: 'L-BFGS-B', 'SLSQP', 'Powell', etc.

#### Filtering
- `SINGLE_METAL_MOFS_ONLY` (bool) - Only generate MOFs with single metal type (default: True)
- `MOFS_ONLY` (bool) - Only generate structures containing metals (default: True)

### Example: Advanced Configuration

```python
from src.api import generate_cif

# Comprehensive configuration
config = {
    # Structure generation
    'USER_SPECIFIED_NODE_ASSIGNMENT': True,
    'SCALING_ITERATIONS': 3,
    
    # Unit cell
    'MIN_CELL_LENGTH': 10.0,
    'PRE_SCALE': 1.1,
    'FIX_UC': (0, 0, 20.0, 90, 90, 90),  # Fix c=20Å and angles
    
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
print(f"Unit cell: {result['metadata']['unit_cell_params']}")
```

For complete documentation of all configuration options, see:
- `CONFIG_OPTIONS.md` - Detailed configuration guide
- `configuration.py` - All available options with defaults
- `CONFIGURATION_GUIDE.md` - Global configuration file documentation

---

## New Examples (ToBaCCo 3.0 Refactored)

### Single Input Example: `single_input_example.py`

Demonstrates basic MOF generation with all three return formats:

```bash
python examples/single_input_example.py
```

**Features:**
- File format (save to disk)
- String format (in-memory processing)
- JSON format (structured data with metadata)
- Custom configuration
- Input flexibility (.cif extensions optional)

### Multiple Input Example: `multiple_input_example.py`

Shows batch MOF generation with multiple inputs:

```bash
python examples/multiple_input_example.py
```

**Features:**
- Multiple nodes, edges, or templates
- Combinatorial generation
- Batch processing with `generate_multiple_mofs()`
- Vertex-specific node assignment
- Large-scale generation

### Deterministic Charge Example: `deterministic_charge_example.py`

Demonstrates reproducible charge generation:

```bash
python examples/deterministic_charge_example.py
```

**Features:**
- Same seed → identical charges
- Different seeds → different charges
- Reproducible research workflows
- Charge neutrality verification
- Seed traceability in metadata

### Advanced Configuration Example: `advanced_config_example.py`

Comprehensive demonstration of configuration options:

```bash
python examples/advanced_config_example.py
```

**Features:**
- `USER_SPECIFIED_NODE_ASSIGNMENT` - Control node selection
- `SCALING_ITERATIONS` - Unit cell optimization
- `CHARGES` - Charge assignment control
- `REMOVE_DUMMY_ATOMS` - Dummy atom handling
- `MIN_CELL_LENGTH` - Cell size constraints
- `RANDOM_SEED` - Deterministic charge generation
- Multiple configuration examples with comparisons

---

## Comprehensive Example: `generate_mof_example.py`

A detailed example showing all features:

```bash
python examples/generate_mof_example.py
```

### Features Demonstrated:

#### 1. List Available Components
```python
list_available_components()
```
Shows all available templates, nodes, and edges from JSON databases.

#### 2. Check Component Existence
```python
check_component_exists("acsh", "template")
check_component_exists("12c_Ce_1_Ch", "nodes")
check_component_exists("1B_1TrU", "edges")
```
Verifies that components exist before generation.

#### 3. Generate Single Structure
```python
result = generate_mof_structure(
    template_name="acsh",
    node_name="12c_Ce_1_Ch",
    edge_name="1B_1TrU"
)
```
Generates a MOF with detailed progress reporting.

#### 4. Generate Multiple Structures
```python
results = generate_multiple_structures()
```
Batch generation of multiple MOF structures.

---

## Understanding the Components

### Input Directory Structure (New in 3.0)

Components are now organized in the `inputs/` directory:

```
inputs/
├── templates/    # Topology templates
├── nodes/        # Node building blocks
└── edges/        # Edge linkers
```

The system automatically searches:
1. `inputs/` directory first
2. JSON databases in `data/` as fallback
3. Legacy root directories for backward compatibility

### Templates (Topologies)
Templates define the **network topology** of the MOF structure.

**Location:** `inputs/templates/` or `data/template_database.json`

**Common examples:**
- `pcu` - Primitive cubic
- `dia` - Diamond
- `acsh` - Augmented cubic
- `fcu` - Face-centered cubic
- `reo` - ReO3 topology

**How to find:** 
```python
import json
with open('data/template_database.json', 'r') as f:
    templates = json.load(f)
    print(list(templates.keys()))
```

### Nodes (Building Blocks)
Nodes are the **metal centers or organic vertices** in the MOF.

**Location:** `inputs/nodes/` or `data/nodes_database.json`

**Naming convention:** `{coordination}c_{metal}_{number}_{type}.cif`
- `12c_Ce_1_Ch` - 12-coordinate Cerium node
- `6c_Cu_1_Ch` - 6-coordinate Copper node
- `4c_Cd_1_Ch` - 4-coordinate Cadmium node

**How to find:**
```python
import json
with open('data/nodes_database.json', 'r') as f:
    nodes = json.load(f)
    print(list(nodes.keys()))
```

### Edges (Linkers)
Edges are the **organic linkers** connecting nodes.

**Location:** `inputs/edges/` or `data/edges_database.json`

**Common examples:**
- `1B_1TrU` - Benzene-based linker
- `btc_edge` - Benzene-1,3,5-tricarboxylate
- `bdc_edge` - Benzene-1,4-dicarboxylate

**How to find:**
```python
import json
with open('data/edges_database.json', 'r') as f:
    edges = json.load(f)
    print(list(edges.keys()))
```

---

## Code Examples

### Example 1: Basic Generation (New API)

```python
from src.api import generate_cif

# Generate a MOF structure (single string inputs now supported!)
result = generate_cif(
    template_name="acsh",
    node_names="12c_Ce_1_Ch",  # Single string (new!)
    edge_names="1B_1TrU"       # Single string (new!)
)

# File is automatically saved to output/cifs/
print(f"Generated: {result['cifname']}")
print(f"Saved to: {result['file_path']}")
```

### Example 2: Return as String (New Feature)

```python
from src.api import generate_cif

# Get CIF content as string instead of file
cif_string = generate_cif(
    template_name="pcu",
    node_names="6c_Cu_1_Ch",
    edge_names="btc_edge",
    return_format='string'  # New parameter!
)

# Process in memory
print(f"CIF content: {len(cif_string)} characters")
```

### Example 3: Return as JSON (New Feature)

```python
from src.api import generate_cif

# Get structured JSON with metadata
json_result = generate_cif(
    template_name="pcu",
    node_names="6c_Cu_1_Ch",
    edge_names="btc_edge",
    return_format='json'  # New parameter!
)

# Access structured data
mof_name = list(json_result.keys())[0]
metadata = json_result[mof_name]['metadata']
print(f"Atoms: {metadata['num_atoms']}")
```

### Example 4: Deterministic Charges (New Feature)

```python
from src.api import generate_cif

# Generate with specific random seed for reproducibility
result = generate_cif(
    template_name="pcu",
    node_names="6c_Cu_1_Ch",
    edge_names="btc_edge",
    random_seed=42  # New parameter!
)

# Same seed always produces same charges
print(f"Seed used: {result['metadata']['random_seed']}")
```

### Example 5: Multiple Inputs (Enhanced)

```python
from src.api import generate_cif

# Generate multiple MOFs with lists
results = generate_cif(
    template_name=["pcu", "dia"],  # Multiple templates
    node_names=["6c_Cu_1_Ch", "6c_Zn_1_Ch"],  # Multiple nodes
    edge_names="btc_edge"
)

# Results is a list of MOFs
print(f"Generated {len(results)} MOFs")
```

### Example 6: Batch Generation (New Function)

```python
from src.api import generate_multiple_mofs

# Define combinations
combinations = [
    {'template': 'pcu', 'nodes': '6c_Cu_1_Ch', 'edges': 'btc_edge'},
    {'template': 'dia', 'nodes': '4c_Zn_1_Ch', 'edges': 'bdc_edge'}
]

# Generate all at once
results = generate_multiple_mofs(combinations)
print(f"Generated {len(results)} MOFs")
```

### Example 7: With Custom Configuration

```python
from src.api import generate_cif

# Custom configuration
config = {
    "USER_SPECIFIED_NODE_ASSIGNMENT": False,  # Use only specified nodes (True) or all available (False)
    "SCALING_ITERATIONS": 5,                  # More optimization iterations
    "CHARGES": True,                          # Include atomic charges
    "BOND_TOL": 3.0,                         # Stricter bond tolerance
    "REMOVE_DUMMY_ATOMS": True,              # Remove dummy atoms
    "MIN_CELL_LENGTH": 10.0,                 # Minimum unit cell length (Å)
    "RANDOM_SEED": 42                        # Seed for reproducible charges
}

result = generate_cif(
    template_name="pcu",
    node_names="6c_Cu_1_Ch",
    edge_names="btc_edge",
    config=config
)
```

### Example 8: Vertex-Specific Node Assignment

```python
from src.api import generate_cif

# Assign specific nodes to specific vertex types
result = generate_cif(
    template_name="pcu",
    node_names={"V": "6c_Cu_1_Ch"},  # Dictionary mapping
    edge_names="btc_edge"
)
```

### Example 9: Access Metadata

```python
from src.api import generate_cif

result = generate_cif(
    template_name="acsh",
    node_names="12c_Ce_1_Ch",
    edge_names="1B_1TrU"
)

# Access metadata
metadata = result['metadata']
print(f"Generation time: {metadata['generation_time']:.2f}s")
print(f"Unit cell a: {metadata['unit_cell_params']['a']:.3f} Å")
print(f"Number of atoms: {metadata['num_atoms']}")
print(f"Random seed: {metadata['random_seed']}")
```

---

## New Features in ToBaCCo 3.0

### 1. Flexible Input Formats
- Single string inputs: `node_names="6c_Cu_1_Ch"`
- List inputs: `node_names=["6c_Cu_1_Ch", "6c_Zn_1_Ch"]`
- Dictionary inputs: `node_names={"V": "6c_Cu_1_Ch"}`

### 2. Multiple Return Formats
- `return_format='file'` - Save to disk (default)
- `return_format='string'` - Return as string
- `return_format='json'` - Return as JSON with metadata

### 3. Deterministic Charge Generation
- Use `random_seed` parameter for reproducibility
- Same seed → identical charges
- Seed recorded in metadata

### 4. Organized Input Directory
- Components in `inputs/` directory
- Automatic fallback to JSON databases
- Backward compatible with legacy structure

### 5. Enhanced Metadata
- Generation time
- Random seed used
- Unit cell parameters
- Atom and bond counts
- Bond check status

---

## Finding Components in JSON Databases

### Method 1: Using Python

```python
import json

# Load template database
with open('data/template_database.json', 'r') as f:
    templates = json.load(f)

# Search for templates containing "cu"
matching = [name for name in templates.keys() if 'cu' in name.lower()]
print(f"Templates with 'cu': {matching}")

# Check if specific template exists
if 'acsh.cif' in templates:
    print("acsh template found!")
```

### Method 2: Using Command Line

```bash
# List all templates
python -c "import json; print('\n'.join(json.load(open('data/template_database.json')).keys()))"

# Search for specific node
python -c "import json; nodes = json.load(open('data/nodes_database.json')); print([k for k in nodes if 'Ce' in k])"

# Count edges
python -c "import json; print(f'Total edges: {len(json.load(open(\"data/edges_database.json\")))}')"
```

### Method 3: Using the Example Script

```python
from examples.generate_mof_example import list_available_components

# This will print all available components
list_available_components()
```

---

## Troubleshooting

### Problem: Component not found

**Error:**
```
FileNotFoundError: Template 'acsh' not found
```

**Solution:**
1. Check if files exist in inputs/ directory:
   ```bash
   ls inputs/templates/
   ls inputs/nodes/
   ls inputs/edges/
   ```

2. If missing, check JSON databases:
   ```bash
   ls data/*.json
   ```

3. If JSON databases missing, export them:
   ```bash
   python scripts/export_databases_to_json.py
   ```

4. Verify component name (case-sensitive):
   ```python
   import json
   with open('data/template_database.json', 'r') as f:
       templates = json.load(f)
       print('acsh.cif' in templates)  # Should be True
   ```

### Problem: Generation fails

**Error:**
```
ValueError: Incompatible node and template
```

**Solution:**
- Check node coordination number matches template requirements
- Try different node/edge combinations
- Increase `BOND_TOL` in configuration

### Problem: Output file not created

**Solution:**
1. Check output directory exists (created automatically by new API)
2. Verify `WRITE_CIF = True` in configuration
3. Check for errors in console output

---

## Migration from Old API

### Old API (Pre-3.0)
```python
# Old: Required lists
result = generate_cif(
    template_name="pcu",
    node_names=["6c_Cu_1_Ch"],  # Required list
    edge_names=["btc_edge"]     # Required list
)

# Old: Manual file handling
with open(f"output/{result['cifname']}", 'w') as f:
    f.write(result['cif_content'])
```

### New API (3.0+)
```python
# New: Single strings supported
result = generate_cif(
    template_name="pcu",
    node_names="6c_Cu_1_Ch",  # Single string OK!
    edge_names="btc_edge"     # Single string OK!
)

# New: File automatically saved
print(f"Saved to: {result['file_path']}")
```

---

## Next Steps

1. **Explore Components:** Run `list_available_components()` to see what's available
2. **Try Examples:** Run the example scripts to understand the workflow
3. **Customize:** Modify configuration parameters for your needs
4. **Batch Process:** Generate multiple structures programmatically
5. **Reproducible Research:** Use random seeds for reproducible results
6. **Analyze:** Use the generated CIF files in molecular simulation software

---

## Additional Resources

- **Main Documentation:** `README.md`
- **Migration Guide:** `docs/MIGRATION_GUIDE.md`
- **API Documentation:** `docs/API_DOCUMENTATION.md`
- **Configuration Guide:** `CONFIGURATION_GUIDE.md`
- **Project Structure:** `PROJECT_STRUCTURE.md`
- **ToBaCCo Manual:** `docs/tobacco_3.0_manual.pdf`

---

**Questions?** Check the main README.md or the ToBaCCo manual in `docs/tobacco_3.0_manual.pdf`
