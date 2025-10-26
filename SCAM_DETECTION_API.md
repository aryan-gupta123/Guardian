# Financial Scam Detection API Documentation

## Overview

The Financial Scam Detection API provides comprehensive analysis of companies to identify potential scam indicators. It uses BrightData web scraping to collect data from multiple sources including:

- Company registration databases (SEC, Companies House, etc.)
- Financial filings and statements
- Domain registration and SSL information
- Regulatory enforcement actions
- Online reviews and reputation data
- Business model analysis

## Table of Contents

1. [Setup](#setup)
2. [Authentication](#authentication)
3. [API Endpoints](#api-endpoints)
4. [Request/Response Examples](#requestresponse-examples)
5. [Risk Scoring System](#risk-scoring-system)
6. [BrightData Integration](#brightdata-integration)
7. [Postman Collection](#postman-collection)

---

## Setup

### 1. Environment Configuration

Add the following variables to your `.env` file:

```env
# BrightData API Configuration
BRIGHTDATA_API_KEY=your-brightdata-api-key-here
BRIGHTDATA_ZONE=your-zone-name
BRIGHTDATA_HOST=brd.superproxy.io
BRIGHTDATA_PORT=22225
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Start the Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

---

## Authentication

Currently, the API uses `AllowAny` permission class. For production deployments, you should:

1. Enable Django's authentication system
2. Use token-based authentication (JWT or DRF tokens)
3. Add rate limiting to prevent abuse

---

## API Endpoints

### 1. Detect Scam

Analyzes a company for scam indicators.

**Endpoint:** `POST /api/scam-detection/`

**Request Body:**

```json
{
  "company_name": "Example Corp",
  "domain": "example.com",
  "jurisdiction": "US",
  "company_identifier": "0001234567",
  "business_description": "Investment platform offering guaranteed returns",
  "promised_returns": 25.0,
  "payment_methods": ["cryptocurrency", "wire_transfer"]
}
```

**Required Fields:**
- `company_name` (string): Name of the company to analyze

**Optional Fields:**
- `domain` (string): Company website domain (e.g., "example.com")
- `jurisdiction` (string): Company jurisdiction (default: "US")
- `company_identifier` (string): CIK number or ticker symbol
- `business_description` (string): Description of the business model
- `promised_returns` (float): Promised annual return percentage
- `payment_methods` (array): List of payment methods accepted

**Response:**

```json
{
  "status": "success",
  "message": "Scam detection analysis completed",
  "analysis": {
    "id": 1,
    "company_name": "Example Corp",
    "domain": "example.com",
    "company_identifier": "0001234567",
    "jurisdiction": "US",
    "overall_risk_score": 0.782,
    "risk_level": "high",
    "category_scores": {
      "company_registration": 0.5,
      "financial_data": 0.4,
      "domain_info": 0.7,
      "regulatory_actions": 0.9,
      "online_reputation": 0.6,
      "business_model": 0.8
    },
    "red_flags": [
      {
        "category": "business_model",
        "severity": "critical",
        "message": "Unrealistic return promises: 25.0% annually"
      },
      {
        "category": "business_model",
        "severity": "high",
        "message": "Risky payment methods: cryptocurrency, wire_transfer"
      },
      {
        "category": "regulatory",
        "severity": "critical",
        "message": "2 regulatory action(s) found from SEC"
      }
    ],
    "green_flags": [
      {
        "category": "registration",
        "message": "Company is actively registered"
      }
    ],
    "detailed_findings": {
      "company_registration": {...},
      "financial_data": {...},
      "domain_info": {...},
      "regulatory_actions": {...},
      "online_reputation": {...},
      "business_model": {...}
    },
    "recommendations": [
      "HIGH RISK: Exercise extreme caution",
      "Conduct thorough due diligence before any engagement",
      "Consult with a financial advisor or attorney",
      "Review regulatory enforcement actions in detail",
      "Unrealistic returns are a major red flag - extremely high risk"
    ],
    "analysis_date": "2025-10-26T12:34:56.789Z",
    "updated_at": "2025-10-26T12:34:56.789Z"
  }
}
```

---

### 2. Get Scam Detection

Retrieve a specific scam detection analysis by ID.

**Endpoint:** `GET /api/scam-detection/{detection_id}/`

**Response:**

Same as the analysis object from the detect scam endpoint.

---

### 3. List Scam Detections

List all scam detection analyses with optional filtering.

**Endpoint:** `GET /api/scam-detections/`

**Query Parameters:**
- `risk_level` (optional): Filter by risk level (low, medium, high, critical)
- `company_name` (optional): Search by company name (case-insensitive)
- `limit` (optional): Number of results to return (default: 50)

**Example:**

```
GET /api/scam-detections/?risk_level=high&limit=10
```

**Response:**

```json
{
  "count": 10,
  "results": [
    {
      "id": 1,
      "company_name": "Example Corp",
      "domain": "example.com",
      "overall_risk_score": 0.782,
      "risk_level": "high",
      "analysis_date": "2025-10-26T12:34:56.789Z"
    },
    ...
  ]
}
```

---

### 4. Get High Risk Companies

Get all companies flagged as high or critical risk.

**Endpoint:** `GET /api/scam-detection/high-risk/`

**Response:**

```json
{
  "count": 5,
  "high_risk_companies": [
    {
      "id": 1,
      "company_name": "Example Corp",
      "domain": "example.com",
      "overall_risk_score": 0.782,
      "risk_level": "high",
      "analysis_date": "2025-10-26T12:34:56.789Z"
    },
    ...
  ]
}
```

---

## Request/Response Examples

### Example 1: Analyzing a Legitimate Company

**Request:**

```bash
curl -X POST http://localhost:8000/api/scam-detection/ \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Apple Inc",
    "domain": "apple.com",
    "jurisdiction": "US",
    "company_identifier": "0000320193"
  }'
```

**Expected Response:**

```json
{
  "status": "success",
  "message": "Scam detection analysis completed",
  "analysis": {
    "overall_risk_score": 0.15,
    "risk_level": "low",
    "red_flags": [],
    "green_flags": [
      {
        "category": "registration",
        "message": "Company is actively registered"
      },
      {
        "category": "registration",
        "message": "Established company (47 years old)"
      },
      {
        "category": "financial",
        "message": "Financial filings are current"
      },
      {
        "category": "domain",
        "message": "Established domain (29 years old)"
      },
      {
        "category": "domain",
        "message": "Valid SSL certificate"
      }
    ]
  }
}
```

---

### Example 2: Analyzing a Suspicious Investment Scheme

**Request:**

```bash
curl -X POST http://localhost:8000/api/scam-detection/ \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "QuickRich Investment Group",
    "domain": "quickrich-invest.xyz",
    "jurisdiction": "US",
    "business_description": "Join our network and earn passive income by recruiting others",
    "promised_returns": 35.0,
    "payment_methods": ["cryptocurrency", "gift_cards"]
  }'
```

**Expected Response:**

```json
{
  "status": "success",
  "message": "Scam detection analysis completed",
  "analysis": {
    "overall_risk_score": 0.89,
    "risk_level": "critical",
    "red_flags": [
      {
        "category": "domain",
        "severity": "high",
        "message": "Domain is less than 1 year old"
      },
      {
        "category": "business_model",
        "severity": "critical",
        "message": "Unrealistic return promises: 35.0% annually"
      },
      {
        "category": "business_model",
        "severity": "high",
        "message": "Risky payment methods: cryptocurrency, gift_cards"
      },
      {
        "category": "business_model",
        "severity": "high",
        "message": "MLM/pyramid scheme indicators detected"
      }
    ],
    "recommendations": [
      "AVOID: This company shows critical scam indicators",
      "DO NOT invest or provide personal/financial information",
      "Report to appropriate regulatory authorities (SEC, FTC, etc.)",
      "Unrealistic returns are a major red flag - extremely high risk"
    ]
  }
}
```

---

## Risk Scoring System

### Category Scores (0-1 scale)

Each category is scored individually:

1. **Company Registration (15% weight)**
   - Company status (active/dissolved)
   - Company age
   - Registered address validity
   - Officer/director information

2. **Financial Data (25% weight)**
   - Filing timeliness
   - Auditor changes
   - Filing status
   - Financial statement quality

3. **Domain Information (15% weight)**
   - Domain age
   - Privacy protection usage
   - SSL certificate validity

4. **Regulatory Actions (20% weight)**
   - SEC enforcement actions
   - FTC complaints
   - State warnings
   - Other regulatory issues

5. **Online Reputation (15% weight)**
   - BBB rating and complaints
   - Trustpilot score
   - Review patterns
   - Suspicious activity

6. **Business Model (10% weight)**
   - Promised returns
   - Payment methods
   - MLM/pyramid indicators
   - Business description red flags

### Overall Risk Levels

- **Low (0.0 - 0.3)**: Standard due diligence recommended
- **Medium (0.3 - 0.6)**: Proceed with caution
- **High (0.6 - 0.8)**: Exercise extreme caution
- **Critical (0.8 - 1.0)**: Avoid - high scam probability

---

## BrightData Integration

The API uses BrightData for web scraping to collect data from various sources.

### Data Sources Scraped

1. **WHOIS Data**
   - Domain registration date
   - Registrar information
   - Privacy protection status

2. **SEC EDGAR Database**
   - Company filings (10-K, 10-Q)
   - CIK numbers
   - Enforcement actions

3. **Better Business Bureau (BBB)**
   - Business ratings
   - Complaint counts
   - Accreditation status

4. **Trustpilot**
   - Review scores
   - Review counts
   - Review patterns

5. **SSL Certificate Verification**
   - Certificate validity
   - Certificate issuer
   - HTTPS availability

### BrightData Configuration

The scraper uses BrightData's proxy network to avoid rate limiting and IP blocks:

```python
proxy_url = f"http://{api_key}:@{host}:{port}"
proxies = {
    "http": proxy_url,
    "https": proxy_url,
}
```

### Rate Limiting

To avoid overwhelming sources or exceeding BrightData limits:

- Implement caching for repeated requests
- Add delays between requests
- Use BrightData's Web Scraper API for complex scraping tasks

---

## Postman Collection

### Setting Up Postman

1. **Create Environment Variables**

```json
{
  "base_url": "http://localhost:8000",
  "api_version": "api"
}
```

2. **Import Collection**

Create a new collection called "Financial Scam Detection API" with the following requests:

#### Request 1: Detect Scam

- **Method:** POST
- **URL:** `{{base_url}}/{{api_version}}/scam-detection/`
- **Headers:**
  - Content-Type: application/json
- **Body (raw JSON):**

```json
{
  "company_name": "Test Company Inc",
  "domain": "testcompany.com",
  "jurisdiction": "US",
  "company_identifier": "0001234567",
  "business_description": "Financial services",
  "promised_returns": 15.0,
  "payment_methods": ["credit_card", "bank_transfer"]
}
```

#### Request 2: Get Scam Detection

- **Method:** GET
- **URL:** `{{base_url}}/{{api_version}}/scam-detection/1/`

#### Request 3: List All Scam Detections

- **Method:** GET
- **URL:** `{{base_url}}/{{api_version}}/scam-detections/?limit=50`

#### Request 4: Filter by Risk Level

- **Method:** GET
- **URL:** `{{base_url}}/{{api_version}}/scam-detections/?risk_level=high`

#### Request 5: Search by Company Name

- **Method:** GET
- **URL:** `{{base_url}}/{{api_version}}/scam-detections/?company_name=example`

#### Request 6: Get High Risk Companies

- **Method:** GET
- **URL:** `{{base_url}}/{{api_version}}/scam-detection/high-risk/`

### Pre-request Scripts

Add this pre-request script to automatically set timestamps:

```javascript
pm.environment.set("timestamp", new Date().toISOString());
```

### Tests

Add these test scripts to validate responses:

```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response has correct structure", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('status');
    pm.expect(jsonData).to.have.property('analysis');
});

pm.test("Risk score is between 0 and 1", function () {
    var jsonData = pm.response.json();
    var riskScore = jsonData.analysis.overall_risk_score;
    pm.expect(riskScore).to.be.at.least(0);
    pm.expect(riskScore).to.be.at.most(1);
});
```

---

## Error Handling

The API returns standard HTTP status codes:

- `200 OK`: Successful request
- `400 Bad Request`: Invalid request data
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

**Error Response Format:**

```json
{
  "status": "error",
  "error": "Error message here",
  "message": "Additional context"
}
```

---

## Production Considerations

Before deploying to production:

1. **Security**
   - Enable authentication (JWT or session-based)
   - Add rate limiting
   - Validate and sanitize all inputs
   - Use HTTPS only

2. **Performance**
   - Implement caching for frequently accessed data
   - Use async/background tasks for scraping (Celery)
   - Add database indexes
   - Monitor BrightData usage limits

3. **Data Privacy**
   - Implement data retention policies
   - Add GDPR compliance features
   - Encrypt sensitive data
   - Add audit logging

4. **Monitoring**
   - Set up error tracking (Sentry)
   - Monitor API response times
   - Track BrightData API usage
   - Set up alerts for high-risk detections

---

## Support

For issues or questions:

1. Check the [Django REST Framework documentation](https://www.django-rest-framework.org/)
2. Review [BrightData documentation](https://docs.brightdata.com/)
3. Open an issue on the project repository

---

## License

This API is part of the Guardian financial anomaly detection system.
