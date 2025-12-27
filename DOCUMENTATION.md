# ToBaCCo 3.0 Documentation Structure

## 📚 Documentation Overview

This document provides a complete guide to ToBaCCo's documentation structure.

## 📁 File Organization

### Root Directory

| File | Purpose | Audience |
|------|---------|----------|
| `README.md` | Project overview and quick start | All users |
| `DOCUMENTATION.md` | Documentation structure guide (this file) | All users |
| `CHANGES.md` | Refactoring changes and history | Developers |
| `LICENSE` | Software license | All users |
| `requirements.txt` | Python dependencies | All users |
| `configuration.py` | Global configuration file | All users |
| `tobacco.py` | Main CLI entry point | End users |
| `check_installation.py` | Installation verification script | All users |

### docs/ Directory

| File | Purpose | Language |
|------|---------|----------|
| `docs/README.md` | Documentation index | English |
| `docs/INSTALLATION.md` | Installation guide | English |
| `docs/CONFIGURATION.md` | Configuration guide | English + 中文 |
| `docs/API_DOCUMENTATION.md` | API reference | English |
| `docs/MIGRATION_GUIDE.md` | Migration guide | English |
| `docs/tobacco_3.0_manual.pdf` | Complete user manual | English |
| `docs/tobacco_3.0_manual.docx` | Editable manual | English |

### examples/ Directory

| File | Purpose |
|------|---------|
| `examples/README.md` | Examples overview and guide |
| `examples/quick_start.py` | Simplest usage example |
| `examples/single_input_example.py` | Single MOF generation |
| `examples/multiple_input_example.py` | Batch generation |
| `examples/deterministic_charge_example.py` | Reproducible charges |
| `examples/advanced_config_example.py` | Configuration options |
| `examples/generate_mof_example.py` | Comprehensive example |
| `examples/CONFIG_OPTIONS.md` | Configuration options reference |
| `examples/EXAMPLES_OVERVIEW.md` | Examples summary |

### scripts/ Directory

| File | Purpose |
|------|---------|
| `scripts/README.md` | Scripts documentation |
| `scripts/export_databases_to_json.py` | Database export |
| `scripts/reindex_building_blocks.py` | CIF reindexing |
| `scripts/make_topologies.py` | Topology generation |
| `scripts/topo_pore_analysis.py` | Pore analysis |
| `scripts/scrape_rcsr.py` | RCSR data scraper |

### tests/ Directory

| File | Purpose |
|------|---------|
| `tests/test_*.py` | Unit tests |
| `tests/ALGORITHM_PRESERVATION_FINDINGS.md` | Test findings |

## 🎯 Documentation by User Type

### New Users

**Start here:**
1. [README.md](README.md) - Project overview
2. [docs/INSTALLATION.md](docs/INSTALLATION.md) - Install ToBaCCo
3. [examples/quick_start.py](examples/quick_start.py) - First MOF
4. [examples/README.md](examples/README.md) - More examples

**Next steps:**
- [docs/CONFIGURATION.md](docs/CONFIGURATION.md) - Customize settings
- [examples/generate_mof_example.py](examples/generate_mof_example.py) - Comprehensive example

### API Users (Developers)

**Start here:**
1. [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) - API reference
2. [examples/single_input_example.py](examples/single_input_example.py) - Basic API usage
3. [examples/multiple_input_example.py](examples/multiple_input_example.py) - Batch generation

**Advanced:**
- [docs/CONFIGURATION.md](docs/CONFIGURATION.md) - Configuration options
- [examples/advanced_config_example.py](examples/advanced_config_example.py) - Advanced usage
- [examples/deterministic_charge_example.py](examples/deterministic_charge_example.py) - Reproducibility

### Researchers

