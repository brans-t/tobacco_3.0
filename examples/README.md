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
3. Save the output

**Example output:**
```
Template: acsh
Node:     12c_Ce_1_Ch
Edge:     1B_1TrU

✓ Success!
   Generated: acsh_12c_Ce_1_Ch_1B_1TrU.cif
   Saved to:  output/cifs/acsh_12c_Ce_1_Ch_1B_1TrU.cif
```

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

### Templates (Topologies)
Templates define the **network topology** of the MOF structure.

**Location:** `data/template_database.json`

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

**Location:** `data/nodes_database.json`

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

**Location:** `data/edges_database.json`

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

### Example 1: Basic Generation

```python
from src import generate_cif

# Generate a MOF structure
result = generate_cif(
    template_name="acsh",
    node_names=["12c_Ce_1_Ch"],
    edge_names=["1B_1TrU"]
)

# Save to file
with open(f"output/{result['cifname']}", 'w') as f:
    f.write(result['cif_content'])

print(f"Generated: {result['cifname']}")
```

### Example 2: With Custom Configuration

```python
from src import generate_cif

# Custom configuration
config = {
    "CHARGES": True,           # Include atomic charges
    "SCALING_ITERATIONS": 5,   # More optimization iterations
    "BOND_TOL": 3.0,          # Stricter bond tolerance
    "REMOVE_DUMMY_ATOMS": True # Remove dummy atoms
}

result = generate_cif(
    template_name="pcu",
    node_names=["6c_Cu_1_Ch"],
    edge_names=["btc_edge"],
    config=config
)
```

### Example 3: Multiple Edge Types

```python
from src import generate_cif

# Use multiple edge types (combinatorial)
config = {"COMBINATORIAL_EDGE_ASSIGNMENT": True}

results = generate_cif(
    template_name="pcu",
    node_names=["6c_Cu_1_Ch"],
    edge_names=["btc_edge", "bdc_edge"],
    config=config
)

# Results is a list of structures
for i, result in enumerate(results):
    print(f"Structure {i+1}: {result['cifname']}")
```

### Example 4: Vertex-Specific Node Assignment

```python
from src import generate_cif

# Assign specific nodes to specific vertex types
result = generate_cif(
    template_name="pcu",
    node_names={"V": "6c_Cu_1_Ch"},  # Dictionary mapping
    edge_names=["btc_edge"]
)
```

### Example 5: Access Metadata

```python
from src import generate_cif

result = generate_cif(
    template_name="acsh",
    node_names=["12c_Ce_1_Ch"],
    edge_names=["1B_1TrU"]
)

# Access metadata
metadata = result['metadata']
print(f"Generation time: {metadata['generation_time']:.2f}s")
print(f"Unit cell a: {metadata['unit_cell_params']['a']:.3f} Å")
print(f"Number of atoms: {metadata['num_atoms']}")
```

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
1. Check if JSON databases exist:
   ```bash
   ls data/*.json
   ```

2. If missing, export databases:
   ```bash
   python scripts/export_databases_to_json.py
   ```

3. Verify component name (case-sensitive):
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
1. Check output directory exists:
   ```python
   from pathlib import Path
   Path("output/cifs").mkdir(parents=True, exist_ok=True)
   ```

2. Verify `WRITE_CIF = True` in configuration

3. Check for errors in console output

---

## Next Steps

1. **Explore Components:** Run `list_available_components()` to see what's available
2. **Try Examples:** Run the example scripts to understand the workflow
3. **Customize:** Modify configuration parameters for your needs
4. **Batch Process:** Generate multiple structures programmatically
5. **Analyze:** Use the generated CIF files in molecular simulation software

---

## Additional Resources

- **Main Documentation:** `README.md`
- **Configuration Guide:** `CONFIGURATION_GUIDE.md`
- **Project Structure:** `PROJECT_STRUCTURE.md`
- **API Documentation:** See docstrings in `src/api.py`
- **Scripts Documentation:** `scripts/README.md`

---

**Questions?** Check the main README.md or the ToBaCCo manual in `docs/tobacco_3.0_manual.pdf`
