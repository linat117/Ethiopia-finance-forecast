# Interim Submission
## Forecasting Financial Inclusion in Ethiopia

**Prepared by:** Hilina Teshome  
**Organization:** Selam Analytics  
**Date:** January 30, 2026  

---

## 1. Business Context and Problem Definition

### 1.1 Selam Analytics and Consortium Goals

Selam Analytics is developing a financial inclusion forecasting system to support evidence-based policy and investment decisions in Ethiopia. The consortium’s goals include:

- **Improving foresight:** Providing actionable forecasts of financial access and usage to guide regulators, financial service providers, and development partners.
- **Aligning with national strategy:** Supporting Ethiopia’s National Digital Payments Strategy (NDPS) and BRIDGE 2030 (2025–2030) by quantifying progress and gaps.
- **Supporting resource allocation:** Helping stakeholders prioritize interventions in rural outreach, digital literacy, and merchant acceptance.

### 1.2 Significance of 2025–2027 Forecasts

Forecasts for 2025–2027 are important because:

- **Phase transition:** Ethiopia moved from NDPS Phase One (2021–2024) to BRIDGE 2030 in early 2025. Forecasts help assess continuity and impact of the new phase.
- **M-Pesa timing:** M-Pesa’s entry (August 2023) and Telebirr growth create a multi-provider market. Forecasts can clarify adoption and usage patterns over 2025–2027.
- **Target setting:** NFIS-II and BRIDGE 2030 define targets; forecasts inform whether current trajectories are sufficient and where interventions are most needed.

### 1.3 Ethiopia’s Digital Financial Transformation

Ethiopia has seen rapid change:

- Mobile money accounts grew from under 1 million (2020) to over 128 million by late 2024.
- Digital transactions exceeded cash in FY2023/24 (9.7 trillion Birr).
- Adult access to formal financial services rose from 35% (2017) to 46% (2023).

However, gaps remain: only about 15% of mobile money accounts and 25% of agents are active, with rural–urban and gender divides. The forecasting system supports decision-making to address these gaps.

### 1.4 The Global Findex Framework

The **Global Findex Database** is the World Bank’s main source for comparable, demand-side financial inclusion data. It:

- Uses nationally representative surveys (age 15+) in over 140 economies.
- Covers ~300 indicators, including **Access** (account ownership) and **Usage** (digital payments, savings, credit).
- Provides breakdowns by gender, income, age, and rural/urban residence.

Our dataset uses Findex-style indicators (account ownership, digital payments) as the core measures for Access and Usage, and supplements them with supply-side data (e.g., NBE) where applicable.

### 1.5 Role of Impact Links

**Impact links** record how policy or market events are expected to affect indicators. Each link connects an event (e.g., Telebirr launch) to one or more indicators (e.g., mobile money adoption) with a direction (positive/negative). This structure supports:

1. **Event-driven forecasting:** Incorporating policy or market shocks into projections.  
2. **Causal exploration:** Testing hypotheses about event–indicator relationships.  
3. **Scenario analysis:** Comparing baseline vs. event-adjusted forecasts.

---

## 2. Data Enrichment Summary

### Enrichment 001: Standardize Temporal Fields

- **Problem:** Multiple date fields (`observation_date`, `period_start`, `period_end`) complicate time series modeling.  
- **Decision:**  
  - Use `observation_date` for observation records.  
  - Derive `event_date` for events from `period_start`.  
- **Reason:** Provides a unified time axis for modeling.  
- **Status:** Documented in `data_enrichment_log.md`.

---

## 3. Exploratory Data Analysis — Key Insights

### 3.1 Record Type Distribution

- Observations dominate (30 records); events are sparse (10 records).
- Impact links connect events to indicators, but coverage is limited.

*Visualization: Figure 1 — Number of records by type (observation, event, impact_link, target).*

### 3.2 Missing Values

- Core analytical fields (`indicator_code`, `value_numeric`) are mostly complete.
- Metadata fields (`region`, `gender`) have gaps, which constrain disaggregated analyses.

