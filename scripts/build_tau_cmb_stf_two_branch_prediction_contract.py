#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"

PACKET_ID = "TAU_CMB_STF_TWO_BRANCH_PREDICTION_CONTRACT_V01"
CLAIM_BOUNDARY = (
    "two_source_frozen_stf_parent_completions_only_"
    "no_continuous_b_fit_no_cmb_score_no_likelihood_no_parent_verdict"
)

K_R = 59.0 / 64.0 - math.sqrt(3.0) / 12.0
I_K = 0.0610078751933
PLANCK_NS_DIAGNOSTIC = 0.9649
Q_TARGET = (1.0 - PLANCK_NS_DIAGNOSTIC) / (
    4.0 - (1.0 - PLANCK_NS_DIAGNOSTIC)
)

FIELDS = [
    "branch_id",
    "completion",
    "quartic_b",
    "source_status",
    "radial_filter_ratio",
    "tangent_filter_ratio",
    "inverse_lambda_target",
    "nearest_cycle_n",
    "nearest_cycle_lambda",
    "nearest_cycle_ns_diagnostic",
    "nearest_path_m",
    "nearest_path_lambda",
    "nearest_path_ns_diagnostic",
    "continuous_b_fit_allowed",
    "score_entry_allowed",
    "likelihood_allowed",
    "parent_selection_verdict_allowed",
    "claim_boundary",
]

FILTER_FIELDS = [
    "lambda",
    "minimal_normalized_filter",
    "ngbd_normalized_filter",
    "ngbd_to_minimal_ratio",
    "ordering",
    "score_entry_allowed",
    "claim_boundary",
]

TERMINAL_FIELDS = [
    "readout",
    "spectrum_type",
    "transfer_kernel_sign",
    "ngbd_vs_minimal_ordering",
    "theorem_status",
    "numeric_bandpower_supplied",
    "score_entry_allowed",
    "claim_boundary",
]

LAMBDA_DIAGNOSTIC_GRID = (0.0, 0.001, 0.01, 0.1, 1.0)


def spectral_tilt(q_value: float) -> float:
    return 1.0 - 4.0 * q_value / (1.0 + q_value)


def nearest_cycle(target: float) -> tuple[int, float]:
    n_value = min(
        range(3, 501),
        key=lambda n: abs(4.0 * math.sin(math.pi / n) ** 2 - target),
    )
    return n_value, 4.0 * math.sin(math.pi / n_value) ** 2


def nearest_path(target: float) -> tuple[int, float]:
    m_value = min(
        range(2, 501),
        key=lambda m: abs(4.0 * math.sin(math.pi / (2.0 * m)) ** 2 - target),
    )
    return m_value, 4.0 * math.sin(math.pi / (2.0 * m_value)) ** 2


