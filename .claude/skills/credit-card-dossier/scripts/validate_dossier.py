#!/usr/bin/env python3
"""Validate a credit card dossier markdown response."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required to run this validator.") from exc


REQUIRED_SECTIONS = [
    "# Card Dossier:",
    "## Card Identity",
    "## Best Public Signup Offer",
    "## Earning Categories",
    "## Cash or Statement Credits",
    "## Hotel Benefits",
    "## Rental Car Benefits",
    "## Travel Protection Benefits",
    "## Lounge Access",
    "## Usage Limits and Frequency Caps",
    "## Sources and Confidence Notes",
]

REQUIRED_TOP_LEVEL_KEYS = [
    "card_name",
    "issuer",
    "network",
    "card_family",
    "card_variant",
    "best_public_signup_offer",
    "earning_categories",
    "cash_or_statement_credits",
    "hotel_benefits",
    "rental_car_benefits",
    "travel_protection_benefits",
    "lounge_access",
    "usage_limits",
    "sources",
    "confidence_notes",
]

LIST_KEYS = [
    "earning_categories",
    "cash_or_statement_credits",
    "hotel_benefits",
    "rental_car_benefits",
    "travel_protection_benefits",
    "lounge_access",
    "usage_limits",
    "sources",
    "confidence_notes",
]


def extract_yaml_block(content: str) -> str:
    match = re.search(r"```yaml\n(.*?)\n```", content, re.DOTALL)
    if not match:
        raise ValueError("Missing fenced yaml block.")
    return match.group(1)


def validate_sections(content: str) -> list[str]:
    errors = []
    last_index = -1
    for section in REQUIRED_SECTIONS:
        index = content.find(section)
        if index == -1:
            errors.append(f"Missing required section: {section}")
            continue
        if index < last_index:
            errors.append(f"Section out of order: {section}")
        last_index = index
    return errors


def validate_yaml_data(data: dict) -> list[str]:
    errors = []
    for key in REQUIRED_TOP_LEVEL_KEYS:
        if key not in data:
            errors.append(f"Missing YAML key: {key}")
    for key in LIST_KEYS:
        if key in data and not isinstance(data[key], list):
            errors.append(f"YAML key must be a list: {key}")
    offer = data.get("best_public_signup_offer")
    if offer is not None and not isinstance(offer, dict):
        errors.append("YAML key must be an object: best_public_signup_offer")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Path to a markdown dossier file")
    args = parser.parse_args()

    content = args.path.read_text(encoding="utf-8")
    errors = validate_sections(content)

    try:
      yaml_block = extract_yaml_block(content)
      data = yaml.safe_load(yaml_block) or {}
    except Exception as exc:  # pragma: no cover
      errors.append(str(exc))
      data = {}

    if isinstance(data, dict):
        errors.extend(validate_yaml_data(data))
    else:
        errors.append("YAML block must parse to an object.")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"OK: {args.path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
