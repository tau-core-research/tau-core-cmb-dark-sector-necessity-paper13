#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
from pathlib import Path
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parents[1]
SOURCE_MANIFEST = ROOT / "data/source_manifest/cmb_source_data_receipt_v01.csv"
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

PREFIX = "cmb_source_data_acquisition_status_v01"
CLAIM_BOUNDARY = (
    "cmb_source_data_acquisition_status_v01_source_acquisition_and_hash_verification_only_"
    "no_likelihood_run_no_tau_score_no_dark_sector_verdict"
)

FIELDS = [
    "acquisition_row_id",
    "receipt_id",
    "source_family",
    "dataset_name",
    "official_url",
    "local_path",
    "expected_file_size_bytes",
    "observed_file_size_bytes",
    "expected_sha256",
    "observed_sha256",
    "preexisting_local_copy",
    "download_attempted",
    "download_succeeded",
    "hash_matches_receipt",
    "size_matches_receipt",
    "acquisition_status",
    "accepted_as_local_working_copy",
    "accepted_for_scoring_now",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "receipt_rows_consumed",
    "local_paths_expected",
    "preexisting_local_copies",
    "download_attempted_rows",
    "download_succeeded_rows",
    "hash_matched_rows",
    "size_matched_rows",
    "accepted_local_working_copy_rows",
    "accepted_for_scoring_rows",
    "planck_pr3_rows_ready",
    "act_dr6_lensing_rows_ready",
    "all_receipt_sources_available",
    "all_hashes_match_receipts",
    "all_sizes_match_receipts",
    "scores_computed",
    "cmb_likelihood_available",
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


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download(url: str, path: Path) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    try:
        with urlopen(url, timeout=120) as response, tmp.open("wb") as handle:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                handle.write(chunk)
        tmp.replace(path)
        return True
    except Exception:
        if tmp.exists():
            tmp.unlink()
        return False


def acquisition_rows(receipts: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, receipt in enumerate(receipts, start=1):
        local_path = ROOT / receipt["local_path"]
        preexisting = local_path.exists()
        attempted = False
        succeeded = False
        if not preexisting:
            attempted = True
            succeeded = download(receipt["official_url"], local_path)

        exists = local_path.exists()
        observed_size = local_path.stat().st_size if exists else 0
        observed_hash = sha256(local_path) if exists else ""
        expected_size = int(receipt["file_size_bytes"])
        hash_matches = observed_hash == receipt["sha256"]
        size_matches = observed_size == expected_size
        accepted_local = exists and hash_matches and size_matches
        rows.append(
            {
                "acquisition_row_id": f"CMBACQ01_{index:03d}",
                "receipt_id": receipt["receipt_id"],
                "source_family": receipt["source_family"],
                "dataset_name": receipt["dataset_name"],
                "official_url": receipt["official_url"],
                "local_path": receipt["local_path"],
                "expected_file_size_bytes": str(expected_size),
                "observed_file_size_bytes": str(observed_size),
                "expected_sha256": receipt["sha256"],
                "observed_sha256": observed_hash,
                "preexisting_local_copy": str(preexisting).lower(),
                "download_attempted": str(attempted).lower(),
                "download_succeeded": str(succeeded).lower(),
                "hash_matches_receipt": str(hash_matches).lower(),
                "size_matches_receipt": str(size_matches).lower(),
                "acquisition_status": (
                    "LOCAL_WORKING_COPY_HASH_AND_SIZE_VERIFIED"
                    if accepted_local
                    else "LOCAL_WORKING_COPY_MISSING_OR_RECEIPT_MISMATCH"
                ),
                "accepted_as_local_working_copy": str(accepted_local).lower(),
                "accepted_for_scoring_now": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    ready = [row for row in rows if row["accepted_as_local_working_copy"] == "true"]
    return [
        {
            "summary_id": "CMB_SOURCE_DATA_ACQUISITION_STATUS_V01",
            "receipt_rows_consumed": len(rows),
            "local_paths_expected": len(rows),
            "preexisting_local_copies": sum(row["preexisting_local_copy"] == "true" for row in rows),
            "download_attempted_rows": sum(row["download_attempted"] == "true" for row in rows),
            "download_succeeded_rows": sum(row["download_succeeded"] == "true" for row in rows),
            "hash_matched_rows": sum(row["hash_matches_receipt"] == "true" for row in rows),
            "size_matched_rows": sum(row["size_matches_receipt"] == "true" for row in rows),
            "accepted_local_working_copy_rows": len(ready),
            "accepted_for_scoring_rows": sum(row["accepted_for_scoring_now"] == "true" for row in rows),
            "planck_pr3_rows_ready": sum(row["source_family"] == "planck_pr3" for row in ready),
            "act_dr6_lensing_rows_ready": sum(row["source_family"] == "act_dr6_lensing" for row in ready),
            "all_receipt_sources_available": str(len(ready) == len(rows)).lower(),
            "all_hashes_match_receipts": str(all(row["hash_matches_receipt"] == "true" for row in rows)).lower(),
            "all_sizes_match_receipts": str(all(row["size_matches_receipt"] == "true" for row in rows)).lower(),
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": (
                "ALL_RECEIPT_SOURCES_ACQUIRED_AND_HASH_VERIFIED_SCORING_STILL_BLOCKED"
                if len(ready) == len(rows)
                else "SOURCE_ACQUISITION_INCOMPLETE_SCORING_BLOCKED"
            ),
            "next_required_artifact": "extract_score_specific_observable_payloads_and_likelihood_adapters",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc(summary_rows: list[dict[str, object]]) -> None:
    row = summary_rows[0]
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / f"{PREFIX}.md").write_text(
        f"""# CMB Source Data Acquisition Status v01

**Doc class:** source data acquisition status
**Status:** official local working copies checked against receipt hashes

This artifact verifies or obtains the CMB source files listed in
`data/source_manifest/cmb_source_data_receipt_v01.csv`. The files remain local
working copies under `data/external/` and are not redistributed by the public
repository package.

Summary:

```text
receipt_rows_consumed={row["receipt_rows_consumed"]}
local_paths_expected={row["local_paths_expected"]}
preexisting_local_copies={row["preexisting_local_copies"]}
download_attempted_rows={row["download_attempted_rows"]}
download_succeeded_rows={row["download_succeeded_rows"]}
hash_matched_rows={row["hash_matched_rows"]}
size_matched_rows={row["size_matched_rows"]}
accepted_local_working_copy_rows={row["accepted_local_working_copy_rows"]}
accepted_for_scoring_rows=0
```

## Claim Boundary

This artifact verifies source acquisition and receipt hashes only. It does not
run a CMB likelihood, does not construct a Tau prediction, does not compute a
score, and permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = acquisition_rows(read_csv(SOURCE_MANIFEST))
    summary_rows = summary(rows)
    write_csv(DERIVED / f"{PREFIX}.csv", rows, FIELDS)
    write_csv(DERIVED / "cmb_source_data_acquisition_status_summary_v01.csv", summary_rows, SUMMARY_FIELDS)
    write_doc(summary_rows)
    print("CMB_SOURCE_DATA_ACQUISITION_STATUS_V01_BUILT")


if __name__ == "__main__":
    main()
