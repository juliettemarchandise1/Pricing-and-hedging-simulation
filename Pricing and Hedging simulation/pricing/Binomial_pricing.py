def price_binomial_euro(
    S0,K,T,r,sigma,steps,
    option_type="call",
    dividend_yield=0):

    # Cas où l'échéance est immédiate
    if T <= 0:
        if option_type == "call":
            return max(0, S0 - K)
        else:
            return max(0, K - S0)    

    #1 - Paramètres du modèle
    
    dt = T/steps
    discount_factor = exp(-r*dt)
    u = exp(sigma*sqrt(dt))
    d = exp(-sigma*sqrt(dt))
    p = (exp((r-dividend_yield)*dt)-d)/(u-d)
    
    #2 - Calcul des prix à l'échéance et des payoffs
    
    ST = np.array([S0 * (u**i) * (d**(steps-i)) for i in range (steps+1)]) # Terminal prices St
    
    if option_type=="call":
        VT = np.maximum(0,ST - K)
    elif option_type=="put":
        VT = np.maximum(0, K-ST)
    else:
        raise ValueError("Veuillez rentrer un type d'option valide 'call/put'")

    #3 - Récursion pour remonter l'arbre
    for i in range (steps-1,-1,-1):
        VT = discount_factor * (p * VT[1:i+2] + (1-p) * VT[0:i+1])
    
    #4 - Prix de l'option au temps 0
    return VT[0]

def price_binomial_US(
    S0,K,T,r,sigma,steps,
    option_type="call"):
    
    # If maturity is immediate
    if T <= 0:
        if option_type == "call":
            return max(0, S0 - K)
        else:
            return max(0, K - S0)
    
    #1 - Parameters of the model
    
    dt = T/steps
    discount_factor = exp(-r*dt)
    u = exp(sigma*sqrt(dt))
    d = exp(-sigma*sqrt(dt))
    p = (exp(r*dt)-d)/(u-d)
    
    #2 - Payoffs at maturity
    ST = np.array([S0 * (u**i) * (d**(steps-i)) for i in range (steps+1)])
    
    if option_type=="call":
        VT = np.maximum(0,ST - K)
    elif option_type=="put":
        VT = np.maximum(0, K-ST)
    else:
        raise ValueError("Please enter a valid option type 'call/put'")

    #3 - Recursion to go back through the tree
    for i in range (steps-1,-1,-1):
        St= S0 * (u**np.arange(i+1)) * (d**(i-np.arange(i+1)))
        Vt = discount_factor * (p * VT[1:i+2] + (1-p) * VT[0:i+1])
        if option_type=="call":
            VT = np.maximum(Vt, St -K)
        else:
            VT = np.maximum(Vt, K-St) 
    
    #4 - Option price at time 0
    return VT[0]

def price_binomial_with_dividend(
    S0, K, T, r, sigma, steps,
    div, T1,
    option_type="call",
    option_style="european"
):
    
    # If maturity is immediate
    if T <= 0:
        if option_type == "call":
            return max(0, S0 - K)
        else:
            return max(0, K - S0)
    
    # 1) Parameters of the model
    dt = T / steps
    u = exp(sigma * sqrt(dt))
    d = exp(-sigma * sqrt(dt))
    p = (exp(r * dt) - d) / (u - d)
    discount = exp(-r * dt)

    # 2) Stock price tree
    S = np.zeros((steps + 1, steps + 1))
    S[0, 0] = S0

    for i in range(1, steps + 1):
        for j in range(i + 1):
            if j == 0:
                S[i, j] = S[i - 1, j] * d
            elif j == i:
                S[i, j] = S[i - 1, j - 1] * u
            else:
                S[i, j] = S[i - 1, j - 1] * u

        # Adjust for dividend payment
    if T1 is not None and (i - 1) * dt < T1 <= i * dt:
        S[i, :i + 1] -= div

    # 3) Option value at maturity
    V = np.zeros_like(S)

    if option_type == "call":
        V[steps, :steps + 1] = np.maximum(S[steps, :steps + 1] - K, 0)
    elif option_type == "put":
        V[steps, :steps + 1] = np.maximum(K - S[steps, :steps + 1], 0)
    else:
        raise ValueError("option_type doit être 'call' ou 'put'")

    # 4) Recursion to go back through the tree
    for i in range(steps - 1, -1, -1):
        for j in range(i + 1):
            continuation = discount * ( p * V[i + 1, j + 1] + (1 - p) * V[i + 1, j])

            if option_style == "american":
                if option_type == "call":
                    V[i, j] = max(continuation, S[i, j] - K)
                else:
                    V[i, j] = max(continuation, K - S[i, j])
            else:
                V[i, j] = continuation

    # 5) Option price at time t = 0
    return V[0, 0]