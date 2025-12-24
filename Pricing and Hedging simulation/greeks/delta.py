def delta_bsm(S0,K,T,r,sigma,option_type='call'):
    if option_type == "call":
        delta=norm.cdf(d1(S0,K,T,r,sigma))
    elif option_type == "put":
        delta=norm.cdf(d1(S0,K,T,r,sigma))-1
    return delta

def delta(
    S0,K,T,r,sigma,
    option_type='call', 
    option_style='european',
    epsilon=1e-3, 
    discret_div=0,
    T1=None):

    T = max(T, 1e-10)  # Prevent division by zero

    if option_style == 'european' or option_style == '1' and discret_div == 0:
        return delta_bsm(S0,K,T,r,sigma,option_type)
    
    elif option_style == 'american' or option_style == '2' and discret_div == 0:    
        V_plus=price_binomial_US(
            S0+epsilon,K,T,r,sigma,
            steps=100,
            option_type=option_type)
        
        V_minus=price_binomial_US(
            S0-epsilon,K,T,r,sigma,
            steps=100,
            option_type=option_type)
        
        d = (V_plus - V_minus) / (2*epsilon)
        return d
    
    else: 
        V_plus = price_binomial_with_dividend(
            S0+epsilon, K, T, r, sigma, 100, discret_div, T1,
            option_type,
            option_style
        )

        V_minus = price_binomial_with_dividend(
            S0-epsilon, K, T, r, sigma, 100, discret_div, T1,
            option_type,
            option_style
        )
        
        d = (V_plus - V_minus) / (2*epsilon)
        return d
        