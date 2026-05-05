import streamlit as st
from db import save_admin_report, create_tables

create_tables()

# SECURITY CHECK
if "is_logged_in" not in st.session_state or not st.session_state["is_logged_in"]:
    st.error("Login required!")
    st.switch_page("login.py")

if st.session_state["role"] != "admin":
    st.error("Admins only!")
    st.stop()

st.title("📊 Admin Panel – Upload Investment Report")

uploaded = st.file_uploader("Upload Investment Report", type=["docx", "txt", "pdf"])

if uploaded:
    save_admin_report(uploaded.name, uploaded.read())
    st.success("Report Uploaded! This report will be used for ALL users until replaced.")

if st.button("Logout"):
    st.session_state.clear()
    st.switch_page("login.py")