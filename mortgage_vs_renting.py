# Intro code for mortgage_vs_renting model

"""Simple model for comparing the long-term costs of renting versus buying."""

from dataclasses import dataclass
import argparse

@dataclass
class OwnershipParameters:
    purchase_price: float
    down_payment: float
    annual_interest_rate: float
    mortgage_years: int
    property_tax_rate: float
    maintenance_rate: float
    appreciation_rate: float

@dataclass
class RentalParameters:
    monthly_rent: float
    rent_increase_rate: float


def monthly_mortgage_payment(principal: float, annual_rate: float, years: int) -> float:
    """Calculate the monthly mortgage payment using the standard formula."""
    monthly_rate = annual_rate / 12
    n_payments = years * 12
    if annual_rate == 0:
        return principal / n_payments
    return principal * (monthly_rate * (1 + monthly_rate) ** n_payments) / ((1 + monthly_rate) ** n_payments - 1)


def simulate_ownership(params: OwnershipParameters, years: int, sell_at_end: bool = True) -> float:
    """Return the net cost of owning a home over the given years."""
    principal = params.purchase_price - params.down_payment
    monthly_payment = monthly_mortgage_payment(principal, params.annual_interest_rate, params.mortgage_years)

    total_cost = params.down_payment
    remaining_principal = principal
    home_value = params.purchase_price

    for month in range(years * 12):
        interest = remaining_principal * (params.annual_interest_rate / 12)
        principal_paid = monthly_payment - interest
        remaining_principal -= principal_paid
        total_cost += monthly_payment
        # yearly costs
        if (month + 1) % 12 == 0:
            total_cost += home_value * params.property_tax_rate
            total_cost += home_value * params.maintenance_rate
            # home value appreciates each year
            home_value *= 1 + params.appreciation_rate

    if sell_at_end:
        equity = home_value - remaining_principal
        total_cost -= equity

    return total_cost


def simulate_renting(params: RentalParameters, years: int) -> float:
    """Return the total cost of renting over the given years."""
    monthly_rent = params.monthly_rent
    total_cost = 0.0
    for month in range(years * 12):
        total_cost += monthly_rent
        if (month + 1) % 12 == 0:
            monthly_rent *= (1 + params.rent_increase_rate)
    return total_cost


def compare_rent_vs_buy(ownership: OwnershipParameters, rental: RentalParameters, years: int) -> None:
    """Print a simple comparison between renting and buying."""
    own_cost = simulate_ownership(ownership, years)
    rent_cost = simulate_renting(rental, years)
    print(f"Net cost of ownership over {years} years: ${own_cost:,.2f}")
    print(f"Total cost of renting over {years} years: ${rent_cost:,.2f}")
    if own_cost < rent_cost:
        print("Buying is cheaper than renting in this scenario.")
    else:
        print("Renting is cheaper than buying in this scenario.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--purchase-price", type=float, default=300000)
    parser.add_argument("--down-payment", type=float, default=60000)
    parser.add_argument("--annual-interest-rate", type=float, default=0.04)
    parser.add_argument("--mortgage-years", type=int, default=30)
    parser.add_argument("--property-tax-rate", type=float, default=0.01)
    parser.add_argument("--maintenance-rate", type=float, default=0.01)
    parser.add_argument("--appreciation-rate", type=float, default=0.02)
    parser.add_argument("--monthly-rent", type=float, default=1500)
    parser.add_argument("--rent-increase-rate", type=float, default=0.03)
    parser.add_argument("--years", type=int, default=30)

    args = parser.parse_args()

    ownership_params = OwnershipParameters(
        purchase_price=args.purchase_price,
        down_payment=args.down_payment,
        annual_interest_rate=args.annual_interest_rate,
        mortgage_years=args.mortgage_years,
        property_tax_rate=args.property_tax_rate,
        maintenance_rate=args.maintenance_rate,
        appreciation_rate=args.appreciation_rate,
    )

    rental_params = RentalParameters(
        monthly_rent=args.monthly_rent,
        rent_increase_rate=args.rent_increase_rate,
    )

    compare_rent_vs_buy(ownership_params, rental_params, years=args.years)
