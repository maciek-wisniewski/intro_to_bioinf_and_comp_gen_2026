#!/usr/bin/env python3
"""Install docking engine binaries (AutoDock Vina, optionally Smina) into ``./bin``.

Cross-platform: Windows, Linux and macOS (x86-64 and arm64/aarch64).

Usage
-----
    uv run scripts/install_docking_tools.py            # install Vina
    uv run scripts/install_docking_tools.py --smina    # also install Smina
    uv run scripts/install_docking_tools.py --plip     # also fetch PLIP source
    python scripts/install_docking_tools.py --dir bin  # without uv

The docking notebooks (``notebooks/docking_lab.ipynb`` and the solution) look for
the ``vina`` binary on the ``PATH`` and in ``./bin`` / ``../bin``, so running this
once is enough. The notebooks can also download Vina on their own as a fallback.
"""
from __future__ import annotations

import argparse
import platform
import stat
import sys
import urllib.request
from pathlib import Path

VINA_VERSION = "1.2.5"
VINA_RELEASE = (
    f"https://github.com/ccsb-scripps/AutoDock-Vina/releases/download/v{VINA_VERSION}"
)

# SourceForge "download" links resolve (via -L / urllib redirects) to the file.
SMINA_URLS = {
    "Linux": "https://sourceforge.net/projects/smina/files/smina.static/download",
    "Darwin": "https://sourceforge.net/projects/smina/files/smina.osx/download",
}


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _platform_tag() -> tuple[str, str]:
    """Return (system, arch) where arch is 'aarch64' or 'x86_64'."""
    system = platform.system()
    machine = platform.machine().lower()
    arch = "aarch64" if machine in ("arm64", "aarch64") else "x86_64"
    return system, arch


def vina_asset() -> tuple[str, str]:
    """Return (release_asset_name, local_binary_name) for the current platform."""
    system, arch = _platform_tag()
    if system == "Windows":
        return f"vina_{VINA_VERSION}_win.exe", "vina.exe"
    if system == "Darwin":
        return f"vina_{VINA_VERSION}_mac_{arch}", "vina"
    if system == "Linux":
        return f"vina_{VINA_VERSION}_linux_{arch}", "vina"
    raise RuntimeError(f"Unsupported operating system: {system!r}")


def _make_executable(path: Path) -> None:
    if platform.system() != "Windows":
        mode = path.stat().st_mode
        path.chmod(mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)


def _download(url: str, dest: Path) -> None:
    print(f"  downloading {url}")
    print(f"  -> {dest}")
    urllib.request.urlretrieve(url, dest)


def install_vina(bin_dir: Path) -> Path:
    asset, local_name = vina_asset()
    dest = bin_dir / local_name
    _download(f"{VINA_RELEASE}/{asset}", dest)
    _make_executable(dest)
    return dest


def install_smina(bin_dir: Path) -> Path | None:
    system = platform.system()
    url = SMINA_URLS.get(system)
    if url is None:
        print(f"  Smina has no prebuilt binary for {system}; skipping.")
        print("  (Use Vina, or build Smina from https://sourceforge.net/projects/smina/)")
        return None
    local_name = "smina.exe" if system == "Windows" else "smina"
    dest = bin_dir / local_name
    try:
        _download(url, dest)
        _make_executable(dest)
    except Exception as exc:  # network / SourceForge hiccup
        print(f"  Failed to download Smina: {exc}")
        return None
    return dest


def install_plip(bin_dir: Path) -> Path | None:
    """Clone the PLIP source into ``bin_dir/plip`` (pure-Python, added to PYTHONPATH).

    PLIP itself has no wheel and its sdist tries to build OpenBabel at install
    time, so we use the documented "PYTHONPATH" route instead. OpenBabel is
    provided cross-platform by the ``openbabel-wheel`` dependency (``uv sync``).
    """
    import shutil as _shutil
    import subprocess

    target = bin_dir / "plip"
    if (target / "plip").is_dir():
        print(f"  PLIP already present: {target}")
        return target
    git = _shutil.which("git")
    if git is None:
        print("  git not found; cannot fetch PLIP. Install git and retry.")
        return None
    try:
        subprocess.run(
            [git, "clone", "--depth", "1",
             "https://github.com/pharmai/plip.git", str(target)],
            check=True,
        )
    except Exception as exc:
        print(f"  Failed to clone PLIP: {exc}")
        return None
    print("  Reminder: OpenBabel comes from 'openbabel-wheel' (run 'uv sync').")
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dir",
        default=None,
        help="Target directory for the binaries (default: <repo>/bin)",
    )
    parser.add_argument(
        "--smina",
        action="store_true",
        help="Also install Smina (Linux/macOS only).",
    )
    parser.add_argument(
        "--plip",
        action="store_true",
        help="Also fetch PLIP (Protein-Ligand Interaction Profiler) source.",
    )
    args = parser.parse_args(argv)

    bin_dir = Path(args.dir).resolve() if args.dir else _repo_root() / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)

    system, arch = _platform_tag()
    print(f"Platform: {system} ({arch}); installing into {bin_dir}")

    print("Installing AutoDock Vina...")
    vina_path = install_vina(bin_dir)
    print(f"  Vina ready: {vina_path}")

    if args.smina:
        print("Installing Smina...")
        smina_path = install_smina(bin_dir)
        if smina_path:
            print(f"  Smina ready: {smina_path}")

    if args.plip:
        print("Fetching PLIP source...")
        plip_path = install_plip(bin_dir)
        if plip_path:
            print(f"  PLIP ready: {plip_path}")

    print("\nDone. The docking notebooks will pick this up automatically.")
    print(f"If needed, add to PATH:  {bin_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
