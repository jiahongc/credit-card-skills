---
name: credit-card-info
description: Research a single major-US credit card and return structured credit card information with the best public signup offer, benefits, usage limits, and source notes. Use when the user names a credit card and wants current issuer-backed details plus approved secondary-source validation.
argument-hint: [card name]
allowed-tools: Read, WebSearch, WebFetch, Bash(curl -sS *)
---

# Credit Card Info

## Quick Start

Use this skill when the user provides a single credit card name and wants a reliable, source-backed summary of its current offer and benefits.

Input example:

```text
/credit-card-info Chase Sapphire Preferred
```

Primary objective:

1. Identify the exact card variant.
2. Research approved sources only.
3. Normalize the findings into a fixed credit card info format.
4. Surface uncertainty clearly when facts conflict or are missing.

For source rules, see [source-policy.yaml](source-policy.yaml).
For output normalization, see [normalization-rules.md](normalization-rules.md).

## Workflow

### Step 1: Confirm Card Identity

- Parse the user input into issuer, product family, and likely variant.
- If the name is ambiguous, state the likely match and list the competing variants.
- Do not merge benefits across variants.

### Step 2: Gather Approved Sources

- Start with issuer domains listed in [source-policy.yaml](source-policy.yaml).
- Use the curated top-20 secondary-source URL list in [source-policy.yaml](source-policy.yaml) before considering any other non-issuer source.
- Use approved secondary domains only when:
  - searching for the best public signup offer
  - filling a detail the issuer site does not state clearly
  - checking whether a benefit has an explicit usage cap or limitation
- Ignore unsupported domains by default.
- Never rely on forums, referrals, targeted offer pages, or user-generated content unless the user explicitly asks for that broader research mode.

### Step 3: Reconcile Findings Conservatively

- Prefer issuer pages for core benefits and terms.
- For signup offers, compare approved public sources and choose the strongest public offer that is still live and clearly sourced.
- When sources conflict:
  - prefer issuer terms for benefit definitions
  - prefer the most recently verifiable public offer page for signup offer details
  - call out the conflict in `sources / confidence notes`
- If a detail cannot be confirmed, mark it `unconfirmed` rather than guessing.

### Step 4: Return The Credit Card Info

Return both:

1. A structured markdown report with the sections below
2. A machine-readable YAML block in a fenced code block labeled `yaml`

Required markdown sections, in this order:

1. `# Credit Card Info: <card name>`
2. `## Card Identity`
3. `## Best Public Signup Offer`
4. `## Earning Categories`
5. `## Cash or Statement Credits`
6. `## Hotel Benefits`
7. `## Rental Car Benefits`
8. `## Travel Protection Benefits`
9. `## Lounge Access`
10. `## Usage Limits and Frequency Caps`
11. `## Sources and Confidence Notes`

### Machine-Readable YAML Contract

Use these top-level keys:

```yaml
card_name:
issuer:
network:
card_family:
card_variant:
best_public_signup_offer:
earning_categories:
cash_or_statement_credits:
hotel_benefits:
rental_car_benefits:
travel_protection_benefits:
lounge_access:
usage_limits:
sources:
confidence_notes:
```

Each benefits collection should be a list of objects, not a prose blob.

## Output Rules

- Use concise, factual language.
- Include citations or explicit source URLs in the prose section when the environment supports links.
- Keep the YAML consistent with the prose. If they diverge, fix the answer before sending.
- For missing data, use `status: unconfirmed` and explain why in `confidence_notes`.
- Do not recommend the card or compare it to other cards in v1.

## Guardrails

- Major US issuers only in v1.
- One card per invocation.
- Public offers only. Exclude targeted, mailed, employee, or referral-only offers unless explicitly requested.
- Unsupported research result: say the card is outside v1 scope or insufficiently sourced.

## Example Skeleton

```markdown
# Credit Card Info: Example Card

## Card Identity
...

## Best Public Signup Offer
...

## Earning Categories
...

## Cash or Statement Credits
...

## Hotel Benefits
...

## Rental Car Benefits
...

## Travel Protection Benefits
...

## Lounge Access
...

## Usage Limits and Frequency Caps
...

## Sources and Confidence Notes
...

```yaml
card_name: Example Card
issuer: Example Issuer
network: Visa
card_family: Example Family
card_variant: Example Variant
best_public_signup_offer:
  summary: Example summary
  source_type: issuer
  status: confirmed
earning_categories: []
cash_or_statement_credits: []
hotel_benefits: []
rental_car_benefits: []
travel_protection_benefits: []
lounge_access: []
usage_limits: []
sources: []
confidence_notes: []
```
```
