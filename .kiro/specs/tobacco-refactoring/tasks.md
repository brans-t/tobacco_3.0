# Implementation Plan: ToBaCCo 3.0 Refactoring

## Overview

This implementation plan breaks down the ToBaCCo refactoring into discrete, manageable tasks. Each task builds on previous tasks and includes specific requirements references.

## Tasks

- [x] 1. Create input directory structure and update path management
  - Create `inputs/` directory with subdirectories for edges, nodes, templates
  - Update `src/utils/paths.py` to support new directory structure
  - Add backward compatibility for legacy directory locations
  - Add path resolution functions that check new location first, then legacy
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7_

- [x] 1.1 Write property test for path resolution consistency
  - **Property 2: Path Resolution Consistency**
  - **Validates: Requirements 1.5, 8.3**
  - Test that path resolution returns same file from new or legacy location
  - _Requirements: 1.5, 8.3_

- [x] 2. Create input loader module
  - [x] 2.1 Implement `load_building_blocks()` function
    - Support loading from JSON databases
    - Support loading from CIF files
    - Implement 'auto' mode (try JSON first, fallback to CIF)
    - Handle single string, list, and dict input formats
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.7, 9.1, 9.2, 9.3, 9.4_

  - [x] 2.2 Implement `validate_inputs()` function
    - Check that all required files exist
    - Validate compatibility between templates, nodes, and edges
    - Return clear error messages for invalid inputs
    - _Requirements: 2.8, 2.9_

  - [x] 2.3 Implement `normalize_input_format()` function
    - Convert single string to list
    - Convert dict to list
    - Preserve list format
    - _Requirements: 2.1, 2.2, 2.3, 2.4_

- [x] 2.4 Write property test for input format normalization
  - **Property 1: Input Format Normalization**
  - **Validates: Requirements 2.1, 2.2, 2.3, 2.4**
  - Test that all input formats normalize to consistent list format
  - _Requirements: 2.1, 2.2, 2.3, 2.4_

- [x] 2.5 Write property test for JSON database fallback
  - **Property 7: JSON Database Fallback**
  - **Validates: Requirements 9.4**
  - Test that system loads from CIF when JSON unavailable
  - _Requirements: 9.4_

- [x] 3. Create output formatter module
  - [x] 3.1 Implement `format_as_file()` function
    - Save CIF content to file in output directory
    - Return file path
    - _Requirements: 3.6, 10.2_

  - [x] 3.2 Implement `format_as_string()` function
    - Return CIF content as string
    - Optionally include metadata
    - _Requirements: 3.1, 10.3_

  - [x] 3.3 Implement `format_as_json()` function
    - Format CIF results as JSON object
    - Use format: {"mof_name": "cif_content"}
    - Include metadata in JSON structure
    - _Requirements: 3.2, 3.3, 3.4, 3.5, 10.4_

  - [x] 3.4 Implement `format_results()` function
    - Dispatch to appropriate formatter based on return_format
    - Validate return_format parameter
    - Support multiple return formats simultaneously
    - _Requirements: 3.7, 10.1, 10.5, 10.6, 10.7_

- [x] 3.5 Write property test for output format equivalence
  - **Property 5: Output Format Equivalence**
  - **Validates: Requirements 3.1, 3.2, 3.3, 3.4**
  - Test that converting between formats preserves CIF content
  - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [x] 4. Create charge generator module
  - [x] 4.1 Implement `initialize_charge_generator()` function
    - Create seeded random number generator
    - Use default seed if none provided
    - Document seed value
    - _Requirements: 4.1, 4.3, 4.4, 4.5_

  - [x] 4.2 Implement `generate_charge_adjustment()` function
    - Use seeded RNG to select atom for charge adjustment
    - Maintain charge neutrality algorithm
    - Preserve original charge assignment logic
    - _Requirements: 4.2, 4.6, 4.7_

  - [x] 4.3 Integrate charge generator into MOF generation workflow
    - Update `src/utils/remove_net_charge.py` to use seeded RNG
    - Pass random seed through generation pipeline
    - Ensure seed is documented in metadata
    - _Requirements: 4.1, 4.2, 4.5_

- [x] 4.4 Write property test for charge determinism
  - **Property 3: Charge Determinism**
  - **Validates: Requirements 4.1, 4.2, 4.3**
  - Test that same seed produces identical charges
  - _Requirements: 4.1, 4.2, 4.3_

