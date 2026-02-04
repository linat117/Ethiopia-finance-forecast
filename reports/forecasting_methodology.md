# Task 4: Forecasting Methodology and Limitations

## Targets

- **Account Ownership Rate (Access):** % of adults (15+) with an account (bank or mobile money).
- **Digital Payment Usage:** % of adults (15+) who made or received digital payments in the past year.
- **Horizon:** 2025, 2026, 2027.

## Approaches

1. **Baseline trend:** Linear regression of indicator on year; prediction intervals from OLS.
2. **Event-augmented trend:** Baseline plus cumulative event impacts (Task 3 events, scaled).
3. **Scenario analysis:** Pessimistic (low trend, low event effectiveness), base, optimistic (higher trend and event effectiveness).

## Assumptions

- Linear trends in time.
- Stable policy environment; no unmodeled shocks.
- Event impacts additive and scaled by scenario.

## Limitations

- Small sample size (~5 Findex points over ~13 years).
- No causal inference; event effects are expert-driven.
- Structural change (e.g. new regulation or crisis) can invalidate extrapolation.

## Uncertainty

- Regression intervals reflect trend uncertainty.
- Scenario ranges (pessimistic–optimistic) reflect uncertainty in adoption and event effectiveness.
- Point precision is limited; intervals are wide.
