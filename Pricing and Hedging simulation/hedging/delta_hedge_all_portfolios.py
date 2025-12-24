def delta_hedge_all_portfolios(
    S0, K, T, r, sigma, 
    steps=50, 
    option_type='call', 
    option_style='european', 
    epsilon=1e-3, 
    div=0, T1=0, 
    N_paths=100):

    # 1) Parameters of the model    
    dt = T / steps
    all_results = []
    
    # 2) Simulating N_paths stock price paths
    for n in range(N_paths):
        S_path = simulate_MC_path(S0, T, r, sigma, steps, div, T1)
        
        # Initial position
        Delta_prev = delta(
            S0, K, T, r, sigma,
            option_type,
            option_style,
            epsilon,
            div,
            T1=T1
        )   

        V0 = price_binomial_with_dividend(S0, K, T, r, sigma, steps, div, T1, option_type, option_style)
        
        cash = V0 - Delta_prev * S0
        portfolio_values = [V0]
        deltas_path = [Delta_prev]
        
        for i in range(1, steps + 1):
            S_t = S_path[i]
            t_remain = T - i * dt
            
            # Accrue interest on cash
            cash *= np.exp(r * dt)
            
            # Handle discrete dividend
            if div != 0 and T1 is not None:
                if (i - 1) * dt < T1 <= i * dt:
                    cash += Delta_prev * div
            
            # Compute new delta at this node
            Delta_t = delta(S_t, K, t_remain, r, sigma,
                           option_type=option_type,
                           option_style=option_style,
                           epsilon=epsilon)
            
            # Rebalance: adjust hedge
            cash -= (Delta_t - Delta_prev) * S_t
            
            # Portfolio value at this node
            portfolio_value = cash + Delta_t * S_t
            portfolio_values.append(portfolio_value)
            deltas_path.append(Delta_t)
            
            Delta_prev = Delta_t
        
        # Final PnL
        final_payoff = max(0, S_path[-1] - K) if option_type == 'call' else max(0, K - S_path[-1])
        final_pnl = portfolio_values[-1] - final_payoff
        
        all_results.append({
            'path': S_path,
            'portfolio_values': portfolio_values,
            'deltas': deltas_path,
            'final_pnl': final_pnl
        })
    
    return all_results