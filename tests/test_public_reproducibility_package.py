from __future__ import annotations

import csv
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_required_files_exist() -> None:
    required = [
        "README.md",
        "DATA_NOTICE.md",
        "LICENSE",
        "CITATION.cff",
        "requirements.txt",
        "paper13_submission_source/main.tex",
        "paper13_submission_source/refs.bib",
        "docs/cmb_constraint_map_v01.md",
        "data/source_manifest/cmb_external_reference_manifest_v01.csv",
        "data/source_manifest/tau_core_cmb_decision_ladder_v01.csv",
        "data/derived/cmb_constraint_map_v01.csv",
        "data/derived/tau_core_dark_sector_requirement_map_v01.csv",
        "data/derived/paper13_readiness_summary_v01.csv",
        "scripts/build_cmb_constraint_map.py",
        "scripts/build_arxiv_source.py",
        "scripts/validate_protocol_manifests.py",
        "scripts/reproduce.py",
        "arxiv_submission_source.zip",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_cmb_constraint_map_blocks_verdicts() -> None:
    constraints = list(csv.DictReader((ROOT / "data/derived/cmb_constraint_map_v01.csv").open()))
    requirements = list(csv.DictReader((ROOT / "data/derived/tau_core_dark_sector_requirement_map_v01.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/paper13_readiness_summary_v01.csv").open()))
    assert len(constraints) == 5
    assert len(requirements) == 5
    assert sum(row["necessity_pressure"] == "HIGH" for row in constraints) == 4
    assert {row["current_protocol_status"] for row in constraints} == {"MAPPED_NOT_SOLVED"}
    assert all(row["allows_dark_sector_verdict"] == "false" for row in requirements)
    assert sum(row["blocks_no_dark_claim"] == "true" for row in requirements) == 4
    assert summary == [
        {
            "summary_id": "PAPER13_CMB_CONSTRAINT_MAP_V01",
            "external_references_registered": "3",
            "cmb_constraints_mapped": "5",
            "requirements_written": "5",
            "high_pressure_constraints": "4",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_verdict_allowed": "false",
            "overall_status": "CMB_CONSTRAINTS_MAP_TO_TAU_RESPONSE_REQUIREMENTS_VERDICT_BLOCKED",
            "next_required_artifact": "tau_cmb_effective_source_equation_v01",
            "claim_boundary": "paper13_cmb_constraint_map_only_no_likelihood_no_dark_sector_verdict",
        }
    ]


def test_manuscript_scope_and_no_overclaim() -> None:
    text = (ROOT / "paper13_submission_source/main.tex").read_text()
    assert "CMB Constraint Mapping" in text
    assert "does not claim that Tau Core explains the CMB" in text
    forbidden_absent = [
        "We show that Tau Core explains the CMB",
        "We show that dark matter does not exist",
        "we detect a Tau dark-sector field",
    ]
    for phrase in forbidden_absent:
        assert phrase not in text


def test_arxiv_zip_is_source_only() -> None:
    with zipfile.ZipFile(ROOT / "arxiv_submission_source.zip") as archive:
        names = set(archive.namelist())
    assert "main.tex" in names
    assert "refs.bib" in names
    assert "main.pdf" not in names
    assert not any(name.endswith(".aux") or name.endswith(".log") for name in names)
