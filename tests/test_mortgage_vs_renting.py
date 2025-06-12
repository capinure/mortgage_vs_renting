"""Unit tests for the mortgage_vs_renting model.

This suite verifies key calculations in ``mortgage_vs_renting.py``.

Run with:

    pytest -q

"""

import math
import importlib.util
import pathlib

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = PROJECT_ROOT / "mortgage_vs_renting.py"

spec = importlib.util.spec_from_file_location("mvr", MODULE_PATH)
mvr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mvr)


def test_monthly_mortgage_payment_zero_interest():
    """Monthly payment should be a simple division if interest is zero."""
    payment = mvr.monthly_mortgage_payment(120000, 0.0, 30)
    assert math.isclose(payment, 120000 / (30 * 12))


def test_simulate_renting_constant_rent():
    """Renting cost over a year with fixed rent should be rent*12."""
    params = mvr.RentalParameters(monthly_rent=1000, rent_increase_rate=0.0)
    cost = mvr.simulate_renting(params, years=1)
    assert math.isclose(cost, 1000 * 12)


def test_simulate_ownership_zero_cost_simple_case():
    """If everything is zeroed out the net cost should be zero."""
    ownership = mvr.OwnershipParameters(
        purchase_price=100000,
        down_payment=0.0,
        annual_interest_rate=0.0,
        mortgage_years=1,
        property_tax_rate=0.0,
        maintenance_rate=0.0,
        appreciation_rate=0.0,
    )
    cost = mvr.simulate_ownership(ownership, years=1)
    assert math.isclose(cost, 0.0, abs_tol=1e-8)


def test_compare_rent_vs_buy_output(capsys):
    """Ensure the CLI-style function prints comparison output."""
    ownership = mvr.OwnershipParameters(
        purchase_price=100000,
        down_payment=0.0,
        annual_interest_rate=0.0,
        mortgage_years=1,
        property_tax_rate=0.0,
        maintenance_rate=0.0,
        appreciation_rate=0.0,
    )
    rental = mvr.RentalParameters(monthly_rent=1000, rent_increase_rate=0.0)
    mvr.compare_rent_vs_buy(ownership, rental, years=1)
    captured = capsys.readouterr()
    assert "Net cost of ownership" in captured.out
    assert "Total cost of renting" in captured.out
