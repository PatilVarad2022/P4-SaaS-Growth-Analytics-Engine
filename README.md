# P4 SaaS Growth Analytics Engine

> **Enterprise-grade customer analytics backend** capable of processing 10,000+ user lifecycles, generating BI-ready datasets, and computing advanced growth metrics (RFM, Churn Risk, CLV, MRR).

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Status: Verified](https://img.shields.io/badge/Status-Verified-green.svg)](VERIFICATION.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🚀 capabilities

This engine is built to demonstrate **production-ready analytics engineering** skills. It simulates a realistic B2B SaaS environment and performs rigorous data processing.

### 1. Data Engineering & Simulation
- **Scale**: Simulates 10,000+ customers, 27k+ transactions, 80k+ events.
- **Event Normalization**: Maps raw, messy event logs to canonical business events (`login`, `feature_use`).
- **Data Integrity**: Enforces strict schemas for Power BI/Tableau ingestion (Star Schema ready).

### 2. Advanced Analytics Logic
- **RFM Segmentation**: Implements quintile-based scoring (1-5) for Recency, Frequency, Monetary value. Generates `rfm_code` (e.g., "5-4-3") for precise targeting.
- **Deterministic Churn Risk**: Flags customers as High/Medium/Low risk based on 30d/14d/7d activity windows and support ticket satisfaction scores (< 2).
- **Cohort Analysis**: Builds monthly acquisition cohorts and tracks retention rates (Month 0 to Month 12).

### 3. Business Intelligence (BI) Integration
- **Dimensional Modeling**: Structured output for direct import into Power BI/Tableau.
- **KPI Engine**: Calculates ARPU, MRR, Churn Rate, LTV, and CAC.
- **Documentation**: Comprehensive documentation for standard business definitions (`docs/LOGIC.md`) and schemas (`docs/SCHEMA.md`).

---

## 🛠️ Quick Start

### 1. Setup
```bash
git clone https://github.com/PatilVarad2022/P4-SaaS-Growth-Analytics-Engine.git
cd P4-SaaS-Growth-Analytics-Engine
pip install -r requirements.txt
```

### 2. Run Pipeline

#### Module A: Data & Analytics Engineering
Generates raw data snapshots (Star Schema ready) and computes row-level metrics (RFM, Churn).
```bash
# 1. Generate synthetic raw data (ETL Simulation)
python export_data_snapshots.py

# 2. Compute Metrics & Generate Samples (Transformation)
python generate_sample_outputs.py
```

#### Module B: Growth Strategy & Forecasting
Aggregates data to calculate Funnels, Cohorts, and project future revenue scenarios.
```bash
# 3. Run full growth analysis (Funnel, Cohorts, LTV, Scenarios)
python run_full_analysis.py
```

### 3. Explore Outputs

#### From Module A (BI Ready):
- **Raw Data** (`data/raw_sample/`): `customers.csv`, `transactions.csv`, `events.csv`
- **Analytic Datasets** (`examples/sample_outputs/`): `customer_metrics.csv` (RFM Scores), `kpi_snapshot.csv`

#### From Module B (Strategic):
- **Cohort Retention**: `outputs/cohort_retention.csv` (Layer Cake / Heatmap data)
- **Financials**: `outputs/revenue_summary.csv` (MRR/ARR), `outputs/unit_economics.csv` (LTV:CAC)
- **Scenarios**: `outputs/scenarios_summary.csv` (6 Growth Projections)

### 4. Verify Correctness
```bash
# Run unit tests
pytest tests/
```

---

## 🔍 Evidence & Verification

Recruiters/Reviewers can verify every claim in this project:

| Claim | Verification Step | Source Code / Evidence |
|-------|-------------------|------------------------|
| **1. Realistic Data Scale** | Run `export_data_snapshots.py` | Check `data/raw_sample/customers.csv` (10k rows) & `transactions.csv` (27k rows). |
| **2. RFM Segmentation** | Inspect `customer_metrics.csv` | See columns `r_q`, `f_q`, `m_q`, `rfm_code` (e.g. "5-5-5"). Logic in `src/metrics.py`. |
| **3. Churn Risk Engine** | Inspect `customer_metrics.csv` | See column `churn_risk` (High/Med/Low). Logic in `src/engine.py`. |
| **4. Cohort Analysis** | Run `run_full_analysis.py` | Output: `outputs/cohort_retention.csv` (Accesses simulation memory efficiently). |
| **5. Financial Modeling** | Inspect `revenue_summary.csv` | Columns for MRR, ARR, ARPU. Logic in `src/revenue.py`. |
| **6. BI Readiness** | Read `docs/POWERBI_README.md` | Defines Star Schema relationships (Customer Dimension -> Transaction Fact). |
| **7. Test Coverage** | Run `pytest` | Passes `tests/test_metrics_corrections.py` validating 100% of churn rules. |
| **8. ML-Free Design** | Inspect `requirements.txt` | No `sklearn`/`torch`. Pure Python business logic implementation. |

---

## 📊 Analytics Methodology 

The engine uses **explainable, rule-based logic** suitable for high-stakes business decisions (vs. black-box ML).

| Metric | Logic | Implementation |
|--------|-------|----------------|
| **Churn Risk** | **High**: No login > 30d OR Ticket Satisfaction < 2 <br> **Medium**: No feature use > 14d | `src/engine.py` |
| **RFM Score** | **Recency**: Days since last interaction (Quintile 5=Recent) <br> **Frequency**: Transaction count (Quintile 5=Frequent) | `src/metrics.py` |
| **Retention** | % of cohort active in subsequent months | `src/retention.py` |
| **LTV** | ARPU × Average Lifespan | `src/unit_economics.py` |

*See [docs/LOGIC.md](docs/LOGIC.md) for full definitions.*

---

## 📂 Repository Structure

```
├── data/raw_sample/           # ETL Outputs (Bronze Layer)
│   ├── customers.csv          # 10k+ rows
│   ├── transactions.csv       # 27k+ rows
│   └── events.csv             # 80k+ rows
│
├── examples/sample_outputs/   # Analytic Outputs (Gold Layer)
│   ├── customer_metrics.csv   # RFM & Churn Risk Tables
│   └── kpi_snapshot.csv       # Executive reporting
│
├── src/                       # Source Code
│   ├── engine.py              # Churn risk logic
│   ├── metrics.py             # RFM calculations
│   ├── funnel.py              # Conversion analytics
│   ├── retention.py           # Cohort logic
│   └── revenue.py             # MRR/ARR calc
│
├── tests/                     # Test Suite
│   └── test_metrics_corrections.py
│
├── docs/                      # Enterprise Documentation
│   ├── SCHEMA.md              # Data dictionary
│   ├── LOGIC.md               # Business rules
│   └── POWERBI_README.md      # BI guide
│
├── export_data_snapshots.py   # Data Generation Script
└── generate_sample_outputs.py # Metric Calculation Script
```

---

## 🏆 Project Highlights for Recruiters

This project demonstrates the ability to:
1.  **Architect Data Pipelines**: End-to-end flow from raw event simulation to aggregated BI tables.
2.  **Implement Complex Business Logic**: translating vague business requirements ("identify at-risk users") into precise Python code.
3.  **Ensure Data Quality**: Automated testing (`pytest`) and validation of metric correctness.
4.  **Documentation**: Writing clear, maintainable documentation for stakeholders.

**Tech Stack**: Python, Pandas, Pytest, Data Modeling (Star Schema), KPI Definition.

---

**Author**: Varad Patil  
**Verified On**: 2024-12-12
