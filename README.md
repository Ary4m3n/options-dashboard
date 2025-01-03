# Options Pricing Dashboard

![Dashboard Screenshot](https://options-pricing-dashboard.onrender.com/assets/dashboard-screenshot.png)

An interactive web application to calculate and visualize options pricing using the Black-Scholes model. This dashboard enables users to explore how option prices, payoff diagrams and option greeks change based on inputs like strike price, time to maturity, interest rates, and volatility.

Live Demo: [Options Pricing Dashboard](https://options-pricing-dashboard.onrender.com/)

---

## Features

- 📈 **Real-time Option Pricing**: Calculate call and put option prices dynamically.
- 📊 **Interactive Payoff Diagram**: Visualize the payoff structure of call and put options.
- 🔢 **Adjustable Parameters**:
  - Strike Price
  - Time to Maturity (Years)
  - Interest Rate (%)
  - Volatility (editable)
- 📋 **Greeks Table**: View key Greek metrics (Delta, Gamma, Theta, Vega, Rho) for options.
- 🔍 **Stock Ticker Integration**: Fetch real-time stock data and integrate it into pricing models.

---

## Usage Instructions

### How to Use the Options Pricing Dashboard

1. **Navigate to the Dashboard:**

   - Open your browser and go to [Options Pricing Dashboard](https://options-pricing-dashboard.onrender.com).

2. **Search for a Stock Ticker:**

   - Use the input field at the top of the page to enter a stock ticker (e.g., `AAPL`, `TSLA`).
   - Click the "Submit" button to load the stock's data.

3. **Adjust Parameters:**

   - **Strike Price:** Use the slider or input box to set the strike price of the option.
   - **Time to Maturity (Years):** Adjust the time to maturity in years using the slider or input box.
   - **Interest Rate (%):** Modify the risk-free interest rate using the slider or input box.
   - **Volatility (%):** Update the historical volatility by modifying the pre-filled input box below the stock information.

4. **View Results:**

   - The dashboard will dynamically calculate and display:
     - **Call Option Value**
     - **Put Option Value**
     - **Payoff Diagram**
     - **Option Greeks** (Delta, Gamma, Theta, Vega, Rho)

5. **Interact with the Cards:**
   - Click on the **CALL Value** or **PUT Value** cards to view the payoff diagram for the respective option type.

---

## Tech Stack

The Options Pricing Dashboard is built using the following technologies:

- **Frontend:**

  - [Dash](https://dash.plotly.com/) for building interactive web applications.
  - [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/) for styling and layout.

- **Backend:**

  - **Python** for implementing the logic and calculations.
  - **Gunicorn** as the WSGI HTTP server for production deployment.

- **Libraries for Financial Calculations:**

  - **NumPy:** For numerical computations.
  - **Plotly:** For generating interactive graphs and visualizations.
  - **Custom Python Modules:**
    - `black_scholes.py`: Implements the Black-Scholes pricing model and calculates option Greeks.
    - `volatility.py`: Computes historical volatility.

- **Deployment:**
  - [Render](https://render.com/): For hosting the web application.

---

## Installation and Setup

### Prerequisites

- Python 3.9 or above
- Pip package manager

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/options-pricing-dashboard.git
   cd options-pricing-dashboard
   ```
