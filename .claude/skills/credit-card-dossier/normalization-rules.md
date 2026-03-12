# Normalization Rules

## Goal

Convert raw research notes into a consistent dossier for one major-US credit card.

## Field Definitions

### Card Identity

- `card_name`: display name used in the final heading
- `issuer`: issuing bank
- `network`: Visa, Mastercard, Amex, or Discover when known
- `card_family`: product family, for example `Sapphire`
- `card_variant`: exact SKU-level match, for example `Preferred`

### Best Public Signup Offer

Represent as an object with:

- `summary`: one-line offer summary
- `bonus_type`: points, miles, cash back, free night, or mixed
- `bonus_amount`: structured numeric or string value
- `spend_requirement`: threshold and qualification window if known
- `annual_fee`: current fee if relevant to interpreting the offer
- `source_name`
- `source_url`
- `source_type`: `issuer` or `secondary`
- `status`: `confirmed`, `conflicting`, or `unconfirmed`

### Benefit Collections

Use a list of objects for these keys:

- `earning_categories`
- `cash_or_statement_credits`
- `hotel_benefits`
- `rental_car_benefits`
- `travel_protection_benefits`
- `lounge_access`
- `usage_limits`

Each item should include:

- `title`
- `summary`
- `status`
- `source_name`
- `source_url`

Add the following when relevant:

- `value`
- `cadence`
- `cap`
- `conditions`
- `coverage_type`
- `network_dependency`
- `applies_to`

### Sources And Confidence

- `sources` should be a list of objects with `name`, `url`, `type`, and `used_for`
- `confidence_notes` should be short strings explaining uncertainty, ambiguity, or conflicts

## Conflict Handling

- If issuer and secondary source agree, mark `confirmed`.
- If issuer is silent and secondary source is plausible but not definitive, mark `unconfirmed`.
- If issuer and secondary source disagree, mark `conflicting` and explain the discrepancy in `confidence_notes`.
- Do not silently average or merge conflicting offer amounts or benefit caps.

## Missing Data

- Empty list is acceptable when a category truly does not apply.
- Use `status: unconfirmed` for a partially sourced item.
- Do not invent cadence, value, or cap details.

## Usage Limit Rules

Include any frequency or cap information that materially limits a benefit, including:

- monthly, quarterly, annual, or one-time credits
- lounge visit guest limits
- rental coverage exclusions
- travel protection coverage caps or trip-count restrictions

If the cap is embedded inside another category, duplicate the limit in `usage_limits` so the final dossier has one dedicated place for all practical constraints.