*Visualization: Figure 2 — Missing values by column across the dataset.*

### 3.3 Indicator Coverage

- Some indicators dominate; others have very few observations.
- Sparse series may limit forecasting accuracy.

*Visualization: Figure 3 — Count of observations per indicator.*

### 3.4 Confidence Levels

- Observations are mostly high confidence.
- Event records show variability, indicating uncertainty in effect sizes.

*Visualization: Figure 4 — Confidence levels by record type.*

### 3.5 Access: Account Ownership Trajectory and 2021–2024 Slowdown

**Analysis:**  
Account ownership (Findex-style) grew strongly up to 2021 but shows signs of moderation in 2021–2024. Possible drivers:

- Base effects: higher initial levels make further gains harder.
- COVID-19 disruption: 2021–2022 adjustments.
- Shift from access to usage: policy focus moving to activation, not just account opening.

**Insight:** Forecasts should allow for a slower Access growth path after 2021 unless structural changes (e.g., rural digital infrastructure) accelerate.

*Visualization: Figure 5 — Account ownership (%) over time, with trend and 2021–2024 period highlighted.*

### 3.6 Usage: Mobile Money and Digital Payment Patterns

**Analysis:**  
Usage indicators (mobile money transactions, digital payments) show faster growth than Access, especially post-2020:

- Telebirr (May 2021) and M-Pesa (Aug 2023) expansion increased adoption.
- Transaction volumes grew rapidly, but activation (e.g., share of accounts used in the past 90 days) remains low.

**Insight:** Usage growth can outpace Access growth over 2025–2027; forecasting should treat Access and Usage as related but distinct series.

*Visualization: Figure 6 — Mobile money/digital payment indicators over time.*

### 3.7 Event Timeline Overlaid on Indicators

**Analysis:**  
Key events:

- **May 2021:** Telebirr launch — visible uptick in mobile money adoption.
- **Aug 2023:** M-Pesa entry — possible contribution to competition and growth.
- **2021–2024:** NDPS Phase One implementation.
- **2025:** BRIDGE 2030 launch.

*Visualization: Figure 7 — Indicator time series with vertical lines for key events (policy launches, provider entries).*

---

## 4. Preliminary Observations on Event–Indicator Relationships

- **Telebirr launch (May 2021):** Likely drove significant growth in mobile money accounts.  
- **M-Pesa entry (Aug 2023):** Expected to influence adoption; lag and magnitude still uncertain.  
- **Policies (NFIS-II targets, regulatory changes):** Documented, but timing and strength of impact need formalization.  
- **Next step:** Task 3 will formalize these relationships using the event–indicator impact matrix.

---

## 5. Data Limitations

- Sparse Findex time series (about 5 points over 13 years).
- Limited event records; causal link strength may be weak.
- Missing metadata reduces disaggregation by gender or region.
- Variable confidence in event impact estimates.
- Some indicators rely on a single source, limiting validation.

---

## 6. Next Steps

### Task 3: Event Impact Modeling

- Merge events with impact_links.  
- Build association/impact matrix.  
- Explore preliminary effect sizes.

### Task 4: Forecasting Access and Usage (2025–2027)

- Use trend + event-based models for Access (account ownership) and Usage (digital payments).  
- **Uncertainty quantification:** Produce prediction intervals (e.g., 80%, 95%) around point forecasts.  
- **Scenario analysis:** Compare baseline, optimistic, and pessimistic scenarios based on policy and market assumptions.

### Task 5: Interactive Dashboard

- Develop an interactive dashboard for visualization and scenario exploration.

---

## 7. Technical Glossary

| Term | Definition |
|------|------------|
| **Global Findex** | World Bank database of demand-side financial inclusion indicators, including account ownership and digital payments. |
| **Access** | Proportion of adults with an account at a formal financial institution or mobile money provider. |
| **Usage** | Intensity of use (e.g., digital payments, savings, credit) among those with access. |
| **Impact link** | Record linking an event (policy, market) to an indicator with an expected direction of effect. |
