#!/usr/bin/env bash
# Run all fixture validations, contract checks, and consistency checks.
# Exit with non-zero status if any check fails.

set -euo pipefail

VALIDATOR=".claude/skills/card-shared/scripts/validate_card_output.py"
COMPOSITION=".claude/skills/card-shared/scripts/check_contract_composition.py"
CONSISTENCY=".claude/skills/card-shared/scripts/check_fixture_consistency.py"

errors=0

run() {
  if ! python3 "$@"; then
    errors=$((errors + 1))
  fi
}

echo "=== Golden fixtures ==="
run "$VALIDATOR" --command card-full     tests/fixtures/golden/card-full-chase-sapphire-preferred.md
run "$VALIDATOR" --command card-transfer tests/fixtures/golden/card-transfer-chase-sapphire-preferred.md
run "$VALIDATOR" --command card-rate     tests/fixtures/golden/card-rate-chase-sapphire-preferred.md
run "$VALIDATOR" --command card-news     tests/fixtures/golden/card-news-chase-sapphire-preferred.md
run "$VALIDATOR" --command card-credits  tests/fixtures/golden/card-credits-chase-sapphire-preferred.md

echo ""
echo "=== Edge-case fixtures ==="
run "$VALIDATOR" --command card-rate     tests/fixtures/ambiguous/card-rate-chase-sapphire-family.md
run "$VALIDATOR" --command card-transfer tests/fixtures/conflict/card-transfer-capital-one-venture-x.md
run "$VALIDATOR" --command card-credits  tests/fixtures/missing/card-credits-discover-it.md
run "$VALIDATOR" --command card-news     tests/fixtures/recency/card-news-capital-one-venture-x.md

echo ""
echo "=== Multi-card fixtures ==="
run "$VALIDATOR" --command card-compare tests/fixtures/golden/card-compare-csp-vs-venture-x.md
run "$VALIDATOR" --command card-value   tests/fixtures/golden/card-value-chase-sapphire-preferred.md
run "$VALIDATOR" --command card-wallet  tests/fixtures/golden/card-wallet-chase-amex-duo.md

echo ""
echo "=== Composition check ==="
run "$COMPOSITION"

echo ""
echo "=== Cross-fixture consistency ==="
run "$CONSISTENCY" tests/fixtures/golden/

echo ""
if [ "$errors" -gt 0 ]; then
  echo "FAILED: $errors check(s) failed."
  exit 1
else
  echo "ALL CHECKS PASSED."
fi
