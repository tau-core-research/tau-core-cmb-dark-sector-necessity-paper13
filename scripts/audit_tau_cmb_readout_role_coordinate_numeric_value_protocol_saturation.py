#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
INGEST_ACCEPTANCE_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_payload_source_ingest_acceptance_audit_summary_v01.json"
INGEST_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_payload_source_ingest_v01.csv"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_protocol_saturation_audit_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_protocol_saturation_audit_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_readout_role_coordinate_numeric_value_protocol_saturation_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_readout_role_coordinate_numeric_value_protocol_saturation_audit_v01_"
    "protocol_only_frontier_closed_physical_value_sources_required_no_likelihood_no_verdict"
)

FIELDS = [
    "protocol_saturation_row_id",
    "source_ingest_row_id",
    "role_name",
    "coordinate_symbol",
    "coordinate_component",
    "formal_slot",
    "current_value_source_accepted",
    "frontier_class",
    "required_next_source",
    "why_protocol_only_cannot_accept",
    "allows_physical_CMB_score",
    "allows_likelihood",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

FRONTIER = {
    "potential_source_presence": (
        "physical_source_required",
        "endpoint-blind Phi_tau_eff(a,k) source or explicit fail evidence",
        "presence cannot be converted into a value without a derived or supplied potential source",
    ),
    "phase_support": (
        "physical_response_required",
        "endpoint-blind acoustic oscillator response or explicit fail evidence",
        "phase support requires an evaluated oscillator response",
    ),
    "relative_peak_height": (
        "physical_response_required",
        "endpoint-blind acoustic amplitude/height response or explicit fail evidence",
        "peak-height ratio requires a concrete response amplitude",
    ),
    "baryon_loading_coupling": (
        "physical_convention_and_sign_required",
        "endpoint-blind baryon-loading coupling sign convention or explicit fail evidence",
        "the coupling sign is a physical/convention choice, not a protocol placeholder",
    ),
    "tau_effective_density": (
        "physical_source_required",
        "endpoint-blind rho_tau_eff(a,k) derivation/source or explicit fail evidence",
        "effective density is a source function and cannot be populated by a guard",
    ),
    "endpoint_blind_amplitude": (
        "provenance_and_amplitude_required",
        "endpoint-blind A_tau provenance plus amplitude value or explicit fail evidence",
        "endpoint-blindness must be evidenced for a concrete amplitude, not merely declared",
    ),
    "omega_c_h2_role_comparison": (
        "benchmark_comparison_required",
        "preselected comparison convention/benchmark plus value or explicit fail evidence",
        "comparison role needs a numeric comparison target or benchmark convention",
    ),
    "lensing_potential_source": (
        "physical_source_required",
        "endpoint-blind Phi_tau_eff(a,k) lensing-era source or explicit fail evidence",
        "lensing potential source is a physical input, not a guard",
    ),
    "transfer_kernel": (
        "operator_required",
        "endpoint-blind T_tau_CMB(k,a) transfer kernel or explicit fail evidence",
        "transfer kernel requires an operator rule and normalization",
    ),
    "amplitude_shape_response": (
        "physical_response_required",
        "endpoint-blind S_lens_tau(L) response or explicit fail evidence",
        "lensing shape response requires a computed or supplied response",
    ),
    "cross_readout_consistency": (
        "cross_role_evidence_required",
        "accepted density/acoustic/lensing source chain consistency or explicit fail evidence",
        "cross-readout consistency cannot be accepted before dependent roles are populated",
    ),
    "operator_rule": (
        "operator_required",
        "endpoint-blind growth transfer operator or explicit fail evidence",
        "growth propagation requires an operator rule, not only an interface declaration",
    ),
    "cross_role_consistency": (
        "cross_role_evidence_required",
        "accepted cross-role consistency chain or explicit fail evidence",
        "cross-role consistency cannot be accepted before dependent physical roles are populated",
    ),
    "tau_radiation_like_contribution": (
        "physical_source_required",
        "endpoint-blind Delta_N_eff_tau derivation/source or explicit fail evidence",
        "radiation-like contribution is a physical value slot",
    ),
    "damping_tail_inequality": (
        "inequality_evaluation_required",
        "numeric Delta_N_eff_tau and selected bound under the same convention or explicit fail evidence",
        "inequality evaluation requires both sides under a shared convention",
    ),
}


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def input_chain_clean() -> bool:
    if not INGEST_ACCEPTANCE_SUMMARY.exists() or not INGEST_TABLE.exists():
        return False
    summary = load_json(INGEST_ACCEPTANCE_SUMMARY)
    return (
        summary.get("status") == "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_SOURCE_INGEST_ACCEPTED_FOCUSED_PROTOCOL_ONLY"
        and summary.get("source_ingest_acceptance_rows") == 33
        and summary.get("protocol_value_component_accepted_rows") == 17
        and summary.get("physical_CMB_component_accepted_rows") == 0
        and summary.get("physical_CMB_score_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def rows() -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("protocol source ingest acceptance audit summary is not clean")
    out: list[dict[str, str]] = []
    for index, source in enumerate(read_csv(INGEST_TABLE), start=1):
        if source["value_source_accepted"] == "true":
            continue
        frontier_class, required_next_source, reason = FRONTIER[source["coordinate_component"]]
        out.append(
            {
                "protocol_saturation_row_id": f"TCMBRRCNVPSA01_{index:03d}",
                "source_ingest_row_id": source["source_ingest_row_id"],
                "role_name": source["role_name"],
                "coordinate_symbol": source["coordinate_symbol"],
                "coordinate_component": source["coordinate_component"],
                "formal_slot": source["formal_slot"],
                "current_value_source_accepted": source["value_source_accepted"],
                "frontier_class": frontier_class,
                "required_next_source": required_next_source,
                "why_protocol_only_cannot_accept": reason,
                "allows_physical_CMB_score": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return out


def write_table(path: Path, table_rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(table_rows)


def build_summary(table_path: Path, table_rows: list[dict[str, str]]) -> dict[str, Any]:
    classes: dict[str, int] = {}
    for row in table_rows:
        classes[row["frontier_class"]] = classes.get(row["frontier_class"], 0) + 1
    return {
        "report_id": "tau_cmb_readout_role_coordinate_numeric_value_protocol_saturation_audit_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_source_ingest_table": rel(INGEST_TABLE),
        "input_source_ingest_acceptance_summary": rel(INGEST_ACCEPTANCE_SUMMARY),
        "input_chain_clean": input_chain_clean(),
        "accepted_protocol_value_sources": 17,
        "remaining_frontier_rows": len(table_rows),
        "frontier_class_counts": classes,
        "protocol_only_frontier_closed": True,
        "physical_CMB_score_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_PROTOCOL_SATURATION_ACCEPTED_PHYSICAL_VALUE_SOURCES_REQUIRED"
            if input_chain_clean() and len(table_rows) == 16
            else "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_PROTOCOL_SATURATION_NONCANONICAL_RESULT"
        ),
        "next_minimal_unblock": "tau_cmb_endpoint_blind_physical_value_source_packet_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Readout Role-Coordinate Numeric Value Protocol Saturation Audit v01

**Doc class:** protocol saturation audit
**Reader role:** Paper 13 / CMB scoring route reviewer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Summary

```text
accepted_protocol_value_sources={summary["accepted_protocol_value_sources"]}
remaining_frontier_rows={summary["remaining_frontier_rows"]}
protocol_only_frontier_closed={summary["protocol_only_frontier_closed"]}
physical_CMB_score_allowed={summary["physical_CMB_score_allowed"]}
likelihood_allowed={summary["likelihood_allowed"]}
dark_sector_verdict_allowed={summary["dark_sector_verdict_allowed"]}
```

The remaining rows require endpoint-blind physical value sources, operators,
responses, comparisons, consistency evidence, or explicit fail evidence. They
are not accepted as further protocol-only value sources.

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB numeric value protocol saturation frontier.")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    table_rows = rows()
    table_path = Path(args.write_table) if args.write_table else DEFAULT_TABLE
    summary = build_summary(table_path, table_rows)
    if args.write_table:
        write_table(table_path, table_rows)
    if args.write_summary:
        summary_path = Path(args.write_summary)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_doc:
        write_doc(Path(args.write_doc), summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
