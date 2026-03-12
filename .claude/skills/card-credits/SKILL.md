---
name: card-credits
description: Return statement credits and cash-like credits for one major-US credit card, including trigger rules, cadence, enrollment requirements, restrictions, and practical usage notes. Use when the user wants the credits picture only.
argument-hint: [card name]
disable-model-invocation: true
allowed-tools: Read, WebSearch, WebFetch, Bash(curl -sS *)
---

# Card Credits

## Goal

Return the credits view of one exact card variant in compact format.

## Workflow

1. Resolve the card using [../card-identity/SKILL.md](../card-identity/SKILL.md). If ambiguous, return a numbered choice list and stop.
2. Follow the fast-search policy in [../card-shared/source-policy.yaml](../card-shared/source-policy.yaml): issuer benefit terms first, up to 2 secondary sources for practical trigger and usability context.
3. Follow [../card-shared/confidence-rules.md](../card-shared/confidence-rules.md).
4. Return compact markdown using the `card-credits` contract in [../card-shared/command-contracts.yaml](../card-shared/command-contracts.yaml).
5. YAML is internal only — do not include it in user-facing output.
6. Do not show inline links, a sources footer, or a "Why It Matters" section.

## Required Sections

- `## 💳 Credits Overview`
- `## 🏷️ Credit Details`
- `## 📏 Usage Rules`
- `## 📋 Confidence Notes`

Omit `## Card Identity` when the match is confident. Use a numbered list for credits with amount, cadence, trigger, and restriction in one compact line per item.
