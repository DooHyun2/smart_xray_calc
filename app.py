import streamlit as st
import math
 
 
# ── Utility: unit conversion ──────────────────────────────────────────────────
 
def ci_to_bq_str(ci):
    """Return activity in SI units (MBq / GBq / TBq) alongside the Ci value."""
    bq = ci * 3.7e10  # 1 Ci = 3.7 × 10^10 Bq (definition)
    if bq >= 1e12:
        return f"{bq / 1e12:.2f} TBq"
    elif bq >= 1e9:
        return f"{bq / 1e9:.2f} GBq"
    else:
        return f"{bq / 1e6:.2f} MBq"
 
 
def format_seconds(seconds):
    """Convert total seconds to a human-readable h/m/s string."""
    if seconds == float('inf'):
        return "Infinite"
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h}h {m}m {s}s" if h > 0 else f"{m}m {s}s"
 
 
# ── Core calculation: radioactive isotope ─────────────────────────────────────
 
def calculate_isotope_exposure(activity_ci, rhm, mu, thickness_mm, distance_cm, target_dose_mgy):
    """
    Calculate exposure time for a radioactive isotope source.
 
    Parameters:
        activity_ci     : Source activity (Ci)
        rhm             : Roentgen per Hour at 1 Meter — R·m²/Ci·h
        mu              : Linear attenuation coefficient (cm⁻¹)
        thickness_mm    : Material thickness (mm)
        distance_cm     : Source-to-film distance, SFD (cm)
        target_dose_mgy : Required dose at detector (mGy)
 
    Returns:
        (time_sec, dose_rate_mgyh)
    """
    thickness_cm = thickness_mm / 10.0   # mm → cm for attenuation formula
    distance_m   = distance_cm  / 100.0  # cm → m for inverse square law
 
    if distance_m <= 0:
        return 0, 0
 
    # Inverse square law + exponential attenuation → dose rate in R/h
    dose_rate_rh = (activity_ci * rhm * math.exp(-mu * thickness_cm)) / (distance_m ** 2)
 
    # Convert R/h to mGy/h — SI standard (1 R = 8.77 mGy in air)
    dose_rate_mgyh = dose_rate_rh * 8.77
 
    # Time (s) = target dose / dose rate, converted from hours to seconds
    time_sec = (target_dose_mgy / dose_rate_mgyh) * 3600 if dose_rate_mgyh > 0 else float('inf')
 
    return time_sec, dose_rate_mgyh
 
 
# ── Core calculation: X-ray tube ──────────────────────────────────────────────
 
def calculate_xray_exposure(ma, output_factor, mu, thickness_mm, sfd_cm, target_dose_mgy):
    """
    Calculate exposure time for an X-ray tube source.
 
    Parameters:
        ma              : Tube current (mA)
        output_factor   : Machine output at given kV — mGy/mA·h at 1m
                          (obtain from equipment spec sheet or calibration data)
        mu              : Linear attenuation coefficient of test material (cm⁻¹)
        thickness_mm    : Material thickness (mm)
        sfd_cm          : Source-to-film distance, SFD (cm)
        target_dose_mgy : Required dose at detector (mGy)
 
    Returns:
        (time_sec, dose_rate_mgyh)
 
    Formula:
        dose_rate [mGy/h] = output_factor × mA / SFD[m]² × e^(−μ · t[cm])
    """
    thickness_cm = thickness_mm / 10.0  # mm → cm for attenuation
    sfd_m        = sfd_cm / 100.0       # cm → m for inverse square law
 
    if sfd_m <= 0 or output_factor <= 0:
        return 0, 0
 
    # Apply inverse square law and material attenuation
    dose_rate = (output_factor * ma / (sfd_m ** 2)) * math.exp(-mu * thickness_cm)
 
    time_sec = (target_dose_mgy / dose_rate) * 3600 if dose_rate > 0 else float('inf')
 
    return time_sec, dose_rate
 
 
# ── Page config ───────────────────────────────────────────────────────────────
 
st.set_page_config(page_title="Smart X-ray Calculator", layout="centered")
st.title("Smart X-ray Exposure Calculator")
 
# ── Source type selector ──────────────────────────────────────────────────────
 
# Let the user choose between a radioactive source and an X-ray tube
mode = st.radio(
    "Select Source Type",
    ["Radioactive Isotope (Ci)", "X-ray Tube (mA)"],
    horizontal=True
)
 
col1, col2 = st.columns(2)
 
# ── Column 1: source parameters (changes based on mode) ──────────────────────
 
with col1:
    st.subheader("1. Source Info")
 
    if mode == "Radioactive Isotope (Ci)":
        activity = st.number_input("Activity (Ci)", value=50.0, step=1.0, min_value=0.0)
        st.caption(f"≈ {ci_to_bq_str(activity)}")  # SI equivalent shown below the input
        rhm = st.number_input("RHM Value (R·m²/Ci·h)", value=1.3, step=0.1, min_value=0.0)
        mu  = st.number_input("Attenuation Coeff μ (cm⁻¹)", value=0.5, step=0.01, min_value=0.0)
 
    else:
        ma = st.number_input("Tube Current (mA)", value=5.0, step=0.1, min_value=0.0)
        kv = st.number_input(
            "Tube Voltage (kV)", value=200.0, step=10.0, min_value=0.0,
            help="Reference only — select the kV that matches your Output Factor measurement."
        )
        output_factor = st.number_input(
            "Output Factor (mGy/mA·h at 1m)", value=1.0, step=0.1, min_value=0.0,
            help=f"Machine output at {kv:.0f} kV. Obtain from equipment spec sheet or calibration data."
        )
        mu_xray = st.number_input(
            "Attenuation Coeff μ (cm⁻¹)", value=0.5, step=0.01, min_value=0.0,
            help="Linear attenuation coefficient of the test material at the selected kV."
        )
 
# ── Column 2: geometry inputs and result output ───────────────────────────────
 
with col2:
    st.subheader("2. Geometry")
    thickness_mm = st.number_input("Thickness (mm)", value=10.0, step=1.0,  min_value=0.0)
    distance_cm  = st.number_input("SFD (cm)",        value=100.0, step=10.0, min_value=0.1)
    target_dose  = st.number_input(
        "Target Dose (mGy)", value=17.5, step=0.1, min_value=0.0,
        help="Required dose at film/detector. (Reference: 2 R ≈ 17.5 mGy)"
    )
 
    # ── Calculate and display results ─────────────────────────────────────────
 
    if st.button("Calculate Time", type="primary"):
 
        # Run the appropriate calculation based on selected source type
        if mode == "Radioactive Isotope (Ci)":
            time_sec, dose_rate = calculate_isotope_exposure(
                activity, rhm, mu, thickness_mm, distance_cm, target_dose
            )
        else:
            time_sec, dose_rate = calculate_xray_exposure(
                ma, output_factor, mu_xray, thickness_mm, distance_cm, target_dose
            )
 
        st.divider()
 
        # Show error if dose rate is too low, otherwise display time and rate
        if dose_rate == 0 or time_sec == float('inf'):
            st.error("Error: Dose rate is too low or zero. Check your input values.")
        else:
            st.success(f"Optimal Time: **{format_seconds(time_sec)}**")
            st.info(f"Dose Rate: {dose_rate:.4f} mGy/h")
 
# ── Footer ────────────────────────────────────────────────────────────────────
 
st.divider()
st.caption("Developed by [Duhyun Kim] · [jiu3753@gmail.com] · 2026")
