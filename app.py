import streamlit as st
import math
import requests
import logging

# Configure logging format
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def log_visitor():
    if 'logged' not in st.session_state:
        h = st.context.headers
        
        # Log basic visitor metrics
        logging.info(f" [V] {h.get('Accept-Language')} | {h.get('User-Agent')}")
        st.session_state.logged = True

# Execute visitor logging
log_visitor()
                
                

def format_seconds(seconds):
    if seconds == float('inf'): return "Infinite"
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h}h {m}m {s}s" if h > 0 else f"{m}m {s}s"

def calculate_exposure(activity, source_coeff, mu, thickness_mm, distance_cm, target_dose):
    thickness_cm = thickness_mm / 10.0
    # Apply attenuation formula
    transmitted = activity * source_coeff * math.exp(-mu * thickness_cm)
    dose_rate = 0.0
    if distance_cm > 0:
        # Calculate dose rate using Inverse Square Law
        dose_rate = transmitted / ((distance_cm / 100) ** 2) 
        time_sec = (target_dose / dose_rate) * 3600 if dose_rate > 0 else float('inf')
        return time_sec, dose_rate
    return 0, 0

def calculate_xray_exposure(ma, kv, thickness, sfd, target_dose):  
    
    if kv <= 0 or sfd <= 0:
        return 0, 0
    k_constant = 0.5 # X-ray generation efficiency constant
    mu_eff = 2.0 / (kv ** 0.5) # Effective attenuation coefficient
    
    # Calculate initial dose rate based on tube parameters
    dose_rate = (k_constant * ma * (kv / 100)**2) / ((sfd / 100)**2)
    # Apply material attenuation
    final_dose_rate = dose_rate * math.exp(-mu_eff * thickness)
    if final_dose_rate > 0:
        time_hours = target_dose / final_dose_rate
        time_sec = time_hours * 3600
    else:
        time_sec = 0
    return time_sec, final_dose_rate
# Page configuration and main title
st.set_page_config(page_title="Smart X-ray Calculator", layout="centered")
st.title("Smart X-ray Exposure Calculator")
# Source selection: Isotope vs. X-ray generator
mode = st.radio("Select Source Type", ["Radioactive Isotope (Ci)", "X-ray Tube (mA)"], horizontal=True)
# Initialize calculation variables
activity, source_coeff, mu = 0.0, 0.0, 0.0
ma, kv, exp_factor, ref_distance = 0.0, 0.0, 0.0, 0.0

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Source Info")
    if mode == "Radioactive Isotope (Ci)":
        # Input parameters for Isotope source
        activity = st.number_input("Activity (Ci)", value=50.0, step=1.0)
        source_coeff = st.number_input("RHM Value", value=1.3, step=0.1)
        mu = st.number_input("Attenuation Coeff (mu)", value=0.5, step=0.01)
    else:
        # Input parameters for X-ray Tube generator
        ma = st.number_input("Tube Current (mA)", value=5.0, step=0.1)
        kv = st.number_input("Tube Voltage (kV)", value=200.0, step=10.0)
        exp_factor = st.number_input("Exposure Factor (E)", value=15.0)
        ref_distance = st.number_input("Reference Distance (cm)", value=60.0)

with col2:
    st.subheader("2. Geometry")
    # Distance and material thickness settings
    thickness_mm = st.number_input("Thickness (mm)", value=10.0, step=1.0)
    distance_cm = st.number_input("SFD (cm)", value=100.0, step=10.0)
    # Define required dosage for imaging
    target_dose = st.number_input("Target Dose (r)", value=2.0, step=0.1, key="target_dose_input")
    
    # Trigger calculation logic
    if st.button("Calculate Time", type="primary"):
        if mode == "Radioactive Isotope (Ci)":
            time_sec, dose_rate = calculate_exposure(activity, source_coeff, mu, thickness_mm, distance_cm, target_dose)
        else:
            time_sec, dose_rate = calculate_xray_exposure(ma, kv, thickness_mm, distance_cm, target_dose)
    
        st.divider()
        # Display results or error handling
        if time_sec == float('inf') or time_sec == 0:
         st.error("Error: Dose rate is too low or zero.")
        else:
            st.success(f"Optimal Time: **{format_seconds(time_sec)}**")
        st.info(f"Dose Rate: {dose_rate:.4f} R/h")
