# Power BI Integration Guide

**Purpose**: Import raw data and build SaaS analytics dashboard  
**Data Location**: `data/raw_sample/`  
**Last Updated**: 2025-12-12

---

## Quick Start

1. Open Power BI Desktop
2. Get Data → Text/CSV
3. Import all 5 files from `data/raw_sample/`
4. Create relationships (see below)
5. Add DAX measures (see templates)

---

## Data Model - Relationships

### Primary Keys
- `customers.customer_id` (PK)
- `transactions.transaction_id` (PK)
- `subscriptions.subscription_id` (PK)
- `events.event_id` (PK)
- `support_tickets.ticket_id` (PK)

### Relationships (One-to-Many)

```
customers (1) ----< (N) transactions
  JOIN: customers[customer_id] = transactions[customer_id]
  
customers (1) ----< (N) subscriptions
  JOIN: customers[customer_id] = subscriptions[customer_id]
  
customers (1) ----< (N) events
  JOIN: customers[customer_id] = events[customer_id]
  
customers (1) ----< (N) support_tickets
  JOIN: customers[customer_id] = support_tickets[customer_id]
```

**Cardinality**: All relationships are One-to-Many (1:N)  
**Cross-filter Direction**: Single (from customers to fact tables)

---

## Data Type Coercion

### Date Fields (Convert to Date type)
- `customers.signup_date`
- `transactions.transaction_date`
- `subscriptions.start_date`
- `subscriptions.end_date`
- `events.event_timestamp`
- `support_tickets.created_at`
- `support_tickets.closed_at`

### Numeric Fields (Convert to Decimal/Whole Number)
- `transactions.amount` → Decimal
- `subscriptions.plan_price` → Whole Number
- `support_tickets.satisfaction_score` → Whole Number

### Text Fields (Keep as Text)
- All `*_id` fields
- `acquisition_source`, `initial_plan`, `currency`, `status`, `event_name`

---

## Event Name Normalization

**File**: `configs/event_name_map.csv`

Use this mapping to normalize event variants:
- "Login", "login", "logged_in" → "login"
- "feature_used", "used_feature" → "feature_use"
- "pageview", "viewed_page" → "page_view"

**Power Query M Code**:
```m
let
    Source = events,
    MergedMapping = Table.NestedJoin(Source, {"event_name"}, event_name_map, {"variant"}, "Mapping", JoinKind.LeftOuter),
    ExpandedMapping = Table.ExpandTableColumn(MergedMapping, "Mapping", {"canonical"}, {"canonical_event"}),
    NormalizedEvents = Table.AddColumn(ExpandedMapping, "event_name_clean", each if [canonical_event] = null then [event_name] else [canonical_event])
in
    NormalizedEvents
```

---

## DAX Measure Templates

### 1. ARPU (Average Revenue Per User)

```dax
ARPU = 
VAR TotalRevenue = SUM(transactions[amount])
VAR ActiveCustomers = DISTINCTCOUNT(transactions[customer_id])
RETURN
    DIVIDE(TotalRevenue, ActiveCustomers, 0)
```

**Usage**: Card visual, trend chart  
**Filter Context**: Apply date slicer for monthly ARPU

---

### 2. Monthly Churn Rate

```dax
Churn Rate = 
VAR StartCustomers = 
    CALCULATE(
        DISTINCTCOUNT(subscriptions[customer_id]),
        subscriptions[status] = "active",
        DATEADD('Date'[Date], -1, MONTH)
    )
VAR ChurnedCustomers = 
    CALCULATE(
        DISTINCTCOUNT(subscriptions[customer_id]),
        subscriptions[status] = "churned",
        subscriptions[end_date] >= STARTOFMONTH('Date'[Date]),
        subscriptions[end_date] <= ENDOFMONTH('Date'[Date])
    )
RETURN
    DIVIDE(ChurnedCustomers, StartCustomers, 0)
```

**Usage**: Line chart, KPI card  
**Filter Context**: Requires Date table with continuous dates

---

### 3. MRR (Monthly Recurring Revenue)

```dax
MRR = 
CALCULATE(
    SUM(subscriptions[plan_price]),
    subscriptions[status] = "active"
)
```

