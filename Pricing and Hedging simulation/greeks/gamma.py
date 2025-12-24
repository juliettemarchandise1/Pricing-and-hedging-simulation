def gamma_bsm(S0,K,T,r,sigma):
    return norm.pdf(d1(S0,K,T,r,sigma)) / (S0*sigma*np.sqrt(T))

def gamma(
    S0,K,T,r,sigma,
    option_type='call', 
    option_style='european', 
    discret_div=0,
    epsilon=1e-3,
    T1=None):

    T = max(T, 1e-10)  # Prevent division by zero

    if option_style == 'european' and discret_div == 0:
        return gamma_bsm(S0,K,T,r,sigma)
    
    elif option_style == 'american' and discret_div == 0:    
        V_plus=price_binomial_US(
            S0+epsilon,K,T,r,sigma,
            steps=100,
            option_type=option_type)
        
        V_minus=price_binomial_US(
            S0-epsilon,K,T,r,sigma,
            steps=100,
            option_type=option_type)
        
        V_0=price_binomial_US(
            S0,K,T,r,sigma,
            steps=100,
            option_type=option_type)

        delta_plus = (V_plus - V_0) / (2 * epsilon)
        delta_minus = (V_0 - V_minus) / (2 * epsilon)

        g = (delta_plus - delta_minus) / (2 * epsilon)
        return g
    
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
        
        V_0 = price_binomial_with_dividend(
            S0, K, T, r, sigma, 100, discret_div, T1,
            option_type,
            option_style
        )

        delta_plus = (V_plus - V_0) / (2 * epsilon)
        delta_minus = (V_0 - V_minus) / (2 * epsilon)

        g = (delta_plus - delta_minus) / (2 * epsilon)
        return g