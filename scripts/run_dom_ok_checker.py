#!/usr/bin/env python3
from tau_cmb_checker_scaffold_common import run_checker


if __name__ == "__main__":
    raise SystemExit(run_checker(
        "domain_membership_rule",
        "run_dom_ok_checker",
        [
            "domain_payload.json",
            "support_record.json",
            "normalization_record.json",
            "domain_replay_trace.json",
            "domain_provenance.json",
            "domain_payload.hashes.json",
            "domain_firewall_trace.json",
        ],
    ))
