"""Shared by the tests: the plugin's scripts on the import path, and a way to run a script's main().

Nothing here uses the network or writes outside a temporary folder.
"""
import contextlib
import io
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "plugins" / "poiesis-frontier"
SKILL = PLUGIN / "skills" / "frontier"
SCRIPTS = SKILL / "scripts"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
sys.path.insert(0, str(SCRIPTS))
sys.dont_write_bytecode = True


def run(module, argv: list[str]) -> tuple[int, str, str]:
    """Run a script's main() with the given arguments; return (exit code, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    saved = sys.argv
    sys.argv = [module.__name__ + ".py", *argv]
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                code = module.main()
            except SystemExit as e:  # argparse errors and explicit exits
                code = e.code
    finally:
        sys.argv = saved
    return code, out.getvalue(), err.getvalue()
