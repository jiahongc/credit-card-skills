# Expected Output Shape

This is a minimal example to illustrate the contract, not live card data.

# Credit Card Info: Example Rewards Card

## Card Identity

- Issuer: Example Bank
- Network: Visa
- Family: Example Rewards
- Variant: Signature

## Best Public Signup Offer

- Summary: 60,000 points after qualifying spend in 3 months.
- Source: Example Bank
- Status: confirmed

## Earning Categories

- 3x dining
- 2x travel booked through issuer portal

## Cash or Statement Credits

- $50 annual hotel credit

## Hotel Benefits

- Automatic Silver status with Example Hotels

## Rental Car Benefits

- Secondary collision damage waiver on eligible rentals

## Travel Protection Benefits

- Trip delay reimbursement on covered delays

## Lounge Access

- No included lounge membership

## Usage Limits and Frequency Caps

- Hotel credit: once per account anniversary year

## Sources and Confidence Notes

- Example Bank product page
- No conflicts found

```yaml
card_name: Example Rewards Card
issuer: Example Bank
network: Visa
card_family: Example Rewards
card_variant: Signature
best_public_signup_offer:
  summary: 60000 points after qualifying spend in 3 months
  bonus_type: points
  bonus_amount: "60000"
  spend_requirement: "$4,000 in 3 months"
  annual_fee: "$95"
  source_name: Example Bank
  source_url: https://example.com/card
  source_type: issuer
  status: confirmed
earning_categories:
  - title: Dining
    summary: 3x points on dining
    status: confirmed
    source_name: Example Bank
    source_url: https://example.com/card
cash_or_statement_credits:
  - title: Hotel credit
    summary: Annual hotel statement credit
    value: "$50"
    cadence: annual
    status: confirmed
    source_name: Example Bank
    source_url: https://example.com/card
hotel_benefits: []
rental_car_benefits: []
travel_protection_benefits: []
lounge_access: []
usage_limits:
  - title: Hotel credit cadence
    summary: Hotel credit resets once per account year
    cap: once per account year
    status: confirmed
    source_name: Example Bank
    source_url: https://example.com/card
sources:
  - name: Example Bank
    url: https://example.com/card
    type: issuer
    used_for: product page
confidence_notes:
  - No conflicting sources found.
```
