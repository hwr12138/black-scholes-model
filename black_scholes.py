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
        self.time_to_maturity = time_to_maturity
        self.strike_price = strike_price
        self.current_price = current_price
        self.volatility = volatility
        self.interest_rate = interest_rate

    def compute(self):
        d1 = (log(self.current_price / self.strike_price) + 
                (self.interest_rate + (self.volatility ** 2) / 2) * self.time_to_maturity
            ) / (self.volatility * sqrt(self.time_to_maturity))
        d2 = d1 - self.volatility * sqrt(self.time_to_maturity)

        # Call and Put Prices
        self.call_price = self.current_price * norm.cdf(d1, 0, 1) - (
            self.strike_price * exp(-(self.interest_rate * self.time_to_maturity)) * 
            norm.cdf(d2, 0, 1))
        self.put_price = (self.strike_price * 
                          exp(-(self.interest_rate * self.time_to_maturity)) * 
                          norm.cdf(-d2, 0, 1)) - self.current_price * norm.cdf(-d1, 0, 1)

        # GREEKS
        self.call_delta = norm.cdf(d1, 0, 1)
        self.put_delta = -norm.cdf(-d1, 0, 1)

        self.gamma = norm.pdf(d1, 0, 1) / (
            self.current_price * self.volatility * sqrt(self.time_to_maturity))

        self.call_theta = (-self.current_price * norm.pdf(d1, 0, 1) * self.volatility) / (
            2 * sqrt(self.time_to_maturity)) - (
                self.interest_rate * self.strike_price * 
                exp(-self.interest_rate * self.time_to_maturity) * norm.cdf(d2, 0, 1))
        self.put_theta = (-self.current_price * norm.pdf(d1, 0, 1) * self.volatility) / (
            2 * sqrt(self.time_to_maturity)) + (
                self.interest_rate * self.strike_price * 
                exp(-self.interest_rate * self.time_to_maturity) * norm.cdf(-d2, 0, 1))
        
        self.vega = self.current_price * norm.pdf(d1, 0, 1) * sqrt(time_to_maturity)

        self.call_rho = 
        self.put_rho = 
    
    # Heat Map
    def plot_heatmap(self, spot_range, vol_range, strike_price):
        call_prices = np.zeros((len(vol_range), len(spot_range)))
        put_prices = np.zeros((len(vol_range), len(spot_range)))
        
        for i, vol in enumerate(vol_range):
            for j, spot in enumerate(spot_range):
                bs_temp = BlackScholes(
                    time_to_maturity=self.time_to_maturity,
                    strike_price=strike_price,
                    current_price=spot,
                    volatility=vol,
                    interest_rate=self.interest_rate
                )
                bs_temp.compute()
                call_prices[i, j] = bs_temp.call_price
                put_prices[i, j] = bs_temp.put_price
        
        # Plotting Call Price Heatmap
        fig_call, ax_call = plt.subplots(figsize=(10, 8))
        sns.heatmap(call_prices, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2), annot=True, fmt=".2f", cmap="viridis", ax=ax_call)
        ax_call.set_title('CALL')
        ax_call.set_xlabel('Spot Price')
        ax_call.set_ylabel('Volatility')
        
        # Plotting Put Price Heatmap
        fig_put, ax_put = plt.subplots(figsize=(10, 8))
        sns.heatmap(put_prices, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2), annot=True, fmt=".2f", cmap="viridis", ax=ax_put)
        ax_put.set_title('PUT')
        ax_put.set_xlabel('Spot Price')
        ax_put.set_ylabel('Volatility')
        
        return fig_call, fig_put


if __name__ == "__main__":
    time_to_maturity = 1  # 1 year
    strike_price = 90
    current_price = 100
    volatility = 0.2
    interest_rate = 0.04

    model = BlackScholes(
        time_to_maturity = time_to_maturity,
        strike_price = strike_price,
        current_price = current_price,
        volatility = volatility,
        interest_rate = interest_rate)
    model.compute()