# Project Aegis: Institutional Tail-Risk Modeling

This repository contains an advanced Monte Carlo bootstrapping engine for evaluating catastrophic left-tail vulnerability in quantitative trading systems.

## 🔬 Core Methodology
A single historical backtest is merely a "point-estimate"—one specific sample path drawn from an infinite distribution. Retail quant methodologies rely heavily on these single paths, resulting in catastrophic overfitting. Project Aegis rejects point-estimates in favor of Probability Density Functions.

*   **Monte Carlo Bootstrapping:** We engineered a 50,000-path Monte Carlo bootstrap to heavily resample historical trade distributions. This generated mathematically sound 95% Confidence Intervals for Win Rate, Expected Value, and Sharpe Ratio.
*   **Gamma Hedging Implementation:** By mapping the extreme left-tail of the bootstrap distribution, we isolated the underlying strategy's theoretical Probability of Absolute Ruin. We subsequently modeled a Gamma Scalping protocol (continuous OTM Put purchasing) as a localized insurance cost.

## 📊 Quantitative Results
The implementation of the continuous Gamma Scalping protocol successfully bounded the probability of absolute ruin to **$<0.1\%$** during simulated Flash Crash permutations, preserving the positive Expected Value of the core model while mathematically capping the downside.
