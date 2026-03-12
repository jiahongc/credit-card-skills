# Credit Card Skills

Agent Skills command suite for researching major-US credit cards. Works with **Claude Code**, **OpenAI Codex**, and any agent that supports the [Agent Skills](https://agentskills.io) open standard.

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

## Compatibility

These skills follow the [Agent Skills](https://agentskills.io) open standard (`SKILL.md` format with YAML frontmatter). They work with any compatible agent:

| Agent | Skill Location | Install Method |
|-------|---------------|----------------|
| **Claude Code** | `.claude/skills/` | Plugin install, `--plugin-dir`, or manual copy |
| **OpenAI Codex** | `.agents/skills/` | Clone repo into project or copy skills |
| **Cursor** | `.cursor/skills/` | Copy skills directory |
| **Gemini CLI** | `.gemini/skills/` | Copy skills directory |
| **Other agents** | Varies | See [agentskills.io](https://agentskills.io) |

The repo ships with both `.claude/skills/` and `.agents/skills/` (symlinked) so Claude Code and Codex work out of the box when the repo is cloned.

## Install

### Claude Code — as a plugin

```bash
# Load directly (development/testing)
claude --plugin-dir /path/to/credit-card-skills

# Or install from a marketplace (if published)
# /plugin install credit-card-skills
```

Skills are namespaced when loaded as a plugin: `/credit-card-skills:card-full`, `/credit-card-skills:card-compare`, etc.

### Claude Code — standalone project skills

```bash
mkdir -p .claude/skills
cp -R /path/to/credit-card-skills/.claude/skills/card-* .claude/skills/
```

Skills are available without a namespace: `/card-full`, `/card-compare`, etc.

### OpenAI Codex

```bash
mkdir -p .agents/skills
cp -R /path/to/credit-card-skills/.agents/skills/card-* .agents/skills/
```

Codex discovers skills automatically. Invoke with `/skills` or let Codex match them implicitly based on the task description.

### Other Agent Skills-compatible agents

Copy the skill directories into your agent's skill location:

```bash
# Generic — adjust the target path for your agent
cp -R /path/to/credit-card-skills/.claude/skills/card-* <your-agent-skills-dir>/
```

Each skill is a self-contained directory with a `SKILL.md` entrypoint and optional supporting files (scripts, references, examples).

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

## Repo Structure

```
credit-card-skills/
├── .claude/skills/          # Authoritative skill source (Claude Code)
│   ├── card-full/           # Full card report
│   ├── card-rate/           # Earning rates
│   ├── card-transfer/       # Transfer partners
│   ├── card-credits/        # Statement credits
│   ├── card-news/           # Recent news
│   ├── card-compare/        # Side-by-side comparison
│   ├── card-value/          # First-year value estimate
│   ├── card-wallet/         # Multi-card wallet audit
│   ├── card-identity/       # Shared card-name resolution (internal)
│   └── card-shared/         # Shared policies, contracts, scripts
├── .agents/skills/          # Symlinks for Codex compatibility
├── .claude-plugin/          # Claude Code plugin manifest
│   └── plugin.json
├── skills/                  # Symlinks for plugin distribution
├── tests/
│   ├── fixtures/            # Golden, ambiguous, conflict, missing, recency
│   └── run_all.sh           # Run all validators
└── sample-outputs.md        # 10 example command outputs
```

## Shared Layer

- `card-identity/SKILL.md` - centralized card-name resolution with abbreviation table and disambiguation logic
- `card-shared/source-policy.yaml` - issuer domains, approved secondary sources, and fast-search policy
- `card-shared/command-contracts.yaml` - required sections and YAML contracts for every command
- `card-shared/section-definitions.md` - how `/card-full` maps the framework into compact sections
- `card-shared/card-identity-rules.md` - variant identification and ambiguity handling rules
- `card-shared/confidence-rules.md` - `confirmed`, `unconfirmed`, and `conflicting` rules
- `card-shared/recency-rules.md` - 3-month news window and freshness expectations
- `card-shared/normalization-rules.md` - shared formatting conventions

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
- Issuer pages are primary; the approved secondary source list is used only when needed and capped per command.
- Commands stop once the contract is satisfied rather than continuing broad enrichment.
- `/card-news` is intentionally independent from `/card-full` composition — news is time-windowed and conceptually separate.
- Skills follow the [Agent Skills](https://agentskills.io) open standard for cross-agent compatibility.
