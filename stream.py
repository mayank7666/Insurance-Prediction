import streamlit as st
import joblib
import numpy as np
import base64

# -------- PAGE CONFIG ----------
st.set_page_config(layout="wide")

# -------- LOAD MODEL ----------
model = joblib.load("insurance_model.pkl")

# -------- HERO IMAGE ----------
def get_base64(img):
    with open(img, "rb") as f:
        return base64.b64encode(f.read()).decode()

img = get_base64("doctor.png")

# -------- CSS ----------
st.markdown(f"""
<style>

[data-testid="stAppViewContainer"] {{
background-image: url("data:image/jpg;base64,{img}");
background-size: cover;
background-position: center;
background-attachment: fixed;
}}

.hero {{
padding-top:160px;
padding-bottom:160px;
text-align:center;
background: rgba(0,0,0,0.6);
border-radius:20px;
}}

.hero-title {{
font-size:75px;
font-weight:800;
color:red;
}}

.hero-text {{
font-size:26px;
color:#e0e0e0;
margin-bottom:40px;
}}

.stButton>button {{
background: linear-gradient(90deg,#00c6ff,#0072ff);
color:white;
border:none;
padding:14px 45px;
font-size:20px;
border-radius:10px;
}}



</style>
""", unsafe_allow_html=True)

# -------- SESSION STATE ----------
if "page" not in st.session_state:
    st.session_state.page = "home"

# -------- HOME PAGE ----------
if st.session_state.page == "home":

    st.markdown("""
    <div class="hero">
    <div class="hero-title">AI Insurance Predictor</div>
    <div class="hero-text">
    
    </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button(" Predict Now"):
        st.session_state.page = "predict"
        st.rerun()

# -------- PREDICT PAGE ----------
elif st.session_state.page == "predict":

    st.title("Enter Your Details")

    col1, col2 = st.columns(2)

    with col1:
        age = st.slider("Age",18,65,25)
        bmi = st.slider("BMI",15.0,40.0,22.0)
        children = st.slider("Children",0,5,0)

    with col2:
        gender = st.selectbox("Gender",["Male","Female"])
        is_female = 1 if gender=="Female" else 0

        smoker = st.selectbox("Smoker",["No","Yes"])
        is_smoker = 1 if smoker=="Yes" else 0

        region = st.selectbox("Region",["Southeast","Other"])
        region_southeast = 1 if region=="Southeast" else 0

    obese = st.selectbox("BMI Obese?",["No","Yes"])
    bmi_obese = 1 if obese=="Yes" else 0

    if st.button("Calculate Insurance"):

        data = np.array([[age,is_female,bmi,children,
                          is_smoker,region_southeast,bmi_obese]])

        prediction = model.predict(data)[0]

        st.success(f"Estimated Insurance Cost: ₹{prediction:,.2f}")

    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"
        st.rerun()