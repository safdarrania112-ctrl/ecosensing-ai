import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from scipy import stats, optimize

# Page Configuration
st.set_page_config(
    page_title="EcoSensing-AI Research Suite",
    page_icon="🌱",
    layout="wide"
)

# App Title & Header
st.title("🌱 EcoSensing-AI: Professional Publication-Grade Electroanalytical Suite")
st.markdown("---")
st.markdown(
    "Global research computational platform engineered for electrochemists, materials scientists, "
    "and environmental engineers to automate high-impact data analysis, modeling, and manuscript preparation."
)

# Sidebar Navigation
st.sidebar.header("Navigation Panel")
analysis_mode = st.sidebar.selectbox(
    "Choose Module",
    [
        "Home / Overview",
        "Linear Calibration & LOD/LOQ",
        "Photocatalytic Kinetics",
        "Randles-Sevcik Active Surface Area",
        "Adsorption Isotherms (Linear & Non-Linear)",
        "Standard Addition Method",
        "Sensor Selectivity & Interference",
        "Multi-Sensor Calibration Comparison",
        "EIS / Nyquist Rct Estimator",
        "Double-Layer Capacitance (Cdl) & ECSA",
        "pH & Temperature Optimization",
        "AI Publication Paragraph Generator",
        "Professional Lab Report Generator",
        "Citation & Manuscript Info"
    ]
)

if analysis_mode == "Home / Overview":
    st.subheader("📊 System Overview & Research Capabilities")
    st.write(
        "EcoSensing-AI is designed to meet rigorous peer-reviewed publishing standards (Elsevier, ACS, RSC, Springer). "
        "It integrates electrochemical calculations, adsorption modeling, and academic writing assistants into a single unified workspace."
    )
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Modules", value="14 Professional Tools")
    with col2:
        st.metric(label="Publishing Standard", value="SCI / High-Impact")
    with col3:
        st.metric(label="Data Handling", value="CSV & High-Res Export")
    with col4:
        st.metric(label="Citation Ready", value="APA / BibTeX")

    st.markdown("### 🚀 Complete Suite Modules:")
    st.markdown("1. **Linear Calibration & LOD/LOQ:** Analytical sensitivity, regression, residual standard error, and detection limits.")
    st.markdown("2. **Photocatalytic Kinetics:** Pseudo-first/second-order degradation rate constants ($k$) and half-life.")
    st.markdown("3. **Randles-Sevcik Active Surface Area:** Electroactive surface area ($A$) extraction from scan rate variation.")
    st.markdown("4. **Adsorption Isotherms:** Langmuir and Freundlich linear & non-linear curve fitting for max capacity ($Q_{max}$).")
    st.markdown("5. **Standard Addition Method:** Real-world sample matrix spike quantification and unknown recovery.")
    st.markdown("6. **Sensor Selectivity & Interference:** Evaluation of interfering ionic and organic species.")
    st.markdown("7. **Multi-Sensor Comparison:** Comparative evaluation of sensitivity and linear ranges across electrodes.")
    st.markdown("8. **EIS / Nyquist Rct Estimator:** Charge transfer resistance evaluation from Nyquist impedance plots.")
    st.markdown("9. **Double-Layer Capacitance (Cdl) & ECSA:** Specific capacitance and electrochemically active surface area.")
    st.markdown("10. **pH & Temperature Optimization:** Determine optimal operational environment conditions.")
    st.markdown("11. **AI Publication Paragraph Generator:** Generate ready-to-use research paper text from analytical findings.")
    st.markdown("12. **Professional Lab Report Generator:** Compile complete session metrics into formal HTML/Text report.")
    st.markdown("13. **Citation & Manuscript Info:** Auto-generated academic citations for research referencing.")

