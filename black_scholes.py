from numpy import exp, sqrt, log
from scipy.stats import norm
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class BlackScholes:
    def __init__(
        self,
        time_to_maturity: float,
        strike_price: float,
        current_price: float,
        volatility: float,
        interest_rate: float,
    ):
        self.S = current_price
        self.K = strike_price
        self.T = time_to_maturity / 365
        self.r = interest_rate / 100
        self.sigma = volatility

    def compute_price(self):
        self.d1 = (log(self.S / self.K) + (self.r + (self.sigma**2) / 2) * self.T) / (self.sigma * sqrt(self.T))
        self.d2 = self.d1 - self.sigma * sqrt(self.T)

        # Call and Put Prices
        self.call_price = self.S * norm.cdf(self.d1, 0, 1) - (self.K * exp(-(self.r * self.T)) * norm.cdf(self.d2, 0, 1))
        self.put_price = (self.K * exp(-(self.r * self.T)) * norm.cdf(-self.d2, 0, 1)) - self.S * norm.cdf(-self.d1, 0, 1)

    def compute_greeks(self):
        self.call_delta = norm.cdf(self.d1, 0, 1)
        self.put_delta = -norm.cdf(-self.d1, 0, 1)

        self.gamma = norm.pdf(self.d1, 0, 1) / (self.S * self.sigma * sqrt(self.T))

        self.call_theta = (-self.S * norm.pdf(self.d1, 0, 1) * self.sigma) / (2 * sqrt(self.T)) - (self.r * self.K * exp(-self.r * self.T) * norm.cdf(self.d2, 0, 1))
        self.put_theta = (-self.S * norm.pdf(self.d1, 0, 1) * self.sigma) / (2 * sqrt(self.T)) + (self.r * self.K * exp(-self.r * self.T) * norm.cdf(-self.d2, 0, 1))
        
        self.vega = self.S * norm.pdf(self.d1, 0, 1) * sqrt(self.T)

        self.call_rho = (self.K * self.T * exp(-self.r * self.T) * norm.cdf(self.d2, 0, 1))
        self.put_rho = -(self.K * self.T * exp(-self.r * self.T) * norm.cdf(-self.d2, 0, 1))

    @staticmethod
    def plot_heatmap(K, T, r, spot_range, vol_range, purchase_price):
        call_prices = np.zeros((len(vol_range), len(spot_range)))
        call_profit = np.zeros((len(vol_range), len(spot_range)))
        put_prices = np.zeros((len(vol_range), len(spot_range)))
        put_profit = np.zeros((len(vol_range), len(spot_range)))
        
        for i, vol in enumerate(vol_range):
            for j, spot in enumerate(spot_range):
                bs_temp = BlackScholes(
                    time_to_maturity=T,
                    strike_price=K,
                    current_price=spot,
                    volatility=vol,
                    interest_rate=r
                )
                bs_temp.compute_price()
                call_prices[i, j] = bs_temp.call_price
                call_profit[i, j] = bs_temp.call_price - purchase_price
                put_prices[i, j] = bs_temp.put_price
                put_profit[i, j] = bs_temp.put_price - purchase_price
        
        # Plotting Call Price Heatmap
        fig_call, ax_call = plt.subplots(figsize=(10, 8))
        sns.heatmap(call_prices, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2), annot=True, fmt=".2f", cmap="RdYlGn", ax=ax_call)
        ax_call.set_title('CALL')
        ax_call.set_xlabel('Spot Price')
        ax_call.set_ylabel('Volatility')
        
        # Plotting Put Price Heatmap
        fig_put, ax_put = plt.subplots(figsize=(10, 8))
        sns.heatmap(put_prices, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2), annot=True, fmt=".2f", cmap="RdYlGn", ax=ax_put)
        ax_put.set_title('PUT')
        ax_put.set_xlabel('Spot Price')
        ax_put.set_ylabel('Volatility')

        # Plotting Call Profit Heatmap
        fig_call_profit, ax_call_profit = plt.subplots(figsize=(10, 8))
        sns.heatmap(call_profit, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2), annot=True, fmt=".2f", cmap="RdYlGn", ax=ax_call_profit)
        ax_call_profit.set_title('CALL')
        ax_call_profit.set_xlabel('Spot Price')
        ax_call_profit.set_ylabel('Volatility')

        # Plotting Put Profit Heatmap
        fig_put_profit, ax_put_profit = plt.subplots(figsize=(10, 8))
        sns.heatmap(put_profit, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2), annot=True, fmt=".2f", cmap="RdYlGn", ax=ax_put_profit)
        ax_put_profit.set_title('PUT')
        ax_put_profit.set_xlabel('Spot Price')
        ax_put_profit.set_ylabel('Volatility')

        return fig_call, fig_put, fig_call_profit, fig_put_profit


if __name__ == "__main__":
    time_to_maturity = 365
    strike_price = 90
    current_price = 100
    volatility = 0.2
    interest_rate = 0.05

    model = BlackScholes(
        time_to_maturity = time_to_maturity,
        strike_price = strike_price,
        current_price = current_price,
        volatility = volatility,
        interest_rate = interest_rate)
    model.compute()