- [x] 5. Enhance API module
  - [x] 5.1 Update `generate_cif()` function signature
    - Add `return_format` parameter (default='file')
    - Add `random_seed` parameter (default=None)
    - Support single string inputs for template, nodes, edges
    - Support list inputs for template, nodes, edges
    - Support dict input for nodes (vertex type mapping)
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 10.1, 10.2, 10.3, 10.4, 10.5_

  - [x] 5.2 Implement multiple input handling in `generate_cif()`
    - Use input_loader to normalize inputs
    - Generate all valid combinations
    - Validate inputs before generation
    - _Requirements: 2.5, 2.8, 2.9_

  - [x] 5.3 Integrate output formatter into `generate_cif()`
    - Use output_formatter to format results
    - Support all three return formats
    - Maintain backward compatibility (default to file)
    - _Requirements: 3.6, 3.7, 10.1, 10.2, 10.3, 10.4, 10.5_

  - [x] 5.4 Integrate charge generator into `generate_cif()`
    - Initialize charge generator with provided seed
    - Pass seeded RNG through generation pipeline
    - Document seed in output metadata
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

  - [x] 5.5 Implement `generate_multiple_mofs()` function
    - Accept list of combinations
    - Generate MOFs for all combinations
    - Return results in specified format
    - _Requirements: 2.5_

- [x] 5.6 Write property test for multiple input expansion
  - **Property 6: Multiple Input Expansion**
  - **Validates: Requirements 2.5**
  - Test that number of MOFs equals product of valid combinations
  - _Requirements: 2.5_

- [x] 6. Update configuration module
  - Add `RANDOM_SEED` configuration option (default=42)
  - Add `INPUT_SOURCE` configuration option (default='auto')
  - Add `DEFAULT_RETURN_FORMAT` configuration option (default='file')
  - Document all new configuration options in English
  - _Requirements: 4.3, 4.4, 9.1, 9.2, 9.3, 10.5, 7.6_

- [x] 7. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 8. Update documentation
  - [x] 8.1 Update README.md
    - Document new `inputs/` directory structure
    - Document new API features (multiple inputs, return formats)
    - Document deterministic charge generation
    - Provide migration guide from old structure
    - All documentation in English
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 2.3, 2.4, 2.5, 3.1, 3.2, 3.3, 4.1, 4.2, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6_

  - [x] 8.2 Update API documentation
    - Document `generate_cif()` new parameters
    - Document `generate_multiple_mofs()` function
    - Provide usage examples for all features
    - Document return format options
    - All documentation in English
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 3.1, 3.2, 3.3, 3.7, 10.1, 10.2, 10.3, 10.4, 7.5_

  - [x] 8.3 Create migration guide
    - Document changes from original structure
    - Provide step-by-step migration instructions
    - Include examples of old vs new usage
    - All documentation in English
    - _Requirements: 8.7, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6_

  - [x] 8.4 Update configuration documentation
    - Document new configuration options
    - Explain default values and their effects
    - All documentation in English
    - _Requirements: 4.3, 4.4, 9.1, 9.2, 9.3, 10.5, 7.6_

- [x] 9. Create example scripts
  - [x] 9.1 Create example for single input generation
    - Demonstrate basic usage with single template, node, edge
    - Show all three return formats
    - _Requirements: 2.1, 3.1, 3.2, 3.3_

  - [x] 9.2 Create example for multiple input generation
    - Demonstrate usage with lists of templates, nodes, edges
    - Show batch generation
    - _Requirements: 2.2, 2.3, 2.4, 2.5_

  - [x] 9.3 Create example for deterministic charge generation
    - Demonstrate reproducible results with random seed
    - Show that same seed produces identical charges
    - _Requirements: 4.1, 4.2, 4.3_

  - [x] 9.4 Update existing examples
    - Ensure all examples work with new structure
    - Update paths to use `inputs/` directory
    - All comments and documentation in English
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 7.1, 7.2, 7.3_

- [x] 10. Verify algorithm preservation
  - [x] 10.1 Run comparison tests
    - Generate test MOFs with original code
    - Generate same MOFs with refactored code
    - Compare structures (excluding random charges)
    - Verify unit cell parameters match
    - Verify atom positions match
    - Verify bond connectivity matches
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6_

  - [x] 10.2 Run backward compatibility tests
    - Test existing scripts with refactored code
    - Verify CLI interface unchanged
    - Verify configuration file format unchanged
    - Verify output file format unchanged
    - Verify output file naming unchanged
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.6_

- [x] 10.3 Write property test for algorithm preservation
  - **Property 4: Algorithm Preservation**
  - **Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.5, 5.6**
  - Test that generated structures match original implementation
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6_

- [x] 10.4 Write property test for backward compatibility
  - **Property 8: Backward Compatibility**
  - **Validates: Requirements 8.1, 8.2, 8.3, 8.4, 8.5, 8.6**
  - Test that existing workflows produce identical results
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.6_

- [x] 11. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- All property-based tests are required for comprehensive validation
- Core algorithm files in `src/core/` should NOT be modified except for:
  - Import statement updates
  - Path resolution updates
  - Charge generator integration
- All new code must include English documentation
- Maintain backward compatibility throughout
- Test after each major task completion