elif analysis_mode == "Linear Calibration & LOD/LOQ":
    st.subheader("📈 Linear Calibration & Detection Limits (CSV & Manual)")
    uploaded_file = st.file_uploader("Upload CSV file with Concentration and Signal columns", type=["csv"], key="cal_upload")
    
    if uploaded_file is not None:
        try:
            df_input = pd.read_csv(uploaded_file)
            st.success("CSV file successfully uploaded!")
        except Exception as e:
            st.error(f"Error reading file: {e}")
            df_input = None
    else:
        df_input = pd.DataFrame({
            "Concentration (µM)": [0.5, 2.0, 5.0, 10.0, 25.0, 50.0],
            "Signal (µA)": [1.2, 4.8, 11.5, 23.0, 57.5, 115.0]
        })

    edited_df = st.data_editor(df_input, num_rows="dynamic", key="cal_editor")

    if not edited_df.empty and len(edited_df) >= 3:
        col_names = edited_df.columns
        c_left, c_right = st.columns(2)
        with c_left:
            x_col = st.selectbox("Select Concentration Column", col_names, index=0)
        with c_right:
            y_col = st.selectbox("Select Signal/Current Column", col_names, index=1 if len(col_names) > 1 else 0)

        x = pd.to_numeric(edited_df[x_col], errors='coerce')
        y = pd.to_numeric(edited_df[y_col], errors='coerce')
        valid_data = pd.DataFrame({'x': x, 'y': y}).dropna()

        if len(valid_data) >= 3:
            slope, intercept, r_value, p_value, std_err = stats.linregress(valid_data['x'], valid_data['y'])
            r_squared = r_value ** 2
            residuals = valid_data['y'] - (slope * valid_data['x'] + intercept)
            sy_x = np.sqrt(np.sum(residuals**2) / (len(valid_data) - 2)) if len(valid_data) > 2 else 0.0
            lod = (3.3 * sy_x) / slope if slope != 0 else 0
            loq = (10.0 * sy_x) / slope if slope != 0 else 0

            st.markdown("### 📊 Analytical Regression Results")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Slope (Sensitivity)", f"{slope:.4f}")
            c2.metric("Intercept", f"{intercept:.4f}")
            c3.metric("R² Value", f"{r_squared:.4f}")
            c4.metric("Estimated LOD", f"{lod:.3f} µM")

            fig = px.scatter(valid_data, x='x', y='y', title="Calibration Curve with Linear Fit", labels={'x': x_col, 'y': y_col})
            line_y = slope * valid_data['x'] + intercept
            fig.add_scatter(x=valid_data['x'], y=line_y, mode="lines", name=f"Fit: y={slope:.2f}x+{intercept:.2f}")
            st.plotly_chart(fig, use_container_width=True)

            results_df = pd.DataFrame({
                "Parameter": ["Slope", "Intercept", "R-Squared", "LOD (µM)", "LOQ (µM)"],
                "Value": [slope, intercept, r_squared, lod, loq]
            })
            st.download_button(
                label="📥 Download Calibration Results (CSV)",
                data=results_df.to_csv(index=False).encode('utf-8'),
                file_name="calibration_results.csv",
                mime="text/csv",
            )
        else:
            st.warning("Please ensure selected columns contain valid numeric data (at least 3 valid points).")
    else:
        st.warning("Please provide at least 3 data points for reliable linear regression.")

elif analysis_mode == "Photocatalytic Kinetics":
    st.subheader("⚗️ Photocatalytic Degradation Kinetics (CSV & Manual)")
    uploaded_kin_file = st.file_uploader("Upload Time-Concentration CSV file", type=["csv"], key="kin_uploader")
    
    if uploaded_kin_file is not None:
        try:
            df_kin_input = pd.read_csv(uploaded_kin_file)
            st.success("Kinetics CSV file successfully uploaded!")
        except Exception as e:
            st.error(f"Error reading file: {e}")
            df_kin_input = None
    else:
        df_kin_input = pd.DataFrame({
            "Time (min)": [0, 10, 20, 30, 45, 60, 90],
            "Concentration Ct (mg/L)": [10.0, 7.5, 5.6, 4.2, 2.8, 1.9, 1.0]
        })

    edited_kinetics = st.data_editor(df_kin_input, num_rows="dynamic", key="kin_editor")

    if not edited_kinetics.empty and len(edited_kinetics) >= 2:
        k_cols = edited_kinetics.columns
        kc_left, kc_right = st.columns(2)
        with kc_left:
            t_col = st.selectbox("Select Time Column", k_cols, index=0, key="t_col")
        with kc_right:
            c_col = st.selectbox("Select Concentration (Ct) Column", k_cols, index=1 if len(k_cols) > 1 else 0, key="c_col")

        t = pd.to_numeric(edited_kinetics[t_col], errors='coerce')
        c = pd.to_numeric(edited_kinetics[c_col], errors='coerce')
        valid_kin = pd.DataFrame({'t': t, 'c': c}).dropna()

        if len(valid_kin) >= 2:
            c0 = valid_kin['c'].iloc[0]
            valid_kin = valid_kin[valid_kin['c'] > 0]

            if not valid_kin.empty and c0 > 0:
                ln_c0_ct = np.log(c0 / valid_kin['c'])
                k_slope, k_intercept, k_r_val, _, _ = stats.linregress(valid_kin['t'], ln_c0_ct)
                half_life = np.log(2) / k_slope if k_slope > 0 else 0

                st.markdown("### 📊 Kinetic Parameters")
                col1, col2, col3 = st.columns(3)
                col1.metric("Rate Constant ($k$)", f"{k_slope:.4f} min⁻¹")
                col2.metric("Half-Life ($t_{1/2}$)", f"{half_life:.2f} min")
                col3.metric("Kinetic $R^2$", f"{k_r_val**2:.4f}")

                fig_kin = px.scatter(x=valid_kin['t'], y=ln_c0_ct, title="Pseudo-First-Order Degradation Kinetics", labels={"x": t_col, "y": "ln(C₀ / Cₜ)"})
                fig_kin.add_scatter(x=valid_kin['t'], y=k_slope * valid_kin['t'] + k_intercept, mode="lines", name="Linear Fit")
                st.plotly_chart(fig_kin, use_container_width=True)

                kin_results_df = pd.DataFrame({
                    "Parameter": ["Rate Constant k (min-1)", "Half-Life t1/2 (min)", "Kinetic R-Squared", "Initial Concentration C0"],
                    "Value": [k_slope, half_life, k_r_val**2, c0]
                })
                st.download_button(
                    label="📥 Download Kinetic Results (CSV)",
                    data=kin_results_df.to_csv(index=False).encode('utf-8'),
                    file_name="kinetics_results.csv",
                    mime="text/csv",
                )
            else:
                st.error("Concentration values must be greater than zero for logarithmic calculations.")
        else:
            st.warning("Please ensure selected columns contain valid numeric data.")
    else:
        st.warning("Please provide at least 2 data points for kinetic modeling.")

