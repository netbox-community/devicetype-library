"""Test-suite package.

Strips the repo root / cwd from ``sys.path`` (GHSA-wwg5-825x-83g6) so a top-level
module added in a pull request cannot shadow an installed package during the
harness's bare imports (e.g. ``from git import ...``). Importing this package
runs before any of its submodules, and before ``python -m tests.generate_slug_list``
reaches its third-party imports.
"""
import os
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[:] = [p for p in sys.path if p not in ("", ".") and os.path.abspath(p) != _ROOT]
