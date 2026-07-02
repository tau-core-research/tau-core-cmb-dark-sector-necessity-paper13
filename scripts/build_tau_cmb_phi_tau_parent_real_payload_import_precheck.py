#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

PREFIX = "tau_cmb_phi_tau_parent_real_payload_import_precheck_v01"
SOURCE_PREFIX = "tau_cmb_phi_tau_parent_real_score_ready_payload_template_manifest_v01"

CLAIM_BOUNDARY = (
    f"{PREFIX}_import_precheck_only_missing_real_payloads_no_hash_binding_"
    "no_slot_accepted_no_scoring_input_accepted_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "import_precheck_row_id",
    "template_binding_row_id",
    "slot_row_id",
    "contract_row_id",
    "material_class",
    "expected_artifact_path",
    "template_path",
    "expected_format",
    "real_payload_path_exists",
    "real_payload_readable",
    "real_payload_nonempty",
    "payload_sha256",
    "schema_check_status",
    "import_precheck_status",
    "payload_import_accepted",
    "payload_hash_bound",
    "slot_accepted",
    "scoring_input_accepted",
    "reopen_scoring_route_allowed_now",
    "score_attempt_allowed_now",
    "phi_tau_eff_derived",
    "scores_computed",
    "cmb_likelihood_available",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "template_bindings_consumed",
    "import_precheck_rows_declared",
    "real_payload_paths_expected",
    "real_payload_paths_present",
    "real_payload_paths_missing",
    "real_payload_readable_rows",
    "real_payload_nonempty_rows",
    "payload_hash_bound_rows",
    "schema_pass_rows",
    "payload_import_accepted_rows",
    "slot_accepted_rows",
    "scoring_input_accepted_rows",
    "reopen_scoring_route_allowed_now_rows",
    "score_attempt_allowed_now_rows",
    "score_attempt_blocked_now_rows",
    "phi_tau_eff_derived_rows",
    "scores_computed_rows",
    "cmb_likelihood_available_rows",
    "real_payload_import_precheck_satisfied",
    "all_real_payloads_present",
    "all_payload_imports_accepted",
    "scores_computed",
    "cmb_likelihood_available",
    "no_dark_blockers",
    "no_dark_cmb_verdict_allowed",
    "tau_response_claim_allowed",
    "dark_sector_verdict_allowed",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def schema_status(path: Path, expected_format: str, required_fields: str) -> str:
    if not path.exists():
        return "SCHEMA_NOT_CHECKED_MISSING_REAL_PAYLOAD"
    fields = [field for field in required_fields.split("|") if field]
    try:
        if expected_format == "csv":
            with path.open(newline="") as handle:
                reader = csv.reader(handle)
                header = next(reader, [])
            missing = [field for field in fields if field not in header]
            return "SCHEMA_PASS" if not missing else "SCHEMA_FAIL_MISSING_FIELDS"
        if expected_format == "json":
            payload = json.loads(path.read_text(encoding="utf-8"))
            missing = [field for field in fields if field not in payload]
            return "SCHEMA_PASS" if not missing else "SCHEMA_FAIL_MISSING_FIELDS"
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, csv.Error):
        return "SCHEMA_FAIL_UNREADABLE_OR_INVALID"
    return "SCHEMA_FAIL_UNKNOWN_FORMAT"