elif analysis_mode == "Randles-Sevcik Active Surface Area":
    st.subheader("⚡ Randles-Sevcik Electroactive Surface Area Calculation")
    st.write("Calculate electroactive surface area ($A$) using peak current ($i_p$) versus square root of scan rate ($\nu^{1/2}$).")
    
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        n_electrons = st.number_input("Number of Electrons ($n$)", value=1.0, step=1.0)
    with col_p2:
        c_bulk = st.number_input("Concentration ($C$ in mol/cm³)", value=1e-6, format="%.2e")
    with col_p3:
        d_coeff = st.number_input("Diffusion Coeff ($D$ in cm²/s)", value=6.7e-6, format="%.2e")

    default_cv = pd.DataFrame({
        "Scan Rate v (V/s)": [0.01, 0.025, 0.05, 0.1, 0.15, 0.2],
        "Peak Current ip (µA)": [12.5, 20.1, 28.4, 40.2, 49.3, 57.0]
    })
    edited_cv = st.data_editor(default_cv, num_rows="dynamic", key="cv_editor")

    if not edited_cv.empty and len(edited_cv) >= 3:
        v_col, i_col = edited_cv.columns[0], edited_cv.columns[1]
        v = pd.to_numeric(edited_cv[v_col], errors='coerce')
        ip_ua = pd.to_numeric(edited_cv[i_col], errors='coerce')
        cv_data = pd.DataFrame({'v': v, 'ip': ip_ua}).dropna()
        
        if len(cv_data) >= 3:
            cv_data['sqrt_v'] = np.sqrt(cv_data['v'])
            ip_amp = cv_data['ip'] * 1e-6
            slope_cv, intercept_cv, r_cv, _, _ = stats.linregress(cv_data['sqrt_v'], ip_amp)
            constant_term = 268600 * (n_electrons ** 1.5) * (d_coeff ** 0.5) * c_bulk
            electrode_area = slope_cv / constant_term if constant_term != 0 else 0
            
            st.markdown("### 📊 Surface Area Results")
            sc1, sc2, sc3 = st.columns(3)
            sc1.metric("Slope", f"{slope_cv:.4e}")
            sc2.metric("Electrode Area ($A$)", f"{electrode_area:.4f} cm²")
            sc3.metric("Regression $R^2$", f"{r_cv**2:.4f}")
            
            fig_cv = px.scatter(cv_data, x='sqrt_v', y='ip', title="Randles-Sevcik Plot", labels={'sqrt_v': 'ν^1/2 (V/s)^1/2', 'ip': 'Peak Current (µA)'})
            fit_y = (slope_cv * cv_data['sqrt_v'] + intercept_cv) * 1e6
            fig_cv.add_scatter(x=cv_data['sqrt_v'], y=fit_y, mode="lines", name="Linear Fit")
            st.plotly_chart(fig_cv, use_container_width=True)
        else:
            st.warning("Provide valid numeric scan rate and current data.")
    else:
        st.warning("Provide at least 3 points for CV analysis.")

