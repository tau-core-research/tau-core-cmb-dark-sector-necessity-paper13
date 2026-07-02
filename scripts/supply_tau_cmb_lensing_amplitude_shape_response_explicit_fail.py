#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ADAPTER_SUMMARY = ROOT / "data/derived/tau_cmb_lensing_amplitude_shape_response_adapter_or_explicit_fail_summary_v01.json"
SCORE_OUTPUT = ROOT / "payloads/tau_lensing_reduced_score_v01.json"
DEFAULT_SUPPLY = ROOT / "physical_value_source_supplies/e_lensing/amplitude_shape_response_explicit_fail_supply_v01.json"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_lensing_amplitude_shape_response_explicit_fail_supply_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_lensing_amplitude_shape_response_explicit_fail_supply_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_lensing_amplitude_shape_response_explicit_fail_supply_v01_"
    "row_specific_explicit_fail_no_shape_response_value_no_score_no_likelihood_no_verdict"
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


def input_chain_clean() -> bool:
    if not ADAPTER_SUMMARY.exists() or not SCORE_OUTPUT.exists():
        return False
    summary = load_json(ADAPTER_SUMMARY)
    return (
        summary.get("status") == "CMB_LENSING_AMPLITUDE_SHAPE_RESPONSE_ADAPTER_REJECTED_EXPLICIT_FAIL_ALLOWED"
        and summary.get("next_minimal_unblock") == "tau_cmb_lensing_amplitude_shape_response_explicit_fail_supply_v01"
        and summary.get("adapter_accepted") is False
        and summary.get("explicit_fail_supply_allowed") is True
        and summary.get("physical_value_source_accepted") is False
        and summary.get("physical_CMB_score_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def supply_payload() -> dict[str, Any]:
    return {
        "artifact_status": "ROW_SPECIFIC_EXPLICIT_FAIL_SUPPLIED_NO_LENSING_AMPLITUDE_SHAPE_RESPONSE",
        "claim_boundary": CLAIM_BOUNDARY,
        "target_role": "lensing",
        "coordinate_symbol": "e_lensing",
        "coordinate_component": "amplitude_shape_response",
        "formal_slot": "S_lens_tau(L) or delta S_lens_tau(L)",
        "supply_type": "explicit_fail_evidence",
        "numeric_value_supplied": False,
        "unit_or_convention": "not_applicable_explicit_fail",
        "provenance": {
            "adapter_or_fail_audit": rel(ADAPTER_SUMMARY),
            "reduced_score_output": rel(SCORE_OUTPUT),
        },
        "replay": "make tau-cmb-lensing-amplitude-shape-response-adapter-or-explicit-fail && make tau-cmb-lensing-amplitude-shape-response-explicit-fail-supply",
        "endpoint_blind_attestation": True,
        "forbidden_input_attestation": True,
        "forbidden_inputs": [
            "CMB endpoint residuals",
            "ACT/Planck likelihood errors",
            "post-endpoint tuning fields",
            "dark-sector verdict labels",
        ],
        "physical_value_source_supplied": False,
        "explicit_fail_supplied": True,
        "physical_value_source_accepted": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "failure_statement": "The available reduced lensing score output is a scalar score artifact, not a direct endpoint-blind S_lens_tau(L) or delta S_lens_tau(L) value-source payload.",
    }


def build_summary(supply_path: Path) -> dict[str, Any]:
    hash_path = supply_path.with_suffix(".hashes.json")
    hash_matches = supply_path.exists() and hash_path.exists() and load_json(hash_path).get("sha256") == sha256(supply_path)
    return {
        "report_id": "tau_cmb_lensing_amplitude_shape_response_explicit_fail_supply_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "supply_artifact": rel(supply_path),
        "supply_hash_artifact": rel(hash_path),
        "input_adapter_or_fail_summary": rel(ADAPTER_SUMMARY),
        "input_score_output": rel(SCORE_OUTPUT),
        "input_chain_clean": input_chain_clean(),
        "target_role": "lensing",
        "coordinate_symbol": "e_lensing",
        "coordinate_component": "amplitude_shape_response",
        "formal_slot": "S_lens_tau(L) or delta S_lens_tau(L)",
        "explicit_fail_supplied": True,
        "numeric_value_supplied": False,
        "physical_value_source_accepted": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "supply_hash_matches": hash_matches,
        "status": (
            "CMB_LENSING_AMPLITUDE_SHAPE_RESPONSE_ROW_SPECIFIC_EXPLICIT_FAIL_SUPPLIED_NO_SCORE"
            if input_chain_clean() and hash_matches
            else "CMB_LENSING_AMPLITUDE_SHAPE_RESPONSE_EXPLICIT_FAIL_SUPPLY_NONCANONICAL_RESULT"
        ),
        "next_minimal_unblock": "tau_cmb_lensing_amplitude_shape_response_explicit_fail_acceptance_audit_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Lensing Amplitude Shape Response Explicit Fail Supply v01

**Doc class:** row-specific explicit fail supply
**Reader role:** Paper 13 / CMB scoring route reviewer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Summary

```text
coordinate_component={summary["coordinate_component"]}
formal_slot={summary["formal_slot"]}
explicit_fail_supplied={summary["explicit_fail_supplied"]}
numeric_value_supplied={summary["numeric_value_supplied"]}
physical_value_source_accepted={summary["physical_value_source_accepted"]}
score_entry_allowed={summary["score_entry_allowed"]}
likelihood_allowed={summary["likelihood_allowed"]}
dark_sector_verdict_allowed={summary["dark_sector_verdict_allowed"]}
```

This is not a lensing amplitude/shape response value source. It supplies
row-specific explicit fail evidence for the absence of a direct
`S_lens_tau(L)`/`delta S_lens_tau(L)` payload.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Supply row-specific explicit fail evidence for Tau CMB lensing amplitude/shape response.")
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
