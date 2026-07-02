#!/usr/bin/env python3
from tau_cmb_checker_scaffold_common import run_checker


if __name__ == "__main__":
    raise SystemExit(run_checker(
        "endpoint_firewall_replay",
        "run_endpoint_firewall_checker",
        [
            "firewall_payload.json",
            "populated_records.json",
            "post_population_firewall_replay.json",
            "provenance_log.json",
            "endpoint_data_access_log.json",
            "score_access_log.json",
            "firewall_payload.hashes.json",
            "endpoint_firewall_attestation.json",
        ],
    ))
