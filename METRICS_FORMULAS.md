# Metrics Formulas

## Core SaaS Metrics

### MRR (Monthly Recurring Revenue)
```
MRR = SUM(invoice_amount) for month M
```
**Code Location**: `src/transform.py`, line 47-56, function `calculate_mrr()`  
**Input**: `invoices.csv` (amount, invoice_date)  
**Output**: Monthly aggregated revenue

---

### ARR (Annual Recurring Revenue)
```
ARR = MRR × 12
```
**Code Location**: `src/transform.py`, line 54  
**Input**: MRR from above  
**Output**: Annualized revenue

---

### LTV (Lifetime Value)
```
LTV = Average Revenue per Customer / Monthly Churn Rate
```
**Code Location**: `src/metrics.py`, line 48  
**Input**: 
- `avg_revenue_per_customer` (total revenue / customer count)
- `churn_rate` (from config, default 0.05)

**Example**:
```
avg_revenue = $500
churn_rate = 0.05 (5%)
LTV = $500 / 0.05 = $10,000
```

---

### LTV:CAC Ratio
```
LTV:CAC = LTV / CAC
```
**Code Location**: `src/metrics.py`, line 51  
**Input**:
- LTV (calculated above)
- CAC (from config, default $500)

**Interpretation**:
- < 1: Unsustainable (losing money on each customer)
- 1-3: Acceptable
- > 3: Healthy
- > 5: Excellent

---

### Monthly Growth Rate
```
Growth Rate = (MRR[month] - MRR[month-1]) / MRR[month-1]
Average Growth = MEAN(all monthly growth rates)
```
**Code Location**: `src/engine.py`, line 27-28  
**Input**: Historical MRR data  
**Output**: Percentage growth rate

---

### Churn Risk Score
```
Activity Score = SUM(event_weight × event_count)

where event_weight:
  login = +1
  feature_use = +2
  support_ticket = -5

Churn Risk Classification:
  "high"   if activity_score < 0
  "medium" if 0 ≤ activity_score < 5
  "low"    if activity_score ≥ 5
```
**Code Location**: `src/transform.py`, line 85-93  
**Input**: `events.csv` (event_type, customer_id)  
**Output**: Risk category per customer

---

### Projected MRR (Forward Projection)
```
MRR[t+1] = MRR[t] × (1 + growth_rate)

where growth_rate varies by scenario:
  Base: historical_avg_growth
  Optimistic: historical_avg_growth × 1.5
  Pessimistic: historical_avg_growth × 0.5
```
**Code Location**: `src/engine.py`, line 71-74  
**Input**: Current MRR, growth rate, churn rate  
**Output**: 12-month forward projection

---

### Customer Churn Calculation
```
Churned Customers[t] = Active Customers[t-1] × churn_rate
New Customers[t] = Active Customers[t-1] × growth_rate + Churned Customers[t]
Net New = New Customers - Churned Customers
```
**Code Location**: `src/engine.py`, line 78-81  
**Input**: Customer count, churn rate, growth rate  
**Output**: Customer movement metrics

---

## Not Implemented (Future)

### CAGR (Compound Annual Growth Rate)
**Formula**:
```
CAGR = (Ending Value / Beginning Value)^(1/years) - 1
```
**Status**: Not applicable - this is a forward projection tool, not historical analysis

### Sharpe Ratio
**Status**: Not applicable - this is not a financial returns analysis tool

### MAPE/RMSE/WAPE
**Status**: Not applicable - no backtesting against actuals implemented

---

## Verification

All formulas can be verified by:
1. Running `python run.py`
2. Checking `outputs/kpi_snapshot.csv` for calculated values
3. Manually recomputing using formulas above
4. Comparing with `outputs_verified/2025-12-12/` for expected values

---

**Last Updated**: 2025-12-12  
**Version**: 1.0.0
