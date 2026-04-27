import streamlit as st

st.set_page_config(page_title="Smart Home Security", layout="wide")

st.title("🏠 Smart Home Intrusion Detection System")

st.subheader("AI + IoT Based Security Monitoring")

st.write("""
This system monitors camera feed in real time and detects human presence.
If an unknown person is detected:
- Image is captured
- Timestamp added
- Email alert sent
- Log stored
""")

st.header("✅ Features")

col1, col2 = st.columns(2)

with col1:
    st.write("✔ Human Detection")
    st.write("✔ Unknown Person Alert")
    st.write("✔ Image Capture")

with col2:
    st.write("✔ Email Notification")
    st.write("✔ CSV Logging")
    st.write("✔ Real-time Monitoring")

st.header("⚙️ Execution Command")
st.code("python smart_intrusion_demo.py")

st.success("Project Successfully Hosted")
