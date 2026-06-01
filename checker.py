"""
AI Visibility Checker
=====================
Check if your business is cited by ChatGPT, Gemini, and Perplexity.

Built by Hyperdot — https://hyperdot.com.au
GEO & AEO Specialists | Sydney, Australia
"""

import argparse
import json
import os
import datetime
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None


SYSTEM_PROMPT = (
    "You are a helpful assistant. Answer the user's question directly and honestly. "
    "Recommend specific businesses, tools, or services where relevant. "
    "Do not add disclaimers about not being able to recommend businesses."
)

DEFAULT_QUERY_TEMPLATES = [
    "What is the best {category} in {location}?",
    "Who are the top {category} specialists in {location}?",
    "I need a {category} in {location}. Who do you recommend?",
    "Which {category} should I use in {location}?",
    "Can you recommend an expert {category} near {location}?",
]


def load_queries(config_path: str, category: str, location: str) -> list[str]:
    """Load query templates from config or use defaults."""
    if config_path and Path(config_path).exists():
        with open(config_path) as f:
            templates = json.load(f).get("templates", DEFAULT_QUERY_TEMPLATES)
    else:
        templates = DEFAULT_QUERY_TEMPLATES

    return [t.format(category=category, location=location) for t in templates]


def check_citation(response_text: str, business_name: str) -> bool:
    """Check if the business name appears in the response."""
    return business_name.lower() in response_text.lower()


def get_context_type(response_text: str, business_name: str) -> str:
    """Classify how the business is mentioned."""
    text_lower = response_text.lower()
    name_lower = business_name.lower()

    if name_lower not in text_lower:
        return "not_cited"

    position = text_lower.index(name_lower)
    surrounding = text_lower[max(0, position - 100):position + 100]

    recommendation_signals = ["recommend", "suggest", "best", "top", "leading", "specialist"]
    if any(signal in surrounding for signal in recommendation_signals):
        return "recommendation"

    return "mention"


