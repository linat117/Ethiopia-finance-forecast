# Data Enrichment Log

## Enrichment 001: Standardize observation date

**Problem**

- Multiple temporal fields exist (`observation_date`, `period_start`, `period_end`)
- Modeling requires a single time axis

**Decision**

- Use `observation_date` for observation records
- Derive `event_date` for event records using `period_start`

**Action**

- Create unified `event_date` column in processed dataset

**Status**

- Planned
