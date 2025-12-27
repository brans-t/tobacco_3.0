# ToBaCCo 3.0 Project Structure

## Overview

This document describes the organized structure of the ToBaCCo 3.0 project after refactoring.

## Directory Structure

```
tobacco_3.0/
├── src/                          # Source code package
│   ├── __init__.py              # Package initialization, exports API
│   ├── api.py                   # Public API interface
│   ├── core/                    # Core algorithm modules
│   │   ├── __init__.py
│   │   ├── ciftemplate2graph.py
│   │   ├── vertex_edge_assign.py
│   │   ├── cycle_cocyle.py
│   │   ├── SBU_geometry.py
│   │   ├── scale.py
│   │   └── scaled_embedding2coords.py
│   ├── utils/                   # Utility modules
│   │   ├── __init__.py
│   │   ├── paths.py            # Path management
│   │   ├── cif_tools.py        # CIF file utilities (NEW)
│   │   ├── svd_alignment.py    # SVD superimposer (moved from Bio.py)
│   │   ├── bbcif_properties.py
│   │   ├── place_bbs.py
│   │   ├── remove_net_charge.py
│   │   ├── remove_dummy_atoms.py
│   │   ├── adjust_edges.py
│   │   └── write_cifs.py
│   └── visualization/           # Visualization modules
│       ├── __init__.py
│       └── scale_animation.py
├── scripts/                     # Utility scripts (NEW)
│   ├── README.md               # Scripts documentation
│   ├── export_databases_to_json.py
│   ├── reindex_building_blocks.py
│   ├── make_topologies.py
│   ├── topo_pore_analysis.py
│   └── scrape_rcsr.py
├── data/                        # Database files
│   ├── edges_database/
│   ├── nodes_database/
│   ├── template_database/
│   ├── template_2D_database/
│   ├── edges_database.json
│   ├── nodes_database.json
│   └── template_database.json
├── output/                      # Generated output files
│   ├── cifs/                    # Generated CIF files
│   └── check_cifs/              # Check files
├── docs/                        # Documentation
│   ├── tobacco_3.0_manual.pdf
│   ├── tobacco_3.0_manual.docx
│   └── RCSRnets-2019-06-01.cgd
├── templates/                   # Working template directory
├── nodes/                       # Working nodes directory
├── edges/                       # Working edges directory
├── tests/                       # Unit tests
│   ├── test_api.py
│   ├── test_paths.py
│   └── test_database_export.py
├── tobacco.py                   # Main entry point (CLI)
├── configuration.py             # Configuration file
├── vertex_assignment.txt        # Vertex assignment config
├── README.md                    # Project documentation
├── CHANGES.md                   # Refactoring changes
├── LICENSE                      # License file
└── requirements.txt             # Python dependencies
```

## Key Changes from Original Structure

### 1. Created `scripts/` Directory
**Purpose:** Organize utility scripts separate from core functionality

**Moved files:**
- `export_databases_to_json.py` → `scripts/`
- `make_topologies.py` → `scripts/`
- `scrape_rcsr.py` → `scripts/`
- `topo_pore_analysis.py` → `scripts/`
- `reindex_bb_cifs.py` → `scripts/reindex_building_blocks.py`

**Benefits:**
- Cleaner main directory
- Clear separation between core code and utility scripts
- Easier to find and use utility tools

### 2. Created `src/utils/cif_tools.py`
**Purpose:** Centralize CIF file manipulation utilities

**Consolidated from:**
- `reindex.py` - Reindexing functions
- `reindex_bb_cifs.py` - Building block reindexing

**Functions:**
- `isfloat()` - Check if value is float
- `iscoord()` - Identify coordinate lines
- `isbond()` - Identify bond lines
- `reindex_cif()` - Reindex CIF file atoms
- `nn()` - Remove non-alphabetic characters
- `nl()` - Remove non-numeric characters

**Benefits:**
- Reusable CIF utilities
- Consistent API for CIF operations
- Part of the main package (importable)

### 3. Moved `Bio.py` to `src/utils/svd_alignment.py`
**Purpose:** Integrate SVD alignment utility into the package structure

