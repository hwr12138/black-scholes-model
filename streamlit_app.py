import streamlit as st
import pandas as pd
import black_scholes as bs
import numpy as np


# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Black-Scholes Model',
    page_icon=':earth_americas:', # This is an emoji shortcode. Could be a URL too.
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

# Pull Fed interest rate

# Custom CSS to inject into Streamlit
st.markdown("""
<style>
.metric-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 8px;
    width: auto;
    margin: 0 auto;
}

.metric-call {
    background-color: #90ee90;
    color: black;
    border-radius: 10px;
}

.metric-put {
    background-color: #ffcccb;
    color: black;
    border-radius: 10px;
}

.metric-value {
    font-size: 1.5rem;
    font-weight: bold;
    margin: 0;
}

.metric-greeks {
    font-size: 1rem;
    margin: 0;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
st.title("Black-Scholes Options Pricing Model")
st.write("`Created by:`")
linkedin_url = "https://www.linkedin.com/in/haowenruiprofile/"
st.markdown(f'<a href="{linkedin_url}" target="_blank" style="text-decoration: none; color: inherit;"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="25" height="25" style="vertical-align: middle; margin-right: 10px;">`Anson (Hao Wen) Rui`</a>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    current_price = st.number_input("Current Asset Price", value=100.0)
    volatility = st.number_input("Volatility (σ)", value=0.2)
with col2:
    strike_price = st.number_input("Strike Price", value=90.0)
    interest_rate = st.number_input("Risk-Free Interest Rate (%)", value=5.00)
with col3:
    time_to_maturity = st.number_input("Time to Maturity (Days)", value=365)

''
''

# Calculate Call and Put values
bs_model = bs.BlackScholes(time_to_maturity, strike_price, current_price, volatility, interest_rate)
bs_model.compute_price()
bs_model.compute_greeks()

# Display Call and Put Values in colored tables
col1, col2 = st.columns([1,1], gap="small")
with col1:
    # Using the custom class for CALL value
    st.markdown(f"""
        <div class="metric-container metric-call">
            <div>
                <div class="metric-value">CALL Value: ${bs_model.call_price:.2f}</div>
                <div class="metric-greeks">Delta (Δ): {bs_model.call_delta:.8f}</div>
                <div class="metric-greeks">Gamma (Γ): {bs_model.gamma:.8f}</div>
                <div class="metric-greeks">Theta (Θ): {bs_model.call_theta:.8f}</div>
                <div class="metric-greeks">Vega (ν): {bs_model.vega:.8f}</div>
                <div class="metric-greeks">Rho (ρ): {bs_model.call_rho:.8f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
with col2:
    # Using the custom class for PUT value
    st.markdown(f"""
        <div class="metric-container metric-put">
            <div>
                <div class="metric-value">PUT Value: ${bs_model.put_price:.2f}</div>
                <div class="metric-greeks">Delta (Δ): {bs_model.put_delta:.8f}</div>
                <div class="metric-greeks">Gamma (Γ): {bs_model.gamma:.8f}</div>
                <div class="metric-greeks">Theta (Θ): {bs_model.put_theta:.8f}</div>
                <div class="metric-greeks">Vega (ν): {bs_model.vega:.8f}</div>
                <div class="metric-greeks">Rho (ρ): {bs_model.put_rho:.8f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("")
st.markdown("---")
st.title("Options Price - Interactive Heatmap")
col1, col2 = st.columns(2)
with col1:
    spot_min = st.number_input('Min Spot Price', min_value=0.01, value=current_price*0.8, step=0.01)
    spot_max = st.number_input('Max Spot Price', min_value=0.01, value=current_price*1.2, step=0.01)
    purchase_price = st.number_input('Options Purchase Price', value=15)

with col2:
    vol_min = st.slider('Min Volatility for Heatmap', min_value=0.01, max_value=1.0, value=volatility*0.5, step=0.01)
    vol_max = st.slider('Max Volatility for Heatmap', min_value=0.01, max_value=1.0, value=volatility*1.5, step=0.01)

spot_range = np.linspace(spot_min, spot_max, 10)
vol_range = np.linspace(vol_min, vol_max, 10)

# Interactive Sliders and Heatmaps for Call and Put Options
col1, col2 = st.columns([1,1], gap="small")
heatmap_fig_call, heatmap_fig_put, heatmap_fig_call_profit, heatmap_fig_put_profit = bs.BlackScholes.plot_heatmap(strike_price, time_to_maturity, interest_rate, spot_range, vol_range, purchase_price)

with col1:
    st.subheader("Call Price Heatmap")
    st.pyplot(heatmap_fig_call)
    st.subheader("Call Profit Heatmap")
    st.pyplot(heatmap_fig_call_profit)

with col2:
    st.subheader("Put Price Heatmap")
    st.pyplot(heatmap_fig_put)
    st.subheader("Put Profit Heatmap")
    st.pyplot(heatmap_fig_put_profit)