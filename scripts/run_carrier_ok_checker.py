#!/usr/bin/env python3
from tau_cmb_checker_scaffold_common import run_checker


if __name__ == "__main__":
    raise SystemExit(run_checker(
        "carrier_well_formedness",
        "run_carrier_ok_checker",
        [
            "carrier_payload.json",
            "role_space_basis_replay.json",
            "role_bundle_replay.json",
            "carrier_provenance.json",
            "carrier_payload.hashes.json",
            "carrier_endpoint_firewall_attestation.json",
        ],
    ))
