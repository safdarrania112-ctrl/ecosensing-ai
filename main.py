import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from scipy import stats

# Page Configuration
st.set_page_config(
    page_title="EcoSensing-AI Analytics Suite",
    page_icon="🌱",
    layout="wide"
)

# App Title & Header
st.title("🌱 EcoSensing-AI: Environmental & Electroanalytical Suite")
st.markdown("---")
st.markdown(
    "Welcome to the research analytics portal. Use the sidebar to navigate between "
    "heavy metal sensor calibration, data processing, and photocatalytic degradation kinetics."
)

# Sidebar Navigation
st.sidebar.header("Navigation Panel")
analysis_mode = st.sidebar.selectbox(
    "Choose Module",
    [
        "Home / Overview",
        "Linear Calibration & LOD/LOQ",
        "Photocatalytic Kinetics",
    ]
)

if analysis_mode == "Home / Overview":
    st.subheader("📊 System Overview")
    st.write(
        "This application automates electroanalytical data processing, calibration curve "
        "generation, limit of detection (LOD/LOQ) calculations, and pseudo-first-order "
        "kinetic modeling for wastewater remediation research."
    )
    
    # Quick Sample Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Target Heavy Metal Ions", value="15+")
    with col2:
        st.metric(label="Calculated R² Confidence", value="> 0.998")
    with col3:
        st.metric(label="Model Status", value="Active & Online")

elif analysis_mode == "Linear Calibration & LOD/LOQ":
    st.subheader("📈 Linear Calibration & Detection Limits")
    st.write("Input your concentration and corresponding analytical signal (Current/Absorbance) data below:")

    # Default sample data
    default_data = pd.DataFrame({
        "Concentration (µM)": [1.0, 5.0, 10.0, 20.0, 50.0, 100.0],
        "Signal (µA)": [2.5, 11.2, 22.4, 45.1, 110.5, 220.0]
    })

    edited_df = st.data_editor(default_data, num_rows="dynamic")

    if not edited_df.empty and len(edited_df) >= 3:
        x = edited_df["Concentration (µM)"]
        y = edited_df["Signal (µA)"]

        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        r_squared = r_value ** 2

        # LOD and LOQ calculations (3.3 * SD / slope and 10 * SD / slope)
        # Estimating residual standard deviation from standard error of estimate
        residuals = y - (slope * x + intercept)
        sy_x = np.sqrt(np.sum(residuals**2) / (len(x) - 2)) if len(x) > 2 else 0.0
        lod = (3.3 * sy_x) / slope if slope != 0 else 0
        loq = (10.0 * sy_x) / slope if slope != 0 else 0

        st.markdown("### 📋 Regression Results")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Slope", f"{slope:.4f}")
        col2.metric("Intercept", f"{intercept:.4f}")
        col3.metric("R² Value", f"{r_squared:.4f}")
        col4.metric("Estimated LOD", f"{lod:.3f} µM")

        # Plotly Calibration Curve
        fig = px.scatter(
            edited_df, x="Concentration (µM)", y="Signal (µA)",
            title="Calibration Curve with Linear Fit",
            labels={"Concentration (µM)": "Concentration (µM)", "Signal (µA)": "Analytical Signal (µA)"}
        )
        # Add regression line
        line_y = slope * x + intercept
        fig.add_scatter(x=x, y=line_y, mode="lines", name=f"Fit: y={slope:.2f}x+{intercept:.2f}")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Please provide at least 3 data points for reliable linear regression.")

elif analysis_mode == "Photocatalytic Kinetics":
    st.subheader("⚗️ Photocatalytic Degradation Kinetics")
    st.write("Analyze dye degradation data over time using pseudo-first-order kinetics ($ln(C_0/C_t) = k \cdot t$).")

    time_data = pd.DataFrame({
        "Time (min)": [0, 15, 30, 45, 60, 90],
        "Concentration Ct (mg/L)": [10.0, 7.8, 5.9, 4.2, 3.1, 1.5]
    })

    edited_kinetics = st.data_editor(time_data, num_rows="dynamic")

    if not edited_kinetics.empty and len(edited_kinetics) >= 2:
        t = edited_kinetics["Time (min)"]
        c = edited_kinetics["Concentration Ct (mg/L)"]
        c0 = c.iloc[0]

        # Prevent log of zero or negative values
        valid_mask = c > 0
        if valid_mask.all() and c0 > 0:
            ln_c0_ct = np.log(c0 / c)
            k_slope, k_intercept, k_r_val, _, _ = stats.linregress(t, ln_c0_ct)

            st.markdown("### 📊 Kinetic Parameters")
            col1, col2 = st.columns(2)
            col1.metric("Rate Constant (k)", f"{k_slope:.4f} min⁻¹")
            col2.metric("Kinetic R²", f"{k_r_val**2:.4f}")

            fig_kin = px.scatter(
                x=t, y=ln_c0_ct,
                title="Pseudo-First-Order Degradation Kinetics",
                labels={"x": "Time (min)", "y": "ln(C₀ / Cₜ)"}
            )
            fig_kin.add_scatter(x=t, y=k_slope * t + k_intercept, mode="lines", name="Linear Fit")
            st.plotly_chart(fig_kin, use_container_width=True)
        else:
            st.error("Concentration values must be strictly greater than zero for logarithmic kinetic calculations.")
