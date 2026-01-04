import streamlit as st
import math
import requests
import numpy as np
import pandas as pd
import altair as alt 

st.set_page_config(page_title="Smart X-ray Calculator", layout="centered")
st.title("Smart X-ray Exposure Calculator")
st.markdown("RT & Operando X-ray Exposure Time Optimizer")
st.caption("Containerized application running on Linux Server")
st.divider()
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Source Info")
    activity = st.number_input("Activity (Ci)", value=50.0, step=1.0)
    source_coeff = st.number_input("RHM Value", value=1.3, step=0.1, help="Co-60=1.3, Ir-192=0.48")
    mu = st.number_input("Attenuation Coeff (mu)", value=0.5, step=0.01)

    with col2:
        st.subheader("2. Geometry")
        thickness_mm = st.number_input("Thickness (mm)", value=10.0, step=1.0)
        distance_cm = st.number_input("SFD (Source-Film Dist) (cm)", value=100.0, step=10.0)
        target_dose = st.number_input("Target Dose (r)", value=2.0, step=0.1)

        def format_seconds(s):
            if s == float('inf') or s > 1e12:
                return "impossible"
            if s < 1:
                return f"{s:.3f} seconds"
            sec = int(round(s))
            h = sec // 3600
            m = (sec % 3600) // 60
            sec = sec % 60
            parts = []
            if h: parts.append(f"{h}hours")
            if m: parts.append(f"{m}mins")
            parts.append(f"{sec}sec")
            return " ".join(parts)

        def calculate_exposure(activity, source_coeff, mu, thickness_mm, distance_cm, target_dose):
            thickness_cm = thickness_mm / 10.0
            transmitted = activity * source_coeff * math.exp(-mu * thickness_cm)
            dose_rate = 0.0
            if distance_cm > 0:
                dose_rate = transmitted / (distance_cm * distance_cm)
                time_sec = float('inf') if dose_rate <= 0 else target_dose / dose_rate
                return time_sec, dose_rate
        

if st.button("Calculate Time", type="primary"):
    time_sec, dose_rate = calculate_exposure(
        activity, source_coeff, mu, thickness_mm, distance_cm, target_dose

    )

    st.divider()
    if time_sec == float('inf'):
        st.error("Error: Dose rate is zero.")
    else:
        st.success(f"Optimal Time: **{format_seconds(time_sec)}**")
        st.info(f"Dose Rate: {dose_rate:.4f} R/h")
