# Business Logic & Definitions

## Reference Date
See `docs/REFERENCE_DATE.md` (Currently 2024-12-31).

## KPI Definitions

| Metric | Formula | Code Reference |
|--------|---------|----------------|
| **ARPU** | Total MRR / Active Customers | `src/metrics.py::compute_arpu` |
| **MRR** | Sum of plan price for all active subscriptions | `src/revenue.py::calculate_revenue_metrics` |
| **Churn Rate** | Churned Customers / Active Customers at Start | `src/retention.py::calculate_churn_rate_monthly` |
| **Retention Rate** | Retained Customers / Cohort Size | `src/retention.py::generate_cohort_retention_matrix` |
| **LTV** | ARPU * Average Customer Lifespan | `src/unit_economics.py` (heuristic) |

## Segmentation Logic

### RFM Analysis
- **Date Reference**: Latest Snapshot Date
- **Lookback Window**: 180 days for Frequency/Monetary
- **Scoring Method**: Quintiles (1-5)
  - **r_q (Recency)**: 5 = Most recent, 1 = Least recent
  - **f_q (Frequency)**: 5 = Most frequent, 1 = Least frequent
  - **m_q (Monetary)**: 5 = Highest spend, 1 = Lowest spend
- **Output Representation**: `rfm_code` (e.g. "5-4-3")
- **Implementation**: `src/metrics.py::compute_rfm`

### Churn Risk Assessment
Deterministic rules used to flag customers:
1. **High Risk**:
   - No `login` event in last 30 days
   - OR Support Ticket Satisfaction < 2 (if present)
2. **Medium Risk**:
   - No `feature_use` event in last 14 days
3. **Low Risk**:
   - Active in last 7 days
- **Implementation**: `src/engine.py::compute_churn_risk`

## Cohort Analysis
- **Cohort ID**: Month of signup (YYYY-MM)
- **Retention Calculation**: Percentage of cohort active (not churned) in subsequent months (Month 0, Month 1, ...).
- **Implementation**: `src/retention.py::generate_cohort_retention_matrix`

## Funnel Stages
Mapping of user state to funnel stage:
1. **Sign-up**: `users.csv` entry exists.
2. **Activated**: `users.activated == True`.
3. **Converted**: `users.converted_to_paid == True`.
4. **Retained**: Paid user active > 30 days.
- **Implementation**: `src/funnel.py::calculate_funnel_metrics`