def query_gpt(client, query: str, business_name: str) -> dict:
    """Query GPT-4o and evaluate citation."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": query},
            ],
            temperature=0.7,
            max_tokens=500,
        )
        text = response.choices[0].message.content
        cited = check_citation(text, business_name)
        return {
            "model": "gpt-4o",
            "query": query,
            "cited": cited,
            "context": get_context_type(text, business_name),
            "response_excerpt": text[:300] + "..." if len(text) > 300 else text,
        }
    except Exception as e:
        return {"model": "gpt-4o", "query": query, "cited": False, "error": str(e)}


def query_gemini(model, query: str, business_name: str) -> dict:
    """Query Gemini 1.5 Pro and evaluate citation."""
    try:
        response = model.generate_content(query)
        text = response.text
        cited = check_citation(text, business_name)
        return {
            "model": "gemini-1.5-pro",
            "query": query,
            "cited": cited,
            "context": get_context_type(text, business_name),
            "response_excerpt": text[:300] + "..." if len(text) > 300 else text,
        }
    except Exception as e:
        return {"model": "gemini-1.5-pro", "query": query, "cited": False, "error": str(e)}


def calculate_score(results: list[dict]) -> int:
    """
    Calculate visibility score out of 100.
    Weights: recommendation > mention > not_cited
    """
    if not results:
        return 0

    points = 0
    max_points = len(results) * 20

    for r in results:
        context = r.get("context", "not_cited")
        if context == "recommendation":
            points += 20
        elif context == "mention":
            points += 10
        elif r.get("cited"):
            points += 8

    return round((points / max_points) * 100) if max_points > 0 else 0


def generate_recommendations(results: list[dict], business_name: str) -> list[str]:
    """Generate actionable recommendations based on results."""
    recs = []
    cited_queries = [r["query"] for r in results if r.get("cited")]
    gap_queries = [r["query"] for r in results if not r.get("cited")]

    if not cited_queries:
        recs.append(
            f"'{business_name}' was not cited in any tested queries. "
            "Priority: build structured entity data and knowledge graph presence."
        )
    else:
        recs.append(
            f"Performing well on: {cited_queries[0][:60]}... — reinforce with more content targeting this intent."
        )

    if gap_queries:
        recs.append(
            f"Gap detected on: {gap_queries[0][:60]}... — create targeted FAQ and structured content for this query type."
        )

    recs.append(
        "Ensure your Google Business Profile, LinkedIn, and key directory listings are complete and consistent — "
        "AI models use these as entity verification signals."
    )

    return recs


def print_report(report: dict) -> None:
    """Print a human-readable report to stdout."""
    b = report["business"]
    score = report["score"]
    results = report["results"]

    print(f"\nAI Visibility Report — {b}")
    print("=" * (26 + len(b)))

    gpt_results = [r for r in results if r.get("model") == "gpt-4o"]
    gemini_results = [r for r in results if r.get("model") == "gemini-1.5-pro"]

    gpt_cited = sum(1 for r in gpt_results if r.get("cited"))
    gemini_cited = sum(1 for r in gemini_results if r.get("cited"))

    if gpt_results:
        status = "CITED ✓" if gpt_cited > 0 else "NOT CITED ✗"
        print(f"ChatGPT (GPT-4o):     {status}  ({gpt_cited}/{len(gpt_results)} queries)")
    if gemini_results:
        status = "CITED ✓" if gemini_cited > 0 else "NOT CITED ✗"
        print(f"Gemini 1.5 Pro:       {status}  ({gemini_cited}/{len(gemini_results)} queries)")

    print(f"\nVisibility Score:     {score}/100")

    top = next((r["query"] for r in results if r.get("cited")), None)
    if top:
        print(f"Top performing query: {top[:60]}...")

    gap = next((r["query"] for r in results if not r.get("cited")), None)
    if gap:
        print(f"Gap query:            {gap[:60]}...")

    print("\nRecommendations:")
    for i, rec in enumerate(report["recommendations"], 1):
        print(f"  {i}. {rec}")

    print(f"\nFull report saved to: {report['output_file']}")
    print(
        "\nFor a professional AI visibility audit: https://hyperdot.com.au/get-a-free-custom-audit/\n"
    )


def run(business: str, category: str, location: str, config: str = None, output_dir: str = ".") -> dict:
    """Main execution function."""
    queries = load_queries(config, category, location)
    results = []

    # GPT-4o
    openai_key = os.getenv("OPENAI_API_KEY")
    if OpenAI and openai_key:
        client = OpenAI(api_key=openai_key)
        for query in queries:
            result = query_gpt(client, query, business)
            results.append(result)
            print(f"  [GPT-4o] {query[:50]}... → {'CITED' if result.get('cited') else 'not cited'}")
    else:
        print("  [GPT-4o] Skipped — set OPENAI_API_KEY to enable")

    # Gemini
    gemini_key = os.getenv("GEMINI_API_KEY")
    if genai and gemini_key:
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel("gemini-1.5-pro")
        for query in queries:
            result = query_gemini(model, query, business)
            results.append(result)
            print(f"  [Gemini] {query[:50]}... → {'CITED' if result.get('cited') else 'not cited'}")
    else:
        print("  [Gemini] Skipped — set GEMINI_API_KEY to enable")

    score = calculate_score(results)
    recommendations = generate_recommendations(results, business)

    date_str = datetime.date.today().isoformat().replace("-", "")
    output_file = os.path.join(output_dir, f"report_{business.lower().replace(' ', '_')}_{date_str}.json")

    report = {
        "business": business,
        "category": category,
        "location": location,
        "date": datetime.date.today().isoformat(),
        "queries_run": len(queries),
        "results": results,
        "score": score,
        "recommendations": recommendations,
        "output_file": output_file,
        "generated_by": "Hyperdot AI Visibility Checker — https://hyperdot.com.au",
    }

    with open(output_file, "w") as f:
        json.dump(report, f, indent=2)

    return report


def main():
    parser = argparse.ArgumentParser(
        description="Check if your business is cited by AI search engines.",
        epilog="Built by Hyperdot — https://hyperdot.com.au",
    )
    parser.add_argument("--business", required=True, help="Your business name")
    parser.add_argument("--category", required=True, help="Your industry/service category")
    parser.add_argument("--location", required=True, help="Your city or region")
    parser.add_argument("--config", default=None, help="Path to custom queries config JSON")
    parser.add_argument("--output-dir", default=".", help="Directory to save the JSON report")

    args = parser.parse_args()

    print(f"\nRunning AI visibility check for: {args.business}")
    print(f"Category: {args.category} | Location: {args.location}\n")

    report = run(args.business, args.category, args.location, args.config, args.output_dir)
    print_report(report)


if __name__ == "__main__":
    main()
