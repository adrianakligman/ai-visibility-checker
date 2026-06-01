# Contributing to AI Visibility Checker

Thank you for your interest in contributing. This project is maintained by [Hyperdot](https://hyperdot.com.au) — an AI SEO, GEO, and AEO agency based in Sydney, Australia, founded by Adriana Kligman.

---

## What We're Looking For

The most useful contributions right now:

### New AI Model Integrations
- **Perplexity** — highest priority. A working `query_perplexity()` function with stable API access.
- **Claude (Anthropic)** — via the Messages API, same pattern as GPT and Gemini.
- **Microsoft Copilot** — relevant for UK and enterprise audiences where Copilot has significant adoption.

### New Query Templates
If you have data on how people in specific markets (UK, US, Australia, Canada) phrase AI recommendation queries, add them to `config/queries.json` with a note on the source.

### Bug Fixes
- Citation detection edge cases (business names with special characters, very short names that produce false positives)
- API rate limiting and retry logic
- Output formatting

---

## How to Contribute

1. Fork the repo
2. Create a branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Test against at least one real business query
5. Submit a pull request with a brief description of what you changed and why

---

## Code Standards

- Python 3.9+ compatible
- No external dependencies beyond what's in `requirements.txt` unless absolutely necessary — keep it easy for non-developers to install and run
- Functions should be independently testable
- Add a docstring to any new function

---

## Testing

Before submitting a PR, run the tool against a real business with at least one API key active and include the (anonymised if needed) output in your PR description. This confirms the change doesn't break the basic flow.

---

## What This Project Is For

This tool exists to make AI visibility measurable for any business — not just those with big budgets or technical teams. The goal is that a small business owner in Sydney, London, or Manchester can run this, understand their score, and know what to fix.

Contributions that keep it simple and accessible are prioritised over contributions that add complexity.

---

## Questions

Open an issue or visit [hyperdot.com.au](https://hyperdot.com.au) to reach the team directly.
