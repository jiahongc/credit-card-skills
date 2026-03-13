---
name: card-value
description: Estimate first-year value for one major-US credit card — welcome bonus + annual earn + credits minus annual fee. Accepts an optional spending breakdown. Covers 11 major US issuers including co-branded hotel and airline cards.
metadata:
  openclaw:
    requires:
      env:
        - BRAVE_API_KEY
      bins:
        - curl
    primaryEnv: BRAVE_API_KEY
---

# Card Value

Return a compact first-year value estimate for one exact card variant.

## When To Use

When the user asks about a card's value, worth, or first-year return. Trigger phrases: "card-value", "is it worth it", "first year value", "value estimate", "how much is the card worth".

## Input Format

The user provides a card name followed by an optional spending breakdown:
- `card-value Chase Sapphire Preferred` — uses default spend profile
- `card-value Chase Sapphire Preferred $500/mo dining, $200/mo travel, $3000/mo other` — uses provided breakdown

Default moderate-spender profile (if none given): $500/mo dining, $200/mo travel, $100/mo streaming, $200/mo groceries, $2000/mo other.

## Workflow

1. **Resolve card identity** — normalize and match to one exact variant. If ambiguous, return a numbered choice list and stop.
2. **Search** — run one Brave Search API call for current welcome offer and fee details.
3. **Research** — collect annual fee, welcome offer (bonus + spend requirement), earning rates by category, and statement credits.
4. **Compute** — `first_year_value = welcome_bonus_value + annual_earn_value + total_credits - annual_fee`.
5. **Confidence** — flag uncertain claims. Use 1 cpp baseline unless a known portal/transfer premium exists.

## Step 1: Card Identity Resolution

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

### Supported Issuers

American Express, Bank of America, Barclays, Bilt, Capital One, Chase, Citi, Discover, Robinhood, U.S. Bank, Wells Fargo.

## Step 2: Search

```bash
curl -sS "https://api.search.brave.com/res/v1/web/search?q=CARD+NAME+welcome+offer+annual+fee&count=20" \
  -H "X-Subscription-Token: $BRAVE_API_KEY"
```

### Source Policy

- **Issuer-first**: check the card's official product page first.
- **Max 5 secondary sources** from: NerdWallet (preferred), The Points Guy (preferred), Bankrate (preferred), One Mile at a Time (preferred), Doctor of Credit (preferred), Upgraded Points.
- **Disallowed**: Reddit, Facebook, Instagram, TikTok, X, YouTube, referral links, user forums.

## Required Output Sections

### `## 💳 Spend Profile`
The spending breakdown being used (default or user-provided), formatted as a compact table.

### `## 🎁 Welcome Bonus`
Bonus amount, spend requirement, qualification window, point valuation used.

### `## 📈 Annual Earn`
Earn by category based on the spend profile, with point values.

### `## 🏷️ Credits`
Applicable statement credits with annual total.

### `## 💰 Net First-Year Value`
Show the math clearly: `welcome_bonus + annual_earn + credits - annual_fee = net_value`.

### `## 📋 Confidence Notes`
Flag any uncertain claims. Note the cpp valuation assumed.

## Output Rules

- Use one emoji per section heading.
- Show the math clearly in the Net First-Year Value section.
- Keep content to condensed facts — no prose padding.
- Omit the Card Identity section when the match is confident.
- Do not show inline links, sources footer, or YAML blocks in output.

## Confidence Definitions

- **confirmed**: supported by issuer terms or multiple approved sources
- **unconfirmed**: plausible but not fully resolved
- **conflicting**: sources disagree on a material fact
