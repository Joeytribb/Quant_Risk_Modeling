# 09. Oxford Review

*Perspective: Professor / Admissions Committee at the Oxford-Man Institute of Quantitative Finance.*

## Initial Impression
The abstract sounds ambitious, but upon opening the code, the illusion immediately shatters. The candidate is trying to dress up a 200-line script of basic XGBoost and toy Monte Carlo loops with the terminology of statistical physics ("Thermodynamic Tail-Risk"). This is a massive red flag. We look for intellectual honesty, mathematical rigor, and pristine methodology.

## Critical Weaknesses That Concern Me
1. **Data Leakage:** The candidate applies `StandardScaler` to the entire dataset before conducting an 80/20 chronological split. This is a first-year undergraduate mistake that invalidates the entire machine learning pipeline. 
2. **Look-Ahead Bias:** By checking `highs` before `lows` in a 4-hour window, the candidate assumes perfect execution at the Take Profit target regardless of intra-candle volatility. In quantitative finance, you assume the worst execution, not the best.
3. **Synthetic Delusions:** When data is missing, the code trains an XGBoost model on a Gaussian random walk, and the Jupyter notebook bootstraps a fabricated normal distribution. The candidate is deriving "Confidence Intervals" for a strategy that has never been exposed to reality.
4. **Options Pricing Ignorance:** Modeling options as a fixed 0.1% cost with a guaranteed 100x payout ignores the entire field of stochastic calculus, implied volatility smiles, and market-maker risk pricing.

## Questions I Would Ask in an Interview
- "Can you explain why you scaled your feature matrix before splitting your train and test sets, and how this impacts your out-of-sample metrics?"
- "You used the term 'Thermodynamic Tail-Risk'. Please mathematically define the thermodynamic property of your noise distribution and how it differs from standard Brownian motion."
- "If a 4H candle hits both your 5% take profit and 2% stop loss, how do you resolve the intra-candle path dependency? Your code seems to just pick the take profit unconditionally."
- "If you train a gradient boosting model on a cumulative sum of random normal variables, what exactly is the model learning?"

## What Would Make It Outstanding?
To salvage this, the applicant must:
1. Strip out all pretentious jargon. Call it what it is: A machine learning approach to Gamma Scalping.
2. Implement rigorous Purged K-Fold Cross-Validation (WFV).
3. Utilize tick-level or 1-minute Limit Order Book data to construct accurate intra-candle trajectories.
4. Replace the toy options model with a realistic pricing model (e.g., Black-Scholes using historical implied volatility surfaces).
5. Prove statistical significance against a naive benchmark using appropriate tests (e.g., Diebold-Mariano).
