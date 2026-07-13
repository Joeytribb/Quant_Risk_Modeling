# Quantitative Risk Modeling & Thermodynamic Tail-Risk Hedging

## Abstract
While academic literature heavily indexes on aggressive alpha generation in frictionless environments, institutional capacity requires rigorous, stochastic risk modeling. This repository demonstrates advanced Monte Carlo simulation pipelines designed to model tail-risk insurance protocols (Gamma Scalping). By simulating highly leveraged directional execution against continuous structural noise, this research mathematically proves that portfolio survival relies on managing systemic thermodynamic crashes.

## Methodologies & Empirical Simulation

### 1. Options-Hedged Scalping Simulator (`2_options_hedged_scalper.py`)
A stochastic Monte Carlo framework designed to stress-test leveraged directional exposure against sudden regime shifts (flash crashes).
*   **The Thermodynamic Problem**: A high win-rate strategy executed with leverage will eventually encounter a 6-sigma tail event, resulting in catastrophic liquidation (a total loss of portfolio equity).
*   **The Insurance Protocol (Gamma Hedging)**: The simulator mathematically injects a continuous premium decay (e.g., 0.1% of equity per trade) representing the systematic purchase of Out-Of-The-Money (OTM) Put Options. 
*   **Empirical Outcome**: When a stochastic flash crash triggers liquidation conditions within the simulation, the OTM Put option yields an asymmetric convex return, recovering the portfolio and permitting compounding to resume. This simulation empirically justifies the necessity of Gamma Hedging in volatile high-frequency portfolios.

### 2. Cross-Asset Stochastic Validation (`3_cross_asset_validation.py`)
A machine learning classification pipeline utilizing strictly regularized gradient boosting to validate directional signals across uncorrelated assets.
*   **Structural Overfitting Prevention**: Employs a heavily constrained XGBoost classifier (`max_depth=3`, `learning_rate=0.05`) to prevent curve-fitting, a systemic bias in financial deep learning.
*   **Friction-Adjusted Monte Carlo**: Rather than relying on simple directional accuracy (win-rate), the script executes a massive Monte Carlo simulation (10,000 parallel paths) incorporating realistic centralized exchange taker fees. It computes the exact stochastic probability of compounding a portfolio across varying volatility bands before encountering ruin.

## Execution Environment
Execute the simulators to generate the stochastic equity curves and survival probabilities:
```bash
# Simulates the Gamma Hedged portfolio against flash crashes
python 2_options_hedged_scalper.py

# Validates cross-asset signaling through constrained XGBoost
python 3_cross_asset_validation.py
```
