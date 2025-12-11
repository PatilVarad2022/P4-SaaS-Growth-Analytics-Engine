# Output Data Schema

## kpi_snapshot.csv

| Column | Type | Description | Range | Nullable |
|--------|------|-------------|-------|----------|
| snapshot_date | date | Date of snapshot | YYYY-MM-DD | No |
| current_mrr | float | Current MRR in USD | > 0 | No |
| current_arr | float | Current ARR in USD | > 0 | No |
| active_customers | int | Active customer count | ≥ 0 | No |
| avg_mrr_per_customer | float | Average MRR per customer | > 0 | No |
| mrr_growth_rate_monthly | float | Monthly growth % | Any | No |
| projected_arr_12m | float | 12-month projected ARR | > 0 | No |
| arr_growth_yoy_projected | float | YoY growth % | Any | No |
| avg_revenue_per_customer | float | Avg total revenue | ≥ 0 | No |
| estimated_ltv | float | Lifetime value estimate | > 0 | No |
| estimated_cac | float | CAC estimate | > 0 | No |
| ltv_cac_ratio | float | LTV:CAC ratio | > 0 | No |
| high_risk_customers | int | High churn risk count | ≥ 0 | No |
| churn_risk_pct | float | Churn risk percentage | 0-100 | No |
| total_customers_analyzed | int | Total customers | > 0 | No |

**Rows**: Always 1  
**Example**: See `outputs_verified/2025-12-12/kpi_snapshot.csv`

---

## base_forecast.csv

| Column | Type | Description | Range | Nullable |
|--------|------|-------------|-------|----------|
| month | date | Forecast month | YYYY-MM-DD | No |
| mrr | float | Projected MRR | > 0 | No |
| arr | float | Projected ARR | > 0 | No |
| active_customers | int | Projected customers | ≥ 0 | No |
| new_customers | int | New acquisitions | ≥ 0 | No |
| churned_customers | int | Churned count | ≥ 0 | No |
| net_new_customers | int | Net change | Any | No |
| scenario | string | Always "base" | base | No |

**Rows**: 12 (one per month)  
**Example**: See `outputs_verified/2025-12-12/base_forecast.csv`

---

## scenario_summary.csv

Same schema as `base_forecast.csv`, but:

| Column | Type | Description | Values |
|--------|------|-------------|--------|
| scenario | string | Scenario name | base, optimistic, pessimistic |

**Rows**: 36 (12 months × 3 scenarios)  
**Example**: See `outputs_verified/2025-12-12/scenario_summary.csv`

---

## customer_metrics.csv

| Column | Type | Description | Range | Nullable |
|--------|------|-------------|-------|----------|
| customer_id | string | Customer identifier | - | No |
| region | string | Geographic region | APAC, EMEA, LATAM | Yes |
| acquisition_channel | string | How acquired | organic_search, paid_ads, etc | Yes |
| total_revenue | float | Total revenue USD | ≥ 0 | No |
| activity_score | float | Weighted activity | Any | No |
| churn_risk | string | Risk level | low, medium, high | No |

**Rows**: Number of customers in sample data  
**Example**: See `outputs/customer_metrics.csv`

---

## historical_mrr.csv

| Column | Type | Description | Range | Nullable |
|--------|------|-------------|-------|----------|
| month | string | Month period | YYYY-MM | No |
| mrr | float | Historical MRR | > 0 | No |
| arr | float | Historical ARR | > 0 | No |
| active_customers | int | Active count | ≥ 0 | No |

**Rows**: Number of historical months in data  
**Example**: See `outputs/historical_mrr.csv`

---

## Data Quality Rules

1. **No Negative Revenue**: All MRR/ARR values must be > 0
2. **No Negative Customers**: Customer counts must be ≥ 0
3. **Valid Dates**: All dates in YYYY-MM-DD format
4. **Valid Scenarios**: Only base/optimistic/pessimistic
5. **Valid Risk Levels**: Only low/medium/high

---

**Last Updated**: 2025-12-12  
**Version**: 1.0.0
