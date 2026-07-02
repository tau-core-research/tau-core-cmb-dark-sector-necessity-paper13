#!/usr/bin/env python3
from tau_cmb_checker_scaffold_common import run_checker


if __name__ == "__main__":
    raise SystemExit(run_checker(
        "source_object_admissibility",
        "run_source_object_checker",
        [
            "source_object_payload.json",
            "source_derivation_transcript.json",
            "known_limit_check.json",
            "source_dimension_gauge_replay.json",
            "source_derivation_replay.json",
            "source_object_provenance.json",
            "source_object_payload.hashes.json",
            "source_endpoint_firewall_trace.json",
        ],
    ))
