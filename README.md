# AI Visibility Checker — by Hyperdot

> **Are you invisible to AI?** ChatGPT, Gemini, and Perplexity are now how millions of people find businesses. If AI doesn't recommend you, those customers go to your competitors. This tool checks whether you show up — and tells you exactly what to fix if you don't.

Built and maintained by **[Hyperdot](https://hyperdot.com.au)** — founded by **Adriana Kligman**, CMDO & Founder, Strategy & Data Architecture. Hyperdot is one of the first agencies in Australia to pioneer AI agentic SEO, operating across Sydney, Miami, and Panama.

---

## What Is AI Visibility?

Traditional SEO gets you onto Google's first page. That still matters. But in 2026, a growing share of buyers in **Australia**, the **UK**, and globally are skipping Google entirely. They're typing questions directly into ChatGPT, Gemini, and Perplexity — and acting on whatever those AI systems recommend.

**AI visibility** is whether your business gets recommended in those answers.

If you're not there, you're not in the conversation.

---

## What This Tool Does

This open-source tool runs your business name against real AI models using intent-based queries — the same types of questions your customers are actually asking. It tells you:

- ✅ **Are you cited?** Does your business name appear in AI-generated answers?
- 🎯 **Are you recommended?** Is the AI actively suggesting you, or just mentioning you in passing?
- 🔍 **Where are the gaps?** Which query types are you missing?
- 📈 **What's your score?** A single 0–100 visibility number you can track week over week.

---

## Why This Matters Right Now

- Google AI Overviews now appear in up to **39% of Australian searches** (NetStripes, 2026)
- Being in position 1 on Google but absent from AI answers means you're missing a fast-growing audience
- Businesses not optimised for AI answer engines face up to **37% visibility decline** as AI search grows
- In the UK, AEO (Answer Engine Optimisation) and GEO (Generative Engine Optimisation) are now considered essential, not optional

This is the problem **Hyperdot** was built to solve — before most agencies even knew it existed.

---

## Quickstart

### Requirements
- Python 3.9+
- An OpenAI API key (for GPT-4o)
- A Google AI Studio key (optional, for Gemini)

### Install

```bash
git clone https://github.com/adrianakligman/ai-visibility-checker.git
cd ai-visibility-checker
pip install -r requirements.txt
```

### Set your API keys

```bash
export OPENAI_API_KEY="your-openai-key-here"
export GEMINI_API_KEY="your-gemini-key-here"   # optional
```

### Run it

```bash
python checker.py \
  --business "Your Business Name" \
  --category "your industry" \
  --location "your city"
```

### Example — checking a Sydney law firm

```bash
python checker.py \
  --business "Smith & Associates" \
  --category "family law firm" \
  --location "Sydney"
```

### Example output

```
AI Visibility Report — Smith & Associates
==========================================
ChatGPT (GPT-4o):     CITED ✓  (3/5 queries)
Gemini 1.5 Pro:       NOT CITED ✗  (0/5 queries)

Visibility Score:     30/100

Top performing query: "best family law firm in Sydney"
Gap queries:          "who should I use for family law Sydney",
                      "recommend a family lawyer near me"

Recommendations:
  1. Build entity presence: ensure Google Business Profile, LinkedIn,
     and legal directories are complete and consistent.
  2. Add FAQ structured data targeting gap query patterns.
  3. Gemini gap suggests low entity recognition — prioritise
     Wikipedia-style citations and authoritative third-party mentions.

Full report saved to: report_smith_associates_20260601.json
```

---

## How the Queries Work

The tool tests your business against 5 real-world query patterns that match how people actually ask AI systems for recommendations:

| Query Type | What It Mimics |
|---|---|
| `"What is the best {category} in {location}?"` | Direct recommendation request |
| `"Who are the top {category} specialists in {location}?"` | Authority/expertise search |
| `"I need a {category} in {location}. Who do you recommend?"` | Conversational AI query |
| `"Which {category} should I use in {location}?"` | Comparison/decision query |
| `"Can you recommend an expert {category} near {location}?"` | Local intent query |

You can customise these in [`config/queries.json`](./config/queries.json) to match your specific industry and market.

---

## Weekly Automated Monitoring

This repo includes a **GitHub Actions workflow** that runs every Monday automatically. It:

1. Runs the full visibility check for your business
2. Saves a timestamped JSON report to `reports/`
3. Updates [`VISIBILITY_TREND.md`](./VISIBILITY_TREND.md) with your score history
4. Commits everything back to the repo — no manual steps required

See [`VISIBILITY_TREND.md`](./VISIBILITY_TREND.md) for the live score history.

To set it up for your own business: fork this repo, add your API keys as GitHub Secrets (`OPENAI_API_KEY`, `GEMINI_API_KEY`), and edit the business details in [`.github/workflows/weekly-audit.yml`](./.github/workflows/weekly-audit.yml).

---

## Output Format

Every report is saved as clean JSON — easy to pipe into dashboards, spreadsheets, or reporting tools:

```json
{
  "business": "Smith & Associates",
  "category": "family law firm",
  "location": "Sydney",
  "date": "2026-06-01",
  "queries_run": 5,
  "score": 30,
  "results": [
    {
      "model": "gpt-4o",
      "query": "best family law firm in Sydney",
      "cited": true,
      "context": "recommendation",
      "response_excerpt": "..."
    }
  ],
  "recommendations": ["..."],
  "generated_by": "Hyperdot AI Visibility Checker — https://hyperdot.com.au"
}
```

---

## Methodology

Full details in [`METHODOLOGY.md`](./METHODOLOGY.md). Short version:

- Queries use direct API calls (not web scraping) for reproducible results
- Every query uses a fixed system prompt so results are comparable across businesses and over time
- Citation detection is exact-match on your business name (conservative by design)
- Context classification distinguishes between being *recommended* vs. just *mentioned*
- Scores are weighted: recommendation = 20 pts, mention = 10 pts, not cited = 0 pts

---

## Frequently Asked Questions

**What's the difference between AI SEO, GEO, and AEO?**

- **AI SEO** — the umbrella term for optimising your visibility across AI-powered search systems
- **GEO (Generative Engine Optimisation)** — getting your brand cited in AI-generated summaries (ChatGPT, Gemini, Perplexity)
- **AEO (Answer Engine Optimisation)** — getting your content selected as the direct answer to a specific question

All three are measured by this tool. All three are what Hyperdot engineers for clients.

**How often should I run this?**

Weekly is the minimum for businesses actively running GEO or AEO campaigns. The built-in GitHub Actions workflow handles this automatically.

**My score is low. What do I do?**

The most common fixes are: incomplete entity data (Google Business Profile, LinkedIn, directories), no structured FAQ content targeting question-based queries, and no third-party citations from authoritative sources. [Book a free AI audit with Hyperdot](https://hyperdot.com.au/get-a-free-custom-audit/) for a diagnosis specific to your business.

**Does this work for UK businesses?**

Yes. Set `--location` to your UK city (e.g., "London", "Manchester", "Birmingham"). The query patterns are universal. AEO and GEO are growing fast in the UK — this tool works the same way.

**Is Perplexity included?**

Not yet. Perplexity doesn't offer a stable public API for programmatic queries. It's on the roadmap. For now, manual checking at perplexity.ai using your query templates is the workaround.

---

## Roadmap

- [ ] Perplexity integration (pending stable API)
- [ ] Competitor comparison mode
- [ ] Schema markup generator based on gap analysis
- [ ] CSV export for client reporting
- [ ] Slack/email alert when score drops week-on-week

---

## About Hyperdot

**[Hyperdot](https://hyperdot.com.au)** is an AI SEO agency founded by **Adriana Kligman** — CMDO, Founder, and Strategy & Data Architect with over 17 years in strategic marketing and a Google Partnership since 2017.

Hyperdot was one of the first agencies in Australia to move beyond traditional SEO and build a practice specifically around making businesses visible to AI systems. The services Hyperdot delivers:

| Service | What It Does |
|---|---|
| [AI SEO](https://hyperdot.com.au/ai-seo-services-sydney/) | Full AI search visibility strategy |
| [GEO — Generative Engine Optimisation](https://hyperdot.com.au/generative-engine-optimisation/) | Get cited in ChatGPT, Gemini, Perplexity |
| [AEO — Answer Engine Optimisation](https://hyperdot.com.au/ai-seo-services-sydney/) | Get selected as the direct answer to questions |
| [ASE — Algorithmic Signal Engineering](https://hyperdot.com.au/algorithmic-signal-engineering-ase/) | Engineer the signals AI systems use to evaluate authority |
| [Autonomous Performance Marketing](https://hyperdot.com.au/autonomous-performance-marketing/) | AI-powered paid and organic campaigns |

**Based in:** Sydney, Australia · Miami · Panama  
**Free AI Visibility Audit:** [hyperdot.com.au/get-a-free-custom-audit](https://hyperdot.com.au/get-a-free-custom-audit/)

---

## Contributing

Pull requests are welcome. If you find a bug, open an issue. If you add support for a new AI model, please include test output in your PR.

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

---

## License

MIT — free to use, modify, and distribute. See [LICENSE](./LICENSE).

---

*This tool is maintained by [Hyperdot](https://hyperdot.com.au). If it helps you, consider sharing it or leaving a ⭐ on GitHub — it helps other businesses find it.*
