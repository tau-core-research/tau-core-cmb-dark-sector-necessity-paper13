#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FRONTIER_V03 = ROOT / "data/derived/tau_cmb_endpoint_blind_physical_value_source_frontier_recompute_summary_v03.json"
DENSITY_DERIVATION = ROOT / "data/derived/tau_cmb_density_amplitude_derivation_summary_v01.csv"
DENSITY_CLOSURE = ROOT / "data/derived/tau_cmb_density_amplitude_closure_summary_v01.csv"
DEFAULT_SUPPLY = ROOT / "physical_value_source_supplies/e_density/density_source_amplitude_explicit_fail_supply_v01.json"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_density_source_amplitude_or_explicit_fail_supply_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_density_source_amplitude_or_explicit_fail_supply_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_density_source_amplitude_or_explicit_fail_supply_v01_"
    "density_direct_rows_explicit_fail_no_density_source_no_score_no_likelihood_no_verdict"
)


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def csv_contains(path: Path, token: str) -> bool:
    return path.exists() and token in path.read_text(encoding="utf-8")


def input_chain_clean() -> bool:
    if not FRONTIER_V03.exists() or not DENSITY_DERIVATION.exists() or not DENSITY_CLOSURE.exists():
        return False
    frontier = load_json(FRONTIER_V03)
    return (
        frontier.get("status") == "CMB_ENDPOINT_BLIND_PHYSICAL_VALUE_SOURCE_FRONTIER_RECOMPUTED_PHI_DIRECT_ROWS_EXPLICIT_FAIL_ACCEPTED"
        and frontier.get("next_minimal_unblock") == "tau_cmb_density_source_amplitude_or_explicit_fail_supply_v01"
        and frontier.get("explicit_fail_accepted_rows") == 4
        and frontier.get("open_frontier_rows") == 12
        and frontier.get("physical_value_source_accepted_rows") == 0
        and csv_contains(DENSITY_DERIVATION, "DENSITY_AMPLITUDE_DEFINITION_DECLARED_DERIVATION_AND_MATCH_BLOCKED")
        and csv_contains(DENSITY_CLOSURE, "DENSITY_AMPLITUDE_PARTIAL_CLOSURE_SCORE_BLOCKED")
    )


def supply_payload() -> dict[str, Any]:
    return {
        "artifact_status": "DENSITY_SOURCE_AMPLITUDE_EXPLICIT_FAIL_SUPPLIED_NO_ENDPOINT_BLIND_DENSITY_SOURCE",
        "claim_boundary": CLAIM_BOUNDARY,
        "target_role": "density",
        "coordinate_symbol": "e_density",
        "coordinate_components_affected": [
            "tau_effective_density",
            "endpoint_blind_amplitude",
            "omega_c_h2_role_comparison",
        ],
        "formal_slots": [
            "rho_tau_eff(a,k)",
            "endpoint_blind(A_tau)",
            "Omega_c h^2 comparison role",
        ],
        "supply_type": "explicit_fail_evidence",
        "numeric_value_supplied": False,
        "unit_or_convention": "not_applicable_explicit_fail",
        "provenance": {
            "frontier_v03": rel(FRONTIER_V03),
            "density_derivation": rel(DENSITY_DERIVATION),
            "density_closure": rel(DENSITY_CLOSURE),
        },
        "replay": "make tau-cmb-endpoint-blind-physical-value-source-frontier-recompute-v03 && make tau-cmb-density-source-amplitude-or-explicit-fail-supply",
        "endpoint_blind_attestation": True,
        "forbidden_input_attestation": True,
        "forbidden_inputs": [
            "CMB endpoint residuals",
            "ACT/Planck likelihood errors",
            "score outputs",
            "post-endpoint tuning fields",
            "dark-sector verdict labels",
        ],
        "physical_value_source_supplied": False,
        "explicit_fail_supplied": True,
        "physical_value_source_accepted": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "failure_statement": "No endpoint-blind rho_tau_eff(a,k), A_tau(a,k), or Omega_c h^2 comparison value is accepted: density derivation and match remain blocked and density closure remains partial.",
    }


def build_summary(supply_path: Path) -> dict[str, Any]:
    hash_path = supply_path.with_suffix(".hashes.json")
    hash_matches = supply_path.exists() and hash_path.exists() and load_json(hash_path).get("sha256") == sha256(supply_path)
    return {
        "report_id": "tau_cmb_density_source_amplitude_or_explicit_fail_supply_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "supply_artifact": rel(supply_path),
        "supply_hash_artifact": rel(hash_path),
        "input_frontier_recompute_v03": rel(FRONTIER_V03),
        "input_density_derivation": rel(DENSITY_DERIVATION),
        "input_density_closure": rel(DENSITY_CLOSURE),
        "input_chain_clean": input_chain_clean(),
        "target_role": "density",
        "affected_frontier_rows": 3,
        "explicit_fail_supplied": True,
        "numeric_value_supplied": False,
        "physical_value_source_accepted": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "supply_hash_matches": hash_matches,
        "status": (
            "CMB_DENSITY_SOURCE_AMPLITUDE_EXPLICIT_FAIL_SUPPLIED_NO_SCORE"
            if input_chain_clean() and hash_matches
            else "CMB_DENSITY_SOURCE_AMPLITUDE_EXPLICIT_FAIL_SUPPLY_NONCANONICAL_RESULT"
        ),
        "next_minimal_unblock": "tau_cmb_density_source_amplitude_explicit_fail_acceptance_audit_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Density Source Amplitude or Explicit Fail Supply v01

**Doc class:** density source explicit fail supply
**Reader role:** Paper 13 / CMB scoring route reviewer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Summary

```text
target_role={summary["target_role"]}
affected_frontier_rows={summary["affected_frontier_rows"]}
explicit_fail_supplied={summary["explicit_fail_supplied"]}
numeric_value_supplied={summary["numeric_value_supplied"]}
physical_value_source_accepted={summary["physical_value_source_accepted"]}
score_entry_allowed={summary["score_entry_allowed"]}
likelihood_allowed={summary["likelihood_allowed"]}
dark_sector_verdict_allowed={summary["dark_sector_verdict_allowed"]}
```

This supplies explicit fail evidence for the absence of accepted endpoint-blind
density source/amplitude/comparison values. It is not a physical density score.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Supply explicit fail evidence for Tau CMB density source/amplitude rows.")
    parser.add_argument("--write-artifact", nargs="?", const=str(DEFAULT_SUPPLY))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    supply_path = Path(args.write_artifact) if args.write_artifact else DEFAULT_SUPPLY
    if args.write_artifact:
        write_json(supply_path, supply_payload())
        write_json(
            supply_path.with_suffix(".hashes.json"),
            {
                "target": rel(supply_path),
                "sha256": sha256(supply_path),
                "claim_boundary": CLAIM_BOUNDARY,
                "explicit_fail_supplied": True,
                "physical_value_source_accepted": False,
                "score_entry_allowed": False,
            },
        )
    summary = build_summary(supply_path)
    if args.write_summary:
        summary_path = Path(args.write_summary)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_doc:
        write_doc(Path(args.write_doc), summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
