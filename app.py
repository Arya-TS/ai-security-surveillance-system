import streamlit as st
import sqlite3
import pandas as pd
import os
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# ---------- PAGE CONFIG ----------

st.set_page_config(
    page_title="AI Security Surveillance",
    page_icon="🛡️",
    layout="wide"
)

# ---------- STYLE ----------

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(120deg,#0f2027,#203a43,#2c5364);
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🛡️ AI Security Surveillance Dashboard")

DB_NAME = "security_logs.db"

# ---------- AUTO REFRESH ----------

st_autorefresh(interval=5000, key="alerts_refresh")

# ---------- DATABASE INIT ----------

def init_db():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            timestamp TEXT,
            image_path TEXT,
            video_path TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------- LOAD ALERTS ----------

def get_alerts():

    conn = sqlite3.connect(DB_NAME)

    try:
        df = pd.read_sql_query(
            "SELECT * FROM alerts ORDER BY id DESC",
            conn
        )
    except:
        df = pd.DataFrame()

    conn.close()

    return df


alerts = get_alerts()

# ---------- SYSTEM OVERVIEW ----------

st.subheader("System Overview")

col1, col2, col3 = st.columns(3)

total_alerts = len(alerts)
today = datetime.now().date()

if total_alerts > 0:

    alerts["date"] = pd.to_datetime(alerts["timestamp"]).dt.date
    today_alerts = len(alerts[alerts["date"] == today])

    unknown_alerts = len(alerts[alerts["name"] == "Unknown"])

else:

    today_alerts = 0
    unknown_alerts = 0

col1.metric("Total Alerts", total_alerts)
col2.metric("Alerts Today", today_alerts)
col3.metric("Unknown Intrusions", unknown_alerts)

st.divider()

# ---------- RECENT ALERTS TABLE ----------

st.subheader("Recent Alerts")

if total_alerts > 0:

    st.dataframe(alerts, use_container_width=True)

else:

    st.info("No alerts recorded yet")

st.divider()

# ---------- SESSION STATE ----------

if "show_image" not in st.session_state:
    st.session_state.show_image = None

if "show_video" not in st.session_state:
    st.session_state.show_video = None

# ---------- ALERT TIMELINE ----------

st.subheader("Alert Timeline")

if total_alerts == 0:

    st.info("No alerts recorded yet")

else:

    for _, row in alerts.iterrows():

        alert_id = row["id"]

        with st.container():

            col1, col2 = st.columns([4,1])

            with col1:

                st.markdown(
                    f"""
                    **Alert #{alert_id}**  
                    👤 Person: **{row['name']}**  
                    🕒 Time: **{row['timestamp']}**
                    """
                )

            with col2:

                if st.button("🖼 View Image", key=f"img_{alert_id}"):

                    st.session_state.show_image = alert_id
                    st.session_state.show_video = None

                if st.button("🎥 Play Video", key=f"vid_{alert_id}"):

                    st.session_state.show_video = alert_id
                    st.session_state.show_image = None


        # ---------- IMAGE DISPLAY ----------

        if st.session_state.show_image == alert_id:

            image_path = row["image_path"]

            if image_path and os.path.exists(image_path):

                st.image(
                    image_path,
                    caption="Captured Evidence",
                    use_container_width=True
                )

            else:

                st.warning("Image file not found")


        # ---------- VIDEO DISPLAY ----------

        if st.session_state.show_video == alert_id:

            video_path = row["video_path"]

            if video_path and os.path.exists(video_path):

                st.video(video_path)

                st.caption(video_path)

            else:
                st.error("Video file not found")
