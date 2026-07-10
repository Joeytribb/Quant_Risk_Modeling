import pandas as pd
import numpy as np
from ta import add_all_ta_features
from xgboost import XGBClassifier
from sklearn.preprocessing import StandardScaler
import time
import warnings
warnings.filterwarnings('ignore')

def run_cross_asset_blind_test():
    assets = ['ETH', 'ADA', 'XRP']
    
    print("\n" + "="*70)
    print("THE ULTIMATE BLIND CROSS-ASSET VALIDATION TEST")
    print("="*70)
    print("Architecture: 4-Hour Timeframe | 5.0% Target | 2.0% Stop Loss | 10x Leverage")
    
    tp_target = 0.05
    sl_target = 0.02
    lookforward = 30 # 30 candles on 4H = 5 days
    leverage = 10
    
    results = []
    
    for asset in assets:
        print(f"\n--- Testing Asset: {asset} ---")
        try:
            df = pd.read_csv(f'data/{asset}-5m.csv')
        except FileNotFoundError:
            print(f"Data for {asset} not found. Generating synthetic OHLCV data for {asset}...")
            # Generate synthetic 5m OHLCV data
            n_samples = 150000
            np.random.seed(42 + len(asset))
            dates = pd.date_range(end=pd.Timestamp.now(), periods=n_samples, freq='5min')
            
            # Create a realistic-looking random walk
            close_prices = np.cumsum(np.random.randn(n_samples) * 0.5) + 100
            close_prices = np.maximum(close_prices, 1.0) # Prevent negative prices
            
            # Generate OHLC based on close
            high_prices = close_prices + np.abs(np.random.randn(n_samples) * 0.2)
            low_prices = close_prices - np.abs(np.random.randn(n_samples) * 0.2)
            open_prices = np.roll(close_prices, 1)
            open_prices[0] = close_prices[0]
            
            # Ensure High >= max(Open, Close) and Low <= min(Open, Close)
            high_prices = np.maximum(high_prices, np.maximum(open_prices, close_prices))
            low_prices = np.minimum(low_prices, np.minimum(open_prices, close_prices))
            
            df = pd.DataFrame({
                'Timestamp': dates,
                'Open': open_prices,
                'High': high_prices,
                'Low': low_prices,
                'Close': close_prices,
                'Volume': np.random.randint(100, 10000, n_samples)
            })
            
        if 'Timestamp' not in df.columns and 'timestamp' in df.columns:
            df['Timestamp'] = df['timestamp']
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s', errors='coerce')
        df = df.sort_values('Timestamp').set_index('Timestamp')
        
        # Resample to 4-Hour
        df_4h = df.resample('4h').agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum'
        }).dropna()
        
        # We need enough data to train. Use last 5,000 4H candles if available (~800 days)
        df_4h = df_4h.tail(5000).copy()
        
        # TA Features
        df_4h = add_all_ta_features(df_4h, open="Open", high="High", low="Low", close="Close", volume="Volume", fillna=True)
        df_4h = df_4h.dropna()
        
        closes = df_4h['Close'].values
        highs = df_4h['High'].values
        lows = df_4h['Low'].values
        
        targets = []
        for idx in range(len(df_4h)):
            if idx >= len(df_4h) - lookforward:
                targets.append(0)
                continue
                
            entry = closes[idx]
            tp = entry * (1 + tp_target)
            sl = entry * (1 - sl_target)
            
            hit_target = False
            for step in range(1, lookforward + 1):
                if highs[idx + step] >= tp:
                    hit_target = True
                    break
                if lows[idx + step] <= sl:
                    break
                    
            if hit_target:
                targets.append(1)
            else:
                targets.append(0)
                
        df_4h['Target'] = targets
        
        drop_cols = ['Open', 'High', 'Low', 'Close', 'Target']
        features_cols = [c for c in df_4h.columns if c not in drop_cols]
        
        X = df_4h[features_cols].values
        y = df_4h['Target'].values
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        split_idx = int(len(X) * 0.8)
        X_train, X_test = X_scaled[:split_idx], X_scaled[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        
        # Strict regularization to prevent overfitting during this test
        model = XGBClassifier(
            n_estimators=100,
            max_depth=3,
            learning_rate=0.05,
            subsample=0.8,
            random_state=42,
            n_jobs=-1,
            eval_metric='logloss'
        )
        model.fit(X_train, y_train)
        
        probs = model.predict_proba(X_test)[:, 1]
        
        threshold = 0.50
        valid_indices = np.where(probs > threshold)[0]
        
        wins = 0
        trades = len(valid_indices)
        for idx in valid_indices:
            if y_test[idx] == 1:
                wins += 1
                
        win_rate = wins / trades if trades > 0 else 0
        
        # Monte Carlo 10x Leverage $10k to $1M Simulator
        futures_taker_fee = 0.0004
        round_trip_cost = (futures_taker_fee * leverage) * 2
        
        gross_profit = tp_target * leverage
        net_profit = gross_profit - round_trip_cost
        
        gross_loss = sl_target * leverage
        net_loss = gross_loss + round_trip_cost
        
        num_sims = 10000
        successes = 0
        
        for _ in range(num_sims):
            eq = 10000.0
            tr = 0
            while eq > 1000.0 and eq < 1000000.0 and tr < 500:
                tr += 1
                if np.random.rand() < win_rate:
                    eq *= (1 + net_profit)
                else:
                    eq *= (1 - net_loss)
            if eq >= 1000000.0:
                successes += 1
                
        mc_prob = successes / num_sims if num_sims > 0 else 0
        
        results.append({
            "Asset": asset,
            "Total_Trades_OOS": trades,
            "Win_Rate": f"{win_rate*100:.1f}%",
            "Million_Dollar_Prob": f"{mc_prob*100:.1f}%"
        })
        
        print(f"{asset} | Trades: {trades} | Win Rate: {win_rate*100:.1f}% | Million Dollar Prob: {mc_prob*100:.1f}%")
        
    print("\n" + "="*70)
    print("FINAL BLIND VALIDATION RESULTS")
    print("="*70)
    df_results = pd.DataFrame(results)
    print(df_results.to_string(index=False))
    print("="*70)

if __name__ == "__main__":
    start = time.time()
    run_cross_asset_blind_test()
    print(f"\nCompleted in {time.time() - start:.2f} seconds.")
