#!/usr/bin/env python3
from tau_cmb_checker_scaffold_common import run_checker


if __name__ == "__main__":
    raise SystemExit(run_checker(
        "quotient_and_equivalence_survival",
        "run_quotient_survival_checker",
        [
            "quotient_payload.json",
            "equivalence_relation.json",
            "null_class.json",
            "representative_family.json",
            "non_null_witness.json",
            "quotient_relation_replay.json",
            "equivalence_axiom_replay.json",
            "quotient_provenance.json",
            "quotient_payload.hashes.json",
            "quotient_firewall_attestation.json",
        ],
    ))
