#!/usr/bin/env python3
"""
Build script for Med-Jeopardy vertical deployments.

Creates separate executables for each vertical:
- MedJeopardy-Boards (Board Study Edition)
- MedJeopardy-GME (GME/Residency Edition)
- MedJeopardy-CME (CME/CE Edition)
- MedJeopardy (Generic Edition)

Usage:
    python build_verticals.py              # Build all verticals
    python build_verticals.py boards       # Build only Boards edition
    python build_verticals.py gme cme      # Build GME and CME editions
"""

import subprocess
import sys
import os
import shutil
import platform
from pathlib import Path

# Vertical configurations
VERTICALS = {
    "boards": {
        "name": "MedJeopardy-Boards",
        "entry": "run_boards.py",
        "bundle_id": "io.onehealth.medjeopardy.boards",
        "description": "Board Study Edition"
    },
    "gme": {
        "name": "MedJeopardy-GME",
        "entry": "run_gme.py",
        "bundle_id": "io.onehealth.medjeopardy.gme",
        "description": "GME/Residency Edition"
    },
    "cme": {
        "name": "MedJeopardy-CME",
        "entry": "run_cme.py",
        "bundle_id": "io.onehealth.medjeopardy.cme",
        "description": "CME/CE Edition"
    },
    "generic": {
        "name": "MedJeopardy",
        "entry": "run.py",
        "bundle_id": "io.onehealth.medjeopardy",
        "description": "Generic Medical Jeopardy"
    }
}


def generate_spec(vertical_key: str, output_dir: str = "dist") -> str:
    """Generate a PyInstaller spec file for a specific vertical."""
    config = VERTICALS[vertical_key]
    uname = platform.uname()
    arch = uname.machine
    icon_ext = "icns" if uname.system == "Darwin" else "ico"
    iconfile = f"resources/icon.{icon_ext}"

    spec_content = f'''# Auto-generated spec file for {config["description"]}
import sys, platform
sys.path.append('')
from jparty.version import version

uname = platform.uname()
arch = uname.machine
iconfile = "{iconfile}"

a = Analysis(['{config["entry"]}'],
             pathex=['.'],
             binaries=[],
             datas=[
                 ("jparty/data/*", "data"),
                 ("jparty/buzzer", "buzzer"),
             ],
             hiddenimports=["qrcode"],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=None,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=None)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='{config["name"]}',
          debug=False,
          bootloader_ignore_signals=False,
          target_arch=arch,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False, icon=iconfile)

if uname.system == "Darwin":
    app = BUNDLE(exe,
                 name='{config["name"]}.app',
                 version=version,
                 icon=iconfile,
                 bundle_identifier='{config["bundle_id"]}')

print(f"Built {config["name"]} for {{uname.system}} with architecture {{arch}}")
'''

    spec_path = f'{config["name"]}.spec'
    with open(spec_path, 'w') as f:
        f.write(spec_content)

    return spec_path


def build_vertical(vertical_key: str) -> bool:
    """Build a specific vertical."""
    config = VERTICALS[vertical_key]
    print(f"\n{'='*60}")
    print(f"Building {config['name']} ({config['description']})")
    print(f"{'='*60}")

    # Check if entry point exists
    if not os.path.exists(config["entry"]):
        print(f"Error: Entry point {config['entry']} not found")
        return False

    # Generate spec file
    spec_path = generate_spec(vertical_key)
    print(f"Generated spec file: {spec_path}")

    # Run PyInstaller
    try:
        result = subprocess.run(
            ["pyinstaller", "-y", spec_path],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"Successfully built {config['name']}")
            return True
        else:
            print(f"Build failed for {config['name']}")
            print(result.stderr)
            return False

    except FileNotFoundError:
        print("Error: PyInstaller not found. Install with: pip install pyinstaller")
        return False


def build_all():
    """Build all verticals."""
    results = {}
    for vertical in VERTICALS:
        results[vertical] = build_vertical(vertical)

    print(f"\n{'='*60}")
    print("Build Summary")
    print(f"{'='*60}")
    for vertical, success in results.items():
        status = "SUCCESS" if success else "FAILED"
        print(f"  {VERTICALS[vertical]['name']}: {status}")

    return all(results.values())


def main():
    if len(sys.argv) > 1:
        # Build specific verticals
        verticals_to_build = sys.argv[1:]
        results = {}
        for v in verticals_to_build:
            if v not in VERTICALS:
                print(f"Unknown vertical: {v}")
                print(f"Available verticals: {', '.join(VERTICALS.keys())}")
                sys.exit(1)
            results[v] = build_vertical(v)

        # Print summary and exit with appropriate code
        if len(results) > 1:
            print(f"\n{'='*60}")
            print("Build Summary")
            print(f"{'='*60}")
            for vertical, success in results.items():
                status = "SUCCESS" if success else "FAILED"
                print(f"  {VERTICALS[vertical]['name']}: {status}")

        # Exit with non-zero if any build failed
        if not all(results.values()):
            sys.exit(1)
    else:
        # Build all verticals
        success = build_all()
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
