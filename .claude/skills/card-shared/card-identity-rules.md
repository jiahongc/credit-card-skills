# Card Identity Rules

## Goal

Match the user’s input to one exact card variant before returning any facts.

## Rules

- Parse issuer, family, and variant separately when possible.
- Do not merge facts across similarly named variants.
- If multiple plausible variants exist, name the leading match and list the competing variants in `confidence_notes`.
- If the exact match cannot be determined, return the best-supported variant with `status: unconfirmed` in the relevant summary field.

## Examples

- `Chase Sapphire` is ambiguous between Preferred and Reserve.
- `Amex Gold` may need issuer confirmation if multiple regional or business variants could match.
