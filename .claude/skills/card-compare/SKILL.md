---
name: card-compare
description: Return a side-by-side comparison of two major-US credit cards across fees, earning rates, credits, transfer partners, and key benefits. Use when the user is deciding between two cards.
argument-hint: "[card A] vs [card B]"
disable-model-invocation: true
allowed-tools: Read, WebSearch, WebFetch, Bash(curl -sS *)
---

# Card Compare

## Goal

Return a compact side-by-side comparison of two exact card variants.

## Workflow

1. Parse two card names from the input (separated by "vs", "versus", "or", or a comma).
2. Resolve each card using [../card-identity/SKILL.md](../card-identity/SKILL.md). If either is ambiguous, return a numbered choice list for the ambiguous card and stop.
3. Follow the fast-search policy in [../card-shared/source-policy.yaml](../card-shared/source-policy.yaml): research both cards in parallel, issuer pages first, up to 4 secondary sources total (not per card).
4. Apply confidence handling from [../card-shared/confidence-rules.md](../card-shared/confidence-rules.md).
5. Return compact markdown using the `card-compare` contract in [../card-shared/command-contracts.yaml](../card-shared/command-contracts.yaml).
6. YAML is internal only — do not include it in user-facing output.
7. Do not show inline links, a sources footer, or a "Why It Matters" section.

## Required Sections

- `## 💰 Fees`
- `## 📈 Earning Rates`
- `## 🏷️ Credits`
- `## 🔄 Transfer Partners`
- `## ✈️ Key Benefits`
- `## 🏆 Bottom Line`
- `## 📋 Confidence Notes`

Omit `## Card Identity` when both matches are confident. Use a two-column format (Card A | Card B) for the comparison sections. The Bottom Line section should give a concise factual summary of which card wins in each major dimension — not a recommendation.