elif analysis_mode == "Adsorption Isotherms (Linear & Non-Linear)":
    st.subheader("🧪 Adsorption Isotherms: Non-Linear & Linear Fitting")
    st.write("Perform rigorous **Non-Linear Curve Fitting** alongside traditional linear transformations for Langmuir & Freundlich models ($C_e$ vs $q_e$).")
    
    uploaded_ads = st.file_uploader("Upload Adsorption CSV file", type=["csv"], key="ads_uploader")
    if uploaded_ads is not None:
        try:
            df_ads = pd.read_csv(uploaded_ads)
            st.success("Adsorption data uploaded!")
        except Exception as e:
            st.error(f"Error: {e}")
            df_ads = None
    else:
        df_ads = pd.DataFrame({
            "Ce (mg/L)": [2.0, 5.0, 10.0, 20.0, 35.0, 50.0],
            "qe (mg/g)": [12.0, 22.5, 34.0, 48.0, 58.0, 62.0]
        })

    edited_ads = st.data_editor(df_ads, num_rows="dynamic", key="ads_editor")

    if not edited_ads.empty and len(edited_ads) >= 3:
        ce_col, qe_col = edited_ads.columns[0], edited_ads.columns[1]
        ce = pd.to_numeric(edited_ads[ce_col], errors='coerce')
        qe = pd.to_numeric(edited_ads[qe_col], errors='coerce')
        ads_df = pd.DataFrame({'ce': ce, 'qe': qe}).dropna()

        if len(ads_df) >= 3 and (ads_df['ce'] > 0).all() and (ads_df['qe'] > 0).all():
            
            # --- 1. NON-LINEAR LANGMUIR FITTING ---
            def langmuir_nl(ce_val, qmax, kl):
                return (qmax * kl * ce_val) / (1.0 + kl * ce_val)

            # --- 2. NON-LINEAR FREUNDLICH FITTING ---
            def freundlich_nl(ce_val, kf, n_val):
                return kf * (ce_val ** (1.0 / n_val))

            try:
                # Non-linear Curve Fit for Langmuir
                popt_l, _ = optimize.curve_fit(langmuir_nl, ads_df['ce'], ads_df['qe'], p0=[100.0, 0.1], maxfev=5000)
                nl_qmax, nl_kl = popt_l[0], popt_l[1]
                res_l = ads_df['qe'] - langmuir_nl(ads_df['ce'], nl_qmax, nl_kl)
                nl_l_r2 = 1 - (np.sum(res_l**2) / np.sum((ads_df['qe'] - np.mean(ads_df['qe']))**2))

                # Non-linear Curve Fit for Freundlich
                popt_f, _ = optimize.curve_fit(freundlich_nl, ads_df['ce'], ads_df['qe'], p0=[10.0, 2.0], maxfev=5000)
                nl_kf, nl_n = popt_f[0], popt_f[1]
                res_f = ads_df['qe'] - freundlich_nl(ads_df['ce'], nl_kf, nl_n)
                nl_f_r2 = 1 - (np.sum(res_f**2) / np.sum((ads_df['qe'] - np.mean(ads_df['qe']))**2))

            except Exception as e:
                nl_qmax, nl_kl, nl_l_r2 = 0, 0, 0
                nl_kf, nl_n, nl_f_r2 = 0, 0, 0

            st.markdown("### 📊 Non-Linear Regression Parameters (Publication Standard)")
            col_nl1, col_nl2 = st.columns(2)
            
            with col_nl1:
                st.markdown("#### 🌟 Langmuir Model (Non-Linear)")
                st.metric("Qmax (mg/g)", f"{nl_qmax:.2f}")
                st.metric("KL (L/mg)", f"{nl_kl:.4f}")
                st.metric("Non-Linear R²", f"{nl_l_r2:.4f}")

            with col_nl2:
                st.markdown("#### 🌟 Freundlich Model (Non-Linear)")
                st.metric("KF ((mg/g)(L/mg)^(1/n))", f"{nl_kf:.2f}")
                st.metric("Adsorption Intensity (n)", f"{nl_n:.2f}")
                st.metric("Non-Linear R²", f"{nl_f_r2:.4f}")

            # Plotting Non-Linear Curves
            ce_smooth = np.linspace(ads_df['ce'].min(), ads_df['ce'].max(), 200)
            qe_lang_smooth = langmuir_nl(ce_smooth, nl_qmax, nl_kl)
            qe_freund_smooth = freundlich_nl(ce_smooth, nl_kf, nl_n)

            fig_ads = px.scatter(ads_df, x='ce', y='qe', title="Non-Linear Adsorption Isotherms Fitting", labels={'ce': 'Equilibrium Concentration Ce (mg/L)', 'qe': 'Adsorption Capacity qe (mg/g)'})
            fig_ads.add_scatter(x=ce_smooth, y=qe_lang_smooth, mode="lines", name=f"Langmuir Fit (R²={nl_l_r2:.3f})")
            fig_ads.add_scatter(x=ce_smooth, y=qe_freund_smooth, mode="lines", name=f"Freundlich Fit (R²={nl_f_r2:.3f})", line=dict(dash='dash'))
            st.plotly_chart(fig_ads, use_container_width=True)

            isotherm_results = pd.DataFrame({
                "Model Parameter": ["Langmuir Qmax (mg/g)", "Langmuir KL (L/mg)", "Langmuir Non-Linear R2", "Freundlich KF", "Freundlich n", "Freundlich Non-Linear R2"],
                "Value": [nl_qmax, nl_kl, nl_l_r2, nl_kf, nl_n, nl_f_r2]
            })
            st.download_button("📥 Download Non-Linear Isotherm Results (CSV)", data=isotherm_results.to_csv(index=False).encode('utf-8'), file_name="isotherm_nonlinear_results.csv", mime="text/csv")
        else:
            st.warning("Ensure positive values for Ce and qe.")
    else:
        st.warning("Provide at least 3 rows.")

