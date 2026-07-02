#!/usr/bin/env python3
from tau_cmb_checker_scaffold_common import run_checker


if __name__ == "__main__":
    raise SystemExit(run_checker(
        "null_control_admissibility",
        "run_null_control_checker",
        [
            "null_control_payload.json",
            "null_readout_candidate.json",
            "no_response_proof_candidate.json",
            "zero_control_replay.json",
            "null_coordinate_replay.json",
            "null_domain_replay.json",
            "null_control_provenance.json",
            "null_control_payload.hashes.json",
            "null_control_firewall_attestation.json",
        ],
    ))
