# Riskli - Risk Analysis API Documentation

## Overview

Riskli is a Risk Analysis API built with FastAPI that leverages OpenAI's GPT-4 model to analyze business risks based on provided data. The API takes various business parameters as input and returns a comprehensive risk analysis including risk level, color-coded risk score, and detailed top risks.

## Base URL

```
/api/v1
```

## Authentication

The API currently does not implement authentication. If you plan to expose this API publicly, you should consider adding authentication mechanisms.

## Endpoints

### Risk Analysis

```
POST /risk/risk-analysis
```

This endpoint analyzes business risks based on the provided data.

#### Request

- **Content-Type**: `application/json`
- **Body**: JSON object with key-value pairs where each key is a question or field and each value is the corresponding answer or data.

**Example Request:**

```json
{
  "business_type": "Software as a Service",
  "annual_revenue": "$2.5 million",
  "employee_count": "45",
  "market_region": "North America, Europe",
  "regulatory_requirements": "GDPR, CCPA"
}
```

#### Response

- **Content-Type**: `application/json`
- **Status Code**: 200 OK

**Example Response:**

```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "analysis": {
    "risk_level": "MODERATE",
    "risk_score_color": "yellow",
    "top_risks": [
      {
        "title": "Data Privacy Compliance",
        "description": "Operating in regions with strict data protection laws (GDPR, CCPA) requires robust compliance measures."
      },
      {
        "title": "Market Competition",
        "description": "SaaS market is highly competitive with low barriers to entry."
      },
      {
        "title": "Cybersecurity Threats",
        "description": "SaaS businesses are frequent targets for data breaches and cyber attacks."
      }
      // Additional risks would be listed here
    ]
  }
}
```

#### Error Response

In case of errors, the API returns:

```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "error": "Error message",
  "details": "Detailed error information"
}
```

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `request_id` | string | Unique identifier for the request |
| `analysis.risk_level` | string | Overall risk assessment (VERY LOW, LOW, MODERATE, HIGH, VERY HIGH) |
| `analysis.risk_score_color` | string | Color code for risk level (green, yellow, amber, red, purple) |
| `analysis.top_risks` | array | List of identified risks sorted from highest to lowest |
| `analysis.top_risks[].title` | string | Short title of the identified risk |
| `analysis.top_risks[].description` | string | Detailed explanation of the risk |

## Rate Limiting

There is no explicit rate limiting implemented in the API. However, be aware that the underlying OpenAI API has its own rate limits.

## Technical Implementation

The API is built using:
- FastAPI framework
- OpenAI's GPT-4 model for risk analysis generation
- Pydantic for request/response validation

## Environment Variables

The API requires the following environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key

## Future Enhancements

Potential improvements for the API:

1. Add authentication (OAuth2, API keys)
2. Implement rate limiting
3. Add caching for similar requests
4. Expand risk analysis with industry-specific parameters
5. Add historical risk analysis tracking
