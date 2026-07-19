import streamlit as st
import pandas as pd
import pickle
import os

st.set_page_config(page_title="Traffic AI Dashboard", layout="wide")

# 🌈 COLORFUL MODERN CSS
st.markdown("""
<style>

/* Background Gradient */
.stApp {
    background: linear-gradient(135deg, #dfe9f3, #ffffff);
}

/* Title */
h1 {
    text-align: center;
    color: #1e293b;
}

/* Card Style */
.card {
    background: linear-gradient(135deg, #ffffff, #f1f5f9);
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.1);
    margin-top: 20px;
}

/* Input labels */
label {
    font-weight: 600 !important;
    color: #374151 !important;
}

/* Button */
.stButton>button {
    background: linear-gradient(to right, #6366f1, #3b82f6);
    color: white;
    border-radius: 10px;
    height: 45px;
    width: 200px;
    font-size: 16px;
    border: none;
}

/* Button hover */
.stButton>button:hover {
    background: linear-gradient(to right, #4f46e5, #2563eb);
}

/* Result Colors */
.high {
    color: #ef4444;
}
.medium {
    color: #f59e0b;
}
.low {
    color: #22c55e;
}

/* Result Box */
.result-box {
    text-align: center;
    font-size: 22px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)

# Title
st.title("🚦 Smart Traffic Management Dashboard")

# Load model
if not os.path.exists("model.pkl"):
    st.error("❌ model.pkl missing!")
    st.stop()

model = pickle.load(open("model.pkl", "rb"))

# Input Card
st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("📊 Enter Traffic Details")

col1, col2, col3, col4 = st.columns(4)

with col1:
    vehicle = st.slider("Vehicle Count", 0, 200)
with col2:
    speed = st.slider("Average Speed", 0, 100)
with col3:
    time = st.slider("Time of Day", 0, 23)
with col4:
    weather = st.selectbox("Weather", ["Clear", "Rain", "Fog"])

st.markdown('</div>', unsafe_allow_html=True)

# Data prepare
weather_map = {"Clear":0, "Rain":1, "Fog":2}
rush_hour = 1 if (7 <= time <= 10 or 17 <= time <= 20) else 0

input_data = pd.DataFrame(
    [[vehicle, speed, time, weather_map[weather], rush_hour]],
    columns=["vehicle_count","avg_speed","time_of_day","weather","rush_hour"]
)

# Prediction
if st.button("🚀 Predict Traffic"):

    result = model.predict(input_data)[0]

    if result == "High":
        signal = 70
        cls = "high"
    elif result == "Medium":
        signal = 40
        cls = "medium"
    else:
        signal = 20
        cls = "low"

    st.markdown(f"""
    <div class="card">
        <div class="result-box {cls}">
            🚦 Traffic Level: {result}
        </div>
        <div class="result-box">
            ⏱ Signal Time: {signal} sec
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<br><br>
<center style="color:#64748b;">
✨ AI Traffic Dashboard | Clean + Colorful UI
</center>
""", unsafe_allow_html=True)