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

    # Extract all fields except 'package' as questions and answers
    questions_answers = {k: v for k, v in data.items() if k != 'package'}

    # Build answers section dynamically from the extracted questions and answers
    answers_section = "\n".join([f"{question}: {answer}" for question, answer in questions_answers.items()])

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

Return json :
- Overall Risk Level (e.g., VERY LOW, LOW, MODERATE, HIGH, VERY HIGH)
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
