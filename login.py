import streamlit as st
from db import create_tables, authenticate

create_tables()

st.set_page_config(page_title="Login", layout="centered")

if "is_logged_in" not in st.session_state:
    st.session_state["is_logged_in"] = False
    st.session_state["role"] = None

st.title("🔐 Login Page")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    role = authenticate(username, password)

    if role:
        st.session_state["is_logged_in"] = True
        st.session_state["role"] = role

        if role == "admin":
            st.switch_page("pages/admin.py")
        else:
            st.switch_page("pages/client.py")

    else:
        st.error("Invalid username or password")