import numpy as np
import time

def run_master_hedged_portfolio():
    start_equity = 10.0
    target_equity = 10000.0
    
    win_rate = 0.9911 # From the 1-year BTC micro-scalping test
    net_profit_per_win = 0.025 # +2.5% account growth per win at 50x leverage
    
    # Insurance Protocol
    insurance_cost_per_trade = 0.001 # 0.1% of equity per trade
    insurance_payout_multiplier = 100.0 # If crash happens, option pays 100x its cost
    
    num_simulations = 100000
    successes = 0
    total_trades_to_10k = 0
    
    print("\n" + "="*70)
    print("MASTER HEDGED PORTFOLIO SIMULATOR (50x Leverage + Insurance)")
    print("="*70)
    
    sample_path = []
    
    for sim in range(num_simulations):
        portfolio_eq = start_equity
        trades = 0
        path = []
        
        while portfolio_eq >= 1.0 and portfolio_eq < target_equity and trades < 3000:
            trades += 1
            
            insurance_premium = portfolio_eq * insurance_cost_per_trade
            scalping_eq = portfolio_eq - insurance_premium
            
            is_flash_crash = np.random.rand() >= win_rate
            
            if not is_flash_crash:
                # Normal Day
                scalping_eq *= (1 + net_profit_per_win)
                portfolio_eq = scalping_eq 
            else:
                # Flash Crash
                insurance_payout = insurance_premium * insurance_payout_multiplier
                portfolio_eq = insurance_payout 
                
            # Log the path for the first successful run that actually encounters a crash
            # to demonstrate the drawdown and recovery.
            if sim == 0 or len(sample_path) == 0:
                path.append((trades, portfolio_eq, is_flash_crash))
                
        if portfolio_eq >= target_equity:
            successes += 1
            total_trades_to_10k += trades
            
            # We want to capture a path that has at least one flash crash to show the user
            if len(sample_path) == 0:
                crashes = sum([1 for x in path if x[2] == True])
                if crashes > 0:
                    sample_path = path
                    
    success_prob = successes / num_simulations
    avg_trades = total_trades_to_10k / successes if successes > 0 else 0
    avg_days = avg_trades / 24 # 1 trade per hour
    
    if len(sample_path) > 0:
        print("Example Compounding Path (Highlighting Flash Crashes):")
        print(f" Start: $10.00")
        
        # We will print the path milestones, explicitly showing crashes
        last_val = 10.0
        for trades, val, is_crash in sample_path:
            if is_crash:
                print(f" [!] FLASH CRASH at Day {trades//24:02d}: Scalper Liquidated. Insurance Pays Out!")
                print(f"     Drawdown: ${last_val:,.2f} ---> ${val:,.2f} (-90%)")
                
            # Print every 5 days or if it's the target
            if trades % 120 == 0 or val >= target_equity:
                if not is_crash:
                    print(f" Day {trades//24:02d}: ${val:,.2f}")
                    
            last_val = val
            
    print("-" * 70)
    print(f"Probability of Survival (Hitting $10k): {success_prob*100:.2f}%")
    if success_prob > 0:
        print(f"Average Trades Required: {avg_trades:.1f}")
        print(f"Average Time Required (at 1 trade/hour): {avg_days:.1f} days")
    print("="*70)

if __name__ == "__main__":
    start = time.time()
    run_master_hedged_portfolio()
    print(f"\nCompleted in {time.time() - start:.2f} seconds.")
