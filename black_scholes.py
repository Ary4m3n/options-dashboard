import numpy as np
from scipy.stats import norm

def black_scholes_price(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("Option type must be 'call' or 'put'.")

def calculate_greeks(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    # delta
    if option_type == 'call':
        delta = norm.cdf(d1)
    else:
        delta = norm.cdf(d1) - 1
    # gamma
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    # theta
    theta = (
        -S * norm.pdf(d1) * sigma / (2 * np.sqrt(T))
        - r * K * np.exp(-r * T) * norm.cdf(d2)
        if option_type == 'call'
        else -S * norm.pdf(d1) * sigma / (2 * np.sqrt(T))
        + r * K * np.exp(-r * T) * norm.cdf(-d2)
    )
    #vega
    vega = S * norm.pdf(d1) * np.sqrt(T)
    #rho
    rho = (
        K * T * np.exp(-r * T) * norm.cdf(d2)
        if option_type == 'call'
        else -K * T * np.exp(-r * T) * norm.cdf(-d2)
    )

    return {
        "Delta": delta,
        "Gamma": gamma,
        "Theta": theta / 365,
        "Vega": vega / 100,
        "Rho": rho / 100
    }
