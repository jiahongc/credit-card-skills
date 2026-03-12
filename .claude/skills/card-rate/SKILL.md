---
name: card-rate
description: Return earning rates, caps, exclusions, activation requirements, and merchant-coding caveats for one major-US credit card. Use when the user wants the earn-side details only.
argument-hint: [card name]
disable-model-invocation: true
allowed-tools: Read, WebSearch, WebFetch, Bash(curl -sS *)
---

# Card Rate

## Goal

Return the earning-structure view of one exact card variant in compact format.

## Workflow

1. Resolve the card using [../card-identity/SKILL.md](../card-identity/SKILL.md). If ambiguous, return a numbered choice list and stop.
2. Follow the fast-search policy in [../card-shared/source-policy.yaml](../card-shared/source-policy.yaml): issuer rates and terms first, up to 2 secondary sources for merchant-coding or caveats.
3. Follow [../card-shared/confidence-rules.md](../card-shared/confidence-rules.md).
4. Return compact markdown using the `card-rate` contract in [../card-shared/command-contracts.yaml](../card-shared/command-contracts.yaml).
5. YAML is internal only — do not include it in user-facing output.
6. Do not show inline links, a sources footer, or a "Why It Matters" section.

## Required Sections

- `## 📊 Rate Summary`
- `## 📈 Earning Categories`
- `## 🚫 Caps And Exclusions`
- `## 📋 Confidence Notes`

Omit `## Card Identity` when the match is confident. Use short category lines and a compact exclusions/caps block.
