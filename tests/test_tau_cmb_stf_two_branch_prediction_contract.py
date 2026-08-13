from __future__ import annotations

import json
import math
from pathlib import Path

from scripts.build_tau_cmb_stf_two_branch_prediction_contract import (
    branch_rows,
    filter_rows,
    terminal_ordering_rows,
)


ROOT = Path(__file__).resolve().parents[1]


def test_two_branch_contract_is_frozen_and_reproducible() -> None:
    rows = branch_rows()
    assert len(rows) == 2
    assert [float(row["quartic_b"]) for row in rows] == [0.0, 0.25]
    assert [int(row["nearest_cycle_n"]) for row in rows] == [67, 62]
    assert [int(row["nearest_path_m"]) for row in rows] == [33, 31]
    assert math.isclose(float(rows[0]["radial_filter_ratio"]), 1.0)
    assert math.isclose(
        float(rows[1]["radial_filter_ratio"]),
        0.875420854231,
        rel_tol=1e-12,
    )
    for row in rows:
        assert row["continuous_b_fit_allowed"] == "false"
        assert row["score_entry_allowed"] == "false"
        assert row["likelihood_allowed"] == "false"
        assert row["parent_selection_verdict_allowed"] == "false"


def test_materialized_contract_preserves_firewall() -> None:
    payload = json.loads(
        (
            ROOT
            / "data"
            / "derived"
            / "tau_cmb_stf_two_branch_prediction_contract_v01.json"
        ).read_text(encoding="utf-8")
    )
    assert payload["law"]["allowed_b_values"] == [0.0, 0.25]
    assert payload["firewall"] == {
        "continuous_b_fit_allowed": False,
        "cmb_score_computed": False,
        "likelihood_computed": False,
        "parent_selection_verdict_allowed": False,
    }


def test_amplitude_free_filter_discriminator_has_fixed_sign() -> None:
    rows = filter_rows()
    ratios = [float(row["ngbd_to_minimal_ratio"]) for row in rows]
    assert math.isclose(ratios[0], 1.0)
    assert all(ratio > 1.0 for ratio in ratios[1:])
    assert ratios == sorted(ratios)
    assert all(row["score_entry_allowed"] == "false" for row in rows)


def test_terminal_ordering_separates_auto_and_cross_spectra() -> None:
    rows = {row["readout"]: row for row in terminal_ordering_rows()}
    for readout in ("TT", "EE", "LENSING_PHI_PHI"):
        assert rows[readout]["ngbd_vs_minimal_ordering"] == "NGBD_GEQ_MINIMAL"
        assert rows[readout]["transfer_kernel_sign"] == (
            "NONNEGATIVE_SQUARED_TRANSFER"
        )
    assert rows["TE"]["ngbd_vs_minimal_ordering"] == "NOT_ORDERED"
    assert rows["TE"]["transfer_kernel_sign"] == "SIGN_INDEFINITE_PRODUCT"
    assert all(row["numeric_bandpower_supplied"] == "false" for row in rows.values())