def build_branch(
    branch_id: str,
    completion: str,
    quartic_b: float,
    source_status: str,
) -> dict[str, str]:
    radial_ratio = 1.0 / (1.0 + 12.0 * quartic_b * K_R * I_K)
    tangent_ratio = 1.0 / (1.0 + 4.0 * quartic_b * K_R * I_K)
    lambda_target = Q_TARGET / radial_ratio
    cycle_n, cycle_lambda = nearest_cycle(lambda_target)
    path_m, path_lambda = nearest_path(lambda_target)
    return {
        "branch_id": branch_id,
        "completion": completion,
        "quartic_b": f"{quartic_b:.12f}",
        "source_status": source_status,
        "radial_filter_ratio": f"{radial_ratio:.12f}",
        "tangent_filter_ratio": f"{tangent_ratio:.12f}",
        "inverse_lambda_target": f"{lambda_target:.12f}",
        "nearest_cycle_n": str(cycle_n),
        "nearest_cycle_lambda": f"{cycle_lambda:.12f}",
        "nearest_cycle_ns_diagnostic": f"{spectral_tilt(radial_ratio * cycle_lambda):.12f}",
        "nearest_path_m": str(path_m),
        "nearest_path_lambda": f"{path_lambda:.12f}",
        "nearest_path_ns_diagnostic": f"{spectral_tilt(radial_ratio * path_lambda):.12f}",
        "continuous_b_fit_allowed": "false",
        "score_entry_allowed": "false",
        "likelihood_allowed": "false",
        "parent_selection_verdict_allowed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def branch_rows() -> list[dict[str, str]]:
    return [
        build_branch(
            "STF_BRANCH_MINIMAL",
            "IPC_SGC_MINIMAL",
            0.0,
            "CONDITIONAL_MINIMAL_CONTROL",
        ),
        build_branch(
            "STF_BRANCH_NGBD",
            "NGBD_STF1",
            0.25,
            "CONDITIONAL_ENRICHED_BODY_COMPLETION",
        ),
    ]


def normalized_filter(radial_ratio: float, lambda_value: float) -> float:
    return 1.0 / (1.0 + radial_ratio * lambda_value) ** 2


def filter_rows() -> list[dict[str, str]]:
    branches = branch_rows()
    minimal_ratio = float(branches[0]["radial_filter_ratio"])
    ngbd_ratio = float(branches[1]["radial_filter_ratio"])
    rows = []
    for lambda_value in LAMBDA_DIAGNOSTIC_GRID:
        minimal_filter = normalized_filter(minimal_ratio, lambda_value)
        ngbd_filter = normalized_filter(ngbd_ratio, lambda_value)
        ratio = ngbd_filter / minimal_filter
        rows.append(
            {
                "lambda": f"{lambda_value:.12f}",
                "minimal_normalized_filter": f"{minimal_filter:.12f}",
                "ngbd_normalized_filter": f"{ngbd_filter:.12f}",
                "ngbd_to_minimal_ratio": f"{ratio:.12f}",
                "ordering": (
                    "EQUAL_AT_ZERO"
                    if lambda_value == 0.0
                    else "NGBD_GREATER_THAN_MINIMAL"
                ),
                "score_entry_allowed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def terminal_ordering_rows() -> list[dict[str, str]]:
    rows = [
        ("TT", "AUTO", "NONNEGATIVE_SQUARED_TRANSFER", "NGBD_GEQ_MINIMAL"),
        ("EE", "AUTO", "NONNEGATIVE_SQUARED_TRANSFER", "NGBD_GEQ_MINIMAL"),
        (
            "LENSING_PHI_PHI",
            "AUTO",
            "NONNEGATIVE_SQUARED_TRANSFER",
            "NGBD_GEQ_MINIMAL",
        ),
        ("TE", "CROSS", "SIGN_INDEFINITE_PRODUCT", "NOT_ORDERED"),
    ]
    return [
        {
            "readout": readout,
            "spectrum_type": spectrum_type,
            "transfer_kernel_sign": kernel_sign,
            "ngbd_vs_minimal_ordering": ordering,
            "theorem_status": "CONDITIONAL_COMMON_TRANSFER_THEOREM",
            "numeric_bandpower_supplied": "false",
            "score_entry_allowed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for readout, spectrum_type, kernel_sign, ordering in rows
    ]


def main() -> None:
    rows = branch_rows()
    discriminator_rows = filter_rows()
    terminal_rows = terminal_ordering_rows()
    DERIVED.mkdir(parents=True, exist_ok=True)

    csv_path = DERIVED / "tau_cmb_stf_two_branch_prediction_contract_v01.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    filter_csv_path = (
        DERIVED / "tau_cmb_stf_two_branch_filter_discriminator_v01.csv"
    )
    with filter_csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=FILTER_FIELDS, lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(discriminator_rows)

    terminal_csv_path = (
        DERIVED / "tau_cmb_stf_two_branch_terminal_ordering_v01.csv"
    )
    with terminal_csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=TERMINAL_FIELDS, lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(terminal_rows)

    payload = {
        "packet_id": PACKET_ID,
        "doc_class": "source_frozen_two_branch_prediction_contract",
        "status": "TWO_BRANCH_DIAGNOSTIC_READY_NUMERICAL_CMB_SCORE_BLOCKED",
        "claim_boundary": CLAIM_BOUNDARY,
        "constants": {
            "k_R": K_R,
            "I_K": I_K,
            "planck_ns_inverse_diagnostic": PLANCK_NS_DIAGNOSTIC,
            "q_inverse_target": Q_TARGET,
        },
        "law": {
            "potential": "V_b=(k_R/2)||Q||^2+b*k_R^2||Q||^4",
            "radial_filter_ratio": "1/(1+12*b*k_R*I_K)",
            "allowed_b_values": [0.0, 0.25],
        },
        "branches": rows,
        "amplitude_free_discriminator": {
            "law": "S_b(lambda)=1/(1+r_b*lambda)^2",
            "ngbd_to_minimal_ratio": (
                "((1+lambda)/(1+0.875420854231*lambda))^2"
            ),
            "ordering": (
                "equal at lambda=0; NGBD greater than minimal and "
                "monotonically separating for lambda>0"
            ),
            "diagnostic_grid": discriminator_rows,
        },
        "terminal_ordering": {
            "premise": (
                "rank-one adiabatic source and identical common transfer "
                "functions between branches"
            ),
            "rows": terminal_rows,
        },
        "firewall": {
            "continuous_b_fit_allowed": False,
            "cmb_score_computed": False,
            "likelihood_computed": False,
            "parent_selection_verdict_allowed": False,
        },
    }
    json_path = DERIVED / "tau_cmb_stf_two_branch_prediction_contract_v01.json"
    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("TAU_CMB_STF_TWO_BRANCH_PREDICTION_CONTRACT_V01_BUILT")


if __name__ == "__main__":
    main()
