# 01. Project Summary

## Objective
The repository aims to model tail-risk insurance protocols (termed "Gamma Scalping") and validate directional trading signals across multiple crypto assets. It seeks to demonstrate that leveraged high-frequency trading (scalping) requires systematic options hedging (insurance) to survive extreme market events ("flash crashes"). Additionally, it attempts to validate alpha generation using machine learning (XGBoost) on technical analysis features.

## Problem Formulation
1. **Tail-Risk in Leveraged Systems:** A highly leveraged portfolio with a high win rate will eventually experience a 6-sigma event, leading to total liquidation. The project formulates this as a "thermodynamic problem" of systemic noise.
2. **Signal Validation:** Identifying directional edge (alpha) in financial time series while purportedly mitigating structural overfitting.

## Input Data
- **Real Data:** The project expects 5-minute OHLCV CSV files (e.g., `ETH-5m.csv`, `ADA-5m.csv`, `XRP-5m.csv`) located in a `data/` directory.
- **Synthetic Data:** If the CSV files are not found, the script generates a 150,000-sample synthetic random walk using cumulative sums of normally distributed variables to simulate the assets.

## Output
- **Simulation Metrics:** Probabilities of survival (reaching a $10k target from $10), average trades required, and empirical Monte Carlo equity curves.
- **Validation Metrics:** Out-of-sample win rates, million-dollar probabilities from Monte Carlo simulations, 95% Confidence Intervals for expected value (EV), and fee sensitivity matrices.

## ML Models & Algorithms
- **Model:** `XGBClassifier` (Gradient Boosted Trees).
- **Features:** Over 80 Technical Analysis (TA) indicators generated via the `ta` library (moving averages, momentum oscillators, volume indicators, volatility bands).
- **Target Variable:** Binary classification (1 if Take Profit is hit before Stop Loss within a 30-candle forward window, 0 otherwise).
- **Algorithmic Simulators:** Custom-built Monte Carlo engines for discrete stochastic paths and parameter sensitivity matrices.

## Pipeline Breakdown
1. **Data Ingestion/Generation:** Loads real data or generates a Gaussian random walk.
2. **Preprocessing:** Resamples 5m data to 4-Hour timeframe.
3. **Feature Engineering:** Applies `add_all_ta_features` and drops NaN values.
4. **Target Labeling:** Scans the next 30 candles (5 days) to determine if a fixed 5% Take Profit (TP) or 2% Stop Loss (SL) is triggered first.
5. **Scaling:** Applies `StandardScaler` to the feature set.
6. **Training/Testing:** Performs an 80/20 chronological split and trains the XGBoost model.
7. **Inference & Simulation:** Predicts probabilities on the test set (threshold > 0.50) and feeds the resulting empirical win rate into a Monte Carlo compounding simulator with exchange friction.

## Configuration & Hyperparameters
- **Leverage:** 50x (Hedged Scalper), 10x (Cross-Asset Validation).
- **Options Protocol:** 0.1% equity cost per trade, 100x payout multiplier.
- **XGBoost:** `n_estimators=100`, `max_depth=3`, `learning_rate=0.05`, `subsample=0.8`.
- **Trading Targets:** TP = 5.0%, SL = 2.0%.
- **Fees:** 4bps (0.04%) taker fee per leg.

## Training Procedure & Evaluation Methodology
- **Training:** Supervised learning on historical (or synthetic) 4H candles using log-loss as the evaluation metric.
- **Evaluation:** Out-of-sample evaluation based purely on binary accuracy (win rate) for trades passing the 0.50 probability threshold.
- **Robustness Testing:** Bootstrapping 10,000 resamples of a synthetic trade distribution to calculate confidence intervals, and Monte Carlo equity path generations to visualize ruin probabilities.

## Deployment
- The repository consists of standalone Python scripts and a Jupyter Notebook. There is no deployment pipeline, CI/CD, Dockerization, or production execution framework.