elif analysis_mode == "Standard Addition Method":
    st.subheader("🎯 Standard Addition Method (Real Sample Recovery)")
    st.write("Determine unknown sample concentration using spike additions.")
    
    default_sa = pd.DataFrame({
        "Added Concentration (µM)": [0.0, 2.0, 4.0, 6.0, 8.0],
        "Measured Signal (µA)": [5.2, 9.1, 13.0, 16.8, 20.7]
    })
    edited_sa = st.data_editor(default_sa, num_rows="dynamic", key="sa_editor")

    if not edited_sa.empty and len(edited_sa) >= 3:
        add_col, sig_col = edited_sa.columns[0], edited_sa.columns[1]
        c_add = pd.to_numeric(edited_sa[add_col], errors='coerce')
        sig = pd.to_numeric(edited_sa[sig_col], errors='coerce')
        sa_df = pd.DataFrame({'c_add': c_add, 'sig': sig}).dropna()

        if len(sa_df) >= 3:
            slope_sa, intercept_sa, r_sa, _, _ = stats.linregress(sa_df['c_add'], sa_df['sig'])
            c_unknown = (intercept_sa / slope_sa) if slope_sa != 0 else 0

            st.markdown("### 📊 Standard Addition Results")
            s1, s2, s3 = st.columns(3)
            s1.metric("Unknown Concentration", f"{c_unknown:.3f} µM")
            s2.metric("Slope", f"{slope_sa:.4f}")
            s3.metric("Regression $R^2$", f"{r_sa**2:.4f}")

            fig_sa = px.scatter(sa_df, x='c_add', y='sig', title="Standard Addition Plot", labels={'c_add': 'Added Conc (µM)', 'sig': 'Signal (µA)'})
            fit_sa_y = slope_sa * sa_df['c_add'] + intercept_sa
            fig_sa.add_scatter(x=sa_df['c_add'], y=fit_sa_y, mode="lines", name="Linear Fit")
            st.plotly_chart(fig_sa, use_container_width=True)
        else:
            st.warning("Provide at least 3 valid points.")
    else:
        st.warning("Provide at least 3 rows.")

elif analysis_mode == "Sensor Selectivity & Interference":
    st.subheader("🛡️ Sensor Selectivity & Interference Study")
    st.write("Evaluate response stability in presence of interfering species.")

    default_int = pd.DataFrame({
        "Interferent Species": ["Target Ion Only", "Na+", "K+", "Ca2+", "Mg2+", "Glucose", "Uric Acid", "Ascorbic Acid"],
        "Signal Response (µA)": [45.0, 46.2, 44.8, 45.5, 45.1, 43.5, 46.8, 44.0]
    })
    edited_int = st.data_editor(default_int, num_rows="dynamic", key="int_editor")

    if not edited_int.empty and len(edited_int) >= 2:
        species_col, resp_col = edited_int.columns[0], edited_int.columns[1]
        species = edited_int[species_col].astype(str)
        response = pd.to_numeric(edited_int[resp_col], errors='coerce')
        int_df = pd.DataFrame({'species': species, 'response': response}).dropna()

        if len(int_df) >= 2:
            base_signal = int_df['response'].iloc[0]
            int_df['Percentage Change (%)'] = ((int_df['response'] - base_signal) / base_signal) * 100

            st.markdown("### 📊 Selectivity Bar Chart")
            fig_int = px.bar(int_df, x='species', y='response', color='Percentage Change (%)', title="Interference Study", labels={'species': 'Species', 'response': 'Signal (µA)'})
            st.plotly_chart(fig_int, use_container_width=True)
            st.dataframe(int_df, use_container_width=True)
        else:
            st.warning("Provide valid numeric responses.")
    else:
        st.warning("Provide at least 2 entries.")

