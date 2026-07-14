# 07. API Documentation

This document outlines the intended documentation for the public functions within the repository. Currently, the codebase lacks docstrings, type hints, and modularity. Below is the standard to which the code must be refactored.

## Module: `2_options_hedged_scalper.py`

### `run_master_hedged_portfolio()`
**Description:**
Simulates the equity curve of a high-leverage directional scalping portfolio protected by a continuous tail-risk hedging protocol (Gamma Scalping). The simulation utilizes a Monte Carlo approach to model sudden drawdown events (flash crashes) against a fixed win rate and insurance premium.

**Parameters:**
None (Currently uses hardcoded internal variables).
*Refactoring Requirement: Extract variables (start_equity, win_rate, leverage, insurance_cost) into function arguments.*

**Returns:**
None (Currently prints to standard out).
*Refactoring Requirement: Return a dictionary or DataFrame containing simulation metrics (survival probability, average trades, equity paths).*

---

## Module: `3_cross_asset_validation.py`

### `run_cross_asset_blind_test()`
**Description:**
Executes an end-to-end machine learning pipeline across multiple assets. It ingests high-frequency data, resamples to a lower timeframe, engineers technical features, trains an XGBoost classifier, and runs a Monte Carlo simulation based on out-of-sample win rates to evaluate risk-adjusted compounding.

**Parameters:**
None (Currently uses hardcoded internal variables and paths).
*Refactoring Requirement: Accept a configuration object defining assets, timeframes, hyperparameter grids, and target thresholds.*

**Returns:**
None (Currently prints a pandas DataFrame to standard out).
*Refactoring Requirement: Return the trained model artifacts, evaluation metrics (LogLoss, ROC-AUC), and the final simulation results DataFrame.*

---

## Notebook: `robustness_teardown.ipynb`

### (Implicit Logic to be Modularized)

#### `calculate_bootstrap_confidence_intervals(returns: np.ndarray, n_bootstraps: int = 10000) -> dict`
**Description:**
*Proposed Function.* Calculates the 95% Confidence Intervals for expected value and win rate using non-parametric resampling with replacement.

#### `generate_sensitivity_matrix(fees: np.ndarray, slippages: np.ndarray, gross_ev: float) -> pd.DataFrame`
**Description:**
*Proposed Function.* Generates a matrix mapping the net expected value of a strategy across varying execution frictions (taker fees and slippage).
