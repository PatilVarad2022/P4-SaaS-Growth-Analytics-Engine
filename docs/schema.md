# Data Schema Documentation

## Purpose
This document defines the data schema for all input and output files in the P4 SaaS Growth Analytics Engine.

---

## Input Data (data/raw_sample/)

### customers.csv

| Column | Type | Description | Sample Values | Constraints |
|--------|------|-------------|---------------|-------------|
| customer_id | string | Unique customer identifier | 7a2d3737, 219e104d | Primary Key, NOT NULL |
| join_date | date | Date customer signed up | 2023-01-03 | Format: YYYY-MM-DD |
| acquisition_channel | string | How customer was acquired | organic_search, paid_ads, referral, sales_outbound | Nullable |
| region | string | Geographic region | APAC, EMEA, LATAM | Nullable |

**Sample Row**:
```
7a2d3737,2023-01-03,organic_search,APAC
```

---

### subscriptions.csv

| Column | Type | Description | Sample Values | Constraints |
|--------|------|-------------|---------------|-------------|
| subscription_id | string | Unique subscription identifier | SUB-001, SUB-002 | Primary Key, NOT NULL |
| customer_id | string | Foreign key to customers | 7a2d3737 | Foreign Key, NOT NULL |
| plan_tier | string | Subscription plan level | starter, professional, enterprise | NOT NULL |
| mrr | float | Monthly recurring revenue | 49, 99, 299 | > 0 |
| start_date | date | Subscription start date | 2023-01-03 | Format: YYYY-MM-DD |
| status | string | Current subscription status | active, churned | NOT NULL |

**Sample Row**:
```
SUB-001,7a2d3737,professional,99,2023-01-03,active
```

---

### invoices.csv

| Column | Type | Description | Sample Values | Constraints |
|--------|------|-------------|---------------|-------------|
| invoice_id | string | Unique invoice identifier | INV-001, INV-002 | Primary Key, NOT NULL |
| customer_id | string | Foreign key to customers | 7a2d3737 | Foreign Key, NOT NULL |
| subscription_id | string | Foreign key to subscriptions | SUB-001 | Foreign Key, NOT NULL |
| amount | float | Invoice amount in USD | 49.00, 99.00, 299.00 | > 0 |
| invoice_date | date | Date invoice was issued | 2023-01-03 | Format: YYYY-MM-DD |

**Sample Row**:
```
INV-001,7a2d3737,SUB-001,99,2023-01-03
```

---

### events.csv

| Column | Type | Description | Sample Values | Constraints |
|--------|------|-------------|---------------|-------------|
| event_id | string | Unique event identifier | EVT-001, EVT-002 | Primary Key, NOT NULL |
| customer_id | string | Foreign key to customers | 7a2d3737 | Foreign Key, NOT NULL |
| event_type | string | Type of event | login, feature_use, support_ticket | NOT NULL |
| event_date | date | Date event occurred | 2023-01-03 | Format: YYYY-MM-DD |

**Sample Row**:
```
EVT-001,7a2d3737,login,2023-01-03
```

**Event Types**:
- `login`: User logged into the platform
- `feature_use`: User used a product feature
- `support_ticket`: User opened a support ticket (negative signal)

---

## Output Data (outputs/)

### kpi_snapshot.csv

| Column | Type | Description | Units |
|--------|------|-------------|-------|
| snapshot_date | date | Date of snapshot | YYYY-MM-DD |
| current_mrr | float | Current monthly recurring revenue | USD |
| current_arr | float | Current annual recurring revenue | USD |
| active_customers | int | Number of active customers | count |
| avg_mrr_per_customer | float | Average MRR per customer | USD |
| mrr_growth_rate_monthly | float | Month-over-month MRR growth | percentage |
| projected_arr_12m | float | Projected ARR in 12 months | USD |
| arr_growth_yoy_projected | float | Year-over-year ARR growth | percentage |
| avg_revenue_per_customer | float | Average total revenue per customer | USD |
| estimated_ltv | float | Estimated customer lifetime value | USD |
| estimated_cac | float | Estimated customer acquisition cost | USD |
| ltv_cac_ratio | float | LTV to CAC ratio | ratio |
| high_risk_customers | int | Number of high churn risk customers | count |
| churn_risk_pct | float | Percentage of customers at high risk | percentage |
| total_customers_analyzed | int | Total customers in analysis | count |

---

### base_forecast.csv

| Column | Type | Description | Units |
|--------|------|-------------|-------|
| month | date | Forecast month | YYYY-MM-DD |
| mrr | float | Projected MRR | USD |
| arr | float | Projected ARR | USD |
| active_customers | int | Projected active customers | count |
| new_customers | int | New customers acquired | count |
| churned_customers | int | Customers churned | count |
| net_new_customers | int | Net new customers (new - churned) | count |

---

### scenario_summary.csv

Same schema as `base_forecast.csv` plus:

| Column | Type | Description | Values |
|--------|------|-------------|--------|
| scenario | string | Scenario name | base, optimistic, pessimistic |

---

### customer_metrics.csv

| Column | Type | Description | Units |
|--------|------|-------------|-------|
| customer_id | string | Customer identifier | - |
| region | string | Geographic region | - |
| acquisition_channel | string | Acquisition channel | - |
| total_revenue | float | Total revenue from customer | USD |
| activity_score | float | Weighted activity score | score |
| churn_risk | string | Churn risk level | low, medium, high |

---

## Data Relationships

```
customers (1) ──< (N) subscriptions
customers (1) ──< (N) invoices
customers (1) ──< (N) events
subscriptions (1) ──< (N) invoices
```

**Join Paths**:
- **Revenue by Customer**: `invoices.customer_id = customers.customer_id`
- **Revenue by Subscription**: `invoices.subscription_id = subscriptions.subscription_id`
- **Activity by Customer**: `events.customer_id = customers.customer_id`

---

## Data Quality Rules

1. **No Orphan Records**: All foreign keys must reference existing primary keys
2. **Positive Amounts**: All `amount` and `mrr` values must be > 0
3. **Valid Dates**: All dates must be in YYYY-MM-DD format and not in the future
4. **Valid Status**: Subscription status must be 'active' or 'churned'
5. **Valid Event Types**: Event types must be 'login', 'feature_use', or 'support_ticket'

---

## Currency & Timezone

- **Currency**: All amounts in USD
- **Timezone**: All dates in UTC
- **Decimal Precision**: 2 decimal places for currency values

---

## Sample Data Statistics

**Included Sample Data** (data/raw_sample/):
- **Customers**: 20 rows
- **Subscriptions**: 20 rows
- **Invoices**: 30 rows
- **Events**: 40 rows
- **Date Range**: 2023-01-03 to 2023-04-23 (4 months)

---

## Notes for Developers

- All CSV files use UTF-8 encoding
- No header row should be skipped (first row contains column names)
- Missing values in nullable columns are represented as empty strings
- Date parsing uses `pd.to_datetime()` with `errors='coerce'` for robustness
