# Design Document: ToBaCCo 3.0 Refactoring

## Overview

This design document describes the architecture and implementation approach for refactoring the ToBaCCo 3.0 project. The refactoring will improve code organization, enhance the API, and add new features while preserving all existing algorithms and maintaining backward compatibility.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface Layer                     │
│  ┌──────────────────┐         ┌──────────────────────────┐ │
│  │  tobacco.py CLI  │         │  API (src/api.py)        │ │
│  │  (backward compat)│         │  (new programmatic API)  │ │
│  └──────────────────┘         └──────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Input Management Layer                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Input Loader (src/utils/input_loader.py)           │  │
│  │  - Load from inputs/ directory                       │  │
│  │  - Load from JSON databases                          │  │
│  │  - Validate inputs                                    │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Core Algorithm Layer                      │
│  (UNCHANGED - Preserve all existing algorithms)             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  src/core/                                           │  │
│  │  - ciftemplate2graph.py                              │  │
│  │  - vertex_edge_assign.py                             │  │
│  │  - cycle_cocyle.py                                   │  │
│  │  - SBU_geometry.py                                   │  │
│  │  - scale.py                                          │  │
│  │  - scaled_embedding2coords.py                        │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Output Management Layer                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Output Formatter (src/utils/output_formatter.py)   │  │
│  │  - Format as file                                    │  │
│  │  - Format as string                                  │  │
│  │  - Format as JSON                                    │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Directory Structure

```
tobacco_3.0/
├── inputs/                      # NEW: Organized input directory
│   ├── edges/                   # Moved from root
│   ├── nodes/                   # Moved from root
│   └── templates/               # Moved from root
├── src/
│   ├── api.py                   # ENHANCED: New features
│   ├── core/                    # UNCHANGED: Preserve algorithms
│   ├── utils/
│   │   ├── input_loader.py      # NEW: Input management
│   │   ├── output_formatter.py  # NEW: Output formatting
│   │   ├── charge_generator.py  # NEW: Deterministic charges
│   │   └── paths.py             # UPDATED: New paths
│   └── visualization/
├── data/                        # Existing JSON databases
├── output/                      # Existing output directory
├── tobacco.py                   # UNCHANGED: CLI interface
└── configuration.py             # ENHANCED: New options
```

## Components and Interfaces

### 1. Input Loader Module (`src/utils/input_loader.py`)

**Purpose:** Centralize input loading logic with support for multiple sources.

**Key Functions:**

```python
def load_building_blocks(names, block_type, source='auto'):
    """
    Load building blocks from JSON database or CIF files.
    
    Args:
        names: str, list, or dict of building block names
        block_type: 'node', 'edge', or 'template'
        source: 'json', 'cif', or 'auto' (try JSON first, fallback to CIF)
    
    Returns:
        dict: {name: cif_content}
    """
    pass

def validate_inputs(template_names, node_names, edge_names):
    """
    Validate that all required inputs exist and are compatible.
    
    Args:
        template_names: str or list of template names
        node_names: str, list, or dict of node names
        edge_names: str or list of edge names
    
    Returns:
        tuple: (valid, error_message)
    """
    pass

def normalize_input_format(input_data):
    """
    Convert single string or list to standardized format.
    
    Args:
        input_data: str, list, or dict
    
    Returns:
        list: Normalized list of names
    """
    pass
```

### 2. Output Formatter Module (`src/utils/output_formatter.py`)

**Purpose:** Provide flexible output formatting options.

**Key Functions:**

```python
def format_as_file(cif_content, filename, output_dir):
    """
    Save CIF content to file.
    
    Args:
        cif_content: str - CIF file content
        filename: str - Output filename
        output_dir: Path - Output directory
    
    Returns:
        Path: Path to saved file
    """
    pass

def format_as_string(cif_content, metadata=None):
    """
    Return CIF content as string with optional metadata.
    
    Args:
        cif_content: str - CIF file content
        metadata: dict - Optional metadata
    
    Returns:
        str or tuple: CIF content (and metadata if provided)
    """
    pass

def format_as_json(cif_results):
    """
    Format CIF results as JSON.
    
    Args:
        cif_results: list of dicts with 'cifname' and 'cif_content'
    
    Returns:
        dict: {"mof_name": "cif_content", ...}
    """
    pass

def format_results(results, return_format='file', output_dir=None):
    """
    Format results according to specified format.
    
    Args:
        results: list of result dicts
        return_format: 'file', 'string', or 'json'
        output_dir: Path - Output directory for files
    
    Returns:
        Formatted results according to return_format
    """
    pass
```