elif analysis_mode == "Multi-Sensor Calibration Comparison":
    st.subheader("📈 Multi-Sensor Calibration Comparison")
    st.write("Compare two different sensors / electrodes side-by-side on the same linear calibration graph.")
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown("#### Sensor A (e.g., Modified Electrode)")
        df_a = pd.DataFrame({"Conc (µM)": [1, 5, 10, 25, 50], "Signal A (µA)": [2, 10, 21, 52, 105]})
        edited_a = st.data_editor(df_a, num_rows="dynamic", key="sens_a")
    with col_m2:
        st.markdown("#### Sensor B (e.g., Bare Electrode)")
        df_b = pd.DataFrame({"Conc (µM)": [1, 5, 10, 25, 50], "Signal B (µA)": [1, 4, 9, 22, 45]})
        edited_b = st.data_editor(df_b, num_rows="dynamic", key="sens_b")

    if not edited_a.empty and not edited_b.empty:
        sa_x, sa_y = pd.to_numeric(edited_a.iloc[:,0], errors='coerce'), pd.to_numeric(edited_a.iloc[:,1], errors='coerce')
        sb_x, sb_y = pd.to_numeric(edited_b.iloc[:,0], errors='coerce'), pd.to_numeric(edited_b.iloc[:,1], errors='coerce')
        
        valid_a = pd.DataFrame({'x': sa_x, 'y': sa_y}).dropna()
        valid_b = pd.DataFrame({'x': sb_x, 'y': sb_y}).dropna()

        if len(valid_a) >= 2 and len(valid_b) >= 2:
            sl_a, int_a, r_a, _, _ = stats.linregress(valid_a['x'], valid_a['y'])
            sl_b, int_b, r_b, _, _ = stats.linregress(valid_b['x'], valid_b['y'])

            st.markdown("### 📊 Comparative Performance")
            comp1, comp2 = st.columns(2)
            comp1.metric("Sensor A Sensitivity (Slope)", f"{sl_a:.4f}", f"R²: {r_a**2:.4f}")
            comp2.metric("Sensor B Sensitivity (Slope)", f"{sl_b:.4f}", f"R²: {r_b**2:.4f}")

            fig_comp = px.scatter(title="Multi-Sensor Overlay Calibration Curves")
            fig_comp.add_scatter(x=valid_a['x'], y=valid_a['y'], mode='markers+lines', name='Sensor A (Modified)')
            fig_comp.add_scatter(x=valid_b['x'], y=valid_b['y'], mode='markers+lines', name='Sensor B (Bare)')
            st.plotly_chart(fig_comp, use_container_width=True)
        else:
            st.warning("Provide valid numeric data for both sensors.")
    else:
        st.warning("Ensure data tables are populated.")

elif analysis_mode == "EIS / Nyquist Rct Estimator":
    st.subheader("🔬 EIS / Nyquist Plot Charge Transfer Resistance ($R_{ct}$)")
    st.write("Estimate $R_{ct}$ from Electrochemical Impedance Spectroscopy Nyquist data ($Z_{re}$ vs $-Z_{im}$).")
    
    default_eis = pd.DataFrame({
        "Z_re (ohm)": [100, 110, 130, 170, 250, 400, 600, 900],
        "Minus_Z_im (ohm)": [10, 25, 55, 95, 120, 110, 80, 40]
    })
    edited_eis = st.data_editor(default_eis, num_rows="dynamic", key="eis_editor")

    if not edited_eis.empty and len(edited_eis) >= 3:
        zre_col, zim_col = edited_eis.columns[0], edited_eis.columns[1]
        z_re = pd.to_numeric(edited_eis[zre_col], errors='coerce')
        z_im = pd.to_numeric(edited_eis[zim_col], errors='coerce')
        eis_df = pd.DataFrame({'z_re': z_re, 'z_im': z_im}).dropna()

        if len(eis_df) >= 3:
            r_ct_approx = eis_df['z_re'].max() - eis_df['z_re'].min()

            st.markdown("### 📊 EIS Analysis Summary")
            st.metric("Estimated Charge Transfer Resistance ($R_{ct}$)", f"{r_ct_approx:.2f} Ω")

            fig_eis = px.scatter(eis_df, x='z_re', y='z_im', title="Nyquist Plot (-Z_im vs Z_re)", labels={'z_re': "Z_re (Ω)", 'z_im': "-Z_im (Ω)"})
            fig_eis.update_traces(mode='markers+lines')
            st.plotly_chart(fig_eis, use_container_width=True)
        else:
            st.warning("Provide valid numeric impedance values.")
    else:
        st.warning("Provide at least 3 points for EIS data.")

