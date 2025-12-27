# ToBaCCo Utility Scripts

This directory contains utility scripts for ToBaCCo database management and analysis.

## Scripts

### Database Management

#### `export_databases_to_json.py`
Exports CIF database files to JSON format for faster programmatic access.

**Usage:**
```bash
python scripts/export_databases_to_json.py
```

**Output:**
- `data/edges_database.json`
- `data/nodes_database.json`
- `data/template_database.json`

---

#### `reindex_building_blocks.py`
Reindexes atoms in building block CIF files (nodes and edges) with sequential numbering.

**Usage:**
```bash
# Basic usage
python scripts/reindex_building_blocks.py

# Include charge information
python scripts/reindex_building_blocks.py --charges
```

**What it does:**
- Renumbers all atoms sequentially
- Updates all bond references
- Processes all CIF files in `nodes/` and `edges/` directories

---

### Topology Generation

#### `make_topologies.py`
Generates topology CIF files from RCSR (Reticular Chemistry Structure Resource) database.

**Requirements:**
- pymatgen
- ase

**Usage:**
```bash
python scripts/make_topologies.py
```

**Configuration:**
Edit the settings at the top of the file:
- `tol`: Distance tolerance (default: 1E-2)
- `scale`: Lattice constant scaling factor (default: 10)
- `cgd_filename`: Path to RCSR .cgd file
- `consider_2D`: Whether to include 2D topologies

**Output:**
- `data/template_database/*.cif` - 3D topology files
- `data/template_2D_database/*.cif` - 2D topology files (if enabled)

---

### Data Collection

#### `scrape_rcsr.py`
Scrapes topology data from the RCSR website.

**Requirements:**
- selenium
- pandas
- chromedriver

**Setup:**
1. Download chromedriver from https://chromedriver.chromium.org/
2. Update the `webdriver` variable in the script

**Usage:**
```bash
python scripts/scrape_rcsr.py
```

**Output:**
- `rcsr_3D.csv` - 3D topology data
- `rcsr_2D.csv` - 2D topology data

---

### Analysis

#### `topo_pore_analysis.py`
Performs Voronoi tessellation analysis on topology CIF files to analyze pore structures.

**Requirements:**
- scipy
- ase
- numpy

**Usage:**
```bash
python scripts/topo_pore_analysis.py
```

**What it does:**
- Performs Voronoi tessellation on topology structures
- Analyzes pore geometry and distribution
- Outputs analysis metrics for each topology

---

## Notes

- All scripts are designed to be run from the project root directory
- Scripts automatically import from the `src/` package
- For detailed information about each script, see the docstring at the top of the file
