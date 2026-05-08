import streamlit as st
import pandas as pd
import numpy as np
import pickle
import datetime
import matplotlib.pyplot as plt

# 💾 Load the trained model
model = pickle.load(open("packet_model.pkl", "rb"))

# 🌐 App Config
st.set_page_config(page_title="Neuro Shield", page_icon="🧠")

# 🎨 Branding
st.title("🛡️ Neuro Shield")
st.subheader("🧠 Smart ML-Powered Network Classifier")
st.markdown("---")

# ✨ Initialize session state
if 'prediction' not in st.session_state:
    st.session_state.prediction = None
if 'traffic_count' not in st.session_state:
    st.session_state.traffic_count = {"Normal": 0, "Video Stream": 0, "Suspicious": 0}

# 🎯 Input Fields
flow_duration = st.number_input("Flow Duration", min_value=1, value=45000)
total_fwd_packets = st.number_input("Total Forward Packets", min_value=0, value=22)
total_bwd_packets = st.number_input("Total Backward Packets", min_value=0, value=18)
fwd_packet_length_mean = st.number_input("Forward Packet Length Mean", min_value=0.0, value=512.3)
bwd_packet_length_mean = st.number_input("Backward Packet Length Mean", min_value=0.0, value=486.7)

# 🚀 Predict Button
if st.button("🚀 Classify Traffic"):
    input_data = np.array([[flow_duration, total_fwd_packets, total_bwd_packets,
                            fwd_packet_length_mean, bwd_packet_length_mean]])
    prediction = model.predict(input_data)[0]
    st.session_state.prediction = prediction
    st.session_state.traffic_count[prediction] += 1

    # Save to CSV
    log_entry = {
        "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Flow Duration": flow_duration,
        "Fwd Packets": total_fwd_packets,
        "Bwd Packets": total_bwd_packets,
        "Fwd Length Mean": fwd_packet_length_mean,
        "Bwd Length Mean": bwd_packet_length_mean,
        "Prediction": prediction
    }

    log_df = pd.DataFrame([log_entry])
    try:
        existing_log = pd.read_csv("packet_log.csv")
        log_df = pd.concat([existing_log, log_df], ignore_index=True)
    except FileNotFoundError:
        pass
    log_df.to_csv("packet_log.csv", index=False)

# ✅ Show Prediction if available
if st.session_state.prediction:
    emoji_map = {
        "Normal": "✅",
        "Video Stream": "🎬",
        "Suspicious": "⚠️"
    }
    st.success(f"{emoji_map.get(st.session_state.prediction, '')} **{st.session_state.prediction} Detected**")
    st.markdown("🌐 Network IQ: Activated.")

    # 📊 Traffic Chart
    st.markdown("### 📈 Live Traffic Count")
    fig, ax = plt.subplots()
    traffic_labels = list(st.session_state.traffic_count.keys())
    traffic_values = list(st.session_state.traffic_count.values())
    ax.bar(traffic_labels, traffic_values, color=["green", "blue", "red"])
    ax.set_ylabel("Count")
    ax.set_xlabel("Traffic Type")
    ax.set_title("Neuro Shield Traffic Overview")
    st.pyplot(fig)

    # 📥 CSV Log Download
    st.markdown("### 🧾 Download Traffic Log")
    with open("packet_log.csv", "rb") as f:
        st.download_button("📥 Download Traffic CSV", f, "NeuroShield_Traffic_Log.csv", "text/csv")

    # 📸 Screenshot Guide
    st.markdown("### 📸 Save Screenshot")
    with st.expander("Click to view screenshot instructions"):
        st.markdown("""
        - 🖱️ Right-click anywhere → Print → Save as PDF  
        - 💻 Or use keyboard shortcuts:
          - Mac: `Cmd + Shift + 4`
          - Windows: `Win + Shift + S`
        """)
        st.info("💡 Tip: Take screenshot **after classification** for full result display.")

st.markdown("---")
