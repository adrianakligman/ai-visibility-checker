# Methodology

How this tool measures AI visibility — explained plainly, with no jargon you don't need.

Built by [Hyperdot](https://hyperdot.com.au) — AI SEO, GEO, and AEO specialists, Sydney, Australia. Founded by Adriana Kligman, CMDO & Founder.

---

## The Core Idea

When someone asks ChatGPT "What's the best accountant in Melbourne?" — does your business name appear in the answer?

That's AI visibility. This tool tests it systematically.

---

## Step 1 — Query Design

The tool tests your business against **5 query templates** that represent the most common ways people ask AI systems for business recommendations.

| Query Pattern | Why It's Used |
|---|---|
| `"What is the best {category} in {location}?"` | The single most common AI recommendation query format |
| `"Who are the top {category} specialists in {location}?"` | Authority/expertise framing — tests whether AI ranks you as an expert |
| `"I need a {category} in {location}. Who do you recommend?"` | Conversational, matches how people actually talk to ChatGPT |
| `"Which {category} should I use in {location}?"` | Comparison/decision intent |
| `"Can you recommend an expert {category} near {location}?"` | Local intent with expertise signal |

These patterns are drawn from observed real-world AI search behaviour in Australia and the UK. You can customise them in `config/queries.json`.

---

## Step 2 — Running the Queries

Each query is sent directly to the AI model's API (not a web interface). This matters because:

- **Reproducible** — you get the same testing conditions every run
- **Comparable** — different businesses are tested under identical conditions
- **No personalisation** — API calls aren't influenced by your search history

Every query uses the same fixed system prompt:

> *"You are a helpful assistant. Answer the user's question directly and honestly. Recommend specific businesses, tools, or services where relevant."*

This instructs the model to actually make recommendations, rather than deflecting.

**Temperature is set to 0.7** — standard conversational setting. Not too random, not robotic.

---

## Step 3 — Citation Detection

The tool checks whether your business name appears in the AI response using exact string matching (case-insensitive).

This is conservative by design. A partial match or abbreviation doesn't count. Your full business name has to appear.

---

## Step 4 — Context Classification

Being mentioned is not the same as being recommended. The tool classifies each citation:

| Context Type | What It Means | Points |
|---|---|---|
| **Recommendation** | Your name appears near words like "recommend", "best", "top", "leading", "specialist" | 20 |
| **Mention** | Your name appears but without a recommendation signal | 10 |
| **Not cited** | Your name doesn't appear at all | 0 |

---

## Step 5 — Scoring

```
Visibility Score (0–100) = (total points earned / maximum possible points) × 100
```

Maximum points = number of queries × 20 (if every result was a recommendation).

A score of **0–30** means you have low or no AI visibility — urgent attention needed.  
A score of **31–60** means partial visibility — you're showing up in some contexts but not others.  
A score of **61–100** means strong visibility — AI systems recognise and recommend you.

---

## Limitations

**AI outputs vary.** LLMs are not deterministic — the same query can produce different answers on different runs. For this reason, the weekly automated monitoring (which averages across multiple weeks) is more reliable than a single run.

**Training data lag.** AI models have a knowledge cutoff. Recent PR coverage, new structured data, or entity improvements may not yet be reflected in model outputs. Changes typically take weeks to months to appear.

**Position is not measured.** This version detects presence, not rank order within a response. Being cited first vs. last scores the same. A future version will address this.

**Perplexity excluded.** Perplexity does not offer a stable public API for programmatic querying. Manual checking at perplexity.ai using the query templates above is currently the only option.

---

## What Affects Your Score (And How to Improve It)

AI systems cite businesses they "trust" — which means businesses with strong, consistent entity signals across the web. The highest-impact improvements are:

1. **Complete entity data** — Google Business Profile, LinkedIn company page, industry directories. Consistent name, address, phone, and description across all of them.
2. **Structured FAQ content** — Pages that directly answer the question patterns above in plain language.
3. **Third-party citations** — Mentions in authoritative publications, industry databases, and review platforms. AI systems treat these as credibility signals.
4. **Schema markup** — Structured data that tells AI crawlers exactly who you are, what you do, and where you operate.

This is exactly what [Hyperdot's GEO and AEO services](https://hyperdot.com.au/generative-engine-optimisation/) engineer for clients.

---

## Further Reading

- [What is Generative Engine Optimisation (GEO)?](https://hyperdot.com.au/generative-engine-optimisation/)
- [What is Answer Engine Optimisation (AEO)?](https://hyperdot.com.au/ai-seo-services-sydney/)
- [Algorithmic Signal Engineering (ASE)](https://hyperdot.com.au/algorithmic-signal-engineering-ase/)
- [Free AI Visibility Audit — Hyperdot](https://hyperdot.com.au/get-a-free-custom-audit/)
