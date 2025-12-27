# ToBaCCo 3.0 Migration Guide

## Overview

This guide helps you migrate from the original ToBaCCo to the refactored ToBaCCo 3.0. The refactored version maintains **full backward compatibility** while adding new features and improvements.

**Key Point:** You can continue using ToBaCCo exactly as before without any changes. This guide shows you how to adopt new features when you're ready.

## Table of Contents

1. [What Changed](#what-changed)
2. [What Stayed the Same](#what-stayed-the-same)
3. [Migration Paths](#migration-paths)
4. [Step-by-Step Migration](#step-by-step-migration)
5. [Feature Comparison](#feature-comparison)
6. [Troubleshooting](#troubleshooting)
7. [FAQ](#faq)

---

## What Changed

### New Features

#### 1. Organized Input Directory Structure

**Old Structure:**
```
tobacco_3.0/
├── templates/
├── nodes/
└── edges/
```

**New Structure (Optional):**
```
tobacco_3.0/
├── inputs/
│   ├── templates/
│   ├── nodes/
│   └── edges/
├── templates/      # Legacy (still supported)
├── nodes/          # Legacy (still supported)
└── edges/          # Legacy (still supported)
```

**Benefits:**
- Better organization
- Clearer separation of inputs from code
- Easier to manage large collections of building blocks

**Backward Compatibility:**
- System checks `inputs/` first, then falls back to legacy directories
- No changes required to existing workflows

#### 2. Enhanced Programmatic API

**Old Way:**
```python
# Had to run tobacco.py and read output files
import subprocess
subprocess.run(['python', 'tobacco.py'])
# Then read generated CIF files
```

**New Way:**
```python
from src.api import generate_cif

result = generate_cif(
    template_name="pcu",
    node_names="6c_Cu_1_Ch",
    edge_names="btc_edge"
)
# Direct access to CIF content
```

**Benefits:**
- Direct programmatic access
- No subprocess calls needed
- Flexible input formats (string, list, dict)
- Multiple return formats (file, string, JSON)
- Better error handling

#### 3. Deterministic Charge Generation

**Old Behavior:**
- Random charges varied between runs
- Impossible to reproduce exact results

**New Behavior:**
```python
# Same seed = identical charges
result1 = generate_cif("pcu", "6c_Cu_1_Ch", "btc_edge", random_seed=42)
result2 = generate_cif("pcu", "6c_Cu_1_Ch", "btc_edge", random_seed=42)
# result1 and result2 are identical
```

**Benefits:**
- Reproducible research
- Consistent simulation results
- Easier debugging

#### 4. Flexible Return Formats

**Old Way:**
```python
# Always saved to file
# Had to read file to get content
```

**New Way:**
```python
# Return as file (default)
result = generate_cif("pcu", "6c_Cu_1_Ch", "btc_edge", return_format='file')

# Return as string (no file I/O)
cif_string = generate_cif("pcu", "6c_Cu_1_Ch", "btc_edge", return_format='string')

# Return as JSON (structured data)
cif_json = generate_cif("pcu", "6c_Cu_1_Ch", "btc_edge", return_format='json')
```

**Benefits:**
- No unnecessary file I/O
- Direct integration with other tools
- Structured metadata access

#### 5. Multiple Input Formats

**Old Way:**
```python
# Had to provide lists
node_names = ["6c_Cu_1_Ch"]
edge_names = ["btc_edge"]
```

**New Way:**
```python
# Single string (simplest)
result = generate_cif("pcu", "6c_Cu_1_Ch", "btc_edge")

# Lists (multiple options)
result = generate_cif("pcu", ["6c_Cu_1_Ch", "4c_Zn_1_Ch"], ["btc_edge"])

# Dict (vertex type mapping)
result = generate_cif("pcu", {"V": "6c_Cu_1_Ch"}, "btc_edge")
```

**Benefits:**
- Simpler API for common cases
- More flexible for complex cases
- Better type safety

#### 6. New Configuration Options

**New Options:**
- `RANDOM_SEED`: Control charge generation (default: 42)
- `INPUT_SOURCE`: Choose between JSON/CIF loading (default: 'auto')
- `DEFAULT_RETURN_FORMAT`: Set default output format (default: 'file')

**All Original Options Preserved:**
- All existing configuration options work exactly as before

---

## What Stayed the Same

### Unchanged Features

✅ **Command-Line Interface**
- `python tobacco.py` works exactly as before
- All interactive prompts unchanged
- Same user experience

✅ **Core Algorithms**
- All structure generation algorithms preserved
- Identical MOF structures produced (excluding random charges)
- Same unit cell scaling behavior
- Same bond formation logic

✅ **Configuration File**
- `configuration.py` in same location
- All original options preserved
- Same default values

✅ **Output Files**
- CIF files saved to `output/cifs/`
- Same file format
- Same naming convention

✅ **File Formats**
- CIF file format unchanged
- Same input file requirements
- Same building block format

✅ **Dependencies**
- Same Python version requirements
- Same package dependencies
- No new required packages

---

## Migration Paths

Choose the migration path that fits your needs:

### Path 1: No Changes (Recommended for Most Users)

**Who:** Users happy with current workflow

**Steps:** None! Continue using ToBaCCo exactly as before.

**Pros:**
- Zero effort
- No risk
- Everything works

**Cons:**
- Miss out on new features

### Path 2: Adopt New Directory Structure

**Who:** Users who want better organization

**Steps:**
1. Create `inputs/` directory structure
2. Move or copy building blocks
3. Continue using as before

**Pros:**
- Better organization
- Still use CLI or API
- Backward compatible

**Cons:**
- One-time file reorganization

### Path 3: Use New API

**Who:** Developers integrating ToBaCCo into tools

**Steps:**
1. Import API functions
2. Replace subprocess calls with API calls
3. Use new features as needed

**Pros:**
- Direct programmatic access
- Flexible input/output formats
- Better error handling

**Cons:**
- Need to update scripts

### Path 4: Full Migration

**Who:** Users who want all new features

**Steps:**
1. Adopt new directory structure
2. Use new API
3. Enable deterministic charges
4. Use flexible return formats

**Pros:**
- All new features
- Best organization
- Most flexible

**Cons:**
- Most effort required

---

## Step-by-Step Migration

### Step 1: Backup Your Work

Before making any changes:

```bash
# Create backup
cp -r tobacco_3.0 tobacco_3.0_backup

# Or use git
git add .
git commit -m "Backup before migration"
```

### Step 2: Verify Current Installation

Test that everything works:

```bash
# Test CLI
python tobacco.py

# Test dependencies
python check_installation.py
```

### Step 3: Choose Migration Path

Decide which features you want to adopt (see [Migration Paths](#migration-paths)).

### Step 4: Migrate Directory Structure (Optional)

If adopting new directory structure:

```bash
# Create new directories
mkdir -p inputs/edges inputs/nodes inputs/templates

# Option A: Move files (removes from old location)
mv edges/* inputs/edges/
mv nodes/* inputs/nodes/
mv templates/* inputs/templates/

# Option B: Copy files (keeps originals)
cp -r edges/* inputs/edges/
cp -r nodes/* inputs/nodes/
cp -r templates/* inputs/templates/
```

**Note:** System supports both locations, so you can keep files in both places during transition.

### Step 5: Update Scripts (Optional)

If adopting new API:

**Old Script:**
```python
import subprocess
import os

# Run ToBaCCo
subprocess.run(['python', 'tobacco.py'])

# Read output
cif_files = os.listdir('output/cifs')
for cif_file in cif_files:
    with open(f'output/cifs/{cif_file}', 'r') as f:
        content = f.read()
    # Process content
```

**New Script:**
```python
from src.api import generate_cif

# Generate MOF
result = generate_cif(
    template_name="pcu",
    node_names="6c_Cu_1_Ch",
    edge_names="btc_edge",
    return_format='string'  # Get content directly
)

# Process content directly
content = result
# No file I/O needed!
```

### Step 6: Enable Deterministic Charges (Optional)

If you want reproducible results:

**Option A: Set in configuration.py**
```python
# configuration.py
RANDOM_SEED = 42  # Or any integer
```

**Option B: Set in API calls**
```python
result = generate_cif(
    "pcu", "6c_Cu_1_Ch", "btc_edge",
    random_seed=42
)
```

### Step 7: Test Migration

Verify everything works:

```bash
# Test CLI
python tobacco.py

# Test API (if using)
python -c "from src.api import generate_cif; print('API works!')"

# Run tests
python -m pytest tests/
```

### Step 8: Update Documentation

Update your own documentation to reflect changes:
- Note new directory structure (if adopted)
- Update API usage examples (if applicable)
- Document random seed usage (if enabled)

---

## Feature Comparison

### Command-Line Interface

| Feature | Original | Refactored |
|---------|----------|------------|
| Interactive mode | ✅ | ✅ |
| Batch mode | ✅ | ✅ |
| Configuration file | ✅ | ✅ |
| Output to files | ✅ | ✅ |
| Error messages | ✅ | ✅ (improved) |

### Programmatic API

| Feature | Original | Refactored |
|---------|----------|------------|
| Direct API access | ❌ | ✅ |
| Flexible input formats | ❌ | ✅ |
| Multiple return formats | ❌ | ✅ |
| Deterministic charges | ❌ | ✅ |
| Batch generation | ❌ | ✅ |
| Error handling | Basic | ✅ Enhanced |

### Directory Structure

| Feature | Original | Refactored |
|---------|----------|------------|
| Root directories | ✅ | ✅ (legacy support) |
| Organized inputs/ | ❌ | ✅ (optional) |
| Backward compatible | N/A | ✅ |

### Configuration

| Feature | Original | Refactored |
|---------|----------|------------|
| All original options | ✅ | ✅ |
| Random seed control | ❌ | ✅ |
| Input source control | ❌ | ✅ |
| Return format control | ❌ | ✅ |
| API overrides | ❌ | ✅ |

### Output Formats

| Feature | Original | Refactored |
|---------|----------|------------|
| CIF files | ✅ | ✅ |
| String return | ❌ | ✅ |
| JSON return | ❌ | ✅ |
| Metadata access | Limited | ✅ Enhanced |

---

## Troubleshooting

### Problem: "File not found" after migration

**Symptoms:**
```
FileNotFoundError: Template file 'pcu.cif' not found
```

**Solutions:**

1. **Check both locations:**
   ```bash
   # Check new location
   ls inputs/templates/pcu.cif
   
   # Check legacy location
   ls templates/pcu.cif
   ```

2. **Verify file exists:**
   ```bash
   find . -name "pcu.cif"
   ```

3. **Check file permissions:**
   ```bash
   ls -l inputs/templates/pcu.cif
   ```

4. **Use absolute paths for testing:**
   ```python
   from pathlib import Path
   template_path = Path("inputs/templates/pcu.cif")
   print(f"Exists: {template_path.exists()}")
   ```

### Problem: Different results after migration

**Symptoms:**
- Generated MOFs have different charges
- Structures look different

**Solutions:**

1. **Set random seed for reproducibility:**
   ```python
   # In configuration.py
   RANDOM_SEED = 42
   
   # Or in API call
   result = generate_cif("pcu", "6c_Cu_1_Ch", "btc_edge", random_seed=42)
   ```

2. **Verify same configuration:**
   ```python
   # Check configuration values
   import configuration
   print(f"CHARGES: {configuration.CHARGES}")
   print(f"SCALING_ITERATIONS: {configuration.SCALING_ITERATIONS}")
   ```

3. **Compare structures (excluding charges):**
   - Structures should be identical except for random charges
   - Unit cell parameters should match
   - Atom positions should match

### Problem: API import errors

**Symptoms:**
```
ImportError: cannot import name 'generate_cif' from 'src.api'
```

**Solutions:**

1. **Check Python path:**
   ```python
   import sys
   print(sys.path)
   ```

2. **Run from project root:**
   ```bash
   cd tobacco_3.0
   python your_script.py
   ```

3. **Use correct import:**
   ```python
   # Correct
   from src.api import generate_cif
   
   # Incorrect
   from api import generate_cif
   ```

### Problem: Old scripts don't work

**Symptoms:**
- Scripts that worked before now fail
- Different behavior than expected

**Solutions:**

1. **Check if using old API:**
   - Old API may have been custom/undocumented
   - Migrate to new documented API

2. **Verify configuration:**
   - Check if configuration.py was modified
   - Restore original values if needed

3. **Use backward compatible mode:**
   ```python
   # Use default return format
   result = generate_cif("pcu", "6c_Cu_1_Ch", "btc_edge")
   # Returns dict with 'file_path' key (backward compatible)
   ```

### Problem: Performance issues

**Symptoms:**
- Slower than before
- High memory usage

**Solutions:**

1. **Use JSON databases:**
   ```bash
   python scripts/export_databases_to_json.py
   ```

2. **Adjust configuration:**
   ```python
   config = {
       "COMBINATORIAL_EDGE_ASSIGNMENT": False,  # Reduce combinations
       "SCALING_ITERATIONS": 1  # Reduce optimization
   }
   ```

3. **Use batch generation:**
   ```python
   # More efficient than multiple calls
   from src.api import generate_multiple_mofs
   results = generate_multiple_mofs(combinations)
   ```

---

## FAQ

### Q: Do I need to change anything?

**A:** No! The refactored version is fully backward compatible. You can continue using ToBaCCo exactly as before.

### Q: Will my existing scripts work?

**A:** Yes, if they use the command-line interface (`python tobacco.py`). If they use custom/undocumented APIs, you may need to migrate to the new documented API.

### Q: Can I use both old and new directory structures?

**A:** Yes! The system checks both locations. Files in `inputs/` take precedence over legacy directories.

### Q: Will I get the same results?

**A:** Almost. The core algorithms are identical, so structures are the same. However, random charges may differ unless you set a random seed.

### Q: How do I get reproducible results?

**A:** Set a random seed:
```python
# In configuration.py
RANDOM_SEED = 42

# Or in API call
result = generate_cif("pcu", "6c_Cu_1_Ch", "btc_edge", random_seed=42)
```

### Q: What if I find a bug?

**A:** The refactored version has been extensively tested, but if you find issues:
1. Check this migration guide
2. Verify your configuration
3. Try with default settings
4. Report the issue with details

### Q: Can I mix old and new features?

**A:** Yes! You can:
- Use CLI with new directory structure
- Use API with legacy directories
- Mix return formats
- Gradually adopt new features

### Q: Do I need to update my building blocks?

**A:** No. All CIF files work exactly as before. No changes needed.

### Q: What about my configuration file?

**A:** Your `configuration.py` works as-is. New options have defaults, so they're optional.

### Q: How do I know which version I'm using?

**A:** Check for new features:
```python
# Try importing new API
try:
    from src.api import generate_cif
    print("Using refactored version")
except ImportError:
    print("Using original version")
```

### Q: Can I go back to the original version?

**A:** Yes! Since it's backward compatible:
1. Restore your backup
2. Or just stop using new features
3. Everything still works

### Q: Where can I get help?

**A:** Resources:
- This migration guide
- [API Documentation](API_DOCUMENTATION.md)
- [Configuration Guide](../CONFIGURATION_GUIDE.md)
- [README](../README.md)
- Example scripts in `examples/`

---

## Examples

### Example 1: Minimal Migration

No changes needed - continue as before:

```bash
# Still works exactly as before
python tobacco.py
```

### Example 2: Adopt New Directory Structure

```bash
# Create directories
mkdir -p inputs/{edges,nodes,templates}

# Copy files (keeps originals)
cp -r edges/* inputs/edges/
cp -r nodes/* inputs/nodes/
cp -r templates/* inputs/templates/

# Use as before
python tobacco.py
```

### Example 3: Migrate to API

**Before:**
```python
import subprocess
subprocess.run(['python', 'tobacco.py'])
```

**After:**
```python
from src.api import generate_cif

result = generate_cif(
    template_name="pcu",
    node_names="6c_Cu_1_Ch",
    edge_names="btc_edge"
)
print(f"Generated: {result['cifname']}")
```

### Example 4: Enable Reproducibility

```python
# Set seed for reproducible results
from src.api import generate_cif

result = generate_cif(
    template_name="pcu",
    node_names="6c_Cu_1_Ch",
    edge_names="btc_edge",
    random_seed=42  # Same seed = same charges
)
```

### Example 5: Use New Return Formats

```python
from src.api import generate_cif

# Get string directly (no file I/O)
cif_string = generate_cif(
    "pcu", "6c_Cu_1_Ch", "btc_edge",
    return_format='string'
)

# Process immediately
lines = cif_string.split('\n')
print(f"CIF has {len(lines)} lines")
```

---

## Summary

### Key Takeaways

1. **Backward Compatible**: Everything works as before
2. **Optional Features**: Adopt new features when ready
3. **No Breaking Changes**: Existing workflows continue to work
4. **Gradual Migration**: Migrate at your own pace
5. **Better Organization**: New directory structure is optional but recommended
6. **Enhanced API**: Programmatic access for integration
7. **Reproducible**: Deterministic charges with random seeds

### Recommended Migration Order

1. **Phase 1**: Continue using as-is (no changes)
2. **Phase 2**: Adopt new directory structure (better organization)
3. **Phase 3**: Try new API for new projects (learn features)
4. **Phase 4**: Migrate existing scripts to API (when convenient)
5. **Phase 5**: Enable deterministic charges (for reproducibility)

### Next Steps

1. Read [API Documentation](API_DOCUMENTATION.md) for detailed API reference
2. Check [Configuration Guide](../CONFIGURATION_GUIDE.md) for new options
3. Try [Examples](../examples/) to see new features in action
4. Migrate at your own pace - no rush!

---

**Last Updated:** December 28, 2024  
**Version:** 3.0
