# Credit Card Dossier Skill

Claude Code skill package for researching a single major-US credit card and returning a structured dossier with current benefits and the best public signup offer found from approved sources.

## What This Repo Contains

- `.claude/skills/credit-card-dossier/SKILL.md` - skill entrypoint and workflow
- `.claude/skills/credit-card-dossier/source-policy.yaml` - approved issuers and secondary domains
- `.claude/skills/credit-card-dossier/normalization-rules.md` - field definitions and conflict handling
- `.claude/skills/credit-card-dossier/examples/` - example prompts and expected output shape
- `.claude/skills/credit-card-dossier/scripts/validate_dossier.py` - validates response structure
- `tests/fixtures/` - sample dossier outputs for validation

## Scope

This repo is a skill package, not a card database. The skill instructs Claude Code how to research and normalize a credit card dossier. It does not ship live card data.

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
cp -R /path/to/credit-card-skills/.claude/skills/credit-card-dossier .claude/skills/
```

Then invoke it in Claude Code with:

```text
/credit-card-dossier Chase Sapphire Preferred
```

## Validate Fixtures

```bash
python3 .claude/skills/credit-card-dossier/scripts/validate_dossier.py tests/fixtures/golden/chase-sapphire-preferred.md
python3 .claude/skills/credit-card-dossier/scripts/validate_dossier.py tests/fixtures/conflict/capital-one-venture-x-conflict.md
```

## Next Steps

- tune the domain allowlist to your preferred research sources
- expand fixtures as you harden the schema
- adapt the package for Codex with a thin wrapper if needed