### 3. Charge Generator Module (`src/utils/charge_generator.py`)

**Purpose:** Generate deterministic atomic charges with seeded randomness.

**Key Functions:**

```python
def initialize_charge_generator(seed=None):
    """
    Initialize random number generator with seed.
    
    Args:
        seed: int or None - Random seed (None uses default)
    
    Returns:
        random.Random: Seeded random generator
    """
    pass

def generate_charge_adjustment(num_atoms, rng):
    """
    Generate charge adjustment using seeded RNG.
    
    Args:
        num_atoms: int - Number of atoms
        rng: random.Random - Seeded random generator
    
    Returns:
        int: Index of atom to adjust
    """
    pass
```

### 4. Enhanced API Module (`src/api.py`)

**Purpose:** Provide enhanced programmatic interface with new features.

**Key Functions:**

```python
def generate_cif(template_name, node_names, edge_names, 
                 config=None, return_format='file', random_seed=None):
    """
    Generate CIF file(s) from template, nodes, and edges.
    
    Args:
        template_name: str or list - Template name(s)
        node_names: str, list, or dict - Node name(s)
        edge_names: str or list - Edge name(s)
        config: dict - Configuration overrides
        return_format: str - 'file', 'string', or 'json'
        random_seed: int - Seed for deterministic charges
    
    Returns:
        Results in specified format
    """
    pass

def generate_multiple_mofs(combinations, config=None, 
                           return_format='file', random_seed=None):
    """
    Generate multiple MOFs from list of combinations.
    
    Args:
        combinations: list of dicts with 'template', 'nodes', 'edges'
        config: dict - Configuration overrides
        return_format: str - 'file', 'string', or 'json'
        random_seed: int - Seed for deterministic charges
    
    Returns:
        list: Results for all combinations
    """
    pass
```

### 5. Updated Paths Module (`src/utils/paths.py`)

**Purpose:** Update path management for new directory structure.

**Key Changes:**

```python
# NEW: Input directories
INPUTS_DIR = PROJECT_ROOT / "inputs"
TEMPLATES_DIR = INPUTS_DIR / "templates"
NODES_DIR = INPUTS_DIR / "nodes"
EDGES_DIR = INPUTS_DIR / "edges"

# BACKWARD COMPATIBILITY: Support old paths
LEGACY_TEMPLATES_DIR = PROJECT_ROOT / "templates"
LEGACY_NODES_DIR = PROJECT_ROOT / "nodes"
LEGACY_EDGES_DIR = PROJECT_ROOT / "edges"

def get_template_path(filename):
    """Get template path, checking new location first, then legacy."""
    pass

def get_node_path(filename):
    """Get node path, checking new location first, then legacy."""
    pass

def get_edge_path(filename):
    """Get edge path, checking new location first, then legacy."""
    pass
```

## Data Models

### Input Specification

```python
# Single inputs (strings)
template = "pcu"
node = "6c_Cu_1_Ch"
edge = "btc_edge"

# Multiple inputs (lists)
templates = ["pcu", "dia", "sod"]
nodes = ["6c_Cu_1_Ch", "4c_Zn_1_Ch"]
edges = ["btc_edge", "bdc_edge"]

# Node mapping (dict)
nodes = {
    "V1": "6c_Cu_1_Ch",
    "V2": "4c_Zn_1_Ch"
}
```

### Output Formats

```python
# File format (default)
result = {
    "cifname": "pcu_v1-6c_Cu_1_Ch_1-btc_edge.cif",
    "file_path": Path("output/cifs/pcu_v1-6c_Cu_1_Ch_1-btc_edge.cif"),
    "metadata": {...}
}

# String format
result = {
    "cifname": "pcu_v1-6c_Cu_1_Ch_1-btc_edge.cif",
    "cif_content": "data_pcu...",
    "metadata": {...}
}

# JSON format
result = {
    "pcu_v1-6c_Cu_1_Ch_1-btc_edge": {
        "cif_content": "data_pcu...",
        "metadata": {...}
    }
}
```

