# Data Schema - Raw Sample Files

**Export Date**: 2025-12-12  
**Location**: `data/raw_sample/`  
**Purpose**: Raw data snapshots for Power BI import and external analysis

---

## customers.csv

**Rows**: 10,000  
**Description**: Customer master table with signup and acquisition data

**Header**:
```
customer_id,signup_date,acquisition_source,initial_plan,activated,country
```

**Sample Row**:
```
U000001,2023-01-23,organic_search,Free,True,UK
```

**Columns**:
- `customer_id` (string): Unique customer identifier (PK)
- `signup_date` (date): Date customer signed up (YYYY-MM-DD)
- `acquisition_source` (string): Marketing channel (organic_search, paid_ads, referral, sales_outbound, content_marketing)
- `initial_plan` (string): First plan selected (Free, Basic, Pro)
- `activated` (boolean): Whether customer activated product (True/False)
- `country` (string): Customer country code (US, UK, CA, AU, DE)

---

## transactions.csv

**Rows**: 27,592  
**Description**: Monthly recurring revenue transactions

**Header**:
```
transaction_id,customer_id,transaction_date,amount,currency,invoice_status
```

**Sample Row**:
```
TXN00000001,U000004,2023-02-11,49,USD,paid
```

**Columns**:
- `transaction_id` (string): Unique transaction identifier (PK)
- `customer_id` (string): Customer reference (FK to customers)
- `transaction_date` (date): Transaction date (YYYY-MM-DD)
- `amount` (numeric): Transaction amount in currency
- `currency` (string): Currency code (USD)
- `invoice_status` (string): Payment status (paid)

---

## subscriptions.csv

**Rows**: 1,295  
**Description**: Active and churned subscriptions

**Header**:
```
subscription_id,customer_id,start_date,end_date,status,plan_price
```

**Sample Row**:
```
SUB000004,U000004,2023-02-11,2023-09-23,churned,49
```

**Columns**:
- `subscription_id` (string): Unique subscription identifier (PK)
- `customer_id` (string): Customer reference (FK to customers)
- `start_date` (date): Subscription start date
- `end_date` (date): Subscription end date (NULL if active)
- `status` (string): Subscription status (active, churned)
- `plan_price` (numeric): Monthly plan price (0, 49, 199)

---

## events.csv

**Rows**: 80,263  
**Description**: User activity events for engagement tracking

**Header**:
```
event_id,customer_id,event_name,event_timestamp
```

**Sample Row**:
```
EVT00000001,U000001,page_view,2023-02-15
```

**Columns**:
- `event_id` (string): Unique event identifier (PK)
- `customer_id` (string): Customer reference (FK to customers)
- `event_name` (string): Event type (login, feature_use, page_view, export_data, invite_sent)
- `event_timestamp` (datetime): Event occurrence timestamp

---

## support_tickets.csv

**Rows**: 4,148  
**Description**: Customer support ticket history

**Header**:
```
ticket_id,customer_id,created_at,closed_at,status,satisfaction_score
```

**Sample Row**:
```
TKT000001,U000001,2023-02-21,2023-02-25,closed,4
```

**Columns**:
- `ticket_id` (string): Unique ticket identifier (PK)
- `customer_id` (string): Customer reference (FK to customers)
- `created_at` (datetime): Ticket creation timestamp
- `closed_at` (datetime): Ticket closure timestamp (NULL if open)
- `status` (string): Ticket status (open, closed)
- `satisfaction_score` (integer): Customer satisfaction rating (1-5, NULL if open)

---

## Relationships

```
customers (1) ----< (N) transactions [customer_id]
customers (1) ----< (N) subscriptions [customer_id]
customers (1) ----< (N) events [customer_id]
customers (1) ----< (N) support_tickets [customer_id]
```

---

## Data Quality Notes

- All `customer_id` values are unique in customers.csv
- All foreign keys reference valid customers
- Dates are in YYYY-MM-DD format
- Timestamps include date only (no time component in current export)
- No NULL values in primary keys
- `end_date` and `closed_at` are NULL for active/open records

---

**For Power BI Import**: See `docs/POWERBI_README.md` for join instructions and DAX templates.
