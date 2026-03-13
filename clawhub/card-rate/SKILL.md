---
name: card-rate
description: Return earning rates, bonus categories, caps, exclusions, and merchant-coding caveats for one major-US credit card. Covers 11 major US issuers including co-branded hotel and airline cards.
metadata:
  openclaw:
    requires:
      env:
        - BRAVE_API_KEY
      bins:
        - curl
    primaryEnv: BRAVE_API_KEY
---

# Card Rate

Return the earning-structure view of one exact card variant in compact format.

## When To Use

When the user asks about a card's earning rates, rewards categories, multipliers, or points structure. Trigger phrases: "card-rate", "earning rates", "how many points", "what categories", "rewards rate".

## Workflow

1. **Resolve card identity** — normalize the input and match to one exact card variant.
2. **Search issuer only** — run one Brave Search API call scoped to the issuer domain. Do NOT search secondary sources.
3. **Compile** — combine search snippets with knowledge to fill all required sections.
4. **Confidence** — flag uncertain or conflicting claims.

## Step 1: Card Identity Resolution

Normalize the card name and resolve to an exact issuer + family + variant.

### Common Abbreviations

| Input | Resolved |
|---|---|
| CSP | Chase Sapphire Preferred |
| CSR | Chase Sapphire Reserve |
| CFU | Chase Freedom Unlimited |
| CFF | Chase Freedom Flex |
| Amex Gold | American Express Gold Card |
| Amex Plat | American Express Platinum Card |
| Venture X | Capital One Venture X Rewards Credit Card |
| Savor | Capital One SavorOne / Savor (ambiguous — ask) |
| Double Cash | Citi Double Cash Card |
| Custom Cash | Citi Custom Cash Card |
| Bilt | Bilt Blue / Obsidian / Palladium (ambiguous — ask) |
| Bilt Blue | Bilt Blue Card |
| Bilt Obsidian | Bilt Obsidian Card |
| Bilt Palladium | Bilt Palladium Card |
| Robinhood | Robinhood Gold Card / Cash Card (ambiguous — ask) |
| Robinhood Gold | Robinhood Gold Card |
| Robinhood Cash | Robinhood Cash Card |
| Amex Biz Gold | American Express Business Gold Card |
| Amex Biz Plat | American Express Business Platinum Card |
| Amex Blue Biz Plus | American Express Blue Business Plus Card |
| Amex Blue Biz Cash | American Express Blue Business Cash Card |
| Ink Preferred | Chase Ink Business Preferred |
| Ink Cash | Chase Ink Business Cash |
| Ink Unlimited | Chase Ink Business Unlimited |
| CIU | Chase Ink Business Unlimited |
| CIC | Chase Ink Business Cash |
| CIP | Chase Ink Business Preferred |
| Spark Cash Plus | Capital One Spark Cash Plus |
| Spark Miles | Capital One Spark Miles |
| Venture X Business | Capital One Venture X Business Card |
| Aviator Red | Barclays AAdvantage Aviator Red World Elite Mastercard |
| Aviator Business | Barclays AAdvantage Aviator Business Mastercard |
| JetBlue Card | Barclays JetBlue Card |
| JetBlue Plus | Barclays JetBlue Plus Card |
| JetBlue Business | Barclays JetBlue Business Card |
| Wyndham Rewards | Barclays Wyndham Rewards Earner Card / Plus / Business (ambiguous — ask) |
| Wyndham Plus | Barclays Wyndham Rewards Earner Plus Card |
| Wyndham Business | Barclays Wyndham Rewards Earner Business Card |
| Altitude Reserve | U.S. Bank Altitude Reserve Visa Infinite Card |
| Altitude Connect | U.S. Bank Altitude Connect Visa Signature Card |
| Altitude Go | U.S. Bank Altitude Go Visa Signature Card |
| Marriott Bonvoy Boundless | Chase Marriott Bonvoy Boundless Credit Card |
| Marriott Bonvoy Bold | Chase Marriott Bonvoy Bold Credit Card |
| Marriott Bonvoy Bountiful | Chase Marriott Bonvoy Bountiful Card |
| Marriott Bonvoy Brilliant | American Express Marriott Bonvoy Brilliant Card |
| Marriott Bonvoy Business | American Express Marriott Bonvoy Business Card |
| Hilton Honors Card | American Express Hilton Honors Card |
| Hilton Surpass | American Express Hilton Honors Surpass Card |
| Hilton Aspire | American Express Hilton Honors Aspire Card |
| Hilton Business | American Express Hilton Honors Business Card |
| IHG Premier | Chase IHG One Rewards Premier Credit Card |
| IHG Traveler | Chase IHG One Rewards Traveler Credit Card |
| IHG Business | Chase IHG One Rewards Premier Business Credit Card |
| World of Hyatt | Chase World of Hyatt Credit Card |
| Hyatt Business | Chase World of Hyatt Business Credit Card |
| United Explorer | Chase United Explorer Card |
| United Quest | Chase United Quest Card |
| United Club Infinite | Chase United Club Infinite Card |
| United Gateway | Chase United Gateway Card |
| United Business | Chase United Business Card |
| Southwest Priority | Chase Southwest Rapid Rewards Priority Credit Card |
| Southwest Plus | Chase Southwest Rapid Rewards Plus Credit Card |
| Southwest Premier | Chase Southwest Rapid Rewards Premier Credit Card |
| Southwest Performance Business | Chase Southwest Rapid Rewards Performance Business Credit Card |
| Southwest Premier Business | Chase Southwest Rapid Rewards Premier Business Credit Card |
| Delta Gold | American Express Delta SkyMiles Gold Card |
| Delta Platinum | American Express Delta SkyMiles Platinum Card |
| Delta Reserve | American Express Delta SkyMiles Reserve Card |
| Delta Biz Gold | American Express Delta SkyMiles Gold Business Card |
| Delta Biz Plat | American Express Delta SkyMiles Platinum Business Card |
| Delta Biz Reserve | American Express Delta SkyMiles Reserve Business Card |
| Alaska Airlines | Bank of America Alaska Airlines Visa Signature Credit Card |
| Alaska Airlines Business | Bank of America Alaska Airlines Visa Business Credit Card |
| AAdvantage MileUp | Citi AAdvantage MileUp Card |
| AAdvantage Platinum Select | Citi AAdvantage Platinum Select World Elite Mastercard |
| AAdvantage Executive | Citi AAdvantage Executive World Elite Mastercard |

