# 🛡️ Guardian

> **Bright Data Sponsorship Track Winner @ Cal Hacks 12.0** — AI-powered fraud detection with real-time transaction scoring, SHAP-based explainability, and autonomous agent actions.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-REST_Framework-092E20?style=flat&logo=django&logoColor=white)
![React](https://img.shields.io/badge/React-Vite-61DAFB?style=flat&logo=react&logoColor=black)
![scikit-learn](https://img.shields.io/badge/scikit--learn-IsolationForest-F7931E?style=flat&logo=scikit-learn&logoColor=white)


DEVPOST/DEMO: https://devpost.com/software/guardian-ai-powered-fraud-prevention-for-your-money
---

## What It Does

Guardian ingests financial transactions in real time, scores them for anomalous behavior using machine learning, and surfaces human-readable explanations for every flagged event. An autonomous agent layer makes and logs decisions with confidence scoring — so analysts always know *why* something was flagged, not just *that* it was.

---

## Tech Stack

| Layer | Technologies |
|---|---|
| Backend | Django, Django REST Framework, PostgreSQL |
| ML | Scikit-learn (IsolationForest), PyOD, NumPy |
| Explainability | SHAP, permutation-based feature importance |
| Frontend | React (Vite), Tailwind CSS, Lucide, Axios |
| Deployment | Render, Gunicorn, WhiteNoise |

---

## Features

- **Real-time scoring** — sub-second anomaly detection on incoming transactions
- **Explainability panel** — top contributing risk features for every flagged transaction (amount, time, frequency, location)
- **Agent actions** — autonomous decision engine with confidence scores and full reasoning logs
- **Risk dashboard** — live metrics, filterable transaction table, status tracking (approved / flagged / blocked)
- **Model persistence** — trained IsolationForest saved and hot-loaded for zero-latency inference

---

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL

### Setup

```bash
git clone https://github.com/aryan-gupta123/Guardian.git
cd Guardian
./setup.sh

cp env.example .env
# Fill in your database credentials
```

### Run Locally

```bash
# Terminal 1 — Backend
source venv/bin/activate
python3 manage.py runserver

# Terminal 2 — Frontend
cd frontend
npm run dev
```

| Service | URL |
|---|---|
| Frontend | http://localhost:3000 |
| API | http://localhost:8000/api/ |
| Admin | http://localhost:8000/admin/ |

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/ingest/` | Ingest new transactions |
| `POST` | `/api/score/` | Score without saving |
| `POST` | `/api/agents/act/` | Trigger agent action |
| `GET` | `/api/transactions/` | List transactions |
| `GET` | `/api/transactions/{id}/explain/` | Get SHAP explanation |
| `GET` | `/api/merchants/` | List merchants |
| `POST` | `/api/merchants/{id}/transactions/` | Transactions by merchant |

---

## Project Structure

```
Guardian/
├── anomaly_detection/     # Django project config
├── backend/               # Core app
│   ├── services/ml/       # IsolationForest + explainability
│   ├── models.py
│   ├── views.py
│   └── serializers.py
├── frontend/              # React (Vite)
│   ├── src/components/
│   └── src/App.jsx
└── requirements.txt
```

---

## Deployment

```bash
python3 manage.py collectstatic
python3 manage.py migrate
gunicorn anomaly_detection.wsgi:application
```

Required environment variables:
```
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@host:port/db
ALLOWED_HOSTS=yourdomain.com
```

---

## Contributors

| | |
|---|---|
| [ronoktanvir](https://github.com/ronoktanvir) | Backend, ML, Integration |
| [MadhavDonthula](https://github.com/MadhavDonthula) | Backend, Integration, Frontend |
| [aryan-gupta123](https://github.com/aryan-gupta123) | Backend, Integration |
| [Bradley Tsou](https://github.com/bradleytsou) | Frontend |

---

MIT License
