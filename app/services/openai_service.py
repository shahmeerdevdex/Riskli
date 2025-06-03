import json
import logging
import uuid
from openai import OpenAI
from app.schemas.risk import RiskAnalysisRequest
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

logger = logging.getLogger("riskli")


async def generate_risk_analysis(data) -> dict:
    request_id = str(uuid.uuid4())
    is_paid = data.get('package', 'free') == 'paid'

    # Extract all fields except 'package' as questions and answers
    questions_answers = {k: v for k, v in data.items() if k != 'package'}

    # Build answers section dynamically from the extracted questions and answers
    answers_section = "\n".join([f"{question}: {answer}" for question, answer in questions_answers.items()])

    if is_paid:
        prompt = f"""
You are a business risk analyst. For each identified risk, assess its impact and likelihood on a scale of 1-5, where 1 is lowest and 5 is highest.
Calculate the risk score by multiplying impact * likelihood.

Risk Score Categories based on individual risk scores and final average:
- Very Low: 1 to <2
- Low: 2 to <6
- Moderate: 6 to <12
- High: 12 to <16
- Very High: 16 to 25

Return your response strictly in the following JSON format:

{{
  "risk_level": "string (based on average risk score)",
  "risk_score_color": "green | yellow | amber | red | purple",
  "average_risk_score": number,
  "top_risks": [
    {{
      "title": "string",
      "description": "string (detailed explanation of how this risk affects the business)",
      "business_impact": "string (comprehensive analysis of potential business consequences)",
      "impact": number(1-5),
      "likelihood": number(1-5),
      "risk_score": number,
      "risk_category": "string",
      "mitigation": "string"
    }},
    ...
  ]
}}

Answers:
{answers_section}

Return json with:
- Calculate average_risk_score as the mean of all individual risk scores
- Set risk_level based on the average_risk_score using the categories above
- Risk Score Gauge Color (use: green for Very Low, yellow for Low, amber for Moderate, red for High, purple for Very High)
- Top 10 Risks Identified, each with:
  * Title and detailed description explaining the risk
  * Business impact analysis explaining consequences to the business
  * Impact score (1-5) with justification
  * Likelihood score (1-5) with justification
  * Risk score (impact * likelihood)
  * Risk category based on individual risk score
  * Detailed mitigation strategy with specific steps
  Sort risks from highest to lowest risk score
"""
    else:
        prompt = f"""
You are a business risk analyst. Return your response strictly in the following JSON format:

{{
  "risk_level": "string",
  "risk_score_color": "green | yellow | amber | red | purple",
  "top_risks": [
    {{
      "title": "string",
      "description": "string"
    }},
    ...
  ]
}}

Answers:
{answers_section}

Return json with:
- Overall Risk Level (VERY LOW, LOW, MODERATE, HIGH, VERY HIGH)
- Risk Score Gauge Color (green, yellow, amber, red, purple)
- Top 10 Risks Identified (each with a short explanation) and sort them from Higher to Low
"""

    logger.info(f"[{request_id}] Risk Analysis Request started.")

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1000,
        )

        raw_content = response.choices[0].message.content
        try:
            result = json.loads(raw_content)
            logger.info(f"[{request_id}] Risk Analysis Success.")
            return {"request_id": request_id, "analysis": result}
        except json.JSONDecodeError:
            logger.error(f"[{request_id}] Invalid JSON in OpenAI response.")
            return {
                "request_id": request_id,
                "error": "Invalid JSON received from OpenAI",
                "raw_response": raw_content
            }

    except Exception as e:
        logger.exception(f"[{request_id}] OpenAI request failed: {str(e)}")
        return {
            "request_id": request_id,
            "error": "OpenAI request failed",
            "details": str(e)
        }
