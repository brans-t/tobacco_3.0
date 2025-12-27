# ToBaCCo Documentation

This directory contains comprehensive documentation for ToBaCCo 3.0.

## Documentation Structure

### User Guides

#### [INSTALLATION.md](INSTALLATION.md)
Complete installation guide covering:
- System requirements
- Installation methods (conda, pip, Docker)
- Dependency details
- Post-installation setup
- Troubleshooting
- Platform-specific notes

#### [CONFIGURATION.md](CONFIGURATION.md)
Configuration guide in English and Chinese:
- Configuration methods
- Key configuration options
- Common scenarios
- Quick reference table
- Troubleshooting tips

### Developer Documentation

#### [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
Complete API reference:
- Function signatures
- Parameters and return values
- Usage examples
- Error handling
- Best practices

#### [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)
Migration guide for upgrading:
- What's changed
- What's new
- Migration steps
- Backward compatibility
- Breaking changes (none!)

### Reference Materials

#### [tobacco_3.0_manual.pdf](tobacco_3.0_manual.pdf)
Complete user manual covering:
- ToBaCCo algorithms
- Input file formats
- Output file formats
- Theoretical background
- Advanced usage

## Quick Links

### Getting Started
1. [Installation Guide](INSTALLATION.md) - Install ToBaCCo
2. [Quick Start](../examples/README.md#quick-start) - First MOF generation
3. [Examples](../examples/README.md) - Usage examples

### Configuration
1. [Configuration Guide](CONFIGURATION.md) - All configuration options
2. [Common Scenarios](CONFIGURATION.md#common-configuration-scenarios) - Pre-configured setups
3. [Quick Reference](CONFIGURATION.md#quick-reference) - Option summary table

### API Usage
1. [API Documentation](API_DOCUMENTATION.md) - Complete API reference
2. [API Examples](../examples/README.md#code-examples) - Code examples
3. [Batch Generation](API_DOCUMENTATION.md#batch-generation) - Multiple MOFs

### Migration
1. [Migration Guide](MIGRATION_GUIDE.md) - Upgrade from older versions
2. [What's New](MIGRATION_GUIDE.md#whats-new) - New features
3. [Backward Compatibility](MIGRATION_GUIDE.md#backward-compatibility) - Compatibility info

## Documentation by Task

### I want to...

#### Install ToBaCCo
→ [INSTALLATION.md](INSTALLATION.md)

#### Generate my first MOF
→ [Quick Start Example](../examples/quick_start.py)

#### Understand configuration options
→ [CONFIGURATION.md](CONFIGURATION.md)

#### Use ToBaCCo in my Python code
→ [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

#### Generate multiple MOFs
→ [Multiple Input Example](../examples/multiple_input_example.py)

#### Get reproducible results
→ [Deterministic Charge Example](../examples/deterministic_charge_example.py)

#### Migrate from older version
→ [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)

#### Understand ToBaCCo algorithms
→ [tobacco_3.0_manual.pdf](tobacco_3.0_manual.pdf)

#### Troubleshoot issues
→ [INSTALLATION.md#troubleshooting](INSTALLATION.md#troubleshooting)

#### Export databases to JSON
→ [scripts/README.md](../scripts/README.md#export_databases_to_jsonpy)

#### Customize MOF generation
→ [CONFIGURATION.md](CONFIGURATION.md) + [Advanced Example](../examples/advanced_config_example.py)

## Language Support

All documentation is available in English.

## Additional Resources

### In Repository
- [Main README](../README.md) - Project overview
- [Examples](../examples/README.md) - Usage examples
- [Scripts](../scripts/README.md) - Utility scripts
- [CHANGES.md](../CHANGES.md) - Refactoring changes

### External
- RCSR Database: http://rcsr.net/
- Reticular Chemistry: https://www.reticular-chemistry.org/

## Contributing to Documentation

If you find errors or have suggestions for improving the documentation:

1. Check existing documentation first
2. Create an issue describing the problem
3. Suggest improvements or corrections
4. Submit a pull request with changes

## Documentation Standards

- **Clear and concise**: Use simple language
- **Examples**: Include code examples
- **Cross-references**: Link to related documentation
- **Up-to-date**: Keep synchronized with code changes
- **Bilingual**: Provide Chinese translations where appropriate

---

**Last Updated:** December 2024  
**ToBaCCo Version:** 3.0
