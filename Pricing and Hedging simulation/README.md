# Delta Hedging and Option Pricing Framework

This project implements a complete option pricing and delta hedging framework in Python, combining analytical models, lattice methods, and Monte Carlo simulations. The objective is to study option pricing, Greeks computation, and the behavior of delta-hedged portfolios under different market assumptions.

---

## 📌 Project Overview

The project is structured around four main components:

- **Option pricing**
  - Black–Scholes–Merton (BSM) model (European options)
  - Binomial tree pricing (CRR) for European and American options
  - Binomial pricing with discrete dividends

- **Greeks computation**
  - Analytical Greeks (Delta, Gamma) under BSM
  - Finite-difference Greeks for American options and dividend-paying assets

- **Monte Carlo simulation**
  - Simulation of equity price paths under geometric Brownian motion
  - Support for discrete dividend payments

- **Delta hedging**
  - Construction of dynamically rebalanced delta-hedged portfolios
  - Analysis of the distribution of final hedging PnL
  - Visualization of stock paths, deltas, and portfolio values over time
  - Convergence analysis with respect to time discretization and number of paths

---

## 🧮 Models Implemented

### Black–Scholes–Merton (BSM)
- Closed-form pricing for European call and put options
- Analytical Delta and Gamma
- Used as a benchmark and for fast Greeks computation

### Binomial Tree (CRR)
- European and American option pricing
- Early exercise feature for American options
- Extension to discrete dividends

### Monte Carlo Simulation
- Simulation of stock price paths using geometric Brownian motion
- Incorporation of discrete dividends
- Used to study hedging performance under realistic dynamics

---

## 📊 Delta Hedging Strategy

The delta hedging strategy follows a self-financing replication approach:
1. Initial option price and delta are computed.
2. A portfolio of cash and underlying shares is constructed.
3. The hedge is rebalanced at each time step along simulated paths.
4. The final hedging error (PnL) is analyzed across multiple Monte Carlo paths.

The project highlights the impact of:
- Discrete hedging
- Dividend payments
- Option style (European vs American)
- Model assumptions

---

## 📈 Visualizations

The notebook includes:
- Simulated stock price paths
- Evolution of Delta and Gamma along paths
- Value of the delta-hedged portfolio over time
- Distribution of final hedging PnL
- Convergence analysis with respect to time steps and number of simulations

---

## ⚠️ Limitations

- Constant volatility and interest rates
- No transaction costs or market frictions
- Discrete-time hedging
- Model risk when hedging American options using approximate Greeks

These limitations are discussed and illustrated through numerical experiments.

---

## 🚀 Possible Extensions

- Transaction costs and liquidity constraints
- Stochastic volatility models
- Alternative hedging strategies (Gamma/Vega hedging)
- Calibration to market data

---

## 🛠️ Technologies

- Python
- NumPy
- SciPy
- Matplotlib

---

## 📁 Project Structure

```text
.
├── notebook/
│   └── delta_hedging.ipynb
├── src/
│   ├── pricing.py
│   ├── greeks.py
│   ├── monte_carlo.py
│   └── hedging.py
├── README.md

