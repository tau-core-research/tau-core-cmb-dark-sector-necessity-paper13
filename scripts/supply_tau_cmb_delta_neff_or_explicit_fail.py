#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FRONTIER_V04 = ROOT / "data/derived/tau_cmb_endpoint_blind_physical_value_source_frontier_recompute_summary_v04.json"
RADIATION_COORDINATE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_radiation_v01.csv"
RADIATION_BOUND = ROOT / "data/derived/tau_cmb_radiation_guard_bound_check_summary_v01.csv"
RADIATION_EVALUATION = ROOT / "data/derived/tau_cmb_radiation_guard_evaluation_summary_v01.csv"
DEFAULT_SUPPLY = ROOT / "physical_value_source_supplies/e_radiation/delta_neff_explicit_fail_supply_v01.json"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_delta_neff_or_explicit_fail_supply_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_delta_neff_or_explicit_fail_supply_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_delta_neff_or_explicit_fail_supply_v01_"
    "radiation_direct_rows_explicit_fail_no_delta_neff_no_bound_eval_no_score_no_likelihood_no_verdict"
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


def text_contains(path: Path, token: str) -> bool:
    return path.exists() and token in path.read_text(encoding="utf-8")


def input_chain_clean() -> bool:
    if not FRONTIER_V04.exists() or not RADIATION_COORDINATE.exists() or not RADIATION_BOUND.exists() or not RADIATION_EVALUATION.exists():
        return False
    frontier = load_json(FRONTIER_V04)
    return (
        frontier.get("status") == "CMB_ENDPOINT_BLIND_PHYSICAL_VALUE_SOURCE_FRONTIER_RECOMPUTED_DENSITY_EXPLICIT_FAILS_ACCEPTED"
        and frontier.get("next_minimal_unblock") == "tau_cmb_delta_neff_or_explicit_fail_supply_v01"
        and frontier.get("explicit_fail_accepted_rows") == 7
        and frontier.get("open_frontier_rows") == 9
        and frontier.get("physical_value_source_accepted_rows") == 0
        and text_contains(RADIATION_COORDINATE, "BLOCKED_TAU_DELTA_NEFF_NOT_DERIVED")
        and text_contains(RADIATION_COORDINATE, "BLOCKED_BOUND_INEQUALITY_NOT_EVALUATED")
        and text_contains(RADIATION_BOUND, "RADIATION_GUARD_BOUND_CHECK_DECLARED_NOT_EVALUATED")
        and text_contains(RADIATION_EVALUATION, "RADIATION_GUARD_EVALUATION_PARTIAL_SCORE_BLOCKED")
    )


def supply_payload() -> dict[str, Any]:
    return {
        "artifact_status": "DELTA_NEFF_EXPLICIT_FAIL_SUPPLIED_NO_ENDPOINT_BLIND_RADIATION_SOURCE",
        "claim_boundary": CLAIM_BOUNDARY,
        "target_role": "radiation",
        "coordinate_symbol": "e_radiation",
        "coordinate_components_affected": [
            "tau_radiation_like_contribution",
            "damping_tail_inequality",
        ],
        "formal_slots": [
            "Delta_N_eff_tau",
            "Delta_N_eff_tau <= Delta_N_eff_bound",
        ],
        "supply_type": "explicit_fail_evidence",
        "numeric_value_supplied": False,
        "unit_or_convention": "not_applicable_explicit_fail",
        "provenance": {
            "frontier_v04": rel(FRONTIER_V04),
            "radiation_coordinate": rel(RADIATION_COORDINATE),
            "radiation_bound_check": rel(RADIATION_BOUND),
            "radiation_evaluation": rel(RADIATION_EVALUATION),
        },
        "replay": "make tau-cmb-endpoint-blind-physical-value-source-frontier-recompute-v04 && make tau-cmb-delta-neff-or-explicit-fail-supply",
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
        "failure_statement": (
            "No endpoint-blind Tau-side radiation-like stress-energy or energy-density mapping is accepted, "
            "so Delta_N_eff_tau is not derived. The damping-tail inequality is therefore non-evaluable because "
            "the left-hand side and shared bound convention are not accepted."
        ),
        "nonclaims": [
            "This is not a numerical Delta_N_eff_tau = 0 statement.",
            "This is not bound satisfaction.",
            "This is not bound violation.",
            "This is not a CMB likelihood result.",
            "This is not a dark-sector verdict.",
        ],
    }


def build_summary(supply_path: Path) -> dict[str, Any]:
    hash_path = supply_path.with_suffix(".hashes.json")
    hash_matches = supply_path.exists() and hash_path.exists() and load_json(hash_path).get("sha256") == sha256(supply_path)
    return {
        "report_id": "tau_cmb_delta_neff_or_explicit_fail_supply_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "supply_artifact": rel(supply_path),
        "supply_hash_artifact": rel(hash_path),
        "input_frontier_recompute_v04": rel(FRONTIER_V04),
        "input_radiation_coordinate": rel(RADIATION_COORDINATE),
        "input_radiation_bound_check": rel(RADIATION_BOUND),
        "input_radiation_evaluation": rel(RADIATION_EVALUATION),
        "input_chain_clean": input_chain_clean(),
        "target_role": "radiation",
        "affected_frontier_rows": 2,
        "explicit_fail_supplied": True,
        "numeric_value_supplied": False,
        "physical_value_source_accepted": False,
        "damping_tail_inequality_evaluable": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "supply_hash_matches": hash_matches,
        "status": (
            "CMB_DELTA_NEFF_EXPLICIT_FAIL_SUPPLIED_NO_SCORE"
            if input_chain_clean() and hash_matches
            else "CMB_DELTA_NEFF_EXPLICIT_FAIL_SUPPLY_NONCANONICAL_RESULT"
        ),
        "next_minimal_unblock": "tau_cmb_delta_neff_explicit_fail_acceptance_audit_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Delta Neff or Explicit Fail Supply v01

**Doc class:** radiation source explicit fail supply
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
damping_tail_inequality_evaluable={summary["damping_tail_inequality_evaluable"]}
score_entry_allowed={summary["score_entry_allowed"]}
likelihood_allowed={summary["likelihood_allowed"]}
dark_sector_verdict_allowed={summary["dark_sector_verdict_allowed"]}
```

This supplies explicit fail evidence for the absence of an accepted
endpoint-blind Tau-side radiation-like source from which
`Delta_N_eff_tau` can be derived. The damping-tail inequality is closed only
as non-evaluable under the current supply. This is not a numerical bound result.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Supply explicit fail evidence for Tau CMB Delta_N_eff radiation rows.")
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
