# Anomaly Detection System

A Django + React application for real-time transaction anomaly detection using machine learning.

## 🏗️ Architecture

### Backend (Django)
- **Django + Django REST Framework** - Main API service
- **PostgreSQL** - Transaction and merchant data storage
- **Scikit-learn** - IsolationForest for anomaly detection
- **NumPy** - Feature transformation and normalization
- **PyOD** - Alternative anomaly detectors
- **Custom explainability service** - Returns top contributing features

### Frontend (React)
- **React (Vite)** - Fast SPA frontend
- **Tailwind CSS** - Dark + blue theme
- **Lucide React** - Modern icons
- **Axios** - API communication

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL

### Installation

1. **Clone and setup:**
```bash
git clone <your-repo>
cd CalHacks
./setup.sh
```

2. **Configure environment:**
```bash
cp env.example .env
# Edit .env with your database credentials
```

3. **Start development servers:**

**Backend (Terminal 1):**
```bash
source venv/bin/activate
python manage.py runserver
```

**Frontend (Terminal 2):**
```bash
cd frontend
npm run dev
```

4. **Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api/
- Django Admin: http://localhost:8000/admin/

## 📊 Features

### Dashboard
- Real-time transaction monitoring
- Risk score visualization
- System status indicators
- Recent high-risk transactions

### Risk Assessment Table
- Comprehensive transaction listing
- Risk score filtering and search
- Status tracking (approved/flagged/blocked)
- Action buttons for review

### Explainability Panel
- AI-powered transaction explanations
- Top contributing features
- Risk factor identification
- Feature importance analysis

### Agent Actions
- Automated decision tracking
- Confidence scoring
- Action reasoning display
- Status management

## 🔧 API Endpoints

### Core Endpoints
- `POST /api/ingest/` - Ingest new transactions
- `POST /api/score/` - Score transactions without saving
- `POST /api/agents/act/` - Agent action handling
- `GET /api/merchants/` - Merchant management
- `GET /api/transactions/` - Transaction listing

### ML Services
- `GET /api/transactions/{id}/explain/` - Get transaction explanation
- `POST /api/merchants/{id}/transactions/` - Get merchant transactions

## 🤖 Machine Learning

### Anomaly Detection
- **IsolationForest** - Primary anomaly detector
- **Feature Engineering** - Amount, time, frequency, location risk
- **Real-time Scoring** - Sub-second response times
- **Model Persistence** - Trained models saved and loaded

### Explainability
- **Feature Importance** - Permutation-based importance
- **Risk Factors** - Human-readable explanations
- **Contribution Analysis** - Individual feature contributions

## 🎨 UI Components

### Design System
- **Dark Theme** - Professional dark interface
- **Blue Accents** - Primary color scheme
- **Responsive Design** - Mobile-friendly layout
- **Accessibility** - Screen reader support

### Key Components
- **Dashboard** - Overview and metrics
- **RiskTable** - Transaction management
- **ExplainPanel** - AI explanations
- **AgentActions** - Automated decisions

## 🚀 Deployment

### Production Setup
1. **Environment Variables:**
```bash
DEBUG=False
SECRET_KEY=your-production-secret
DATABASE_URL=postgresql://user:pass@host:port/db
ALLOWED_HOSTS=yourdomain.com
```

2. **Static Files:**
```bash
python manage.py collectstatic
```

3. **Database Migration:**
```bash
python manage.py migrate
```

4. **Gunicorn:**
```bash
gunicorn anomaly_detection.wsgi:application
```

## 🔒 Security

- **CORS Configuration** - Proper cross-origin setup
- **Environment Variables** - Secure credential management
- **Input Validation** - API request validation
- **SQL Injection Protection** - Django ORM usage

## 📈 Performance

- **Database Indexing** - Optimized queries
- **Caching Strategy** - Model and data caching
- **Async Processing** - Background ML tasks
- **CDN Ready** - Static asset optimization

## 🧪 Testing

```bash
# Backend tests
python manage.py test

# Frontend tests
cd frontend
npm test
```

## 📝 Development

### Adding New Features
1. **Backend:** Add models, views, serializers
2. **Frontend:** Create components, update routing
3. **ML:** Extend anomaly detection algorithms
4. **API:** Update endpoints and documentation

### Code Structure
```
├── anomaly_detection/     # Django project
├── backend/              # Django app
│   ├── services/ml/      # ML services
│   ├── models.py         # Database models
│   ├── views.py         # API views
│   └── serializers.py    # Data serialization
├── frontend/             # React app
│   ├── src/components/   # React components
│   ├── src/App.jsx       # Main app
│   └── package.json      # Dependencies
└── requirements.txt      # Python dependencies
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

