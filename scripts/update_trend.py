"""
update_trend.py
===============
Reads all JSON reports in reports/ and writes a VISIBILITY_TREND.md
summary table showing score over time.

Run automatically by the weekly GitHub Actions workflow.
"""

import json
import os
from pathlib import Path
from datetime import datetime


REPORTS_DIR = Path("reports")
OUTPUT_FILE = Path("VISIBILITY_TREND.md")


def load_reports() -> list[dict]:
    reports = []
    for path in sorted(REPORTS_DIR.glob("report_*.json")):
        try:
            with open(path) as f:
                data = json.load(f)
                data["_file"] = path.name
                reports.append(data)
        except (json.JSONDecodeError, KeyError):
            continue
    return reports


def score_bar(score: int) -> str:
    filled = round(score / 10)
    return "█" * filled + "░" * (10 - filled)


def citation_summary(results: list[dict]) -> dict:
    gpt = [r for r in results if r.get("model") == "gpt-4o"]
    gemini = [r for r in results if r.get("model") == "gemini-1.5-pro"]
    return {
        "gpt_cited": sum(1 for r in gpt if r.get("cited")),
        "gpt_total": len(gpt),
        "gemini_cited": sum(1 for r in gemini if r.get("cited")),
        "gemini_total": len(gemini),
    }


def write_trend(reports: list[dict]) -> None:
    lines = [
        "# AI Visibility Trend — Hyperdot",
        "",
        "Auto-generated weekly by GitHub Actions. "
        "Tracks how often [Hyperdot](https://hyperdot.com.au) is cited by AI models over time.",
        "",
        "## Score History",
        "",
        "| Date | Score | Bar | GPT-4o | Gemini |",
        "|------|-------|-----|--------|--------|",
    ]

    for r in reversed(reports):  # most recent first
        date = r.get("date", "unknown")
        score = r.get("score", 0)
        results = r.get("results", [])
        cs = citation_summary(results)

        gpt_str = f"{cs['gpt_cited']}/{cs['gpt_total']}" if cs["gpt_total"] else "—"
        gemini_str = f"{cs['gemini_cited']}/{cs['gemini_total']}" if cs["gemini_total"] else "—"
        bar = score_bar(score)

        lines.append(f"| {date} | {score}/100 | `{bar}` | {gpt_str} | {gemini_str} |")

    if len(reports) >= 2:
        latest = reports[-1].get("score", 0)
        previous = reports[-2].get("score", 0)
        delta = latest - previous
        direction = "▲" if delta > 0 else ("▼" if delta < 0 else "→")
        lines += [
            "",
            "## Latest vs Previous",
            "",
            f"**{direction} {abs(delta)} points** week-on-week "
            f"({previous} → {latest})",
        ]

    if reports:
        latest_report = reports[-1]
        recs = latest_report.get("recommendations", [])
        if recs:
            lines += [
                "",
                "## Current Recommendations",
                "",
            ]
            for rec in recs:
                lines.append(f"- {rec}")

    lines += [
        "",
        "---",
        "",
        f"*Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}*",
        "",
        "Built by [Hyperdot](https://hyperdot.com.au) — "
        "Sydney's AI SEO, GEO & AEO specialists.",
    ]

    OUTPUT_FILE.write_text("\n".join(lines))
    print(f"Trend written to {OUTPUT_FILE} ({len(reports)} reports)")


def main():
    if not REPORTS_DIR.exists():
        print("No reports/ directory found. Run checker.py first.")
        return

    reports = load_reports()
    if not reports:
        print("No report JSON files found in reports/")
        return

    write_trend(reports)


if __name__ == "__main__":
    main()
