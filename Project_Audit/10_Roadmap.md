# 10. Refactoring Roadmap

This is a prioritized plan to elevate this repository from a flawed script into a rigorous, institutional-grade research project.

## 🔴 CRITICAL ISSUES (Fix Immediately)
These issues completely invalidate the current findings and must be resolved before any further analysis.

1. **Fix Data Leakage:** 
   - Move `StandardScaler` application to strictly *after* the train-test split. Fit on `X_train`, transform `X_train` and `X_test`.
2. **Fix Intra-Candle Look-Ahead Bias:**
   - Remove the optimistic target generator. If both TP and SL are breached in a 4H candle, it must be labeled a loss (SL hit first) or the logic must drill down into 1-minute data to verify the exact path.
3. **Remove Random Walk ML Training:**
   - Delete the logic that generates synthetic data for the ML pipeline. If real data is missing, the script should raise a `FileNotFoundError`, not train XGBoost on noise.

## 🟠 HIGH PRIORITY (Methodology Debt)
1. **Implement Walk-Forward Validation:**
   - Replace the single 80/20 chronological split with Purged K-Fold Cross-Validation or a Rolling Walk-Forward window to simulate true out-of-sample performance across shifting market regimes.
2. **Realistic Options Pricing Engine:**
   - Remove the hardcoded 0.1% cost / 100x payout assumptions. Implement a Black-Scholes module or ingest historical Implied Volatility (IV) data to dynamically price the hedging cost.
3. **Feature Selection & Ablation:**
   - Stop using `add_all_ta_features`. Select a smaller, stationary subset of features. Perform SHAP value analysis or feature ablation to prove predictive power.

## 🟡 MEDIUM PRIORITY (Engineering Debt)
1. **Object-Oriented Refactoring:**
   - Break `run_cross_asset_blind_test` into classes: `DataLoader`, `FeatureEngineer`, `ModelTrainer`, `Backtester`.
2. **Configuration Management:**
   - Extract all magic numbers (`max_depth`, `leverage`, `tp_target`, seeds) into a `config.yaml` file.
3. **Unit Testing:**
   - Add a `tests/` directory. Write `pytest` cases to verify target generation logic, scaler implementation, and Monte Carlo loops.

## 🟢 LOW PRIORITY (Quick Wins & Documentation Debt)
1. **Remove Buzzwords:**
   - Rewrite the `README.md` to remove terms like "Thermodynamic" and "Systemic noise". Focus on precise, standard quantitative terminology.
2. **Vectorize Simulations:**
   - Rewrite the Monte Carlo `while` loops using `numpy` matrix operations to speed up execution by 100x.
3. **Dependency Management:**
   - Add a `requirements.txt` listing `pandas`, `numpy`, `xgboost`, `scikit-learn`, `ta`, and `matplotlib`.
