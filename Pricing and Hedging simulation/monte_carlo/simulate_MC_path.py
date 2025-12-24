def simulate_MC_path(S0, T, r, sigma, steps, div=0, T1=0):

    dt = T / steps
    S_path = [S0]
    for i in range(1, steps+1):
        S_prev = S_path[-1]
        Z = np.random.randn()  # normal random variable
        S_t = S_prev * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z)
        
        # Discrete dividend application if needed
        if div > 0 and (i-1)*dt < T1 <= i*dt:
            S_t -= div
            
        S_path.append(S_t)
    return np.array(S_path)