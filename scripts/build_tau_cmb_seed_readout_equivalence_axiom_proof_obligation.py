#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EQUIV_AUDIT = ROOT / "data/derived/tau_cmb_seed_readout_equivalence_relation_audit_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_seed_readout_equivalence_axiom_proof_obligation_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_seed_readout_equivalence_axiom_proof_obligation_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_seed_readout_equivalence_axiom_proof_obligation_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_seed_readout_equivalence_axiom_proof_obligation_v01_obligation_only_"
    "no_equivalence_proof_no_quotient_map_no_readout_evaluation_no_survival_claim_no_score_no_verdict"
)

FIELDS = [
    "obligation_row_id",
    "obligation",
    "formal_target",
    "minimal_required_object",
    "proof_shape",
    "current_evidence",
    "obligation_status",
    "blocking_reason",
    "next_required_artifact",
    "allows_equivalence_proof",
    "allows_quotient_map",
    "allows_readout_evaluation",
    "allows_survival_claim",
    "allows_score_entry",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

ROWS = [
    {
        "obligation": "carrier_predicate",
        "formal_target": "x in C_CMB^seed iff x is a well-formed CMB role-space representative",
        "minimal_required_object": "C_CMB^seed carrier predicate with role-space basis and unit/dimension roles",
        "proof_shape": "define the set on which ~_{R_CMB,seed} is allowed to act",
        "current_evidence": "CMB_role_space_candidate is named but not materialized",
        "obligation_status": "REQUIRED_NOT_SUPPLIED",
        "blocking_reason": "without a carrier predicate, reflexivity and quotient classes are not well typed",
        "next_required_artifact": "tau_cmb_readout_role_space_basis_v01",
    },
    {
        "obligation": "control_predicate",
        "formal_target": "K_CMB(x,y) := all declared null/gauge/convention/endpoint-blind controls identify x and y",
        "minimal_required_object": "explicit control predicate or control family list K_CMB",
        "proof_shape": "state the predicate that defines indistinguishability before proving its axioms",
        "current_evidence": "control-family labels are named: null, gauge, convention, endpoint-blind",
        "obligation_status": "REQUIRED_NOT_SUPPLIED",
        "blocking_reason": "labels alone do not define a mathematical relation",
        "next_required_artifact": "tau_cmb_seed_readout_control_predicate_candidate_v01",
    },
    {
        "obligation": "reflexivity_lemma",
        "formal_target": "forall x in C_CMB^seed: x ~_{R_CMB,seed} x",
        "minimal_required_object": "identity-preserving controls K_CMB(x,x)",
        "proof_shape": "show every allowed control leaves a well-formed representative equivalent to itself",
        "current_evidence": "relation symbol and carrier label are declared",
        "obligation_status": "BLOCKED_BY_CARRIER_AND_CONTROL_PREDICATE",
        "blocking_reason": "carrier predicate and control predicate are missing",
        "next_required_artifact": "tau_cmb_seed_readout_reflexivity_lemma_candidate_v01",
    },
    {
        "obligation": "symmetry_lemma",
        "formal_target": "forall x,y in C_CMB^seed: x ~ y => y ~ x",
        "minimal_required_object": "symmetric control predicate or symmetric metric/tolerance rule",
        "proof_shape": "show indistinguishability is orientation-free",
        "current_evidence": "relation syntax is declared",
        "obligation_status": "BLOCKED_BY_CONTROL_PREDICATE",
        "blocking_reason": "no symmetric predicate, metric, or tolerance rule is supplied",
        "next_required_artifact": "tau_cmb_seed_readout_symmetry_lemma_candidate_v01",
    },
    {
        "obligation": "transitivity_lemma",
        "formal_target": "forall x,y,z in C_CMB^seed: x ~ y and y ~ z => x ~ z",
        "minimal_required_object": "transitive control predicate or quotient-safe closure rule",
        "proof_shape": "show chained indistinguishability remains inside the same quotient class",
        "current_evidence": "relation syntax is declared",
        "obligation_status": "BLOCKED_BY_QUOTIENT_SAFE_CLOSURE_RULE",
        "blocking_reason": "no closure rule prevents tolerance drift or control leakage",
        "next_required_artifact": "tau_cmb_seed_readout_transitivity_lemma_candidate_v01",
    },
    {
        "obligation": "quotient_well_definedness_lemma",
        "formal_target": "C_CMB^seed / ~_{R_CMB,seed} exists and [seed_tau_CMB] is well-defined",
        "minimal_required_object": "proved equivalence relation plus quotient map q_R",
        "proof_shape": "construct q_R(x)=[x] after the three equivalence axioms are available",
        "current_evidence": "quotient class notation is declared but not evaluated",
        "obligation_status": "BLOCKED_BY_EQUIVALENCE_AXIOMS",
        "blocking_reason": "quotient map cannot be accepted before the equivalence relation is proved",
        "next_required_artifact": "tau_cmb_seed_quotient_map_candidate_v01",
    },
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def table_rows() -> list[dict[str, str]]:
    return [
        {
            "obligation_row_id": f"TCMBSERAPO01_{index:03d}",
            "allows_equivalence_proof": "false",
            "allows_quotient_map": "false",
            "allows_readout_evaluation": "false",
            "allows_survival_claim": "false",
            "allows_score_entry": "false",
            "allows_dark_sector_verdict": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            **row,
        }
        for index, row in enumerate(ROWS, start=1)
    ]


def write_table(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_summary(table_path: Path, rows: list[dict[str, str]]) -> dict[str, Any]:
    audit = load_json(EQUIV_AUDIT) if EQUIV_AUDIT.exists() else {}
    input_ok = (
        audit.get("status") == "SEED_READOUT_EQUIVALENCE_RELATION_AUDITED_BLOCKED_NOT_PROVED"
        and audit.get("failed_rows") == 0
    )
    return {
        "report_id": "tau_cmb_seed_readout_equivalence_axiom_proof_obligation_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_equivalence_audit": rel(EQUIV_AUDIT),
        "input_equivalence_audit_clean": input_ok,
        "obligation_rows": len(rows),
        "required_rows": sum(row["obligation_status"].startswith("REQUIRED") for row in rows),
        "blocked_rows": sum(row["obligation_status"].startswith("BLOCKED") for row in rows),
        "equivalence_proof_allowed": False,
        "quotient_map_allowed": False,
        "readout_evaluation_allowed": False,
        "quotient_survival_claim_allowed": False,
        "score_entry_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "SEED_READOUT_EQUIVALENCE_AXIOM_PROOF_OBLIGATION_DECLARED_BLOCKED"
            if input_ok
            else "SEED_READOUT_EQUIVALENCE_AXIOM_PROOF_OBLIGATION_BLOCKED_BY_INPUT_AUDIT"
        ),
        "next_minimal_unblock": (
            "tau_cmb_readout_role_space_basis_v01"
            if input_ok
            else "repair_seed_readout_equivalence_relation_audit"
        ),
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    row_text = "\n".join(
        f"- `{row['obligation_row_id']}` `{row['obligation']}`: {row['obligation_status']} | next: `{row['next_required_artifact']}`"
        for row in rows
    )
    text = f"""# Tau CMB Seed Readout Equivalence Axiom Proof Obligation v01

**Doc class:** equivalence axiom proof obligation
**Status:** {summary["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact turns the blocked equivalence-relation audit into explicit proof
obligations. It does not prove the relation. It lists the minimum objects and
lemma shapes needed before `~_{{R_CMB,seed}}` can become a real equivalence
relation suitable for quotienting.

## Minimal Proof Chain

```text
carrier predicate C_CMB^seed
-> control predicate K_CMB
-> reflexivity lemma
-> symmetry lemma
-> transitivity lemma
-> quotient well-definedness lemma
```

## Obligations

{row_text}

## Status

```text
{summary["status"]}
```

No equivalence proof, quotient map, readout evaluation, survival claim, score
entry, or dark-sector verdict is allowed from this obligation artifact.

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB seed readout equivalence axiom proof obligation.")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    rows = table_rows()
    table_path = Path(args.write_table or DEFAULT_TABLE)
    if args.write_table:
        write_table(table_path, rows)
    summary = build_summary(table_path, rows)
    if args.write_summary:
        summary_path = Path(args.write_summary)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_doc:
        write_doc(Path(args.write_doc), rows, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
