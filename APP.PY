import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.signal import find_peaks

# Page Configuration
st.set_page_config(
    page_title="EcoSensing-AI | Interfacial Electrochemistry & Oxidation Forensics",
    page_icon="🧪",
    layout="wide"
)

# Custom Styling
st.markdown("""
    <style>
    .main-header { font-size: 2.2rem; font-weight: 700; color: #1e3a8a; }
    .sub-header { font-size: 1.1rem; color: #475569; margin-bottom: 20px; }
    .card { background-color: #f8fafc; padding: 20px; border-radius: 10px; border: 1px solid #e2e8f0; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🧪 EcoSensing-AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Cyber-Laboratory for Interfacial Electrochemistry & Advanced Oxidation Forensics</div>', unsafe_allow_html=True)

# Tabs Navigation
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 CV Processor", 
    "🤖 Kinetic Optimizer", 
    "☀️ Photo-Fenton Engine", 
    "🧪 Forensic Toxicity", 
    "📄 Researcher Portfolio"
])

# ---------------------------------------------------------
# TAB 1: Voltammetry Data Processor
# ---------------------------------------------------------
with tab1:
    st.header("📊 Automated Voltammetry Data Processor")
    st.write("Upload raw CV/DPV CSV files to detect redox peaks and compute Electroactive Surface Area (EASA).")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Experimental Parameters")
        uploaded_file = st.file_uploader("Upload Instrument Data (.csv)", type=["csv"])
        n = st.number_input("Electrons Transferred (n)", min_value=1, value=1)
        C = st.number_input("Concentration (C) [mol/cm³]", value=5.0e-6, format="%.2e")
        D = st.number_input("Diffusion Coeff (D) [cm²/s]", value=6.7e-6, format="%.2e")
        v = st.number_input("Scan Rate (ν) [V/s]", value=0.10)
        bare_area = st.number_input("Bare GCE Area [cm²]", value=0.0707)
        
    with col2:
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.success("File Uploaded Successfully!")
        else:
            st.info("💡 Generating simulated Ferri/Ferrocyanide CV data for demonstration...")
            pot = np.linspace(-0.2, 0.6, 500)
            curr = 15 * np.sin(pot * 10) + np.random.normal(0, 0.5, 500)
            df = pd.DataFrame({"Potential (V)": pot, "Current (uA)": curr})
        
        # Peak Detection
        current_vals = df.iloc[:, 1].values
        peaks_pos, _ = find_peaks(current_vals, height=0)
        peaks_neg, _ = find_peaks(-current_vals, height=0)
        
        Ipa = np.max(current_vals) if len(peaks_pos) == 0 else current_vals[peaks_pos[0]]
        Ipc = np.min(current_vals) if len(peaks_neg) == 0 else current_vals[peaks_neg[0]]
        
        Ipa_A = abs(Ipa) * 1e-6
        area = Ipa_A / (2.69e5 * (n**1.5) * np.sqrt(D) * C * np.sqrt(v))
        enhancement = ((area - bare_area) / bare_area) * 100
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.iloc[:, 0], y=df.iloc[:, 1], mode='lines', name='CV Curve', line=dict(color='#2563eb')))
        fig.add_trace(go.Scatter(x=[df.iloc[peaks_pos[0], 0] if len(peaks_pos)>0 else 0.2], y=[Ipa], mode='markers', marker=dict(size=12, color='red'), name='Ipa (Anodic Peak)'))
        fig.add_trace(go.Scatter(x=[df.iloc[peaks_neg[0], 0] if len(peaks_neg)>0 else 0.0], y=[Ipc], mode='markers', marker=dict(size=12, color='green'), name='Ipc (Cathodic Peak)'))
        fig.update_layout(title="Voltammetric Response Curve", xaxis_title="Potential (V)", yaxis_title="Current (μA)")
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(f"""
        <div class="card">
            <h4>📈 Analytical Results Summary</h4>
            <p><b>Anodic Peak Current (Ipa):</b> {Ipa:.2f} μA</p>
            <p><b>Cathodic Peak Current (Ipc):</b> {Ipc:.2f} μA</p>
            <p><b>Calculated Active Surface Area (A):</b> <b>{area:.4f} cm²</b></p>
            <p><b>Surface Area Enhancement:</b> <span style="color:green; font-weight:bold;">+{enhancement:.2f}%</span> over Bare GCE</p>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 2: Kinetic Optimizer
# ---------------------------------------------------------
with tab2:
    st.header("🤖 AI-Driven Photocatalytic & Fenton Kinetic Optimizer")
    st.write("Predict optimized operational matrix using Pseudo-First-Order Kinetics.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        pollutant = st.selectbox("Target Pollutant", ["Methylene Blue (MB)", "Rhodamine B (RhB)", "Ciprofloxacin (CIP)", "Lead/Cadmium Complex"])
        target_eff = st.slider("Target Efficiency (%)", 50.0, 99.9, 95.0)
        target_time = st.slider("Target Treatment Time (min)", 10, 180, 45)
        
    with col2:
        fraction = 1 - (target_eff / 100.0)
        k_req = -np.log(fraction) / target_time
        
        fe2o3_ratio = 70 if target_eff > 90 else 60
        cuo_ratio = 100 - fe2o3_ratio
        cat_dose = 0.25 + (target_eff / 200.0)
        h2o2_conc = 5.0 + (target_eff / 20.0)
        
        st.markdown(f"""
        <div class="card">
            <h3>🔬 Optimized Operational Recipe Matrix</h3>
            <hr>
            <p><b>Required Degradation Rate Constant (k):</b> <code>{k_req:.4f} min⁻¹</code></p>
            <p><b>Nanocomposite Catalyst Ratio:</b> Fe₂O₃ ({fe2o3_ratio}%) : CuO ({cuo_ratio}%)</p>
            <p><b>Optimal Fenton Sweet Spot pH:</b> <span style="color: #d97706; font-weight:bold;">3.0 ± 0.2</span> (Prevents Fe³⁺ Precipitation)</p>
            <p><b>Recommended Catalyst Load:</b> {cat_dose:.2f} g/L</p>
            <p><b>Required H₂O₂ Concentration:</b> {h2o2_conc:.1f} mM (Scavenging Inhibited)</p>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 3: Dark vs. Photo-Fenton Engine
# ---------------------------------------------------------
with tab3:
    st.header("☀️ Comparative Kinetic Engine (Dark vs. Photo-Fenton)")
    
    c1, c2, c3 = st.columns(3)
    with c1: C0 = st.slider("Initial Conc (C₀) [mg/L]", 10, 100, 50)
    with c2: time_max = st.slider("Max Time (min)", 10, 120, 60)
    with c3: light_intensity = st.slider("Solar Intensity (W/m²)", 100, 1000, 500)
    
    t_vals = np.linspace(0, time_max, 100)
    k_dark = 0.015
    k_photo = k_dark + (light_intensity / 10000.0) + 0.04
    
    C_dark = C0 * np.exp(-k_dark * t_vals)
    C_photo = C0 * np.exp(-k_photo * t_vals)
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=t_vals, y=C_dark/C0, mode='lines', name='Dark Fenton (Slow Fe²⁺/Fe³⁺ Cycle)', line=dict(color='#475569', dash='dash')))
    fig2.add_trace(go.Scatter(x=t_vals, y=C_photo/C0, mode='lines', name='Photo-Fenton (Light Accelerated)', line=dict(color='#ea580c', width=3)))
    fig2.update_layout(title="Normalized Concentration Decay (C_t / C_0)", xaxis_title="Time (min)", yaxis_title="C_t / C_0")
    
    st.plotly_chart(fig2, use_container_width=True)
    
    ratio = k_photo / k_dark
    st.info(f"⚡ **Photocatalytic Acceleration Factor:** Light irradiation increases the degradation efficiency by **{ratio:.2f}x** compared to dark conditions.")

# ---------------------------------------------------------
# TAB 4: Forensic Toxicity Tracker
# ---------------------------------------------------------
with tab4:
    st.header("🧪 Digitized Forensic Toxicity Tracker & Router")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Analytical LOD/LOQ Calculator")
        sigma = st.number_input("Blank Std Dev (σ)", value=0.0012, format="%.4f")
        slope = st.number_input("Calibration Slope (S)", value=0.0450, format="%.4f")
        
        lod = (3 * sigma) / slope
        loq = (10 * sigma) / slope
        st.write(f"**Limit of Detection (LOD):** `{lod:.4f} ppm` | **Limit of Quantification (LOQ):** `{loq:.4f} ppm`")
        
        st.subheader("Sample Heavy Metal Quantitation")
        pb = st.slider("Lead (Pb²⁺) [mg/L]", 0.00, 0.10, 0.03, step=0.005)
        cd = st.slider("Cadmium (Cd²⁺) [mg/L]", 0.00, 0.05, 0.002, step=0.001)
        hg = st.slider("Mercury (Hg²⁺) [mg/L]", 0.00, 0.02, 0.008, step=0.001)
        
    with col2:
        st.subheader("WHO Compliance & Remediation Status")
        
        def get_status(val, limit):
            return "🔴 CRITICAL EXCEEDANCE" if val > limit else "🟢 SAFE (WHO Compliant)"
            
        data = {
            "Heavy Metal": ["Lead (Pb²⁺)", "Cadmium (Cd²⁺)", "Mercury (Hg²⁺)"],
            "Detected Level (mg/L)": [pb, cd, hg],
            "WHO Threshold (mg/L)": [0.010, 0.003, 0.006],
            "Status": [get_status(pb, 0.010), get_status(cd, 0.003), get_status(hg, 0.006)]
        }
        st.table(pd.DataFrame(data))
        
        if pb > 0.010 or cd > 0.003 or hg > 0.006:
            st.warning("⚠️ **Remediation Router Suggestion:** Safe drinking standards exceeded! Recommended Filter Matrix: **Thiol-Functionalized CuO/Fe₂O₃ Photo-Fenton Nanocomposite Membrane** for targeted heavy metal chelation and radical oxidation.")

# ---------------------------------------------------------
# TAB 5: Researcher Portfolio
# ---------------------------------------------------------
with tab5:
    st.header("📄 Researcher Profile & Academic Credentials")
    
    st.markdown("""
    <div class="card">
        <h2>Rania Safdar</h2>
        <p><b>Academic Background:</b> BS Chemistry (CGPA: 3.32 / 4.00)</p>
        <p><b>Institution:</b> Thal University Bhakkar (formerly Sub-Campus, University of Sargodha)</p>
        <p><b>Specialization:</b> Analytical Chemistry, Electrochemistry, Photocatalysis & Sensor Technology</p>
        <hr>
        <h4>📜 Key Peer-Reviewed Publications</h4>
        <ul>
            <li><b>The Role of Iron in Advanced Oxidation Technologies: A Review of Applications in Wastewater Remediation</b> — <i>Indus Journal of Bioscience Research</i> (2025).</li>
        </ul>
        <h4>✍️ Ongoing Research Manuscripts</h4>
        <ul>
            <li><b>Biomass-Derived Carbon-Based Nanomaterials for Electrochemical Detection of Pb(II) and Cd(II): Recent Advances, Machine Learning-Assisted Signal Processing, and Future Perspectives</b> (Under Preparation).</li>
            <li><b>Cerium/Calcium Oxide Nanozymes in Advanced Oxidation Processes</b> (Under Preparation).</li>
        </ul>
        <hr>
        <p><b>Core Analytical Expertise:</b> XRD Phase Analysis (Jade), UV-Vis, FTIR, Cyclic Voltammetry (CV), DPV, Zeta Potential Analysis, and Green Synthesis of Metal Oxide Nanoparticles.</p>
    </div>
    """, unsafe_allow_html=True)