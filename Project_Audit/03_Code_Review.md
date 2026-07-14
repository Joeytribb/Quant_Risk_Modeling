# 03. Code Review

This review evaluates the engineering quality of the codebase. The standard applied is that of a tier-1 quantitative research team (e.g., Jane Street, Oxford-Man Institute).

## General Codebase Issues
- **Monolithic Scripts:** The logic is crammed into massive single functions (e.g., `run_cross_asset_blind_test` is 180 lines long). There is no separation of concerns (Data Loading, Preprocessing, Modeling, Evaluation).
- **Missing Object-Oriented Design (OOP):** The codebase entirely lacks classes, making it impossible to inherit, extend, or unit test individual components.
- **Zero Tests:** There are no unit tests (`pytest`), integration tests, or property-based tests. Financial logic must be rigorously tested.
- **Hardcoded Magic Numbers:** The code is riddled with magic numbers scattered throughout the execution flow (e.g., `3000` max trades, `100000` simulations, `0.025` net profit, `42` random seeds). These should be extracted into configuration files (`.yaml`, `.json`) or at least defined as global constants at the top of the files.
- **Poor Dependency Management:** There is no `requirements.txt`, `Pipfile`, or `pyproject.toml`. Dependencies like `ta` and `xgboost` are assumed to be installed.

## File: `2_options_hedged_scalper.py`
- **Toy Implementation:** The simulation is extremely simplistic. `win_rate = 0.9911` is hardcoded. A single `np.random.rand() >= win_rate` dictates a "flash crash" and instantaneous 90% drawdown.
- **Suboptimal Looping:** Simulating 100,000 paths using Python `while` loops is computationally inefficient. This should be vectorized using `numpy` arrays. A 100k simulation loop written in pure Python is a major red flag for a quant engineer.
- **Hardcoded Formatting:** The string formatting and console output logic is hardcoded deeply inside the simulation loop. 

## File: `3_cross_asset_validation.py`
- **Data Generation Absurdity:** Lines 31-57 generate synthetic OHLCV data using a Gaussian random walk if the CSV is missing. Training an ML model to find signal in a random walk is a fundamental contradiction. 
- **Fatal Data Leakage (Line 115-116):**
  ```python
  scaler = StandardScaler()
  X_scaled = scaler.fit_transform(X)
  split_idx = int(len(X) * 0.8)
  ```
  Scaling the *entire* dataset before the train-test split means the training set has access to the mean and variance of the future test set. This invalidates the entire ML pipeline.
- **Intra-Candle Look-Ahead Bias (Lines 94-100):**
  ```python
  if highs[idx + step] >= tp:
      hit_target = True
      break
  if lows[idx + step] <= sl:
      break
  ```
  If a 4H candle has a high that hits TP and a low that hits SL, the code assumes TP was hit first because the `if` statement for `highs` precedes `lows`. In a 4H window, this creates a massive optimistic bias.
- **Poor Vectorization:** Target generation (Lines 84-106) uses slow Python `for` loops to iterate through array indices. This should be optimized using rolling windows or Numba.
- **Inefficient Memory Use:** Using `add_all_ta_features` generates dozens of redundant features, wasting memory and computation time.
- **Silent Failures:** Using `errors='coerce'` in `pd.to_datetime` and dropping NaNs without logging the volume of lost data can hide severe data quality issues.

## File: `robustness_teardown.ipynb`
- **Synthetic Illusions:** The entire notebook operates on a synthetically generated normal distribution (`oos_returns = np.random.normal(...)`), which is then arbitrarily skewed: `oos_returns[oos_returns > 0] = oos_returns[oos_returns > 0] * 1.5`. Running complex bootstrapping and sensitivity matrices on a fictional, arbitrarily skewed Gaussian distribution provides zero insight into real-world robustness.
- **Visualization Hardcoding:** Heatmaps and plots have hardcoded titles and axes based on the specific synthetic inputs used.

## Engineering Verdict
The engineering quality is unacceptable for production or rigorous research. It reads like a rough draft or a hackathon project. The presence of future data leakage via the scaler is a catastrophic error that disqualifies the resulting metrics.
