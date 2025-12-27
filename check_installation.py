#!/usr/bin/env python
"""
ToBaCCo Installation Checker

This script verifies that all required dependencies are installed
and checks the Python version.

Usage:
    python check_installation.py
"""

import sys
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible."""
    print("=" * 70)
    print("Checking Python Version")
    print("=" * 70)
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    print(f"\nPython version: {version_str}")
    print(f"Python executable: {sys.executable}")
    
    if version.major < 3:
        print("❌ ERROR: Python 2 is not supported")
        print("   Please upgrade to Python 3.7 or higher")
        return False
    elif version.major == 3 and version.minor < 7:
        print(f"❌ ERROR: Python {version_str} is too old")
        print("   Please upgrade to Python 3.7 or higher")
        return False
    elif version.major == 3 and version.minor >= 7:
        print(f"✓ Python {version_str} is compatible")
        if version.minor >= 9:
            print("  (Recommended version)")
        return True
    else:
        print(f"✓ Python {version_str} should be compatible")
        return True


def check_dependencies():
    """Check if all required dependencies are installed."""
    print("\n" + "=" * 70)
    print("Checking Dependencies")
    print("=" * 70)
    
    dependencies = {
        'numpy': '1.19.0',
        'networkx': '2.5',
        'scipy': '1.5.0'
    }
    
    all_ok = True
    
    for package, min_version in dependencies.items():
        try:
            module = __import__(package)
            version = getattr(module, '__version__', 'unknown')
            print(f"\n✓ {package}: {version}")
            
            # Check version if possible
            if version != 'unknown':
                try:
                    from packaging import version as pkg_version
                    if pkg_version.parse(version) < pkg_version.parse(min_version):
                        print(f"  ⚠️  Warning: Version {version} is older than recommended {min_version}")
                except ImportError:
                    pass  # packaging not available, skip version check
                    
        except ImportError:
            print(f"\n❌ {package}: NOT INSTALLED")
            print(f"   Install with: pip install {package}>={min_version}")
            all_ok = False
    
    return all_ok


def check_optional_dependencies():
    """Check optional dependencies."""
    print("\n" + "=" * 70)
    print("Checking Optional Dependencies")
    print("=" * 70)
    
    optional = {
        'pytest': 'Testing',
        'pymatgen': 'Topology generation',
        'ase': 'Topology generation',
        'selenium': 'Web scraping',
        'pandas': 'Data processing',
        'matplotlib': 'Visualization'
    }
    
    print("\nOptional packages (not required for basic usage):")
    
    for package, purpose in optional.items():
        try:
            module = __import__(package)
            version = getattr(module, '__version__', 'unknown')
            print(f"  ✓ {package}: {version} ({purpose})")
        except ImportError:
            print(f"  - {package}: not installed ({purpose})")


def check_project_structure():
    """Check if project structure is correct."""
    print("\n" + "=" * 70)
    print("Checking Project Structure")
    print("=" * 70)
    
    required_dirs = [
        'src',
        'src/core',
        'src/utils',
        'data',
        'scripts',
        'examples'
    ]
    
    required_files = [
        'tobacco.py',
        'configuration.py',
        'requirements.txt',
        'README.md'
    ]
    
    all_ok = True
    
    print("\nRequired directories:")
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists() and dir_path.is_dir():
            print(f"  ✓ {dir_name}/")
        else:
            print(f"  ❌ {dir_name}/ - NOT FOUND")
            all_ok = False
    
    print("\nRequired files:")
    for file_name in required_files:
        file_path = Path(file_name)
        if file_path.exists() and file_path.is_file():
            print(f"  ✓ {file_name}")
        else:
            print(f"  ❌ {file_name} - NOT FOUND")
            all_ok = False
    
    return all_ok


def check_databases():
    """Check if databases are available."""
    print("\n" + "=" * 70)
    print("Checking Databases")
    print("=" * 70)
    
    data_dir = Path('data')
    
    # Check for JSON databases (faster)
    json_dbs = [
        'edges_database.json',
        'nodes_database.json',
        'template_database.json'
    ]
    
    print("\nJSON databases (recommended):")
    json_ok = True
    for db_name in json_dbs:
        db_path = data_dir / db_name
        if db_path.exists():
            size = db_path.stat().st_size / 1024  # KB
            print(f"  ✓ {db_name} ({size:.1f} KB)")
        else:
            print(f"  - {db_name} - not found")
            json_ok = False
    
    if not json_ok:
        print("\n  💡 Tip: Export databases to JSON for faster access:")
        print("     python scripts/export_databases_to_json.py")
    
    # Check for CIF databases (original)
    cif_dbs = [
        'edges_database',
        'nodes_database',
        'template_database'
    ]
    
    print("\nCIF databases (original):")
    for db_name in cif_dbs:
        db_path = data_dir / db_name
        if db_path.exists() and db_path.is_dir():
            cif_count = len(list(db_path.glob('*.cif')))
            print(f"  ✓ {db_name}/ ({cif_count} CIF files)")
        else:
            print(f"  - {db_name}/ - not found")


def test_import():
    """Test if ToBaCCo can be imported."""
    print("\n" + "=" * 70)
    print("Testing ToBaCCo Import")
    print("=" * 70)
    
    try:
        from src import generate_cif
        print("\n✓ ToBaCCo API can be imported successfully")
        print("  Function 'generate_cif' is available")
        return True
    except ImportError as e:
        print(f"\n❌ Failed to import ToBaCCo API: {e}")
        return False


def main():
    """Run all checks."""
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║" + " " * 20 + "ToBaCCo Installation Checker" + " " * 20 + "║")
    print("╚" + "═" * 68 + "╝\n")
    
    results = {
        'Python Version': check_python_version(),
        'Dependencies': check_dependencies(),
        'Project Structure': check_project_structure(),
        'ToBaCCo Import': test_import()
    }
    
    # Optional checks (don't affect overall status)
    check_optional_dependencies()
    check_databases()
    
    # Summary
    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)
    
    all_passed = all(results.values())
    
    for check, passed in results.items():
        status = "✓ PASS" if passed else "❌ FAIL"
        print(f"{status}: {check}")
    
    if all_passed:
        print("\n" + "╔" + "═" * 68 + "╗")
        print("║" + " " * 15 + "✓ Installation is complete and working!" + " " * 15 + "║")
        print("╚" + "═" * 68 + "╝")
        print("\n💡 Next steps:")
        print("   1. Export databases: python scripts/export_databases_to_json.py")
        print("   2. Try an example: python examples/quick_start.py")
        print("   3. Read the docs: README.md and examples/README.md\n")
        return 0
    else:
        print("\n" + "╔" + "═" * 68 + "╗")
        print("║" + " " * 12 + "❌ Installation has issues - see above" + " " * 13 + "║")
        print("╚" + "═" * 68 + "╝")
        print("\n💡 Troubleshooting:")
        print("   1. Check Python version: python --version")
        print("   2. Install dependencies: pip install -r requirements.txt")
        print("   3. See INSTALLATION.md for detailed instructions\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
