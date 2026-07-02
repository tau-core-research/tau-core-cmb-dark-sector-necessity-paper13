#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FRONTIER_V05 = ROOT / "data/derived/tau_cmb_endpoint_blind_physical_value_source_frontier_recompute_summary_v05.json"
ACOUSTIC_COORDINATE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_acoustic_v01.csv"
ACOUSTIC_EVALUATION = ROOT / "data/derived/tau_cmb_acoustic_reduced_evaluation_summary_v01.csv"
ACOUSTIC_BENCHMARK = ROOT / "data/derived/tau_cmb_acoustic_role_reduced_benchmark_summary_v01.csv"
DEFAULT_SUPPLY = ROOT / "physical_value_source_supplies/e_acoustic/acoustic_response_bundle_explicit_fail_supply_v01.json"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_acoustic_response_bundle_or_explicit_fail_supply_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_acoustic_response_bundle_or_explicit_fail_supply_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_acoustic_response_bundle_or_explicit_fail_supply_v01_"
    "acoustic_direct_rows_explicit_fail_no_acoustic_source_no_score_no_likelihood_no_verdict"
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
    if not FRONTIER_V05.exists() or not ACOUSTIC_COORDINATE.exists() or not ACOUSTIC_EVALUATION.exists() or not ACOUSTIC_BENCHMARK.exists():
        return False
    frontier = load_json(FRONTIER_V05)
    return (
        frontier.get("status") == "CMB_ENDPOINT_BLIND_PHYSICAL_VALUE_SOURCE_FRONTIER_RECOMPUTED_DELTA_NEFF_EXPLICIT_FAILS_ACCEPTED"
        and frontier.get("next_minimal_unblock") == "tau_cmb_acoustic_response_bundle_or_explicit_fail_supply_v01"
        and frontier.get("explicit_fail_accepted_rows") == 9
        and frontier.get("open_frontier_rows") == 7
        and frontier.get("physical_value_source_accepted_rows") == 0
        and text_contains(ACOUSTIC_COORDINATE, "BLOCKED_OSCILLATOR_RESPONSE_NOT_EVALUATED")
        and text_contains(ACOUSTIC_COORDINATE, "BLOCKED_AMPLITUDE_NOT_AVAILABLE")
        and text_contains(ACOUSTIC_COORDINATE, "BLOCKED_COUPLING_SIGN_MISSING")
        and text_contains(ACOUSTIC_EVALUATION, "ACOUSTIC_REDUCED_EVALUATION_PARTIAL_SCORE_BLOCKED")
        and text_contains(ACOUSTIC_BENCHMARK, "ACOUSTIC_REDUCED_BENCHMARK_DECLARED_NOT_EVALUATED")
    )


