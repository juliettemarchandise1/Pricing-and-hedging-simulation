def d1(S0,K,T,r,sigma):
    T = max(T, 1e-10)  # Prevent division by zero
    return ( np.log(S0/K) + (r+(sigma**2)/2)*T ) / (sigma*np.sqrt(T))

def d2(S0,K,T,r,sigma):
    T = max(T, 1e-10)  # Prevent division by zero
    return d1(S0,K,T,r,sigma) - sigma*np.sqrt(T)

def price_bsm(S0,K,T,r,sigma,option_type='call',option_style='european'):
    if option_style == 'american':
        raise ValueError("BSM model is only for European options.")
    
    else :     
        if option_type == "call":
            price=S0*norm.cdf(d1(S0,K,T,r,sigma))-K*np.exp(-r*T)*norm.cdf(d2(S0,K,T,r,sigma))
        elif option_type == "put":
            price=K*np.exp(-r*T)*norm.cdf(-d2(S0,K,T,r,sigma))-S0*norm.cdf(-d1(S0,K,T,r,sigma))
        return price