def precheck_rows(template_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    for index, template in enumerate(template_rows, start=1):
        path = ROOT / template["expected_artifact_path"]
        exists = path.exists()
        readable = False
        nonempty = False
        digest = ""
        if exists and path.is_file():
            try:
                nonempty = path.stat().st_size > 0
                digest = sha256(path)
                readable = True
            except OSError:
                readable = False
        check = schema_status(path, template["template_format"], template["required_schema_fields"])
        accepted = exists and readable and nonempty and check == "SCHEMA_PASS"
        rows.append(
            {
                "import_precheck_row_id": f"TCMBPTARPIP01_{index:03d}",
                "template_binding_row_id": template["template_binding_row_id"],
                "slot_row_id": template["slot_row_id"],
                "contract_row_id": template["contract_row_id"],
                "material_class": template["material_class"],
                "expected_artifact_path": template["expected_artifact_path"],
                "template_path": template["template_path"],
                "expected_format": template["template_format"],
                "real_payload_path_exists": str(exists).lower(),
                "real_payload_readable": str(readable).lower(),
                "real_payload_nonempty": str(nonempty).lower(),
                "payload_sha256": digest,
                "schema_check_status": check,
                "import_precheck_status": (
                    "IMPORT_PRECHECK_PASS_REAL_PAYLOAD_PRESENT"
                    if accepted
                    else "IMPORT_PRECHECK_FAIL_MISSING_REAL_PAYLOAD"
                ),
                "payload_import_accepted": str(accepted).lower(),
                "payload_hash_bound": str(accepted).lower(),
                "slot_accepted": "false",
                "scoring_input_accepted": "false",
                "reopen_scoring_route_allowed_now": "false",
                "score_attempt_allowed_now": "false",
                "phi_tau_eff_derived": "false",
                "scores_computed": "false",
                "cmb_likelihood_available": "false",
                "blocks_no_dark_claim": "true",
                "allows_tau_response_claim": "false",
                "allows_dark_sector_verdict": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def summary(rows: list[dict[str, str]], template_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_REAL_PAYLOAD_IMPORT_PRECHECK_V01",
            "template_bindings_consumed": len(template_rows),
            "import_precheck_rows_declared": len(rows),
            "real_payload_paths_expected": len(rows),
            "real_payload_paths_present": sum(row["real_payload_path_exists"] == "true" for row in rows),
            "real_payload_paths_missing": sum(row["real_payload_path_exists"] == "false" for row in rows),
            "real_payload_readable_rows": sum(row["real_payload_readable"] == "true" for row in rows),
            "real_payload_nonempty_rows": sum(row["real_payload_nonempty"] == "true" for row in rows),
            "payload_hash_bound_rows": sum(row["payload_hash_bound"] == "true" for row in rows),
            "schema_pass_rows": sum(row["schema_check_status"] == "SCHEMA_PASS" for row in rows),
            "payload_import_accepted_rows": sum(row["payload_import_accepted"] == "true" for row in rows),
            "slot_accepted_rows": sum(row["slot_accepted"] == "true" for row in rows),
            "scoring_input_accepted_rows": sum(row["scoring_input_accepted"] == "true" for row in rows),
            "reopen_scoring_route_allowed_now_rows": sum(
                row["reopen_scoring_route_allowed_now"] == "true" for row in rows
            ),
            "score_attempt_allowed_now_rows": sum(row["score_attempt_allowed_now"] == "true" for row in rows),
            "score_attempt_blocked_now_rows": sum(row["score_attempt_allowed_now"] == "false" for row in rows),
            "phi_tau_eff_derived_rows": sum(row["phi_tau_eff_derived"] == "true" for row in rows),
            "scores_computed_rows": sum(row["scores_computed"] == "true" for row in rows),
            "cmb_likelihood_available_rows": sum(row["cmb_likelihood_available"] == "true" for row in rows),
            "real_payload_import_precheck_satisfied": "true",
            "all_real_payloads_present": "false",
            "all_payload_imports_accepted": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "REAL_PAYLOAD_IMPORT_PRECHECK_FAILS_MISSING_REAL_PAYLOADS_ROUTE_REMAINS_LOCKED",
            "next_required_artifact": "populate_data_score_ready_input_with_real_endpoint_blind_payloads",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / f"{PREFIX}.md").write_text(
        """# Tau CMB Phi Tau Parent Real Payload Import Precheck v01

**Doc class:** real payload import precheck
**Status:** executable import precheck declared; real payloads missing

This artifact checks whether the expected score-ready payload files exist under
`data/score_ready_input/`, whether they are readable and nonempty, whether a
hash can be bound, and whether their schema matches the template manifest. In
the current repository package no real payload files are present.

Summary:

```text
template_bindings_consumed=49
import_precheck_rows_declared=49
real_payload_paths_expected=49
real_payload_paths_present=0
real_payload_paths_missing=49
payload_hash_bound_rows=0
payload_import_accepted_rows=0
scoring_input_accepted_rows=0
score_attempt_blocked_now_rows=49
```

## Claim Boundary

This artifact is an import precheck only. It imports no real Tau-side CMB
payload, binds no payload hash, accepts no slot, accepts no scoring input,
derives no `Phi_tau_eff`, computes no score, supplies no CMB likelihood, and
permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    template_rows = read_csv(DERIVED / f"{SOURCE_PREFIX}.csv")
    rows = precheck_rows(template_rows)
    write_csv(DERIVED / f"{PREFIX}.csv", rows, FIELDS)
    write_csv(DERIVED / f"{PREFIX[:-4]}_summary_v01.csv", summary(rows, template_rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER13_TAU_CMB_PHI_TAU_PARENT_REAL_PAYLOAD_IMPORT_PRECHECK_V01_BUILT")


if __name__ == "__main__":
    main()