### Business vs Personal

Both personal and business credit cards are supported. If the user specifies "business" or "biz", resolve to the business variant. If a card name exists in both versions and the user does not specify, treat as ambiguous and ask.

### Ambiguity Rules

- If the input maps to 2+ plausible variants, return a **numbered choice list** and stop.
- If no match exists, return: "Could not match a card. Try including the full card name with issuer."

### Supported Issuers

American Express, Bank of America, Barclays, Bilt, Capital One, Chase, Citi, Discover, Robinhood, U.S. Bank, Wells Fargo.

## Step 2: Search (Issuer Only)

Run one Brave Search API call scoped to the issuer domain:

```bash
curl -sS "https://api.search.brave.com/res/v1/web/search?q=CARD+NAME+site:ISSUER_DOMAIN&count=5" \
  -H "X-Subscription-Token: $BRAVE_API_KEY"
```

### Issuer Domains

| Issuer | Domain |
|---|---|
| American Express | americanexpress.com |
| Bank of America | bankofamerica.com |
| Barclays | cards.barclaycardus.com |
| Bilt | bfrrewards.com |
| Capital One | capitalone.com |
| Chase | chase.com |
| Citi | citi.com |
| Discover | discover.com |
| Robinhood | robinhood.com |
| U.S. Bank | usbank.com |
| Wells Fargo | wellsfargo.com |

Use up to 1 secondary source (prefer Bankrate) for merchant-coding caveats if needed. Combine the issuer search snippets with training knowledge.

## Required Output Sections

### `## 📊 Rate Summary`
Base earn rate, point currency, key mechanic (e.g., rotating categories, pay-over-time requirement).

### `## 📈 Earning Categories`
Each bonus category with multiplier, numbered list. Include activation requirements if applicable.

### `## 🚫 Caps And Exclusions`
Annual/quarterly caps, excluded merchant types, category restrictions.

### `## 📋 Confidence Notes`
Flag any detail that may have changed since training data.

## Output Rules

- Use one emoji per section heading and numbered lists for categories.
- Keep content to condensed facts — no prose padding.
- Omit the Card Identity section when the match is confident.
- Do not show inline links, sources footer, or YAML blocks in output.

## Confidence Definitions

- **confirmed**: supported by issuer terms or multiple approved sources
- **unconfirmed**: plausible but not fully resolved
- **conflicting**: sources disagree on a material fact
