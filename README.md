# Sector-Specific Portfolio Optimization in the Indian Stock Markets

## Overview
This project focuses on optimizing sector-specific investment portfolios in the Indian stock market. By leveraging historical data and applying Mean-Variance Optimization (MVO) with dynamic rebalancing, it aims to maximize returns while managing risk effectively.

## Features
- **Historical Data Analysis:** Analyzes stock prices from January 1, 2019, to December 31, 2022.
- **Sector-Based Portfolio Optimization:** Maximizes the Sharpe ratio for six key sectors as defined by the NSE.
- **Mean-Variance Optimization (MVO):** Utilizes Markowitz’s model to determine efficient portfolio weights.
- **Dynamic Rebalancing:** Adjusts sector weights quarterly based on economic conditions.
- **Backtesting:** Evaluates portfolio performance using cumulative returns from January 1, 2023, to December 31, 2024.
- **Visualization Dashboard:** Presents results using Dash and Plotly for better insights.

## Methodology
1. **Data Collection and Processing (Week 1)**
   - Fetch stock prices using Python's `pandas-datareader` and APIs like NSE/BSE.
   - Compute logarithmic returns for stocks and sector indices.
   
2. **Sector-Wise Risk and Return Analysis (Week 2)**
   - Calculate returns (μ) and volatility (σ) for each stock and sector.
   - Compute correlation matrices and beta values to analyze stock-sector relationships.

3. **Portfolio Optimization and Dynamic Rebalancing (Week 3)**
   - Implement Markowitz’s model with constraints (sector caps ≤ 0.3, weight bounds, etc.).
   - Optimize for maximum Sharpe ratio.
   - Introduce quarterly rebalancing on the portfolio.

4. **Backtesting and Dashboard Development (Week 4)**
   - Train the model on historical data and evaluate performance using metrics like Sharpe and Sortino ratios.
   - Develop an interactive dashboard using Dash/Plotly.

## Technologies Used
- **Python** (pandas, numpy, yfinance, scipy, matplotlib, seaborn)
- **APIs** (Yahoo Finance, NSE/BSE, Quandl)
- **Optimization Tools** (cvxpy, scipy.optimize)
- **Visualization** (Dash, Plotly)

## Usage
- Run the notebooks in the order `Data_Preprocess.ipynb`, `Sector_Analysis.ipynb`, `MVO_Model.ipynb` and `BackTesting.ipynb`.
- Run `monthwise_dashboard.py` to visualize results interactively.

## References
- [Jaydip Sen & Abhishek Dutta, 2022] – Sector-based portfolio optimization.
- [Gupta & Basu, 2022] – Correlation analysis of Indian stock sectors.
- Yahoo Finance, NSE/BSE APIs for stock and sector data.

## Contact
**Megh Bhavesh Shah**  
[Email](mailto:megh_bs@cs.iitr.ac.in)  
[LinkedIn](https://www.linkedin.com/in/megh-bhavesh-shah/)
