import streamlit as st
from db import save_finance, get_latest_admin_report
import docx
from io import BytesIO
import re

# LOGIN CHECK
if "is_logged_in" not in st.session_state:
    st.error("Login required!")
    st.switch_page("login.py")

if st.session_state["role"] != "client":
    st.error("Clients only!")
    st.stop()

st.title("💰 Smart Financial Advisor")

# ------------------------------
# USER INPUT
# ------------------------------
income = st.number_input("Income (₹)", min_value=0.0)
rent = st.number_input("Rent (₹)", min_value=0.0)
food = st.number_input("Food (₹)", min_value=0.0)
transport = st.number_input("Transport (₹)", min_value=0.0)
other = st.number_input("Other Expenses (₹)", min_value=0.0)

if "savings_done" not in st.session_state:
    st.session_state["savings_done"] = False

# ------------------------------
# CALCULATE SAVINGS
# ------------------------------
if st.button("Calculate Savings"):
    expenses = rent + food + transport + other
    savings = income - expenses

    st.session_state["savings"] = savings
    st.session_state["savings_done"] = True

    st.success(f"Your Savings: ₹{savings}")
    save_finance(income, expenses, savings)

if not st.session_state["savings_done"]:
    st.stop()

# ------------------------------
# RISK SELECTION
# ------------------------------
risk_choice = st.radio(
    "Select Your Risk Level",
    ["Low Risk", "Medium Risk", "High Risk"]
)

# ------------------------------
# LOAD ADMIN REPORT
# ------------------------------
report = get_latest_admin_report()
if not report:
    st.warning("Admin must upload the investment analysis DOCX file.")
    st.stop()

file_name, file_data = report
doc = docx.Document(BytesIO(file_data))
text = "\n".join([p.text for p in doc.paragraphs])

matches = re.findall(r"([A-Za-z ]+):\s*([0-9.]+)%", text)
investment_data = {inv.strip(): float(ret) for inv, ret in matches}

# ------------------------------
# RISK SETUP
# ------------------------------
risk_map = {
    "Low Risk": ["PPF", "FD", "Government Bonds"],
    "Medium Risk": ["Mutual Funds", "Gold"],
    "High Risk": ["Stocks"]
}

# ------------------------------
# SHOW ONLY SELECTED RISK CATEGORY
# ------------------------------
st.subheader(f"📊 Recommended Options for {risk_choice}")

best_option = None
best_return = -1

for investment, ret in investment_data.items():
    if investment not in risk_map[risk_choice]:
        continue

    st.write(f"### 📌 {investment}")
    st.write(f"Expected Return: **{ret}%**")
    st.write("---")

    if ret > best_return:
        best_return = ret
        best_option = investment

# ------------------------------
# SHOW BEST RECOMMENDATION
# ------------------------------
if best_option:
    st.success(f"🏆 Best Option for {risk_choice}: **{best_option} ({best_return}%)**")
else:
    st.warning("No investments found for this risk category.")

# ------------------------------
# LOGOUT
# ------------------------------
if st.button("Logout"):
    st.session_state.clear()
    st.switch_page("login.py")