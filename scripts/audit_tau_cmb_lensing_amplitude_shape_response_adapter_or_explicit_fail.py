#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FRONTIER_RECOMPUTE_SUMMARY = ROOT / "data/derived/tau_cmb_endpoint_blind_physical_value_source_frontier_recompute_summary_v01.json"
SCORE_OUTPUT = ROOT / "payloads/tau_lensing_reduced_score_v01.json"
SCORE_AUDIT = ROOT / "data/derived/cmb_tau_lensing_score_output_status_audit_v01.json"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_lensing_amplitude_shape_response_adapter_or_explicit_fail_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_lensing_amplitude_shape_response_adapter_or_explicit_fail_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_lensing_amplitude_shape_response_adapter_or_explicit_fail_v01_"
    "adapter_rejected_explicit_fail_allowed_no_value_source_no_score_no_likelihood_no_verdict"
)


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def input_chain_clean() -> bool:
    if not FRONTIER_RECOMPUTE_SUMMARY.exists() or not SCORE_OUTPUT.exists() or not SCORE_AUDIT.exists():
        return False
    frontier = load_json(FRONTIER_RECOMPUTE_SUMMARY)
    audit = load_json(SCORE_AUDIT)
    return (
        frontier.get("status") == "CMB_ENDPOINT_BLIND_PHYSICAL_VALUE_SOURCE_FRONTIER_RECOMPUTED_ONE_EXPLICIT_FAIL_ACCEPTED"
        and frontier.get("next_minimal_unblock") == "tau_cmb_lensing_amplitude_shape_response_adapter_or_explicit_fail_v01"
        and frontier.get("explicit_fail_accepted_rows") == 1
        and frontier.get("open_frontier_rows") == 15
        and frontier.get("physical_value_source_accepted_rows") == 0
        and audit.get("audit_decision") == "PHYSICAL_TAU_SCORE_OUTPUT_ACCEPTED"
        and audit.get("score_likelihood_run") is False
        and audit.get("score_dark_sector_verdict") is False
    )


def build_summary() -> dict[str, Any]:
    score = load_json(SCORE_OUTPUT) if SCORE_OUTPUT.exists() else {}
    scalar_score_only = "chi2_tau" in score and "chi2_per_naive_dof" in score and "S_lens_tau" not in score and "delta_S_lens_tau" not in score
    adapter_accepted = False
    explicit_fail_allowed = input_chain_clean() and scalar_score_only
    return {
        "report_id": "tau_cmb_lensing_amplitude_shape_response_adapter_or_explicit_fail_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "input_frontier_recompute_summary": rel(FRONTIER_RECOMPUTE_SUMMARY),
        "input_score_output": rel(SCORE_OUTPUT),
        "input_score_output_audit": rel(SCORE_AUDIT),
        "input_chain_clean": input_chain_clean(),
        "target_role": "lensing",
        "coordinate_symbol": "e_lensing",
        "coordinate_component": "amplitude_shape_response",
        "formal_slot": "S_lens_tau(L) or delta S_lens_tau(L)",
        "score_output_route_id": score.get("route_id"),
        "score_output_projected_shape": score.get("projected_shape"),
        "score_output_is_scalar_score_only": scalar_score_only,
        "adapter_accepted": adapter_accepted,
        "explicit_fail_supply_allowed": explicit_fail_allowed,
        "physical_value_source_supplied": False,
        "physical_value_source_accepted": False,
        "physical_CMB_score_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_LENSING_AMPLITUDE_SHAPE_RESPONSE_ADAPTER_REJECTED_EXPLICIT_FAIL_ALLOWED"
            if explicit_fail_allowed and not adapter_accepted
            else "CMB_LENSING_AMPLITUDE_SHAPE_RESPONSE_ADAPTER_AUDIT_NONCANONICAL_RESULT"
        ),
        "next_minimal_unblock": "tau_cmb_lensing_amplitude_shape_response_explicit_fail_supply_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Lensing Amplitude Shape Response Adapter or Explicit Fail v01

**Doc class:** adapter/fail decision audit
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
score_output_is_scalar_score_only={summary["score_output_is_scalar_score_only"]}
adapter_accepted={summary["adapter_accepted"]}
explicit_fail_supply_allowed={summary["explicit_fail_supply_allowed"]}
physical_value_source_accepted={summary["physical_value_source_accepted"]}
physical_CMB_score_allowed={summary["physical_CMB_score_allowed"]}
likelihood_allowed={summary["likelihood_allowed"]}
dark_sector_verdict_allowed={summary["dark_sector_verdict_allowed"]}
```

The reduced lensing score output is not accepted as a direct
`S_lens_tau(L)`/`delta S_lens_tau(L)` value-source row. It may only support a
row-specific explicit-fail supply unless a dedicated adapter is supplied later.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB lensing amplitude/shape response adapter or explicit fail path.")
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    summary = build_summary()
    if args.write_summary:
        summary_path = Path(args.write_summary)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_doc:
        write_doc(Path(args.write_doc), summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
