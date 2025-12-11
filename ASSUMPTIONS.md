# Assumptions & Methodology

## Data Assumptions

### Input Data
- **Currency**: All amounts in USD
- **Timezone**: All dates in UTC
- **Frequency**: Monthly aggregation
- **Date Range**: Sample data covers 4 months (Jan-Apr 2023)

### Customer Data
- **Assumption**: Each customer has one active subscription
- **Assumption**: Customer IDs are unique and persistent
- **Assumption**: Acquisition channel is known at signup

### Revenue Data
- **Assumption**: Invoices represent recurring monthly revenue (MRR)
- **Assumption**: No one-time charges or setup fees included
- **Assumption**: All invoices are in same currency (USD)

## Methodology

### MRR Calculation
```
MRR = SUM(invoice_amount) per month
ARR = MRR × 12
```
**Code**: `src/transform.py`, function `calculate_mrr()`

### Churn Rate
```
Monthly Churn Rate = Churned Customers / Total Active Customers
```
**Default**: 5% (configurable in `configs/default.yaml`)

### Growth Projection
```
Next Month MRR = Current MRR × (1 + growth_rate)
```
**Method**: Simple trend extrapolation using historical average growth rate  
**Code**: `src/engine.py`, function `project_forward()`

### Scenarios

**Base Scenario**:
- Growth rate: Historical average
- Churn rate: 5% (default)

**Optimistic Scenario**:
- Growth rate: Historical average × 1.5 (+50%)
- Churn rate: Default × 0.8 (-20%)

**Pessimistic Scenario**:
- Growth rate: Historical average × 0.5 (-50%)
- Churn rate: Default × 1.5 (+50%)

**Code**: `src/engine.py`, function `run_growth_simulation()`

### LTV Calculation
```
LTV = Average Revenue per Customer / Churn Rate
```
**Example**: $500 avg revenue / 0.05 churn = $10,000 LTV  
**Code**: `src/metrics.py`, function `calculate_kpis()`

### CAC (Customer Acquisition Cost)
**Method**: Fixed estimate (not calculated from actual marketing spend)  
**Default**: $500 (configurable)  
**Limitation**: Real implementation would use actual marketing spend data

### Churn Risk Scoring
```
Activity Score = SUM(event_weight × event_count)
Churn Risk = "high" if activity_score < 0
           = "medium" if 0 ≤ activity_score < 5
           = "low" if activity_score ≥ 5
```
**Event Weights**:
- login: +1
- feature_use: +2
- support_ticket: -5

**Code**: `src/transform.py`, function `calculate_customer_metrics()`

## Limitations

### No Seasonality
- Projections use simple trend extrapolation
- Does not account for seasonal patterns
- Real implementation would use ARIMA/Prophet

### No Discount Rate
- LTV calculation does not include time value of money
- Real implementation would apply discount rate

### Simplified Churn
- Binary churn (active/churned)
- Does not model partial churn (downgrades)

### Fixed CAC
- CAC is estimated, not calculated from actual spend
- Real implementation would integrate with marketing data

### No Cohort Decay
- Retention matrix is simplified
- Does not include full cohort LTV curves

## Reproducibility

### Deterministic Runs
- **Random Seed**: 42 (set in `configs/default.yaml`)
- **Purpose**: Ensures identical outputs for same inputs
- **Verification**: Run `python verify_run.py` to generate checksums

### Data Quality
- **Validation**: Schema checks on load
- **Assertions**: Negative values trigger errors
- **Missing Data**: Handled with fillna(0) for metrics

## Error Metrics

### Not Applicable
This project does not use MAPE/RMSE/WAPE as it is a forward projection tool, not a backtesting/forecasting accuracy tool.

**Future Enhancement**: Add backtesting module to compare projections vs. actuals

---

**Last Updated**: 2025-12-12  
**Version**: 1.0.0
