# Credit Card Info Skill

Claude Code skill package for researching a single major-US credit card and returning structured credit card information with current benefits and the best public signup offer found from approved sources.

## What This Repo Contains

- `.claude/skills/credit-card-info/SKILL.md` - skill entrypoint and workflow
- `.claude/skills/credit-card-info/source-policy.yaml` - approved issuers and secondary domains
- `.claude/skills/credit-card-info/normalization-rules.md` - field definitions and conflict handling
- `.claude/skills/credit-card-info/examples/` - example prompts and expected output shape
- `.claude/skills/credit-card-info/scripts/validate_card_info.py` - validates response structure
- `tests/fixtures/` - sample outputs for validation

## Scope

This repo is a skill package, not a card database. The skill instructs Claude Code how to research and normalize credit card information. It does not ship live card data.

v1 scope:

- one card at a time
- major US issuers only
- issuer pages are primary
- curated secondary sources are allowed for offer discovery and missing details
- returns structured markdown plus a machine-readable YAML block

## Install

Copy or symlink the skill directory into a Claude Code workspace:

```bash
mkdir -p .claude/skills
cp -R /path/to/credit-card-skills/.claude/skills/credit-card-info .claude/skills/
```

Then invoke it in Claude Code with:

```text
/credit-card-info Chase Sapphire Preferred
```

## Validate Fixtures

```bash
python3 .claude/skills/credit-card-info/scripts/validate_card_info.py tests/fixtures/golden/chase-sapphire-preferred.md
python3 .claude/skills/credit-card-info/scripts/validate_card_info.py tests/fixtures/conflict/capital-one-venture-x-conflict.md
```

## Next Steps

- tune the domain allowlist to your preferred research sources
- expand fixtures as you harden the schema
- adapt the package for Codex with a thin wrapper if needed
