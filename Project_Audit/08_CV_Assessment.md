# 08. CV Assessment

This assessment evaluates the repository's value if included on a CV submitted to elite quantitative programs (e.g., Oxford-Man Institute) or tier-1 proprietary trading firms.

## Quantitative Scoring (1-10)

- **Novelty (2/10):** The concepts of Gamma scalping, XGBoost on TA features, and Monte Carlo equity simulation are foundational, not novel. Attempting to rebrand them with terms like "Thermodynamic Tail-Risk" detracts from the project.
- **Difficulty (3/10):** Writing basic `while` loops, calling `xgboost.fit()`, and using a technical analysis library requires minimal engineering or mathematical difficulty. 
- **Engineering Quality (3/10):** Single monolithic scripts, lack of OOP, missing tests, hardcoded magic numbers, and missing environment/dependency management.
- **Research Quality (1/10):** Contains catastrophic data leakage (`StandardScaler` applied before train/test split), intra-candle look-ahead bias, and relies entirely on synthetic random walks to prove its central thesis.
- **Code Quality (3/10):** Unstructured, repetitive, and unoptimized. Missing type hints and docstrings.
- **Reproducibility (2/10):** Relies on missing local CSV files. The synthetic data generation is reproducible due to a seed, but the logic being reproduced is mathematically flawed.
- **Scientific Rigor (1/10):** Confuses bootstrapping synthetic data with robust statistical significance. Ignores market microstructure, realistic options pricing, and path dependency.
- **Documentation (2/10):** The `README.md` is well-formatted but highly misleading, prioritizing buzzwords over accurate architectural explanations.
- **Portfolio Value (2/10):** In its current state, presenting this repository to an expert interviewer would result in immediate, fatal probing regarding the data leakage and look-ahead bias.

## Overall Impact
**Negative.** 
Including this project on a CV for an elite quantitative role or PhD program is highly risky. While it demonstrates enthusiasm, the fundamental errors in the ML pipeline (data leakage) and the reliance on pseudo-scientific jargon indicate a lack of formal rigor. It signals that the applicant lacks a fundamental understanding of how to backtest financial hypotheses without cheating (whether intentionally or accidentally).
