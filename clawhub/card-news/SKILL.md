---
name: card-news
description: Return material news about one major-US credit card from the last 3 months — direct card changes, issuer updates, and major coverage. Covers 11 major US issuers including co-branded hotel and airline cards.
metadata:
  openclaw:
    requires:
      env:
        - BRAVE_API_KEY
      bins:
        - curl
    primaryEnv: BRAVE_API_KEY
---

# Card News

Return the last-3-month news view of one exact card variant in compact format.

## When To Use

When the user asks about recent changes, news, or updates for a credit card. Trigger phrases: "card-news", "any changes", "recent news", "what's new with", "updates for".

## Workflow

1. **Resolve card identity** — normalize and match to one exact variant. If ambiguous, return a numbered choice list and stop.
2. **Search** — run one Brave Search API call with freshness filter for recent results.
3. **Filter** — apply 3-month lookback window and inclusion rules.
4. **Compile** — assemble the news report.
5. **Confidence** — flag uncertain or conflicting claims.

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

Run one Brave Search API call with freshness filter:

```bash
curl -sS "https://api.search.brave.com/res/v1/web/search?q=CARD+NAME+news+CURRENT_YEAR&count=20&freshness=pm" \
  -H "X-Subscription-Token: $BRAVE_API_KEY"
```

The `freshness=pm` parameter limits results to the past month. Replace `CURRENT_YEAR` with the actual current year.

### Source Policy

- **Issuer newsrooms first**: check issuer blogs and press release pages.
- **Max 5 secondary sources** from: Doctor of Credit (preferred), The Points Guy (preferred), One Mile at a Time (preferred), NerdWallet (preferred), Bankrate (preferred), Upgraded Points.
- **Disallowed**: Reddit, Facebook, Instagram, TikTok, X, YouTube, referral links, user forums.

## Recency Rules

- Use a **3-month lookback window** only.
- **Include**: direct card changes, issuer updates that materially affect the card, major approved-site coverage that changes how the card should be understood.
- **Exclude**: generic issuer chatter, evergreen "best card" articles that do not describe a recent change.

## Required Output Sections

### `## 📅 News Window`
Start and end dates of the 3-month lookback window.

### `## 📰 Recent Updates`
Numbered list of material changes with date and short summary per item.

### `## 📝 Summary`
2-3 sentence synthesis of what changed and what stayed the same.

### `## 📋 Confidence Notes`
Flag any uncertain, unconfirmed, or conflicting claims.

## Output Rules

- Use one emoji per section heading and numbered lists for updates.
- Keep content to condensed facts — no prose padding.
- Omit the Card Identity section when the match is confident.
- Do not show inline links, sources footer, or YAML blocks in output.

## Confidence Definitions

- **confirmed**: supported by issuer terms or multiple approved sources
- **unconfirmed**: plausible but not fully resolved
- **conflicting**: sources disagree on a material fact