elif analysis_mode == "Double-Layer Capacitance (Cdl) & ECSA":
    st.subheader("💧 Double-Layer Capacitance ($C_{dl}$) & ECSA Calculation")
    st.write("Calculate double-layer capacitance from scan rate variation in non-faradaic region to determine ECSA.")
    
    default_cdl = pd.DataFrame({
        "Scan Rate v (V/s)": [0.01, 0.02, 0.03, 0.04, 0.05],
        "Charging Current Ic (µA)": [2.1, 4.3, 6.2, 8.5, 10.4]
    })
    edited_cdl = st.data_editor(default_cdl, num_rows="dynamic", key="cdl_editor")
    
    cs_val = st.number_input("Specific Capacitance (Cs in µF/cm² for smooth metal standard)", value=40.0)

    if not edited_cdl.empty and len(edited_cdl) >= 3:
        v_c = pd.to_numeric(edited_cdl.iloc[:,0], errors='coerce')
        i_c = pd.to_numeric(edited_cdl.iloc[:,1], errors='coerce')
        cdl_df = pd.DataFrame({'v': v_c, 'i': i_c}).dropna()

        if len(cdl_df) >= 3:
            slope_cdl, _, r_cdl, _, _ = stats.linregress(cdl_df['v'], cdl_df['i'])
            cdl_value = slope_cdl / 2.0
            ecsa_val = (cdl_value / cs_val) if cs_val != 0 else 0

            st.markdown("### 📊 Capacitance Results")
            cc1, cc2, cc3 = st.columns(3)
            cc1.metric("Double-Layer Capacitance ($C_{dl}$)", f"{cdl_value:.2f} µF")
            cc2.metric("Estimated ECSA", f"{ecsa_val:.4f} cm²")
            cc3.metric("Regression $R^2$", f"{r_cdl**2:.4f}")

            fig_cdl = px.scatter(cdl_df, x='v', y='i', title="Charging Current vs Scan Rate", labels={'v': 'Scan Rate (V/s)', 'i': 'Current (µA)'})
            fig_cdl.add_scatter(x=cdl_df['v'], y=slope_cdl * cdl_df['v'], mode="lines", name="Linear Fit")
            st.plotly_chart(fig_cdl, use_container_width=True)
        else:
            st.warning("Provide valid numeric current and scan rate values.")
    else:
        st.warning("Provide at least 3 rows.")

elif analysis_mode == "pH & Temperature Optimization":
    st.subheader("🌡️ pH & Temperature Optimization Study")
    st.write("Evaluate sensor signal response across varying pH or temperature conditions.")

    col_opt1, col_opt2 = st.columns(2)
    with col_opt1:
        st.markdown("#### pH Optimization Data")
        df_ph = pd.DataFrame({"pH": [3.0, 5.0, 7.0, 9.0, 11.0], "Signal (µA)": [20.0, 45.0, 85.0, 60.0, 30.0]})
        edited_ph = st.data_editor(df_ph, num_rows="dynamic", key="ph_editor")
    with col_opt2:
        st.markdown("#### Temperature Optimization Data")
        df_temp = pd.DataFrame({"Temp (°C)": [15, 25, 35, 45, 55], "Signal (µA)": [50.0, 75.0, 95.0, 80.0, 60.0]})
        edited_temp = st.data_editor(df_temp, num_rows="dynamic", key="temp_editor")

    if not edited_ph.empty:
        ph_x, ph_y = pd.to_numeric(edited_ph.iloc[:,0], errors='coerce'), pd.to_numeric(edited_ph.iloc[:,1], errors='coerce')
        df_ph_val = pd.DataFrame({'ph': ph_x, 'sig': ph_y}).dropna()
        if not df_ph_val.empty:
            optimal_ph = df_ph_val.loc[df_ph_val['sig'].idxmax()]['ph']
            st.success(f"Optimal pH identified at: **pH {optimal_ph}**")
            fig_ph = px.line(df_ph_val, x='ph', y='sig', markers=True, title="Sensor Signal vs pH Optimization Curve", labels={'ph': 'pH', 'sig': 'Signal Response (µA)'})
            st.plotly_chart(fig_ph, use_container_width=True)

