# Quantitative Risk Modeling & Tail-Risk Hedging

## Project Overview
While aggressive alpha generation is the focus of most quantitative strategies, institutional survival requires rigorous risk modeling. This repository demonstrates advanced portfolio simulations, specifically modeling tail-risk insurance protocols (Gamma Scalping) against highly leveraged directional algorithms.

Retail strategies optimize for the highest backtest APY. Institutional strategies optimize for the highest probability of survival under flash-crash conditions.

## Architecture

### 1. Options-Hedged Scalping Simulator (`2_options_hedged_scalper.py`)
A Monte Carlo simulator designed to stress-test a 50x leveraged directional scalping strategy.
- **The Problem**: A high win-rate scalper will eventually suffer a catastrophic liquidation (flash crash) that wipes out the entire portfolio equity.
- **The Solution (Insurance Protocol)**: The simulator deducts a continuous premium (e.g., 0.1% of equity per trade) to simulate buying Out-Of-The-Money (OTM) Put Options. 
- **The Outcome**: When a flash crash triggers the liquidation condition in the simulation, the OTM Put option pays out an asymmetric 100x return, recovering the portfolio and allowing compounding to continue. This mathematically proves the necessity of Gamma Hedging in high-leverage portfolios.

### 2. Cross-Asset XGBoost Validation (`3_cross_asset_validation.py`)
A robust machine learning classification pipeline to validate directional signals across multiple assets (ETH, ADA, XRP).
- **Strict Regularization**: Uses a heavily constrained XGBoost classifier (`max_depth=3`, `learning_rate=0.05`) to prevent curve-fitting and overfitting, which is notoriously common in financial ML.
- **Taker-Fee Monte Carlo**: Rather than relying on simple win-rates, the script runs a Monte Carlo simulation (10,000 paths) incorporating realistic futures taker fees to calculate the true "Million Dollar Probability" (the probability of compounding a $10k account to $1M before ruin).

## Execution
Run the simulators to observe the stochastic paths and survival probabilities:
```bash
python 2_options_hedged_scalper.py
python 3_cross_asset_validation.py
```
