#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str], cwd: Path = ROOT) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, check=True)


def main() -> None:
    run(["python", "scripts/build_cmb_constraint_map.py"])
    tectonic = shutil.which("tectonic")
    if tectonic:
        run([tectonic, "main.tex"], cwd=ROOT / "paper13_submission_source")
    else:
        print("warning: tectonic not found; skipping PDF build")
    run(["python", "scripts/build_arxiv_source.py"])
    run(["python", "scripts/validate_protocol_manifests.py"])
    run(["pytest", "-q"])
    print("PAPER13_REPRODUCTION_COMPLETE")


if __name__ == "__main__":
    main()