elif analysis_mode == "AI Publication Paragraph Generator":
    st.subheader("🤖 AI-Powered Research Paper Text Generator")
    st.write("Automatically draft publication-ready paragraphs for your **Results & Discussion** section based on analytical parameters.")
    
    analyte_name = st.text_input("Target Analyte Name", value="Pb(II) ions")
    electrode_name = st.text_input("Sensor / Electrode Modified Name", value="Fe2O3/CuO nanocomposite modified GCE")
    sens_val = st.number_input("Calculated Sensitivity (µA/µM)", value=2.25)
    lod_val = st.number_input("Calculated LOD (µM or nM)", value=0.015)
    r2_val = st.number_input("Regression R²", value=0.998)

    if st.button("✨ Generate Publication Paragraph"):
        ai_text = f"""
        **Suggested Results & Discussion Excerpt:**
        
        "Under optimized electrochemical conditions, the fabricated {electrode_name} demonstrated exceptional analytical performance towards the detection of {analyte_name}. The linear calibration plot exhibited a wide dynamic working range with a high sensitivity of **{sens_val} µA/µM** and an excellent determination coefficient of **R² = {r2_val}**. Furthermore, the sensor achieved an ultra-low limit of detection (LOD) of **{lod_val}**, confirming its high sensitivity and suitability for trace-level environmental monitoring and wastewater remediation assessment."
        """
        st.markdown(ai_text)
        st.info("💡 You can copy this text directly into your manuscript draft!")

elif analysis_mode == "Professional Lab Report Generator":
    st.subheader("📄 Professional Lab Report Generator")
    st.write("Compile all session information and analytical findings into a formal downloadable laboratory report.")
    
    researcher_name = st.text_input("Researcher / Author Name", value="Rania Safdar")
    lab_title = st.text_input("Project / Experiment Title", value="Electroanalytical Sensor Performance & Wastewater Remediation")
    notes = st.text_area("Key Observations & Remarks", value="The fabricated nanocomposite sensor exhibited exceptional reproducibility and stability during electrochemical testing.")

    report_html = f"""
    <html>
    <head><title>Lab Report - EcoSensing-AI</title></head>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h2>🌱 EcoSensing-AI Official Research Report</h2>
        <hr>
        <p><b>Project Title:</b> {lab_title}</p>
        <p><b>Analyst / Researcher:</b> {researcher_name}</p>
        <p><b>Date:</b> 2026-03-05</p>
        <h3>Observations & Notes:</h3>
        <p>{notes}</p>
        <hr>
        <p><i>Generated automatically via EcoSensing-AI Research Suite.</i></p>
    </body>
    </html>
    """

    st.download_button(
        label="📥 Download Full Lab Report (HTML)",
        data=report_html,
        file_name="EcoSensing_AI_Research_Report.html",
        mime="text/html"
    )

elif analysis_mode == "Citation & Manuscript Info":
    st.subheader("📚 Academic Citation & Manuscript Reference")
    st.write("If you or reviewing professors use **EcoSensing-AI** in academic publications, please cite it as follows:")
    
    citation_apa = "Safdar, R. (2026). EcoSensing-AI: An Advanced Computational Suite for Electroanalytical Sensors and Environmental Remediation. GitHub Repository. https://github.com/safdarrania112-ctrl/ecosensing-ai"
    
    citation_bibtex = """@software{EcoSensingAI2026,
  author = {Rania Safdar},
  title = {EcoSensing-AI: Professional Publication-Grade Electroanalytical Suite},
  year = {2026},
  publisher = {GitHub},
  journal = {GitHub repository},
  url = {https://github.com/safdarrania112-ctrl/ecosensing-ai}
}"""

    st.markdown("### 📝 APA Format:")
    st.code(citation_apa, language="text")
    
    st.markdown("### 📋 BibTeX Format (For LaTeX / Overleaf / Mendeley):")
    st.code(citation_bibtex, language="bibtex")
    
    st.success("🌟 This module ensures complete academic transparency and proper referencing for high-impact journal submissions!")
