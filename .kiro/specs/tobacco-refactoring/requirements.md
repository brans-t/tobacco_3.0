# Requirements Document: ToBaCCo 3.0 Refactoring

## Introduction

This document specifies the requirements for refactoring the ToBaCCo 3.0 (Topologically Based Crystal Constructor) project. The refactoring aims to improve project organization, enhance the API, and add new features while maintaining full backward compatibility with existing algorithms and functionality.

## Glossary

- **MOF**: Metal-Organic Framework - A porous crystalline material
- **CIF**: Crystallographic Information File - Standard file format for crystal structures
- **Template**: Topological network structure defining connectivity
- **Node**: Building block representing vertices in the network
- **Edge**: Building block representing connections between nodes
- **SBU**: Secondary Building Unit - Molecular building block
- **ToBaCCo**: Topologically Based Crystal Constructor - The software system
- **API**: Application Programming Interface
- **JSON**: JavaScript Object Notation - Data interchange format
- **Database**: Collection of CIF files (nodes, edges, or templates)
- **Charge**: Atomic partial charge for molecular simulation

## Requirements

### Requirement 1: Input File Organization

**User Story:** As a user, I want input files organized in a dedicated directory, so that I can easily manage and locate building blocks and templates.

#### Acceptance Criteria

1. THE System SHALL create an `inputs/` directory in the project root
2. THE System SHALL move the `edges/` directory to `inputs/edges/`
3. THE System SHALL move the `nodes/` directory to `inputs/nodes/`
4. THE System SHALL move the `templates/` directory to `inputs/templates/`
5. THE System SHALL update all path references to use the new `inputs/` directory structure
6. WHEN the system starts, THE System SHALL verify that input directories exist
7. THE System SHALL maintain backward compatibility by supporting both old and new directory structures

### Requirement 2: Enhanced API for MOF Generation

**User Story:** As a developer, I want to generate MOFs programmatically with flexible input options, so that I can integrate ToBaCCo into automated workflows.

#### Acceptance Criteria

1. THE System SHALL accept single node/edge/template inputs as strings
2. THE System SHALL accept multiple nodes as a list of strings
3. THE System SHALL accept multiple edges as a list of strings
4. THE System SHALL accept multiple templates as a list of strings
5. WHEN multiple inputs are provided, THE System SHALL generate MOFs for all valid combinations
6. THE System SHALL read building blocks from JSON database files when available
7. THE System SHALL fall back to reading CIF files from `inputs/` directories when JSON is unavailable
8. THE System SHALL validate all inputs before generation
9. THE System SHALL provide clear error messages for invalid inputs

### Requirement 3: CIF Content Return Format

**User Story:** As a developer, I want to retrieve generated CIF content in multiple formats, so that I can process results without file I/O.

#### Acceptance Criteria

1. THE System SHALL provide a function to return CIF content as a string
2. THE System SHALL provide a function to return CIF content as JSON
3. WHEN returning JSON, THE System SHALL use the format: `{"mof_name": "cif_content_string"}`
4. WHEN multiple MOFs are generated, THE System SHALL return a JSON object with multiple entries
5. THE System SHALL include metadata in JSON returns (generation time, parameters, unit cell)
6. THE System SHALL still save CIF files to `output/cifs/` by default
7. THE System SHALL allow users to choose between file output, string return, or JSON return
8. THE System SHALL provide a function to convert between return formats

### Requirement 4: Deterministic Charge Generation

**User Story:** As a researcher, I want identical inputs to produce identical charges, so that I can reproduce simulation results.

#### Acceptance Criteria

1. THE System SHALL use a seeded random number generator for charge assignment
2. WHEN the same inputs are provided, THE System SHALL generate identical atomic charges
3. THE System SHALL allow users to specify a random seed in configuration
4. THE System SHALL use a default seed value when none is specified
5. THE System SHALL document the seed value in output metadata
6. THE System SHALL maintain charge neutrality as in the original implementation
7. THE System SHALL preserve the original charge assignment algorithm logic

### Requirement 5: Algorithm Preservation

**User Story:** As a user, I want the refactored code to produce identical results, so that I can trust the refactored version.

#### Acceptance Criteria

1. THE System SHALL preserve all core algorithm implementations without modification
2. THE System SHALL produce identical MOF structures for identical inputs (excluding random charges)
3. THE System SHALL maintain the same unit cell scaling behavior
4. THE System SHALL maintain the same bond formation logic
5. THE System SHALL maintain the same coordinate calculation methods
6. THE System SHALL maintain the same symmetry tolerance handling
7. THE System SHALL pass all existing validation tests

### Requirement 6: Project Structure and Maintainability

**User Story:** As a developer, I want a well-organized codebase, so that I can easily understand and maintain the code.

#### Acceptance Criteria

1. THE System SHALL follow Python package best practices
2. THE System SHALL use clear module names that describe functionality
3. THE System SHALL provide comprehensive docstrings for all public functions
4. THE System SHALL separate concerns (API, core algorithms, utilities)
5. THE System SHALL use consistent coding style throughout
6. THE System SHALL avoid excessive complexity in module organization
7. THE System SHALL maintain readability with clear variable and function names

### Requirement 7: English Language Documentation

**User Story:** As an international user, I want all documentation in English, so that I can understand and use the system.

#### Acceptance Criteria

1. THE System SHALL provide all code comments in English
2. THE System SHALL provide all docstrings in English
3. THE System SHALL provide all error messages in English
4. THE System SHALL provide all user-facing documentation in English
5. THE System SHALL provide all API documentation in English
6. THE System SHALL provide all configuration descriptions in English

### Requirement 8: Backward Compatibility

**User Story:** As an existing user, I want the refactored version to work with my existing workflows, so that I don't need to change my scripts.

#### Acceptance Criteria

1. THE System SHALL maintain the `tobacco.py` command-line interface
2. THE System SHALL support the existing `configuration.py` file format
3. THE System SHALL support the existing directory structure as a fallback
4. THE System SHALL produce CIF files in the same format as the original
5. THE System SHALL maintain the same output file naming convention
6. THE System SHALL support all existing configuration options
7. THE System SHALL provide migration guidance for new features

### Requirement 9: JSON Database Integration

**User Story:** As a user, I want to load building blocks from JSON databases, so that I can access components faster than reading individual CIF files.

#### Acceptance Criteria

1. THE System SHALL read from `data/nodes_database.json` when available
2. THE System SHALL read from `data/edges_database.json` when available
3. THE System SHALL read from `data/template_database.json` when available
4. WHEN JSON database is not found, THE System SHALL fall back to CIF files
5. THE System SHALL validate JSON database format on load
6. THE System SHALL provide clear error messages for corrupted JSON databases
7. THE System SHALL document the JSON database format

### Requirement 10: Flexible Return Value Options

**User Story:** As a developer, I want to choose how results are returned, so that I can integrate ToBaCCo into different workflows.

#### Acceptance Criteria

1. THE System SHALL provide a `return_format` parameter accepting "file", "string", or "json"
2. WHEN `return_format="file"`, THE System SHALL save to `output/cifs/` and return file path
3. WHEN `return_format="string"`, THE System SHALL return CIF content as string
4. WHEN `return_format="json"`, THE System SHALL return structured JSON with metadata
5. THE System SHALL default to "file" for backward compatibility
6. THE System SHALL allow multiple return formats simultaneously
7. THE System SHALL validate the `return_format` parameter

