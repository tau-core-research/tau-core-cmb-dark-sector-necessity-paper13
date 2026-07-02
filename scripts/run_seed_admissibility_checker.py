#!/usr/bin/env python3
from tau_cmb_checker_scaffold_common import run_checker


if __name__ == "__main__":
    raise SystemExit(run_checker(
        "seed_admissibility",
        "run_seed_admissibility_checker",
        [
            "seed_domain_payload.json",
            "seed_descriptor_pass.json",
            "activation_pass.json",
            "quotient_survival_witness.json",
            "seed_equivalence_replay.json",
            "seed_activation_replay.json",
            "seed_domain_provenance.json",
            "seed_domain_payload.hashes.json",
            "seed_endpoint_firewall_attestation.json",
        ],
    ))
