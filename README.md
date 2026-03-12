# Credit Card Info

Claude Code command suite for researching major-US credit cards with shared sourcing rules and compact command-specific output contracts.

## Commands

### Single-Card Research

- `/card-full [card name]` - compact full card report: fees, offer, earnings, redemption, credits, benefits, protections, mechanics, eligibility, strategy
- `/card-transfer [card name]` - numbered transfer partner list with ratios, timing, and restrictions
- `/card-rate [card name]` - earning rates by category with caps and exclusions
- `/card-news [card name]` - numbered recent-updates list from the last 3 months
- `/card-credits [card name]` - numbered credits list with amount, cadence, trigger, and restrictions

### Multi-Card & Analytical

- `/card-compare [card A] vs [card B]` - side-by-side comparison across fees, earning rates, credits, transfer partners, and key benefits
- `/card-value [card name] [optional spend breakdown]` - first-year value estimate: welcome bonus + earn + credits - annual fee
- `/card-wallet [card1], [card2], ...` - multi-card wallet audit for overlap, gaps, and total annual cost

All commands return compact markdown with emoji section headings and numbered lists. YAML is an internal contract only — it does not appear in user-facing output.

## Output Style

- One emoji per section heading
- Numbered lists for credits, transfer partners, earning categories, and news items
- No inline links or sources footer
- No "Why It Matters" section
- No visible YAML block
- Card Identity section omitted when the match is confident

## Fast-Search Policy

Commands target a ~2-minute budget:
- 0-20s: normalize card name, resolve exact variant
- 20-60s: fetch issuer product page and key terms/benefits pages
- 60-110s: consult only 2-4 approved secondary sources if needed
- 110-120s: finalize compact output; mark unresolved fields in confidence notes

## Shared Layer

- `.claude/skills/card-identity/SKILL.md` - centralized card-name resolution with abbreviation table and disambiguation logic
- `.claude/skills/card-shared/source-policy.yaml` - issuer domains (including blogs/newsrooms), top-20 approved secondary sources, and fast-search policy
- `.claude/skills/card-shared/command-contracts.yaml` - required sections and YAML contracts for every command
- `.claude/skills/card-shared/section-definitions.md` - how `/card-full` maps the framework into compact sections
- `.claude/skills/card-shared/card-identity-rules.md` - variant identification and ambiguity handling rules
- `.claude/skills/card-shared/confidence-rules.md` - `confirmed`, `unconfirmed`, and `conflicting` rules
- `.claude/skills/card-shared/recency-rules.md` - 3-month news window and freshness expectations
- `.claude/skills/card-shared/normalization-rules.md` - shared formatting conventions
- `.claude/skills/card-shared/scripts/validate_card_output.py` - schema-driven fixture validator (checks sections, YAML schema, no visible links/YAML, `last_validated` field)
- `.claude/skills/card-shared/scripts/check_contract_composition.py` - verifies `/card-full` reuses the focused command contracts
- `.claude/skills/card-shared/scripts/check_fixture_consistency.py` - cross-checks card-full fixtures against focused-command fixtures for identity consistency

## Install

Copy the whole skill suite into a Claude Code workspace:

```bash
mkdir -p .claude/skills
cp -R /path/to/credit-card-info/.claude/skills/card-* .claude/skills/
```

Then invoke commands directly:

```text
/card-full Chase Sapphire Preferred
/card-compare Chase Sapphire Preferred vs Capital One Venture X
/card-value Chase Sapphire Preferred $500/mo dining, $200/mo travel
/card-wallet Chase Sapphire Preferred, Amex Gold
```

## Validate Fixtures

Run all validations at once:

```bash
./tests/run_all.sh
```

Or validate individually:

```bash
python3 .claude/skills/card-shared/scripts/validate_card_output.py --command card-full tests/fixtures/golden/card-full-chase-sapphire-preferred.md
python3 .claude/skills/card-shared/scripts/validate_card_output.py --command card-compare tests/fixtures/golden/card-compare-csp-vs-venture-x.md
python3 .claude/skills/card-shared/scripts/validate_card_output.py --command card-value tests/fixtures/golden/card-value-chase-sapphire-preferred.md
python3 .claude/skills/card-shared/scripts/validate_card_output.py --command card-wallet tests/fixtures/golden/card-wallet-chase-amex-duo.md
```

## Notes

- v2 targets compact, fast output with a ~2-minute search budget.
- Major US issuers only.
- Issuer pages are primary; the approved top-20 list is used only when needed and capped per command.
- Commands stop once the contract is satisfied rather than continuing broad enrichment.
- `/card-news` is intentionally independent from `/card-full` composition — news is time-windowed and conceptually separate.
