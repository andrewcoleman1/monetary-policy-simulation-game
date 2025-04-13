import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("💸 Monetary Policy Simulation Game")

# Session state initialization
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.output_growth = []
    st.session_state.inflation = []
    st.session_state.real_interest_rate = []
    st.session_state.nominal_interest_rate = []

def simulate_step():
    # Random simulation of economic indicators
    real_growth = max(0, 2 + np.random.uniform(-1, 1))
    inflation = max(0, 2 + np.random.uniform(-0.5, 1.5))
    nominal_rate = inflation + 2
    real_rate = nominal_rate - inflation

    # Append values to session state
    st.session_state.output_growth.append(real_growth)
    st.session_state.inflation.append(inflation)
    st.session_state.nominal_interest_rate.append(nominal_rate)
    st.session_state.real_interest_rate.append(real_rate)
    st.session_state.step += 1

    return real_growth, inflation, real_rate, nominal_rate

# Layout buttons
col1, col2, col3 = st.columns(3)
if col1.button("🔁 STEP"):
    simulate_step()

if col2.button("🔁 RESET"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()

# Latest statistics
if st.session_state.step > 0:
    latest = {
        "Real Output Growth": st.session_state.output_growth[-1],
        "Inflation": st.session_state.inflation[-1],
        "Real Interest Rate": st.session_state.real_interest_rate[-1],
        "Nominal Interest Rate": st.session_state.nominal_interest_rate[-1],
    }
    st.write("### 📊 Latest Economic Data")
    for k, v in latest.items():
        st.metric(k, f"{v:.2f}%")

# Chart display function
def plot_metric(data, title):
    fig, ax = plt.subplots()
    ax.plot(data, marker="o", color="blue")
    ax.set_title(title)
    ax.set_ylim(0, 100)
    ax.grid(True)
    st.pyplot(fig)

# Show charts
if st.session_state.step > 0:
    col1, col2 = st.columns(2)
    with col1:
        plot_metric(st.session_state.output_growth, "Real Output Growth")
        plot_metric(st.session_state.real_interest_rate, "Real Interest Rate")
    with col2:
        plot_metric(st.session_state.inflation, "Inflation")
        plot_metric(st.session_state.nominal_interest_rate, "Nominal Interest Rate")