### Configuration Extensions

```python
# New configuration options in configuration.py
RANDOM_SEED = 42  # For deterministic charges
INPUT_SOURCE = 'auto'  # 'json', 'cif', or 'auto'
DEFAULT_RETURN_FORMAT = 'file'  # 'file', 'string', or 'json'
```

## Error Handling

### Input Validation Errors

```python
class InputValidationError(ValueError):
    """Raised when inputs are invalid or incompatible."""
    pass

class FileNotFoundError(Exception):
    """Raised when required input files are missing."""
    pass

class DatabaseError(Exception):
    """Raised when JSON database is corrupted or invalid."""
    pass
```

### Error Messages

- Clear, descriptive error messages in English
- Include suggestions for fixing the error
- Provide context about what was being attempted
- List available options when applicable

## Testing Strategy

### Unit Tests

- Test input loader with various input formats
- Test output formatter with all return formats
- Test charge generator for determinism
- Test path resolution with new and legacy paths
- Test API with single and multiple inputs

### Integration Tests

- Test complete MOF generation workflow
- Test backward compatibility with existing scripts
- Test JSON database loading with fallback to CIF
- Test deterministic charge generation across runs

### Property-Based Tests

Will be defined in the correctness properties section below.

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Input Format Normalization

*For any* valid input format (string, list, or dict), normalizing the input should produce a consistent list format that can be processed by the core algorithms.

**Validates: Requirements 2.1, 2.2, 2.3, 2.4**

### Property 2: Path Resolution Consistency

*For any* building block name, resolving its path should return the same file regardless of whether it's in the new `inputs/` directory or the legacy root directory.

**Validates: Requirements 1.5, 8.3**

### Property 3: Charge Determinism

*For any* MOF structure and random seed, generating charges twice with the same seed should produce identical charge values for all atoms.

**Validates: Requirements 4.1, 4.2, 4.3**

### Property 4: Algorithm Preservation

*For any* valid input combination, the generated MOF structure (excluding random charges) should be identical to the structure generated by the original implementation.

**Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.5, 5.6**

### Property 5: Output Format Equivalence

*For any* generated MOF, converting between output formats (file → string → JSON) should preserve the CIF content exactly.

**Validates: Requirements 3.1, 3.2, 3.3, 3.4**

### Property 6: Multiple Input Expansion

*For any* list of templates, nodes, and edges, the number of generated MOFs should equal the product of valid combinations (accounting for compatibility constraints).

**Validates: Requirements 2.5**

### Property 7: JSON Database Fallback

*For any* building block, if the JSON database is unavailable or corrupted, the system should successfully load the building block from CIF files.

**Validates: Requirements 9.4**

### Property 8: Backward Compatibility

*For any* existing ToBaCCo script or workflow, the refactored system should produce identical results when using the same configuration and inputs.

**Validates: Requirements 8.1, 8.2, 8.3, 8.4, 8.5, 8.6**

## Implementation Notes

### Critical Constraints

1. **DO NOT modify core algorithm files** in `src/core/` except for:
   - Import statement updates
   - Path resolution updates
   - Charge generator integration

2. **Preserve all numerical calculations** exactly as implemented

3. **Maintain charge neutrality** using the same algorithm

4. **Keep random seed separate** from other randomization

### Migration Strategy

1. Create new modules (`input_loader.py`, `output_formatter.py`, `charge_generator.py`)
2. Update `paths.py` with new directory structure and backward compatibility
3. Enhance `api.py` with new features
4. Update `configuration.py` with new options
5. Create `inputs/` directory structure
6. Update documentation
7. Run comprehensive tests to verify preservation

### Performance Considerations

- JSON database loading should be faster than CIF file reading
- Caching loaded building blocks to avoid repeated file I/O
- Lazy loading of databases (only load when needed)

## Documentation Requirements

All documentation must be in English:

- Module docstrings
- Function docstrings
- Inline comments
- Error messages
- User guides
- API documentation
- Migration guides

---

**Design Version:** 1.0  
**Last Updated:** December 28, 2024
