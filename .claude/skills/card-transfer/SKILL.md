---
name: card-transfer
description: Return transfer partners, transfer ratios, timing notes, and restrictions for one major-US credit card. Use when the user wants redemption-transfer details only.
argument-hint: [card name]
disable-model-invocation: true
allowed-tools: Read, WebSearch, WebFetch, Bash(curl -sS *)
---

# Card Transfer

## Goal

Return the transfer-program view of one exact card variant in compact format.

## Workflow

1. Resolve the card using [../card-identity/SKILL.md](../card-identity/SKILL.md). If ambiguous, return a numbered choice list and stop.
2. Follow the fast-search policy in [../card-shared/source-policy.yaml](../card-shared/source-policy.yaml): issuer program pages first, up to 2 secondary sources for timing or caveats.
3. Follow [../card-shared/confidence-rules.md](../card-shared/confidence-rules.md).
4. Return compact markdown using the `card-transfer` contract in [../card-shared/command-contracts.yaml](../card-shared/command-contracts.yaml).
5. YAML is internal only — do not include it in user-facing output.
6. Do not show inline links, a sources footer, or a "Why It Matters" section.

## Required Sections

- `## 🔄 Transfer Program`
- `## 🤝 Transfer Partners`
- `## ⚠️ Transfer Caveats`
- `## 📋 Confidence Notes`

Omit `## Card Identity` when the match is confident. Use a numbered list for transfer partners with ratio and one short note per item.
