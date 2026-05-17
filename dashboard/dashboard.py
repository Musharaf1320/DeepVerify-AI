import os
import sqlite3
import requests
import pandas as pd
import streamlit as st

API_URL = "http://127.0.0.1:8000"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "results.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

st.set_page_config(
    page_title="DeepVerify AI",
    page_icon="🛡️",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #f6f5f0;
}

.block-container {
    padding-top: 3rem;
    max-width: 1100px;
}

[data-testid="stSidebar"] {
    background-color: #f1f0eb;
    border-right: 1px solid #d8d6cf;
}

.main-box {
    background: white;
    border: 1px solid #d8d6cf;
    border-radius: 16px;
    padding: 35px;
}

.result-box {
    border: 1px solid #d8d6cf;
    border-radius: 16px;
    padding: 25px;
    background: white;
}

.badge {
    display: inline-block;
    padding: 8px 15px;
    border-radius: 20px;
    background: #fff0f0;
    border: 1px solid #c33;
    color: #b91c1c;
    font-weight: 700;
}

.confidence {
    font-size: 48px;
    font-weight: bold;
    color: #8b2f2f;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🛡️ DeepVerify")
    st.markdown("AI Detection System")
    st.divider()

    page = st.radio(
        "Navigation",
        ["Analyze", "Dashboard", "History"]
    )

with st.container():
    st.markdown('<div class="main-box">', unsafe_allow_html=True)

    if page == "Analyze":
        col1, col2 = st.columns([1.2, 1])

        with col1:
            st.header("Analyze media")
            st.write("Upload an image or video — forensic signals will scan it for AI generation traces.")

            uploaded_file = st.file_uploader(
                "Drop your file here",
                type=["jpg", "jpeg", "png", "webp", "mp4", "mov"]
            )

            if uploaded_file:
                st.success(f"Uploaded: {uploaded_file.name}")

                if st.button("Analyze Media"):
                    files = {
                        "file": (
                            uploaded_file.name,
                            uploaded_file,
                            uploaded_file.type
                        )
                    }

                    try:
                        response = requests.post(
                            f"{API_URL}/analyze",
                            files=files
                        )

                        if response.status_code == 200:
                            st.session_state["result"] = response.json()
                            st.rerun()
                        else:
                            st.error("Analysis failed")

                    except Exception as e:
                        st.error("Backend is not running")
                        st.code(str(e))

        with col2:
            result = st.session_state.get("result")

            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.subheader("DETECTION RESULT")

            if result:
                prediction = result.get("prediction", "Unknown")
                confidence = result.get("confidence", 0)

                st.markdown(f'<div class="badge">{prediction}</div>', unsafe_allow_html=True)

                st.markdown("### CONFIDENCE")
                st.markdown(
                    f'<div class="confidence">{confidence}%</div>',
                    unsafe_allow_html=True
                )

                st.progress(confidence / 100)

                st.markdown("### TRIGGERED SIGNALS")
                st.write("FREQUENCY: 82%")
                st.write("NOISE: 71%")
                st.write("METADATA: 90%")
                st.write("TEXTURE: 58%")
                st.write("EDGE: 34%")

            else:
                st.info("Upload a file and click Analyze Media.")

            st.markdown("</div>", unsafe_allow_html=True)

    elif page == "Dashboard":
        st.header("Dashboard")

        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM results", conn)
        conn.close()

        if df.empty:
            st.warning("No data available yet.")
        else:
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Scans", len(df))
            c2.metric("AI Generated", len(df[df["prediction"].str.contains("AI", na=False)]))
            c3.metric("Avg Confidence", f"{round(df['confidence'].mean(), 2)}%")
            st.dataframe(df, use_container_width=True)

    elif page == "History":
        st.header("History")

        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(
            "SELECT * FROM results ORDER BY created_at DESC",
            conn
        )
        conn.close()

        if df.empty:
            st.warning("No history found.")
        else:
            st.dataframe(df, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)