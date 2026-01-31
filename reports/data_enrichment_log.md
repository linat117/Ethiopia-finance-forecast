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

---

## Implemented Enrichments

### Enrichment 002: Mobile money and bank account observations (NBE / GSMA)

**Source URL:** https://nbe.gov.et/wp-content/uploads/2025/06/Annual-Report-2023-2024.pdf

**Confidence:** high

**Collected by:** enrichment_script

**Collection date:** 2025-01-31

**Usefulness notes:** Adds mobile money account counts (12.2M in 2020 → 139.5M in 2025) and bank account counts (9.1M → 54M). Critical for account ownership trends, growth rate analysis, and digital payments modeling. Directly addresses Ethiopia’s National Digital Payments Strategy and BRIDGE 2030 targets.

**Records added:** 5 observations (MOBILE_MONEY_ACCTS_MN, BANK_ACCTS_MN, MOBILE_MONEY_ACTIVATION_PCT)

**Status:** Implemented

---

### Enrichment 003: Policy and regulatory events

**Source URL:** https://nbe.gov.et/ndps/

**Confidence:** high

**Collected by:** enrichment_script

**Collection date:** 2025-01-31

**Usefulness notes:** Adds three policy events: (1) National Digital Payments Strategy 2021 launch, (2) Mobile money licensing (M-Pesa, Telebirr) in 2020, (3) BRIDGE 2030 strategy launch in 2026. Enables event–indicator modeling, causal analysis, and scenario forecasting.

**Records added:** 3 events (policy_launch category)

**Status:** Implemented

---

### Enrichment 004: Event–indicator impact links

**Source URL:** N/A (derived from Enrichment 002–003)

**Confidence:** medium

**Collected by:** enrichment_script

**Collection date:** 2025-01-31

**Usefulness notes:** Links mobile money licensing and NDPS launch to MOBILE_MONEY_ACCTS_MN and BANK_ACCTS_MN with positive impact_direction. Supports event-based forecasting and impact attribution.

**Records added:** 3 impact_link records

**Status:** Implemented

---

## Enriched dataset

**Path:** `data/processed/ethiopia_fi_enriched.csv`

**Contents:** Original unified data plus 11 new records (5 observations, 3 events, 3 impact_links) following the schema.
