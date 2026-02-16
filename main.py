import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
 
st.set_page_config(
    page_title="Smart Campus Energy Dashboard",
    layout="wide"
)
 
st.title("🏫 Smart Campus Energy Efficiency Dashboard")
 
# ---------------- MOCK DATA ---------------- #
np.random.seed(21)
 
blocks = [
    "M Block - Classrooms",
    "M Block - Labs",
    "M Block - Auditorium",
    "Old Building - A Block",
    "Old Building - B Block",
    "Old Building - C Block",
    "Old Building - D Block",
    "Old Building - E Block",
    "Old Building - F Block",
    "Old Building - G Block",
    "Old Building - Lower Floor Labs",
    "Canteens"
]
 
df = pd.DataFrame({
    "Block": blocks,
    "Peak Energy (kWh)": np.random.randint(400, 1200, len(blocks)),
    "Non-Peak Energy (kWh)": np.random.randint(200, 700, len(blocks)),
    "Efficiency Score (%)": np.random.randint(55, 95, len(blocks)),
    "Solar Offset (%)": np.random.randint(20, 60, len(blocks))
})
 
df["Total Energy (kWh)"] = df["Peak Energy (kWh)"] + df["Non-Peak Energy (kWh)"]
df["Grid Dependency (%)"] = 100 - df["Solar Offset (%)"]
df["CO₂ Impact (kg/day)"] = df["Total Energy (kWh)"] * 0.78
 
# ---------------- SIDEBAR ---------------- #
st.sidebar.title("⚙️ Controls")
 
selected_blocks = st.sidebar.multiselect(
    "Select Blocks",
    df["Block"],
    default=df["Block"]
)
 
efficiency_range = st.sidebar.slider(
    "Efficiency Range (%)",
    0, 100, (60, 95)
)
 
filtered = df[
    (df["Block"].isin(selected_blocks)) &
    (df["Efficiency Score (%)"].between(efficiency_range[0], efficiency_range[1]))
]
 
# ---------------- KPI ROW ---------------- #
k1, k2, k3, k4 = st.columns(4)
 
k1.metric("⚡ Total Energy (kWh/day)", int(filtered["Total Energy (kWh)"].sum()))
k2.metric("🌞 Avg Solar Offset (%)", int(filtered["Solar Offset (%)"].mean()))
k3.metric("♻️ Avg Efficiency (%)", int(filtered["Efficiency Score (%)"].mean()))
k4.metric("🌍 CO₂ Impact (kg/day)", int(filtered["CO₂ Impact (kg/day)"].sum()))
 
st.divider()
 
# ---------------- ENERGY FLOW VISUAL ---------------- #
st.subheader("🔁 Energy Usage Pattern (Peak vs Non-Peak)")
 
fig_stack = go.Figure(data=[
    go.Bar(
        name="Peak",
        x=filtered["Block"],
        y=filtered["Peak Energy (kWh)"]
    ),
    go.Bar(
        name="Non-Peak",
        x=filtered["Block"],
        y=filtered["Non-Peak Energy (kWh)"]
    )
])
 
fig_stack.update_layout(
    barmode="stack",
    height=320
)
 
st.plotly_chart(fig_stack, use_container_width=True)
 
# ---------------- MIDDLE SECTION ---------------- #
c1, c2 = st.columns(2)
 
with c1:
    st.subheader("📉 Energy Efficiency Comparison")
    fig_eff = px.line(
        filtered,
        x="Block",
        y="Efficiency Score (%)",
        markers=True,
        height=300
    )
    st.plotly_chart(fig_eff, use_container_width=True)
 
with c2:
    st.subheader("☀️ Solar Offset vs Grid Dependency")
    fig_bubble = px.scatter(
        filtered,
        x="Solar Offset (%)",
        y="Grid Dependency (%)",
        size="Total Energy (kWh)",
        color="Block",
        height=300
    )
    st.plotly_chart(fig_bubble, use_container_width=True)
 
# ---------------- BOTTOM SECTION ---------------- #
b1, b2 = st.columns(2)
 
with b1:
    st.subheader("🌍 CO₂ Impact by Block")
    fig_co2 = px.bar(
        filtered,
        x="Block",
        y="CO₂ Impact (kg/day)",
        height=280
    )
    st.plotly_chart(fig_co2, use_container_width=True)
 
with b2:
    st.subheader("📊 Energy Distribution Share")
    fig_donut = px.pie(
        filtered,
        names="Block",
        values="Total Energy (kWh)",
        hole=0.4,
        height=280
    )
    st.plotly_chart(fig_donut, use_container_width=True)
 
# ---------------- INSIGHTS ---------------- #
st.divider()
st.subheader("🧠 Key Insights & Action Plan")
 
st.success(
    "• Peak-hour energy usage dominates in M Block labs and auditorium.\n"
    "• Old building blocks show lower efficiency, indicating retrofit potential.\n"
    "• Higher solar offset directly reduces grid dependency and emissions.\n"
    "• Energy efficiency improves significantly during non-peak hours."
)
 
st.info(
    "🔮 Sustainability Roadmap:\n"
    "• Introduce time-based energy pricing awareness\n"
    "• Shift heavy loads to non-peak hours\n"
    "• Improve insulation and natural ventilation\n"
    "• Deploy predictive analytics for energy planning\n"
    "• Long-term goal: energy-efficient smart campus"
)
 