**What it does:**
- SVD (Singular Value Decomposition) superimposer from Biopython
- Aligns two sets of 3D points by finding optimal rotation and translation
- Used by `place_bbs.py` for building block placement

**Benefits:**
- Consistent with package structure
- Clear module naming
- Part of the utils package

### 4. Removed Duplicate/Temporary Files
**Deleted:**
- `test_api_checkpoint.py`
- `test_backward_compatibility.py`
- `test_cif_equivalence.py`
- `test_path_resolution.py`
- `test_tobacco_execution.py`
- `verify_module_structure.py`
- `MODULE_STRUCTURE_VERIFICATION.md`
- `TASK_10_COMPLETION_SUMMARY.md`
- `scale_animation.py` (duplicate, already in src/visualization/)

**Benefits:**
- Cleaner main directory
- No confusion from duplicate files
- Test files properly organized in `tests/` directory

### 5. Removed `output_cifs/` Directory
**Consolidated into:** `output/cifs/`

**Benefits:**
- Single output directory structure
- Consistent with refactored path management
- Less confusion about where outputs go

## File Organization Principles

### Main Directory
**Contains only:**
- Entry points (`tobacco.py`)
- Configuration (`configuration.py`)
- Core utilities (`Bio.py`)
- Documentation (`README.md`, `CHANGES.md`, `LICENSE`)
- Dependencies (`requirements.txt`)
- Config files (`vertex_assignment.txt`)

### `src/` Package
**Contains:**
- Core algorithms (`src/core/`)
- Utility functions (`src/utils/`)
- Visualization tools (`src/visualization/`)
- Public API (`src/api.py`)

### `scripts/` Directory
**Contains:**
- Database management scripts
- Data collection tools
- Analysis utilities
- One-off processing scripts

### `data/` Directory
**Contains:**
- Database directories
- JSON exports
- Input data files

### `output/` Directory
**Contains:**
- Generated CIF files
- Check files
- Temporary outputs

## Usage Patterns

### For End Users
```bash
# Run ToBaCCo interactively
python tobacco.py

# Export databases to JSON
python scripts/export_databases_to_json.py
```

### For Developers
```python
# Use the API
from src import generate_cif

result = generate_cif(
    template_name="pcu",
    node_names=["6c_Cu_1_Ch"],
    edge_names=["btc_edge"]
)
```

### For Database Management
```bash
# Reindex building blocks
python scripts/reindex_building_blocks.py

# Generate topologies
python scripts/make_topologies.py

# Analyze pores
python scripts/topo_pore_analysis.py
```

## Benefits of New Structure

1. **Cleaner Main Directory**
   - Only essential files visible
   - Easy to understand project layout
   - Professional appearance

2. **Better Organization**
   - Clear separation of concerns
   - Logical grouping of related files
   - Easier navigation

3. **Improved Maintainability**
   - Utilities are reusable
   - Scripts are self-contained
   - Clear dependencies

4. **Enhanced Usability**
   - Scripts have clear documentation
   - Consistent command-line interface
   - Easy to find tools

5. **Professional Structure**
   - Follows Python best practices
   - Similar to other scientific software
   - Ready for distribution

## Migration Notes

### For Existing Users
- All original functionality preserved
- `tobacco.py` works exactly as before
- No changes to command-line interface

### For Script Users
- Update script paths: `python export_databases_to_json.py` → `python scripts/export_databases_to_json.py`
- All scripts now in `scripts/` directory
- See `scripts/README.md` for usage

### For Developers
- Import CIF utilities: `from src.utils.cif_tools import reindex_cif`
- All utilities now in `src/utils/`
- See module docstrings for API

## Future Improvements

Potential future enhancements:
1. Move `Bio.py` to `src/utils/svd_alignment.py`
2. Create `scripts/__init__.py` for script imports
3. Add more comprehensive script documentation
4. Create a CLI wrapper for common scripts
5. Add configuration file for scripts

---

**Last Updated:** December 27, 2024
**Version:** 3.0
