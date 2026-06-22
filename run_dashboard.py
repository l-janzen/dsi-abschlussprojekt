#!/usr/bin/env python3

from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parent
APP_FILE = PROJECT_ROOT / "03_dashboard_app" / "V2" / "Streamlit_Hypertonie_V2.py"


def main() -> int:
    if not APP_FILE.exists():
        print(f"Streamlit app not found: {APP_FILE}", file=sys.stderr)
        return 1

    command = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(APP_FILE),
    ]

    command.extend(sys.argv[1:])
    return subprocess.call(command, cwd=PROJECT_ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
