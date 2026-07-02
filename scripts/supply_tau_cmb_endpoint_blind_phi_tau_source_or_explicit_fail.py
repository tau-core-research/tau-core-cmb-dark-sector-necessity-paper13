#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
UNBLOCK_PLAN = ROOT / "data/derived/tau_cmb_physical_source_dependency_unblock_plan_summary_v01.json"
PHI_CONTRACT = ROOT / "data/derived/tau_cmb_endpoint_blind_phi_tau_derivation_contract_summary_v01.csv"
PHI_HANDOFF = ROOT / "data/derived/tau_cmb_effective_potential_source_handoff_summary_v01.csv"
PHI_PAYLOAD_CANDIDATE = ROOT / "data/derived/tau_cmb_phi_tau_parent_input_concrete_payload_candidate_summary_v01.csv"
DEFAULT_SUPPLY = ROOT / "physical_value_source_supplies/e_shared/phi_tau_eff_explicit_fail_supply_v01.json"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_endpoint_blind_phi_tau_source_or_explicit_fail_supply_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_endpoint_blind_phi_tau_source_or_explicit_fail_supply_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_endpoint_blind_phi_tau_source_or_explicit_fail_supply_v01_"
    "shared_phi_explicit_fail_no_phi_source_no_score_no_likelihood_no_verdict"
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
    if not UNBLOCK_PLAN.exists() or not PHI_CONTRACT.exists() or not PHI_HANDOFF.exists() or not PHI_PAYLOAD_CANDIDATE.exists():
        return False
    plan = load_json(UNBLOCK_PLAN)
    return (
        plan.get("status") == "CMB_PHYSICAL_SOURCE_DEPENDENCY_UNBLOCK_PLAN_ACCEPTED_PRIORITIZED_NO_SCORE"
        and plan.get("top_priority_target") == "Phi_tau_eff(a,k)"
        and plan.get("physical_value_source_accepted_rows") == 0
        and plan.get("physical_CMB_score_allowed") is False
        and csv_contains(PHI_CONTRACT, "ENDPOINT_BLIND_PHI_TAU_DERIVATION_CONTRACT_DECLARED_UNSATISFIED")
        and csv_contains(PHI_HANDOFF, "EFFECTIVE_POTENTIAL_SOURCE_HANDOFF_DECLARED_BUT_BLOCKED")
        and csv_contains(PHI_PAYLOAD_CANDIDATE, "PHI_TAU_PARENT_INPUT_CONCRETE_PAYLOAD_CANDIDATE_DECLARED_UNACCEPTED")
    )


def supply_payload() -> dict[str, Any]:
    return {
        "artifact_status": "SHARED_PHI_TAU_EFF_EXPLICIT_FAIL_SUPPLIED_NO_ENDPOINT_BLIND_SOURCE",
        "claim_boundary": CLAIM_BOUNDARY,
        "target_role": "shared_potential_source",
        "coordinate_components_affected": [
            "e_acoustic.potential_source_presence",
            "e_lensing.lensing_potential_source",
            "e_acoustic.phase_support",
            "e_lensing.cross_readout_consistency",
            "e_radiation.cross_role_consistency",
        ],
        "formal_slot": "Phi_tau_eff(a,k)",
        "supply_type": "explicit_fail_evidence",
        "numeric_value_supplied": False,
        "unit_or_convention": "not_applicable_explicit_fail",
        "provenance": {
            "unblock_plan": rel(UNBLOCK_PLAN),
            "phi_derivation_contract": rel(PHI_CONTRACT),
            "effective_potential_handoff": rel(PHI_HANDOFF),
            "parent_input_payload_candidate": rel(PHI_PAYLOAD_CANDIDATE),
        },
        "replay": "make tau-cmb-physical-source-dependency-unblock-plan && make tau-cmb-endpoint-blind-phi-tau-source-or-explicit-fail-supply",
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
        "failure_statement": "No endpoint-blind Phi_tau_eff(a,k) source or derivation is accepted: the derivation contract is unsatisfied, the potential-source handoff is blocked, and the parent-input payload candidate is unaccepted.",
    }


def build_summary(supply_path: Path) -> dict[str, Any]:
    hash_path = supply_path.with_suffix(".hashes.json")
    hash_matches = supply_path.exists() and hash_path.exists() and load_json(hash_path).get("sha256") == sha256(supply_path)
    return {
        "report_id": "tau_cmb_endpoint_blind_phi_tau_source_or_explicit_fail_supply_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "supply_artifact": rel(supply_path),
        "supply_hash_artifact": rel(hash_path),
        "input_unblock_plan": rel(UNBLOCK_PLAN),
        "input_phi_derivation_contract": rel(PHI_CONTRACT),
        "input_effective_potential_handoff": rel(PHI_HANDOFF),
        "input_parent_payload_candidate": rel(PHI_PAYLOAD_CANDIDATE),
        "input_chain_clean": input_chain_clean(),
        "target_role": "shared_potential_source",
        "formal_slot": "Phi_tau_eff(a,k)",
        "affected_frontier_rows": 5,
        "explicit_fail_supplied": True,
        "numeric_value_supplied": False,
        "physical_value_source_accepted": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "supply_hash_matches": hash_matches,
        "status": (
            "CMB_ENDPOINT_BLIND_PHI_TAU_SOURCE_EXPLICIT_FAIL_SUPPLIED_NO_SCORE"
            if input_chain_clean() and hash_matches
            else "CMB_ENDPOINT_BLIND_PHI_TAU_SOURCE_EXPLICIT_FAIL_SUPPLY_NONCANONICAL_RESULT"
        ),
        "next_minimal_unblock": "tau_cmb_endpoint_blind_phi_tau_source_explicit_fail_acceptance_audit_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Endpoint-Blind Phi Tau Source or Explicit Fail Supply v01

**Doc class:** shared physical-source explicit fail supply
**Reader role:** Paper 13 / CMB scoring route reviewer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Summary

```text
formal_slot={summary["formal_slot"]}
affected_frontier_rows={summary["affected_frontier_rows"]}
explicit_fail_supplied={summary["explicit_fail_supplied"]}
numeric_value_supplied={summary["numeric_value_supplied"]}
physical_value_source_accepted={summary["physical_value_source_accepted"]}
score_entry_allowed={summary["score_entry_allowed"]}
likelihood_allowed={summary["likelihood_allowed"]}
dark_sector_verdict_allowed={summary["dark_sector_verdict_allowed"]}
```

This supplies explicit fail evidence for the absence of an accepted
endpoint-blind `Phi_tau_eff(a,k)` source. It is not a physical source value.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Supply explicit fail evidence for endpoint-blind Phi_tau_eff source.")
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
