# Card Dossier: Capital One Venture X Rewards Credit Card

## Card Identity

- Issuer: Capital One
- Network: Visa
- Family: Venture X
- Variant: Rewards Credit Card

## Best Public Signup Offer

- Summary: Example conflicting offer fixture.
- Source: Capital One and approved secondary source
- Status: conflicting

## Earning Categories

- Example earning category entry.

## Cash or Statement Credits

- Example travel credit entry.

## Hotel Benefits

- Example hotel collection entry.

## Rental Car Benefits

- Example rental benefit entry.

## Travel Protection Benefits

- Example travel protection entry.

## Lounge Access

- Example lounge access entry.

## Usage Limits and Frequency Caps

- Example lounge guest cap entry.

## Sources and Confidence Notes

- Example conflict note.

```yaml
card_name: Capital One Venture X Rewards Credit Card
issuer: Capital One
network: Visa
card_family: Venture X
card_variant: Rewards Credit Card
best_public_signup_offer:
  summary: Example conflicting public offer values between sources
  bonus_type: miles
  bonus_amount: "75000"
  spend_requirement: "$4,000 in 3 months"
  annual_fee: "$395"
  source_name: Capital One
  source_url: https://www.capitalone.com/
  source_type: issuer
  status: conflicting
earning_categories:
  - title: Travel portal hotels
    summary: Example category
    status: confirmed
    source_name: Capital One
    source_url: https://www.capitalone.com/
cash_or_statement_credits:
  - title: Travel credit
    summary: Example annual travel credit
    status: confirmed
    source_name: Capital One
    source_url: https://www.capitalone.com/
hotel_benefits:
  - title: Lifestyle collection
    summary: Example hotel benefit
    status: unconfirmed
    source_name: Capital One
    source_url: https://www.capitalone.com/
rental_car_benefits:
  - title: Auto rental collision coverage
    summary: Example rental benefit
    status: confirmed
    source_name: Capital One
    source_url: https://www.capitalone.com/
travel_protection_benefits:
  - title: Trip interruption insurance
    summary: Example protection benefit
    status: confirmed
    source_name: Capital One
    source_url: https://www.capitalone.com/
lounge_access:
  - title: Capital One Lounge
    summary: Example lounge benefit
    status: confirmed
    source_name: Capital One
    source_url: https://www.capitalone.com/
usage_limits:
  - title: Lounge guest limit
    summary: Example guesting restriction
    cap: see source terms
    status: conflicting
    source_name: Capital One
    source_url: https://www.capitalone.com/
sources:
  - name: Capital One
    url: https://www.capitalone.com/
    type: issuer
    used_for: product page
  - name: Example Secondary Source
    url: https://www.example.com/venture-x
    type: secondary
    used_for: offer cross-check
confidence_notes:
  - Fixture only. Demonstrates conflict handling.
  - Final live responses should explain the exact discrepancy.
```
