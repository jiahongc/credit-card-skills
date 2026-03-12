---
name: card-full
description: Return a compact full report for one major-US credit card, covering fees, offer, earnings, redemption, credits, travel benefits, protections, mechanics, eligibility, and strategy. Use when the user wants the whole card picture.
argument-hint: [card name]
disable-model-invocation: true
allowed-tools: Read, WebSearch, WebFetch, Bash(curl -sS *)
---

# Card Full

## Goal

Return a compact, complete card framework for one exact card variant.

## Workflow

1. Resolve the card using [../card-identity/SKILL.md](../card-identity/SKILL.md). If ambiguous, return a numbered choice list and stop.
2. Follow the fast-search policy in [../card-shared/source-policy.yaml](../card-shared/source-policy.yaml): issuer pages first, stop early if the contract is satisfied, consult up to 4 secondary sources only for unresolved sections.
3. Follow section composition rules from [../card-shared/section-definitions.md](../card-shared/section-definitions.md).
4. Apply confidence handling from [../card-shared/confidence-rules.md](../card-shared/confidence-rules.md).
5. Return compact markdown using the `card-full` contract in [../card-shared/command-contracts.yaml](../card-shared/command-contracts.yaml).
6. YAML is internal only — do not include it in user-facing output.
7. Do not show inline links, a sources footer, or a "Why It Matters" section.

## Required Sections

- `## 💰 Fees`
- `## 🎁 Welcome Offer`
- `## 📈 Earning Rates`
- `## 🔄 Redemption`
- `## 🏷️ Credits`
- `## ✈️ Travel Benefits`
- `## 🛡️ Protections`
- `## ⚙️ Account Mechanics`
- `## ✅ Eligibility`
- `## 🧭 Strategy`
- `## 📋 Confidence Notes`

Omit `## Card Identity` when the match is confident. Each section should contain condensed facts in numbered lists where appropriate.
