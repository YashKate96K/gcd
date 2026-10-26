# FraudWatch AI: Real-Time Banking Fraud Detection Dashboard

A high-performance banking fraud monitoring dashboard and telemetry system built with **React (Vite)**, **Tailwind CSS**, **Recharts**, **FastAPI**, **PostgreSQL**, **Scikit-learn (Isolation Forest)**, and **PySpark**.

---

## 🏛️ System Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                        REACT FRONTEND (Vite)                           │
│  - Tailwind CSS (Dark navy sidebar #0a0f1d, executive canvas #f8fafc)  │
│  - Recharts (Transaction Volume & Fraud Trends, Risk Distribution)     │
│  - Dynamic KPI Cards (Total, Suspicious, High-Risk, Under Review)      │
│  - Searchable, Filterable, Sortable Transaction Monitor Table          │
│  - Full Investigation Modal with Audit Notes & Status Updates          │
└─────────────────────────────────▲──────────────────────────────────────┘
                                  │ REST APIs (JSON)
┌─────────────────────────────────▼──────────────────────────────────────┐
│                        FASTAPI BACKEND                                 │
│  - GET   /api/dashboard/stats      (Dynamic aggregations & counts)     │
│  - GET   /api/transactions         (Search, risk filters, pagination)  │
│  - POST  /api/transactions         (Ingestion + on-the-fly ML scoring) │
│  - POST  /api/transactions/analyze (What-if ML risk score simulator)   │
│  - PATCH /api/investigations/{id}  (Disposition status & audit log)    │
└──────────────────▲──────────────────────────────▲──────────────────────┘
                   │                              │
┌──────────────────▼──────────┐        ┌──────────▼──────────────────────┐
│     POSTGRESQL DATABASE     │        │     MACHINE LEARNING & BDA      │
│  - `transactions` table     │        │  - Scikit-learn Isolation Forest│
│  - `investigation_audits`   │        │  - Explainability Diagnostics   │
│  - Automatic SQLite Fallback│        │  - PySpark Batch Processing     │
└─────────────────────────────┘        └─────────────────────────────────┘
```

---

## 📂 Project Structure

```
BDA_poject/
├── frontend/                          # React + Vite application
│   ├── src/
│   │   ├── components/
│   │   │   ├── Sidebar.jsx            # Dark navy navigation & ML status
│   │   │   ├── Header.jsx             # Top bar with live stream & anomaly injector
│   │   │   ├── StatCard.jsx           # Dynamic KPI cards (computed from data)
│   │   │   ├── Charts/
│   │   │   │   ├── VolumeTrendChart.jsx      # Recharts volume & fraud area chart
│   │   │   │   └── RiskDistributionChart.jsx  # Recharts risk distribution donut
│   │   │   ├── TransactionTable.jsx   # Filterable, sortable, searchable audit table
│   │   │   ├── InvestigationModal.jsx # Accessible investigation disposition modal
│   │   │   ├── InvestigationQueueView.jsx # Priority triage queue view
│   │   │   └── AnalyticsView.jsx      # Deep-dive fraud channel analytics
│   │   ├── data/
│   │   │   └── mockTransactions.js    # Realistic synthetic banking transactions
│   │   ├── services/
│   │   │   └── api.js                 # Frontend REST client with auto-fallback
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css                  # Tailwind styles
│   ├── package.json
│   └── tailwind.config.js
│
├── backend/                           # FastAPI Python backend
│   ├── app/
│   │   ├── main.py                    # App entrypoint & CORS middleware
│   │   ├── config.py                  # Pydantic environment configuration
│   │   ├── database.py                # SQLAlchemy engine with PostgreSQL & SQLite fallback
│   │   ├── models.py                  # Database tables (transactions, audits)
│   │   ├── schemas.py                 # Pydantic request/response schemas
│   │   ├── seed.py                    # Database seeder script
│   │   ├── ml/
│   │   │   ├── isolation_forest.py    # Isolation Forest anomaly scoring model
│   │   │   └── explainability.py      # Feature attribution & flag reasoning
│   │   └── routers/
│   │       ├── dashboard.py           # Dashboard stats & Recharts aggregations
│   │       ├── transactions.py        # Ingestion, search, and ML analysis
│   │       └── investigations.py      # Investigation queue & status updates
│   ├── requirements.txt
│   ├── .env.example
│   └── .env
│
├── big_data_pipeline/                 # PySpark batch analytics module
│   └── spark_fraud_batch.py           # PySpark batch processor for aggregations
│
└── README.md
```

---

## 🚀 Getting Started

### 1. Prerequisites
- **Node.js**: v18+ (tested with v22)
- **Python**: 3.10+
- **PostgreSQL 17** (optional; the application includes an automatic local SQLite fallback if PostgreSQL is not running)

---

### 2. Frontend Setup & Run

Open a terminal and navigate to `frontend`:
```powershell
cd frontend
npm install
npm run dev
```
The React dashboard will be running at:
👉 **`http://localhost:5173/`**

---

### 3. Backend Setup & Run

Open a second terminal and navigate to `backend`:
```powershell
cd backend

# 1. Activate the Python virtual environment
.\venv\Scripts\Activate.ps1

# 2. (Optional) Configure PostgreSQL in .env
# Edit .env with your PostgreSQL credentials:
# POSTGRES_USER=postgres
# POSTGRES_PASSWORD=your_password
# POSTGRES_DB=fraud_db

# 3. Seed the database with initial transactions and ML scores
python app/seed.py

# 4. Start the FastAPI server
uvicorn app.main:app --reload --port 8000
```

The FastAPI backend will be running at:
👉 **`http://localhost:8000`**
Interactive Swagger Documentation:
👉 **`http://localhost:8000/docs`**

---

### 4. Running the PySpark Big Data Processing Pipeline

To demonstrate distributed big data batch processing on banking transactions:
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python ..\big_data_pipeline\spark_fraud_batch.py
```
This script:
- Ingests 5,000 synthetic banking records using PySpark DataFrames.
- Applies **PySpark Window functions** to compute rolling cardholder baselines.
- Calculates distributed **Z-scores** to flag macro statistical anomalies.
- Generates a **Channel Risk Aggregation Matrix** exported to CSV.

---

## 🧠 Machine Learning Engine: XGBoost 5-Fold Ensemble + Isolation Forest

The backend features a dual-engine architecture:

### 1. Primary Model: XGBoost 5-Fold CV Ensemble (`fraud_model_v2.joblib`)
- **Trained on**: Kaggle Credit Card Fraud Detection dataset (`creditcard.csv`).
- **Architecture**: 5-Fold Stratified Cross-Validation ensemble with probability voting (`predict_proba` average across all 5 models).
- **Features Used**: `['V1'...'V28', 'Amount', 'hour_sin', 'hour_cos', 'log_amount']`.
- **Decision Threshold**: Calibrated out-of-fold at **`0.1706`** (optimizing high recall while maintaining precision >= 0.85).
- **Scoring Output**: Maps ensemble probabilities into a normalized **0–100 Risk Score**:
  - Probability $\ge 0.1706 \rightarrow$ Score 75–99 (**High Risk / Flagged Anomaly**)
  - Probability $< 0.1706 \rightarrow$ Score 3–69 (**Low to Medium Risk**)

### 2. Explainability & Diagnostics Engine
- Located in `backend/app/ml/explainability.py`.
- Generates plain-English diagnostic explanations for investigators detailing why a transaction exceeded the risk threshold (e.g. extreme deviation against historical customer baseline, high-risk merchant category, or nocturnal cross-border execution).

### 3. Fallback: Isolation Forest
- If the `.joblib` model file is not present, the system seamlessly falls back to an unsupervised **Scikit-learn Isolation Forest** (`n_estimators=100, contamination=0.06`).

---

## 🛡️ Core Features Walkthrough

1. **Executive Dashboard**:
   - Dynamic KPI cards (*Total Transactions, Suspicious, High-Risk Outliers, Under Investigation, Flagged Exposure*).
   - Volume trends and risk category distribution charts.
2. **Transaction Monitor**:
   - Live audit table with search by ID, cardholder, merchant, account, or location.
   - Filter by risk level (High, Medium, Low) and investigation status.
3. **Investigation Queue**:
   - Triage queue of suspicious transactions.
   - One-click disposition updates (*Under Review, Confirmed Fraud, Legitimate*).
   - Investigator audit notes saved to the database.
4. **Live Stream & Simulation Controls**:
   - **Stream Live (ON)** toggle: periodically injects live simulated transactions.
   - **+ Inject Anomaly** button: triggers an immediate high-risk anomaly with instant toast alert.
