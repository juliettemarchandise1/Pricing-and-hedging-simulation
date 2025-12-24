def delta_hedge_MC(
    S0, K, T, r, sigma, 
    steps=50, 
    option_type='call', 
    option_style='european', 
    epsilon=1e-3, 
    div=0, T1=0, 
    N_paths=100
):
    # 1) Parameters of the model
    
    dt = T / steps
    all_portfolios = []
    
    # 2) Simulating N_paths stock price paths
    
    for n in range(N_paths):
        S_path = simulate_MC_path(S0, T, r, sigma, steps, div, T1)
        
        dt = T / steps
        
        Delta_prev = delta(
            S0, K, T, r, sigma,
            option_type,
            option_style,
            epsilon,
            div,
            T1=T1
        )   
    
    # 3) Hedging along the path
        # 3a) Initial parameter
        V0 = price_binomial_with_dividend(S0, K, T, r, sigma, steps, div, T1, option_type, option_style)
        
        cash = V0 - Delta_prev * S0
        
        portfolio = []

        # 3b) Creating the portfolio value at each time step
        for i in range(1, steps+1):
            S_t = S_path[i]
            t_remain = T - i*dt
            
            cash*= np.exp(r * dt) # interest on cash
            
            if div!=0 and T1 is not None:
                if (i-1)*dt < T1 <= i*dt:
                    cash += Delta_prev * div
                
            Delta_t = delta(S_t, K, t_remain, r, sigma,
                            option_type=option_type,
                            option_style=option_style,
                            epsilon=epsilon)

        # 3c) Rebalancing the portfolio
            cash -= (Delta_t - Delta_prev) * S_t

        # 3d) Total portfolio value
            portfolio_value = cash + Delta_t * S_t
            portfolio.append(portfolio_value)
            
            Delta_prev = Delta_t

        # 3e) At maturity, we compute the final PnL
        all_portfolios.append(portfolio[-1])

    return np.array(all_portfolios)