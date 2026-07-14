# 06. Quantitative Finance Review

This review evaluates the project from the perspective of an institutional quantitative hedge fund.

## 1. Market Mechanics & Assumptions
- **Options Pricing Disconnect:** `2_options_hedged_scalper.py` assumes a constant insurance premium of 0.1% per trade that guarantees a 100x payout precisely when a flash crash occurs. In real markets, market makers dynamically price risk. If you are consistently buying short-dated, deep OTM options in a volatile asset to support 50x leverage, theta decay and IV premiums will bleed your portfolio dry well before a crash occurs.
- **Liquidity and Execution Reality:** At 50x leverage, a 2% adverse price movement liquidates the position. The simulation models a trade as a binary coin flip (`win_rate = 0.9911`) and completely abstracts away the path taken to reach the profit target. In high-frequency scalping, spread crossing, slippage, and queue position in the Limit Order Book (LOB) dictate success. None of this is modeled.

## 2. Structural Bias in Testing
- **Intra-Candle Look-Ahead Bias:** As noted in the ML review, assuming TP is hit before SL within a 4-hour window because `highs` is checked before `lows` is a fatal flaw. High-leverage strategies must be tested on tick-level data (or at least 1-minute data) to accurately simulate path dependency. 
- **Path Dependency Ignored:** The cross-asset validator calculates a static `win_rate` and feeds it into a generic Monte Carlo loop. It ignores autocorrelation in returns (volatility clustering) and changing market regimes. Consecutive losses occur in clusters in the real world, heavily altering drawdown dynamics compared to uniform random sampling.

## 3. Risk Management & Metrics
- **Missing Standard Metrics:** Institutional investors require standard risk-adjusted performance metrics. The codebase completely lacks calculations for:
  - Sharpe Ratio / Sortino Ratio
  - Maximum Drawdown (calmar ratio)
  - Beta to the underlying asset
  - Value at Risk (VaR) / Expected Shortfall (CVaR)
- **Position Sizing:** The sizing strategy is static compounding (`eq *= (1 + net_profit)`). There is no dynamic risk sizing (e.g., Kelly Criterion, volatility-targeted sizing). 

## 4. The Taker Fee Illusion
While `robustness_teardown.ipynb` includes a sensitivity matrix for taker fees and slippage, applying static slippage across all market conditions is naive. Slippage during a "flash crash" (the exact scenario the strategy attempts to model) is often orders of magnitude higher than average, and liquidity can evaporate entirely, preventing stop-loss execution.

## Institutional Verdict
No hedge fund would deploy this model, nor would it pass a preliminary desk review. The strategy relies on a retail understanding of leverage and options pricing. It abstracts away the exact microstructure frictions that destroy high-frequency strategies. The Monte Carlo paths are essentially mathematical fantasies untethered from real-world limit order book dynamics.
