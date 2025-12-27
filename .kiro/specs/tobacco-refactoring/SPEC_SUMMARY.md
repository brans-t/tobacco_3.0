# ToBaCCo 3.0 Refactoring Specification Summary

## Overview

This specification defines a comprehensive refactoring of the ToBaCCo 3.0 (Topologically Based Crystal Constructor) project to improve organization, enhance the API, and add new features while maintaining full backward compatibility and preserving all existing algorithms.

## Specification Files

1. **requirements.md** - Detailed requirements with acceptance criteria
2. **design.md** - Architecture, components, and correctness properties
3. **tasks.md** - Implementation task list with requirements traceability
4. **SPEC_SUMMARY.md** - This summary document

## Key Requirements

### 1. Input File Organization (Requirement 1)
- Create `inputs/` directory structure
- Move `edges/`, `nodes/`, `templates/` to `inputs/`
- Maintain backward compatibility with legacy locations

### 2. Enhanced API (Requirement 2)
- Support single string inputs: `"pcu"`, `"6c_Cu_1_Ch"`, `"btc_edge"`
- Support list inputs: `["pcu", "dia"]`, `["6c_Cu_1_Ch", "4c_Zn_1_Ch"]`
- Support dict inputs for nodes: `{"V1": "6c_Cu_1_Ch", "V2": "4c_Zn_1_Ch"}`
- Generate all valid combinations for multiple inputs
- Read from JSON databases with CIF fallback

### 3. Flexible Output Formats (Requirement 3)
- **File format** (default): Save to `output/cifs/` and return path
- **String format**: Return CIF content as string
- **JSON format**: Return as `{"mof_name": "cif_content", ...}` with metadata

### 4. Deterministic Charges (Requirement 4)
- Use seeded random number generator
- Same inputs + same seed = identical charges
- Configurable seed value
- Document seed in metadata

### 5. Algorithm Preservation (Requirement 5)
- **CRITICAL**: Do NOT modify core algorithm logic
- Preserve all numerical calculations
- Maintain identical structure generation (excluding random charges)
- Pass all validation tests

### 6. Project Structure (Requirement 6)
- Follow Python best practices
- Clear module organization
- Comprehensive English documentation
- Avoid excessive complexity

### 7. Backward Compatibility (Requirement 8)
- Maintain `tobacco.py` CLI interface
- Support existing `configuration.py` format
- Support legacy directory structure as fallback
- Produce identical output formats

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface Layer                     │
│  ┌──────────────────┐         ┌──────────────────────────┐ │
│  │  tobacco.py CLI  │         │  API (src/api.py)        │ │
│  └──────────────────┘         └──────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Input Management Layer                    │
│  - input_loader.py: Load from JSON/CIF, validate, normalize │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Core Algorithm Layer                      │
│  (UNCHANGED - Preserve all existing algorithms)             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Output Management Layer                   │
│  - output_formatter.py: Format as file/string/JSON          │
│  - charge_generator.py: Deterministic charge generation     │
└─────────────────────────────────────────────────────────────┘
```

## New Modules

### 1. `src/utils/input_loader.py`
- `load_building_blocks()` - Load from JSON/CIF with auto fallback
- `validate_inputs()` - Validate existence and compatibility
- `normalize_input_format()` - Convert string/list/dict to standard format

### 2. `src/utils/output_formatter.py`
- `format_as_file()` - Save to file and return path
- `format_as_string()` - Return CIF content as string
- `format_as_json()` - Return structured JSON with metadata
- `format_results()` - Dispatch to appropriate formatter

### 3. `src/utils/charge_generator.py`
- `initialize_charge_generator()` - Create seeded RNG
- `generate_charge_adjustment()` - Deterministic charge selection

### 4. Enhanced `src/api.py`
- Updated `generate_cif()` with new parameters:
  - `return_format='file'` - Choose output format
  - `random_seed=None` - Seed for deterministic charges
- New `generate_multiple_mofs()` - Batch generation

### 5. Updated `src/utils/paths.py`
- New `INPUTS_DIR` paths
- Backward compatibility for legacy paths
- Path resolution with fallback

## Correctness Properties

8 properties defined for property-based testing:

1. **Input Format Normalization** - All formats normalize consistently
2. **Path Resolution Consistency** - Same file from new or legacy location
3. **Charge Determinism** - Same seed produces identical charges
4. **Algorithm Preservation** - Identical structures (excluding random charges)
5. **Output Format Equivalence** - Converting formats preserves content
6. **Multiple Input Expansion** - Correct number of combinations generated
7. **JSON Database Fallback** - Loads from CIF when JSON unavailable
8. **Backward Compatibility** - Existing workflows produce identical results

## Implementation Tasks

11 main tasks with 8 property-based test sub-tasks:

1. Create input directory structure (1 property test)
2. Create input loader module (2 property tests)
3. Create output formatter module (1 property test)
4. Create charge generator module (1 property test)
5. Enhance API module (1 property test)
6. Update configuration module
7. Checkpoint - verify tests pass
8. Update documentation (all in English)
9. Create example scripts
10. Verify algorithm preservation (2 property tests)
11. Final checkpoint

## Critical Constraints

### DO NOT MODIFY
- Core algorithm files in `src/core/` (except imports and path updates)
- Numerical calculations
- Charge neutrality algorithm
- Unit cell scaling logic
- Bond formation logic
- Coordinate calculation methods

### MUST PRESERVE
- Identical MOF structures for identical inputs (excluding random charges)
- Same unit cell parameters
- Same atom positions
- Same bond connectivity
- Same symmetry tolerance handling

## Usage Examples

### Single Input (Current)
```python
from src import generate_cif

