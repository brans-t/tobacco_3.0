# ToBaCCo 3.0 Installation Guide

## System Requirements

### Python Version
- **Required:** Python 3.7 or higher
- **Recommended:** Python 3.9 or 3.10
- **Not Supported:** Python 2.7 (deprecated)

### Operating Systems
- ✅ Linux (Ubuntu, CentOS, etc.)
- ✅ macOS
- ✅ Windows (with WSL or native)

### Hardware
- **Minimum:** 2 GB RAM
- **Recommended:** 4 GB RAM or more
- **Disk Space:** ~500 MB for installation and databases

---

## Installation Methods

### Method 1: Using Conda (Recommended)

Conda provides the most reliable environment management.

#### Step 1: Install Conda
If you don't have Conda installed, download and install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/products/distribution).

#### Step 2: Create Environment
```bash
# Create a new environment with Python 3.9
conda create --name tobacco python=3.9

# Activate the environment
conda activate tobacco
```

#### Step 3: Install Dependencies
```bash
# Install core dependencies
conda install numpy networkx scipy

# Or use pip within conda
pip install -r requirements.txt
```

#### Step 4: Verify Installation
```bash
python -c "import numpy, networkx, scipy; print('✓ All dependencies installed!')"
```

---

### Method 2: Using pip with Virtual Environment

#### Step 1: Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv tobacco_env

# Activate on Linux/macOS
source tobacco_env/bin/activate

# Activate on Windows
tobacco_env\Scripts\activate
```

#### Step 2: Install Dependencies
```bash
# Upgrade pip
pip install --upgrade pip

# Install from requirements.txt
pip install -r requirements.txt
```

#### Step 3: Verify Installation
```bash
python -c "import numpy, networkx, scipy; print('✓ All dependencies installed!')"
```

---

### Method 3: System-Wide Installation (Not Recommended)

```bash
# Install dependencies system-wide
pip3 install numpy>=1.19.0 networkx>=2.5 scipy>=1.5.0

# Verify
python3 -c "import numpy, networkx, scipy; print('✓ All dependencies installed!')"
```

**Warning:** System-wide installation may conflict with other Python packages.

---

## Dependency Details

### Core Dependencies

#### NumPy
- **Purpose:** Numerical computations, array operations
- **Version:** >= 1.19.0
- **Recommended:** 1.21.0+

```bash
pip install numpy>=1.19.0
```

#### NetworkX
- **Purpose:** Graph algorithms, topology analysis
- **Version:** >= 2.5
- **Recommended:** 2.6+

```bash
pip install networkx>=2.5
```

#### SciPy
- **Purpose:** Scientific computing, optimization
- **Version:** >= 1.5.0
- **Recommended:** 1.7.0+

```bash
pip install scipy>=1.5.0
```

### Optional Dependencies

#### For Testing
```bash
pip install pytest>=6.0.0
```

#### For Topology Generation (scripts/make_topologies.py)
```bash
pip install pymatgen>=2022.0.0 ase>=3.22.0
```

#### For Web Scraping (scripts/scrape_rcsr.py)
```bash
pip install selenium>=4.0.0 pandas>=1.3.0
```

#### For Visualization
```bash
pip install matplotlib>=3.3.0
```

---

## Post-Installation Setup

### 1. Export Databases to JSON (Optional but Recommended)

For faster access, export CIF databases to JSON format:

```bash
python scripts/export_databases_to_json.py
```

This creates:
- `data/edges_database.json`
- `data/nodes_database.json`
- `data/template_database.json`

### 2. Test Installation

Run a quick test to ensure everything works:

```bash
python examples/quick_start.py
```

Expected output:
```
✓ Success!
   Generated: acsh_12c_Ce_1_Ch_1B_1TrU.cif
   Saved to:  output/cifs/acsh_12c_Ce_1_Ch_1B_1TrU.cif
```

### 3. Run Tests (Optional)

```bash
pytest tests/
```

---

## Troubleshooting

### Problem: ImportError: No module named 'numpy'

**Solution:**
```bash
# Make sure you're in the correct environment
conda activate tobacco  # or source tobacco_env/bin/activate

# Reinstall numpy
pip install numpy
```

### Problem: Python version too old

**Error:**
```
SyntaxError: invalid syntax
```

**Solution:**
Check your Python version:
```bash
python --version
```

If it's < 3.7, upgrade Python:
```bash
# Using conda
conda install python=3.9

# Or download from python.org
```

### Problem: Permission denied when installing

**Solution:**
Use virtual environment or add `--user` flag:
```bash
pip install --user -r requirements.txt
```

### Problem: Conflicting package versions

**Solution:**
Create a fresh environment:
```bash
# Remove old environment
conda env remove --name tobacco

# Create new one
conda create --name tobacco python=3.9
conda activate tobacco
pip install -r requirements.txt
```

### Problem: Windows-specific issues

**Solution:**
1. Use WSL (Windows Subsystem for Linux)
2. Or install Visual C++ Build Tools for compilation
3. Use pre-built wheels: `pip install --only-binary :all: numpy scipy`

---

## Verifying Your Installation

### Quick Check
```bash
python -c "
import sys
import numpy as np
import networkx as nx
import scipy

print(f'Python: {sys.version}')
print(f'NumPy: {np.__version__}')
print(f'NetworkX: {nx.__version__}')
print(f'SciPy: {scipy.__version__}')
print('✓ All dependencies OK!')
"
```

### Full Test
```bash
# Run all tests
pytest tests/ -v

# Run a simple generation
python examples/quick_start.py
```

---

## Updating ToBaCCo

### Update Dependencies
```bash
# Using conda
conda update numpy networkx scipy

# Using pip
pip install --upgrade numpy networkx scipy
```

### Update ToBaCCo Code
```bash
# If using git
git pull origin main

# Or download latest release
```

---

## Uninstallation

### Remove Conda Environment
```bash
conda deactivate
conda env remove --name tobacco
```

### Remove Virtual Environment
```bash
deactivate
rm -rf tobacco_env
```

### Remove System-Wide Installation
```bash
pip uninstall numpy networkx scipy
```

---

## Platform-Specific Notes

### Linux (Ubuntu/Debian)
```bash
# Install system dependencies (if needed)
sudo apt-get update
sudo apt-get install python3-dev python3-pip

# Then follow standard installation
pip3 install -r requirements.txt
```

### macOS
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.9

# Then follow standard installation
pip3 install -r requirements.txt
```

### Windows
```bash
# Option 1: Use WSL (Recommended)
# Install WSL from Microsoft Store
# Then follow Linux instructions

# Option 2: Native Windows
# Download Python from python.org
# Install with "Add to PATH" option
# Then follow standard installation
pip install -r requirements.txt
```

---

## Docker Installation (Advanced)

Create a Dockerfile:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "tobacco.py"]
```

Build and run:
```bash
docker build -t tobacco .
docker run -it tobacco
```

---

## Getting Help

If you encounter issues:

1. **Check Python version:** `python --version` (must be >= 3.7)
2. **Check dependencies:** Run verification script above
3. **Check documentation:** See README.md and examples/
4. **Run tests:** `pytest tests/` to identify issues
5. **Check logs:** Look for error messages in console output

---

## Recommended Setup for Development

```bash
# Create environment
conda create --name tobacco-dev python=3.9
conda activate tobacco-dev

# Install core dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8 mypy

# Install optional dependencies
pip install pymatgen ase selenium pandas matplotlib

# Export databases
python scripts/export_databases_to_json.py

# Run tests
pytest tests/
```

---

**Last Updated:** December 27, 2024  
**ToBaCCo Version:** 3.0  
**Python Support:** 3.7+
