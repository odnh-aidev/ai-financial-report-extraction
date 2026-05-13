import os
import json
import random
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

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

    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=prompt
    )
    return response.text