def supply_payload() -> dict[str, Any]:
    return {
        "artifact_status": "ACOUSTIC_RESPONSE_BUNDLE_EXPLICIT_FAIL_SUPPLIED_NO_ENDPOINT_BLIND_ACOUSTIC_SOURCE",
        "claim_boundary": CLAIM_BOUNDARY,
        "target_role": "acoustic",
        "coordinate_symbol": "e_acoustic",
        "coordinate_components_affected": [
            "phase_support",
            "relative_peak_height",
            "baryon_loading_coupling",
        ],
        "formal_slots": [
            "phase_tau_acoustic",
            "height_ratio_tau_acoustic",
            "coupling_sign_tau_baryon",
        ],
        "supply_type": "explicit_fail_evidence",
        "numeric_value_supplied": False,
        "unit_or_convention": "not_applicable_explicit_fail",
        "provenance": {
            "frontier_v05": rel(FRONTIER_V05),
            "acoustic_coordinate": rel(ACOUSTIC_COORDINATE),
            "acoustic_evaluation": rel(ACOUSTIC_EVALUATION),
            "acoustic_benchmark": rel(ACOUSTIC_BENCHMARK),
        },
        "replay": "make tau-cmb-endpoint-blind-physical-value-source-frontier-recompute-v05 && make tau-cmb-acoustic-response-bundle-or-explicit-fail-supply",
        "endpoint_blind_attestation": True,
        "forbidden_input_attestation": True,
        "forbidden_inputs": [
            "CMB endpoint residuals",
            "ACT/Planck likelihood errors",
            "score outputs",
            "post-endpoint tuning fields",
            "dark-sector verdict labels",
        ],
        "required_missing_objects": [
            "endpoint-blind Tau acoustic source S_tau_ac(k,a)",
            "accepted recombination-era driving source or equivalent",
            "endpoint-blind amplitude normalization A_tau or equivalent",
            "photon-baryon oscillator response equation or Green function",
            "baryon-loading coupling law and sign convention",
            "shared gauge/domain/convention",
        ],
        "prior_explicit_fail_interactions": [
            "Phi_tau_eff(a,k)|recombination explicit fail",
            "Phi_tau_eff(a,k) lensing source explicit fail",
            "endpoint_blind(A_tau) explicit fail",
        ],
        "physical_value_source_supplied": False,
        "explicit_fail_supplied": True,
        "physical_value_source_accepted": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "failure_statements": {
            "phase_support": (
                "No endpoint-blind Tau-side acoustic source, accepted recombination-era driving source, "
                "or oscillator response equation / Green function is supplied from which phase_tau_acoustic can be derived."
            ),
            "relative_peak_height": (
                "No endpoint-blind Tau-side amplitude normalization, accepted acoustic source response, "
                "or photon-baryon oscillator coupling is supplied from which height_ratio_tau_acoustic can be formed."
            ),
            "baryon_loading_coupling": (
                "No endpoint-blind Tau-source baryon-loading coupling law and associated sign convention is supplied; "
                "a sign label alone is not a physical value-source."
            ),
        },
        "nonclaims": [
            "This is not a claim that Tau Core has no acoustic effect.",
            "This is not a CMB peak phase fit or mismatch.",
            "This is not a peak-height likelihood result.",
            "This is not an empirical validation or exclusion.",
            "This is not a dark-sector verdict.",
        ],
    }


def build_summary(supply_path: Path) -> dict[str, Any]:
    hash_path = supply_path.with_suffix(".hashes.json")
    hash_matches = supply_path.exists() and hash_path.exists() and load_json(hash_path).get("sha256") == sha256(supply_path)
    return {
        "report_id": "tau_cmb_acoustic_response_bundle_or_explicit_fail_supply_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "supply_artifact": rel(supply_path),
        "supply_hash_artifact": rel(hash_path),
        "input_frontier_recompute_v05": rel(FRONTIER_V05),
        "input_acoustic_coordinate": rel(ACOUSTIC_COORDINATE),
        "input_acoustic_evaluation": rel(ACOUSTIC_EVALUATION),
        "input_acoustic_benchmark": rel(ACOUSTIC_BENCHMARK),
        "input_chain_clean": input_chain_clean(),
        "target_role": "acoustic",
        "affected_frontier_rows": 3,
        "explicit_fail_supplied": True,
        "numeric_value_supplied": False,
        "physical_value_source_accepted": False,
        "acoustic_score_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "supply_hash_matches": hash_matches,
        "status": (
            "CMB_ACOUSTIC_RESPONSE_BUNDLE_EXPLICIT_FAIL_SUPPLIED_NO_SCORE"
            if input_chain_clean() and hash_matches
            else "CMB_ACOUSTIC_RESPONSE_BUNDLE_EXPLICIT_FAIL_SUPPLY_NONCANONICAL_RESULT"
        ),
        "next_minimal_unblock": "tau_cmb_acoustic_response_bundle_explicit_fail_acceptance_audit_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Acoustic Response Bundle or Explicit Fail Supply v01

**Doc class:** acoustic source explicit fail supply
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
acoustic_score_allowed={summary["acoustic_score_allowed"]}
likelihood_allowed={summary["likelihood_allowed"]}
dark_sector_verdict_allowed={summary["dark_sector_verdict_allowed"]}
```

This supplies explicit fail evidence for the absence of an accepted
endpoint-blind Tau acoustic source bundle. It closes only the direct acoustic
phase, relative-height, and baryon-loading coupling rows as non-score failures.
It is not a CMB peak fit, acoustic likelihood, or dark-sector verdict.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Supply explicit fail evidence for Tau CMB acoustic response direct rows.")
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
