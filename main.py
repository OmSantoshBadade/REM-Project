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

# System types for energy consumption breakdown
system_types = ["HVAC", "Lighting", "Computers & IT", "Lab Equipment", "Other Appliances"]
 
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

# Generate system-wise energy breakdown for each block
system_data = []
for block in blocks:
    total_energy = df[df["Block"] == block]["Total Energy (kWh)"].values[0]
    
    # Generate realistic percentages for each system type
    # HVAC typically consumes most, followed by lighting, then equipment
    percentages = np.random.dirichlet(np.array([3.5, 2.0, 2.5, 2.0, 1.0]))
    
    for i, system in enumerate(system_types):
        system_data.append({
            "Block": block,
            "System Type": system,
            "Energy (kWh)": round(total_energy * percentages[i], 2),
            "Percentage": round(percentages[i] * 100, 1)
        })

df_systems = pd.DataFrame(system_data)
 
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

view_mode = st.sidebar.radio(
    "View Mode",
    ["Overview", "System Type Analysis"]
)
 
filtered = df[
    (df["Block"].isin(selected_blocks)) &
    (df["Efficiency Score (%)"].between(efficiency_range[0], efficiency_range[1]))
]

filtered_systems = df_systems[df_systems["Block"].isin(selected_blocks)]
 
# ---------------- KPI ROW ---------------- #
k1, k2, k3, k4 = st.columns(4)
 
k1.metric("⚡ Total Energy (kWh/day)", int(filtered["Total Energy (kWh)"].sum()))
k2.metric("🌞 Avg Solar Offset (%)", int(filtered["Solar Offset (%)"].mean()))
k3.metric("♻️ Avg Efficiency (%)", int(filtered["Efficiency Score (%)"].mean()))
k4.metric("🌍 CO₂ Impact (kg/day)", int(filtered["CO₂ Impact (kg/day)"].sum()))
 
st.divider()

# ---------------- VIEW MODES ---------------- #
if view_mode == "Overview":
    # ---------------- ENERGY FLOW VISUAL ---------------- #
    st.subheader("📊 Energy Usage Pattern (Peak vs Non-Peak)")
    
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

else:  # System Type Analysis
    st.subheader("🔌 Energy Consumption by System Type")
    
    # Overall system breakdown
    system_totals = filtered_systems.groupby("System Type")["Energy (kWh)"].sum().reset_index()
    system_totals = system_totals.sort_values("Energy (kWh)", ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Overall System Energy Distribution")
        fig_system_pie = px.pie(
            system_totals,
            names="System Type",
            values="Energy (kWh)",
            hole=0.4,
            height=350,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_system_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_system_pie, use_container_width=True)
    
    with col2:
        st.markdown("### Energy by System Type (kWh)")
        fig_system_bar = px.bar(
            system_totals,
            x="System Type",
            y="Energy (kWh)",
            height=350,
            color="System Type",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_system_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_system_bar, use_container_width=True)
    
    st.divider()
    
    # System breakdown by block
    st.subheader("🏢 System Energy Breakdown by Block")
    
    fig_stacked_systems = go.Figure()
    
    for system in system_types:
        system_df = filtered_systems[filtered_systems["System Type"] == system]
        fig_stacked_systems.add_trace(go.Bar(
            name=system,
            x=system_df["Block"],
            y=system_df["Energy (kWh)"],
        ))
    
    fig_stacked_systems.update_layout(
        barmode='stack',
        height=400,
        xaxis_title="Building Block",
        yaxis_title="Energy Consumption (kWh)",
        legend_title="System Type"
    )
    
    st.plotly_chart(fig_stacked_systems, use_container_width=True)
    
    # Detailed table
    st.subheader("📋 Detailed System Energy Consumption")
    
    # Pivot table for better view
    pivot_table = filtered_systems.pivot_table(
        values="Energy (kWh)",
        index="Block",
        columns="System Type",
        aggfunc="sum"
    ).round(2)
    
    pivot_table["Total"] = pivot_table.sum(axis=1)
    pivot_table = pivot_table.sort_values("Total", ascending=False)
    
    st.dataframe(pivot_table, use_container_width=True)
    
    # Top energy consumers by system
    st.divider()
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("### 🔥 Top 5 Energy-Intensive Systems")
        top_systems = filtered_systems.nlargest(5, "Energy (kWh)")[["Block", "System Type", "Energy (kWh)"]]
        st.dataframe(top_systems.reset_index(drop=True), use_container_width=True)
    
    with col4:
        st.markdown("### 💡 System Type Comparison")
        avg_by_system = filtered_systems.groupby("System Type").agg({
            "Energy (kWh)": ["mean", "sum"]
        }).round(2)
        avg_by_system.columns = ["Avg per Block (kWh)", "Total (kWh)"]
        st.dataframe(avg_by_system, use_container_width=True)
 
# ---------------- INSIGHTS ---------------- #
st.divider()
st.subheader("🧠 Key Insights & Action Plan")

if view_mode == "Overview":
    st.success(
        "• Peak-hour energy usage dominates in M Block labs and auditorium.\n"
        "• Old building blocks show lower efficiency, indicating retrofit potential.\n"
        "• Higher solar offset directly reduces grid dependency and emissions.\n"
        "• Energy efficiency improves significantly during non-peak hours."
    )
else:
    # Calculate top system
    top_system = system_totals.iloc[0]["System Type"]
    top_system_energy = system_totals.iloc[0]["Energy (kWh)"]
    top_system_pct = (top_system_energy / system_totals["Energy (kWh)"].sum() * 100)
    
    st.success(
        f"• **{top_system}** is the largest energy consumer, accounting for {top_system_pct:.1f}% of total usage.\n"
        f"• HVAC systems typically show high consumption - optimize temperature settings and schedules.\n"
        f"• Lab equipment in research blocks contributes significantly to energy load.\n"
        f"• Lighting optimization can provide quick energy savings with LED upgrades."
    )
 
st.info(
    "🔮 Sustainability Roadmap:\n"
    "• Introduce time-based energy pricing awareness\n"
    "• Shift heavy loads to non-peak hours\n"
    "• Improve insulation and natural ventilation\n"
    "• Deploy predictive analytics for energy planning\n"
    "• Upgrade to energy-efficient HVAC and lighting systems\n"
    "• Implement smart sensors for automated system control\n"
    "• Long-term goal: energy-efficient smart campus"
)

# ---------------- DOWNLOAD DATA ---------------- #
st.divider()
st.subheader("📥 Export Data")

col_download1, col_download2 = st.columns(2)

with col_download1:
    csv_overview = filtered.to_csv(index=False)
    st.download_button(
        label="Download Overview Data (CSV)",
        data=csv_overview,
        file_name="energy_overview.csv",
        mime="text/csv"
    )

with col_download2:
    csv_systems = filtered_systems.to_csv(index=False)
    st.download_button(
        label="Download System Data (CSV)",
        data=csv_systems,
        file_name="system_energy_data.csv",
        mime="text/csv"
    )
