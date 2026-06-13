#!/usr/bin/env python3
from __future__ import annotations

import csv
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_external_reference_manifest() -> None:
    rows = read_csv(ROOT / "data/source_manifest/cmb_external_reference_manifest_v01.csv")
    require(len(rows) == 3, "expected three external CMB references")
    require({row["citation_key"] for row in rows} == {"planck2018parameters", "actdr6lensing", "actdr6extended"}, "reference keys mismatch")
    require(all(row["claim_boundary"] == "external_reference_only_no_tau_core_validation" for row in rows), "external refs cannot validate Tau Core")


def validate_decision_ladder() -> None:
    rows = read_csv(ROOT / "data/source_manifest/tau_core_cmb_decision_ladder_v01.csv")
    require([row["decision_id"] for row in rows] == ["TC0", "TC1", "TC2"], "decision ladder order mismatch")
    forbidden = " ".join(row["forbidden_interpretation"] for row in rows).lower()
    require("galaxy-rotation fit alone" in forbidden, "ladder must forbid galaxy-only CMB conclusion")
    require("tau field detected" in forbidden, "ladder must forbid detection overclaim")
    require(all(row["claim_boundary"] == "no_verdict_without_cmb_likelihood" for row in rows), "decision ladder must block verdicts")


def validate_cmb_constraint_map() -> None:
    constraints = read_csv(ROOT / "data/derived/cmb_constraint_map_v01.csv")
    requirements = read_csv(ROOT / "data/derived/tau_core_dark_sector_requirement_map_v01.csv")
    summary = read_csv(ROOT / "data/derived/paper13_readiness_summary_v01.csv")
    require(len(constraints) == 5, "expected five mapped CMB constraints")
    require(len(requirements) == 5, "expected five Tau Core requirements")
    require(sum(row["necessity_pressure"] == "HIGH" for row in constraints) == 4, "expected four high-pressure constraints")
    require(all(row["current_protocol_status"] == "MAPPED_NOT_SOLVED" for row in constraints), "constraints must remain unsolved")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in requirements), "requirements cannot allow verdicts")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in requirements) == 4, "expected four no-dark blockers")
    require(len(summary) == 1, "summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "PAPER13_CMB_CONSTRAINT_MAP_V01", "summary id mismatch")
    require(row["external_references_registered"] == "3", "reference count mismatch")
    require(row["cmb_constraints_mapped"] == "5", "constraint count mismatch")
    require(row["requirements_written"] == "5", "requirement count mismatch")
    require(row["high_pressure_constraints"] == "4", "high-pressure count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_verdict_allowed"] == "false", "Tau response verdict must be blocked")
    require(row["next_required_artifact"] == "tau_cmb_effective_source_equation_v01", "next artifact mismatch")


def validate_arxiv_zip() -> None:
    path = ROOT / "arxiv_submission_source.zip"
    require(path.exists(), "missing arxiv source zip")
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
    require("main.tex" in names, "arxiv zip missing main.tex")
    require("refs.bib" in names, "arxiv zip missing refs.bib")
    require("main.pdf" not in names, "arxiv zip must not include PDF")


def main() -> None:
    validate_external_reference_manifest()
    validate_decision_ladder()
    validate_cmb_constraint_map()
    validate_arxiv_zip()
    print("PAPER13_PROTOCOL_MANIFESTS_VALID")


if __name__ == "__main__":
    main()
