# Event Impact Modeling — Methodology

## Approach

We build an **Event × Indicator** signed impact matrix from analyst-defined impact links. Each link connects an event (e.g. Telebirr launch) to an indicator (e.g. ACC_MM_ACCOUNT) with:

- **Direction:** positive / negative (or increase / decrease)
- **Magnitude:** numeric (e.g. percentage points) or categorical (low / medium / high → 0.5, 1.5, 3.0)
- **Lag:** months after the event before the effect starts

Temporal impact is applied with a **lag** (effect begins after `lag_months`) and **linear accumulation** over a fixed duration (e.g. 36 months), with **no decay**.

## Functional Form

- **Signed impact:** `signed_impact = direction_sign × magnitude` (direction_sign = +1 or -1).
- **Matrix:** Rows = events, columns = indicators; values = sum of signed impacts when multiple links exist for the same (event, indicator).
- **Over time:** For each observation date, cumulative effect = sum over events of  
  `min(months_since_effect_start / duration_months, 1) × impact_pp`  
  so effect accumulates linearly from effect_start and is capped at total impact per event.

## Appropriateness Given Data Constraints

- Sparse time series and few events justify a simple, interpretable model.
- We avoid decay or saturation to keep the model auditable and to avoid overfitting.
- Additivity and linear accumulation are stated assumptions, not estimated from data.

## Assumptions

- **Linearity:** Impact accumulates linearly over the chosen duration.
- **Additivity:** Multiple events affecting the same indicator add (no interaction terms).
- **No decay:** Effect does not fade over time within the horizon.
- **Proxy use of comparable countries:** Magnitude and lag (e.g. for Telebirr) are informed by Kenya/Tanzania mobile money evidence.

## Limitations

- **No causal identification:** Associations are expert-defined, not causally identified.
- **Sparse pre-event data:** Limits counterfactual comparison.
- **Subjective magnitude estimation:** Magnitudes are analyst judgments.
- **Aggregation bias:** National-level indicators may mask heterogeneity.

## Confidence

- **High:** Telebirr → ACC_MM_ACCOUNT (well-documented launch; comparable evidence).
- **Medium:** M-Pesa/Safaricom entry effects.
- **Low:** Policy events with unclear timing; single-source indicators.