result = generate_cif(
    template_name="pcu",
    node_names=["6c_Cu_1_Ch"],
    edge_names=["btc_edge"]
)
```

### Multiple Inputs (New)
```python
result = generate_cif(
    template_name=["pcu", "dia"],
    node_names=["6c_Cu_1_Ch", "4c_Zn_1_Ch"],
    edge_names=["btc_edge", "bdc_edge"]
)
# Generates all valid combinations
```

### JSON Return Format (New)
```python
result = generate_cif(
    template_name="pcu",
    node_names=["6c_Cu_1_Ch"],
    edge_names=["btc_edge"],
    return_format="json"
)
# Returns: {"mof_name": "cif_content", "metadata": {...}}
```

### Deterministic Charges (New)
```python
result = generate_cif(
    template_name="pcu",
    node_names=["6c_Cu_1_Ch"],
    edge_names=["btc_edge"],
    random_seed=42
)
# Same seed always produces same charges
```

## Configuration Extensions

New options in `configuration.py`:

```python
RANDOM_SEED = 42  # For deterministic charges
INPUT_SOURCE = 'auto'  # 'json', 'cif', or 'auto'
DEFAULT_RETURN_FORMAT = 'file'  # 'file', 'string', or 'json'
```

## Migration Path

### For Existing Users
1. No changes required - full backward compatibility
2. Optional: Move files to `inputs/` directory
3. Optional: Use new API features

### For Developers
1. Import new modules: `from src.utils.input_loader import load_building_blocks`
2. Use enhanced API: `generate_cif(..., return_format='json')`
3. Set random seed: `generate_cif(..., random_seed=42)`

## Testing Strategy

### Unit Tests
- Input loader with various formats
- Output formatter with all return formats
- Charge generator for determinism
- Path resolution with new and legacy paths
- API with single and multiple inputs

### Property-Based Tests (8 required)
- All 8 correctness properties must pass
- Minimum 100 iterations per property test
- Each test references design document property

### Integration Tests
- Complete MOF generation workflow
- Backward compatibility with existing scripts
- JSON database loading with CIF fallback
- Deterministic charge generation across runs

## Success Criteria

✅ All 10 requirements fully implemented  
✅ All 8 correctness properties validated  
✅ All 11 implementation tasks completed  
✅ Core algorithms unchanged and verified  
✅ Backward compatibility maintained  
✅ All documentation in English  
✅ All tests passing  

## Next Steps

1. Review and approve this specification
2. Begin implementation following task list
3. Execute tasks incrementally with testing
4. Verify algorithm preservation at checkpoints
5. Complete documentation and examples
6. Final validation and release

---

**Specification Version:** 1.0  
**Created:** December 28, 2024  
**Status:** Ready for Implementation