**For reproducible research:**
1. [examples/deterministic_charge_example.py](examples/deterministic_charge_example.py) - Reproducible charges
2. [docs/CONFIGURATION.md](docs/CONFIGURATION.md#reproducible-research) - Research configuration
3. [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) - Programmatic usage

**For understanding algorithms:**
- [docs/tobacco_3.0_manual.pdf](docs/tobacco_3.0_manual.pdf) - Complete manual
- [CHANGES.md](CHANGES.md) - Algorithm preservation

### Migrating Users

**Upgrading from older versions:**
1. [docs/MIGRATION_GUIDE.md](docs/MIGRATION_GUIDE.md) - Migration guide
2. [CHANGES.md](CHANGES.md) - What changed
3. [docs/CONFIGURATION.md](docs/CONFIGURATION.md) - New options

## 🔍 Documentation by Topic

### Installation

- **Main guide**: [docs/INSTALLATION.md](docs/INSTALLATION.md)
- **Quick check**: [check_installation.py](check_installation.py)
- **Requirements**: [requirements.txt](requirements.txt)

### Configuration

- **Complete guide**: [docs/CONFIGURATION.md](docs/CONFIGURATION.md)
- **Quick reference**: [docs/CONFIGURATION.md#quick-reference](docs/CONFIGURATION.md#quick-reference)
- **Examples**: [examples/advanced_config_example.py](examples/advanced_config_example.py)
- **Options list**: [examples/CONFIG_OPTIONS.md](examples/CONFIG_OPTIONS.md)

### API Usage

- **API reference**: [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md)
- **Basic example**: [examples/single_input_example.py](examples/single_input_example.py)
- **Batch generation**: [examples/multiple_input_example.py](examples/multiple_input_example.py)
- **Code examples**: [examples/README.md#code-examples](examples/README.md#code-examples)

### Examples

- **Overview**: [examples/README.md](examples/README.md)
- **Quick start**: [examples/quick_start.py](examples/quick_start.py)
- **All examples**: [examples/EXAMPLES_OVERVIEW.md](examples/EXAMPLES_OVERVIEW.md)

### Utility Scripts

- **Scripts guide**: [scripts/README.md](scripts/README.md)
- **Database export**: [scripts/export_databases_to_json.py](scripts/export_databases_to_json.py)
- **Reindexing**: [scripts/reindex_building_blocks.py](scripts/reindex_building_blocks.py)

### Algorithms & Theory

- **User manual**: [docs/tobacco_3.0_manual.pdf](docs/tobacco_3.0_manual.pdf)
- **Algorithm preservation**: [tests/ALGORITHM_PRESERVATION_FINDINGS.md](tests/ALGORITHM_PRESERVATION_FINDINGS.md)
- **Changes**: [CHANGES.md](CHANGES.md)

## 📖 Reading Order Recommendations

### For First-Time Users

1. [README.md](README.md) - Understand what ToBaCCo does
2. [docs/INSTALLATION.md](docs/INSTALLATION.md) - Install ToBaCCo
3. [examples/quick_start.py](examples/quick_start.py) - Generate first MOF
4. [examples/README.md](examples/README.md) - Explore more examples
5. [docs/CONFIGURATION.md](docs/CONFIGURATION.md) - Customize settings

### For Developers

1. [README.md](README.md) - Project overview
2. [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) - API reference
3. [examples/single_input_example.py](examples/single_input_example.py) - Basic usage
4. [examples/multiple_input_example.py](examples/multiple_input_example.py) - Batch processing
5. [docs/CONFIGURATION.md](docs/CONFIGURATION.md) - Configuration options
6. [CHANGES.md](CHANGES.md) - Implementation details

### For Researchers

1. [README.md](README.md) - Project overview
2. [docs/tobacco_3.0_manual.pdf](docs/tobacco_3.0_manual.pdf) - Theory and algorithms
3. [examples/deterministic_charge_example.py](examples/deterministic_charge_example.py) - Reproducibility
4. [docs/CONFIGURATION.md](docs/CONFIGURATION.md) - Research settings
5. [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) - Automation

## 🌐 Language Support

### English Documentation
All documentation is available in English.

### Chinese Documentation (中文文档)
- [docs/CONFIGURATION.md](docs/CONFIGURATION.md#中文版本) - Configuration guide in Chinese

## 🔧 Troubleshooting Documentation

### Installation Issues
→ [docs/INSTALLATION.md#troubleshooting](docs/INSTALLATION.md#troubleshooting)

### Configuration Issues
→ [docs/CONFIGURATION.md](docs/CONFIGURATION.md) (see FAQ sections)

### API Issues
→ [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) (see error handling)

### General Issues
→ [README.md#troubleshooting](README.md#troubleshooting)

## 📝 Documentation Standards

### File Naming
- Use descriptive names in UPPERCASE for main docs (e.g., `INSTALLATION.md`)
- Use lowercase for supporting docs (e.g., `examples/README.md`)
- Use snake_case for Python files (e.g., `quick_start.py`)

### Content Structure
- Start with clear title and overview
- Use hierarchical headings (##, ###, ####)
- Include code examples where appropriate
- Add cross-references to related documentation
- Provide troubleshooting sections

### Code Examples
- Use syntax highlighting (```python)
- Include complete, runnable examples
- Add comments explaining key points
- Show expected output

### Maintenance
- Keep documentation synchronized with code
- Update version numbers and dates
- Test all code examples
- Review for clarity and accuracy

## 🔄 Documentation Updates

### When to Update

**Update immediately when:**
- Adding new features
- Changing API signatures
- Modifying configuration options
- Fixing bugs that affect usage

**Update periodically:**
- Version numbers
- Last updated dates
- External links
- Examples with new best practices

### What to Update

**For new features:**
- README.md (if user-facing)
- API_DOCUMENTATION.md (if API change)
- CONFIGURATION.md (if config change)
- Examples (add new example if needed)
- CHANGES.md (document change)

**For bug fixes:**
- Relevant documentation
- Troubleshooting sections
- CHANGES.md

## 📊 Documentation Metrics

### Coverage
- ✅ Installation guide
- ✅ Configuration guide (English + Chinese)
- ✅ API documentation
- ✅ Usage examples
- ✅ Migration guide
- ✅ Utility scripts documentation
- ✅ Troubleshooting guides

### Quality
- ✅ Clear and concise
- ✅ Code examples included
- ✅ Cross-referenced
- ✅ Up-to-date
- ✅ Bilingual support (partial)

## 🎓 Learning Path

### Beginner Path (1-2 hours)
1. Read [README.md](README.md) (10 min)
2. Follow [docs/INSTALLATION.md](docs/INSTALLATION.md) (20 min)
3. Run [examples/quick_start.py](examples/quick_start.py) (10 min)
4. Read [examples/README.md](examples/README.md) (20 min)
5. Try [examples/single_input_example.py](examples/single_input_example.py) (30 min)

### Intermediate Path (3-4 hours)
1. Complete Beginner Path
2. Read [docs/CONFIGURATION.md](docs/CONFIGURATION.md) (30 min)
3. Try [examples/advanced_config_example.py](examples/advanced_config_example.py) (30 min)
4. Read [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) (45 min)
5. Try [examples/multiple_input_example.py](examples/multiple_input_example.py) (45 min)
6. Experiment with own MOFs (60 min)

### Advanced Path (6-8 hours)
1. Complete Intermediate Path
2. Read [docs/tobacco_3.0_manual.pdf](docs/tobacco_3.0_manual.pdf) (2 hours)
3. Read [CHANGES.md](CHANGES.md) (30 min)
4. Study [scripts/README.md](scripts/README.md) (30 min)
5. Explore utility scripts (60 min)
6. Read source code in `src/` (2 hours)

## 📞 Getting Help

### Documentation
1. Check this documentation structure guide
2. Read relevant documentation files
3. Try examples
4. Check troubleshooting sections

### Community
1. Search existing issues
2. Create new issue with details
3. Provide minimal reproducible example
4. Include error messages and logs

---

**Last Updated:** December 2024  
**ToBaCCo Version:** 3.0  
**Documentation Version:** 1.0
