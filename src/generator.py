import os
import json
import random
from urllib import response
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def generate_financials(company: str, sector: str, base_revenue_m: float) -> dict:
    revenue = base_revenue_m * random.uniform(0.95, 1.12)
    ebitda_margin = random.uniform(0.18, 0.32)
    ebitda = revenue * ebitda_margin
    net_income = ebitda * random.uniform(0.45, 0.65)
    shares_m = random.uniform(200, 800)
    eps = (net_income / shares_m) * 1000

    return {
        "company":           company,
        "sector":            sector,
        "revenue_m":         round(revenue, 1),
        "ebitda_m":          round(ebitda, 1),
        "ebitda_margin_pct": round(ebitda_margin * 100, 1),
        "net_income_m":      round(net_income, 1),
        "eps":               round(eps, 2),
        "guidance_low_m":    round(revenue * 1.03, 1),
        "guidance_high_m":   round(revenue * 1.08, 1),
    }

def generate_report_narrative(f: dict) -> str:
    prompt = f"""Write a realistic Q3 earnings report excerpt for {f['company']},
a {f['sector']} firm. Use EXACTLY these figures in the narrative:

- Revenue:     ${f['revenue_m']}M
- EBITDA:      ${f['ebitda_m']}M ({f['ebitda_margin_pct']}% margin)
- Net income:  ${f['net_income_m']}M
- EPS:         ${f['eps']}
- FY guidance: ${f['guidance_low_m']}M - ${f['guidance_high_m']}M

Include:
1. An MD&A paragraph
2. A segment revenue sentence with numbers embedded in prose
3. A CEO quote referencing at least one metric
4. A forward guidance paragraph

Write in formal 10-Q SEC filing style. 400-500 words. No bullet points."""

    response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": prompt
    }]
)
    return response.content[0].text

def generate_report(company: str, sector: str, base_revenue_m: float) -> dict:
    print(f"  Generating financials for {company}...")
    financials = generate_financials(company, sector, base_revenue_m)

    print(f"  Calling Claude for narrative...")
    narrative = generate_report_narrative(financials)

    return {
        "ground_truth": financials,
        "document":     narrative
    }

def main():
    companies = [
        ("Meridian Capital Group",  "Investment Banking",  4200),
        ("Archway Financial",       "Asset Management",    1800),
        ("Crestline Securities",    "Brokerage",           950),
        ("Vantage Advisory Group",  "Wealth Management",   1200),
        ("Halcyon Credit Partners", "Credit & Lending",    2600),
    ]

    os.makedirs("data/reports", exist_ok=True)

    reports = []
    for company, sector, revenue in companies:
        report = generate_report(company, sector, revenue)
        print(json.dumps(report, indent=2))
        reports.append(report)
        filename = company.lower().replace(" ", "_") + ".json"
        filepath = os.path.join("data", "reports", filename)
        with open(filepath, "w") as f:
            json.dump(report, f, indent=2)
        print(f"  Saved → {filepath}")

    with open(os.path.join("data", "reports", "_all_reports.json"), "w") as f:
        json.dump(reports, f, indent=2)
    print(f"\nDone — {len(reports)} reports saved.")

if __name__ == "__main__":
    main()