**Usage**: Card visual, waterfall chart  
**Filter Context**: Current month or selected date range

---

### 4. LTV:CAC Ratio

```dax
LTV:CAC Ratio = 
VAR AvgLTV = 
    AVERAGE(
        ADDCOLUMNS(
            customers,
            "CustomerLTV",
            CALCULATE(SUM(transactions[amount]))
        )
    )
VAR AvgCAC = 300  // Placeholder - replace with actual CAC data
RETURN
    DIVIDE(AvgLTV, AvgCAC, 0)
```

**Usage**: KPI card, gauge  
**Note**: Replace `AvgCAC` with actual marketing spend data if available

---

### 5. Activation Rate

```dax
Activation Rate = 
VAR TotalCustomers = COUNTROWS(customers)
VAR ActivatedCustomers = 
    CALCULATE(
        COUNTROWS(customers),
        customers[activated] = TRUE()
    )
RETURN
    DIVIDE(ActivatedCustomers, TotalCustomers, 0)
```

**Usage**: Funnel chart, KPI card

---

### 6. Conversion Rate (Free → Paid)

```dax
Conversion Rate = 
VAR FreeCustomers = 
    CALCULATE(
        COUNTROWS(customers),
        customers[initial_plan] = "Free"
    )
VAR ConvertedCustomers = 
    CALCULATE(
        DISTINCTCOUNT(transactions[customer_id]),
        RELATEDTABLE(customers),
        customers[initial_plan] = "Free"
    )
RETURN
    DIVIDE(ConvertedCustomers, FreeCustomers, 0)
```

**Usage**: Funnel chart, conversion dashboard

---

## Recommended Visuals

### Dashboard 1: Executive Overview
- **KPI Cards**: MRR, ARR, Active Customers, Churn Rate
- **Line Chart**: MRR Trend (monthly)
- **Funnel Chart**: Signup → Activate → Convert → Retain
- **Donut Chart**: Revenue by Plan (Free/Basic/Pro)

### Dashboard 2: Customer Analytics
- **Table**: Top 10 customers by LTV
- **Scatter Plot**: Recency vs Frequency (RFM)
- **Bar Chart**: Customers by Acquisition Source
- **Heatmap**: Cohort Retention Matrix

### Dashboard 3: Churn Analysis
- **Line Chart**: Monthly Churn Rate
- **Bar Chart**: Churn Reasons (if available)
- **Table**: At-Risk Customers (high churn risk)
- **Waterfall**: MRR Bridge (New/Expansion/Contraction/Churned)

---

## Date Table (Required for Time Intelligence)

Create a Date table for proper time-based calculations:

```dax
Date = 
CALENDAR(
    DATE(2022, 1, 1),
    DATE(2024, 12, 31)
)
```

Add calculated columns:
- Year, Month, Quarter
- Month Name, Year-Month
- Is Current Month, Is Last Month

---

## Troubleshooting

### Issue: Relationships not creating automatically
**Fix**: Manually create relationships in Model view using the join map above

### Issue: Date filters not working
**Fix**: Ensure Date table is marked as Date Table in Model view

### Issue: Incorrect totals in visuals
**Fix**: Check measure context - use CALCULATE() to override filter context

### Issue: Event names not matching in funnel
**Fix**: Apply event normalization using `configs/event_name_map.csv`

---

## Sample Queries

### Get Active Customers by Month
```dax
Active Customers = 
CALCULATE(
    DISTINCTCOUNT(transactions[customer_id]),
    DATESINPERIOD('Date'[Date], MAX('Date'[Date]), -1, MONTH)
)
```

### Get New Customers This Month
```dax
New Customers = 
CALCULATE(
    COUNTROWS(customers),
    customers[signup_date] >= STARTOFMONTH('Date'[Date]),
    customers[signup_date] <= ENDOFMONTH('Date'[Date])
)
```

---

## Next Steps

1. Import all 5 CSV files
2. Create relationships as shown above
3. Add Date table
4. Create measures using templates above
5. Build dashboards using recommended visuals
6. Apply filters and slicers for interactivity

---

**For Questions**: See `docs/LOGIC.md` for metric definitions  
**For Schema**: See `docs/SCHEMA.md` for column details  
**Last Updated**: 2025-12-12
