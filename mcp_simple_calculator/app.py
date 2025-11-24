import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8000"

st.title("🧮 Simple Calculator – Streamlit UI")
st.write("This Streamlit app communicates with your FastAPI MCP Calculator Server.")

# --- Quick Operations ---
st.subheader("Enter Numbers")

a = st.number_input("Enter first number (a)", value=0.0)
b = st.number_input("Enter second number (b)", value=0.0)

operation = st.selectbox(
    "Choose Operation",
    ("add", "subtract", "multiply", "divide")
)

if st.button("Calculate"):
    payload = {
        "a": a,
        "b": b,
        "operation": operation
    }

    try:
        response = requests.post(f"{API_BASE}/calculate", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            st.success(f"Result: {data['result']}")
            st.code(data["expression"])
        else:
            st.error(response.json()["detail"])

    except Exception as e:
        st.error(f"Error connecting to API: {e}")

# --- Quick GET Tools ---
st.subheader("🔧 Quick Test Endpoints")

col1, col2, col3, col4 = st.columns(4)

if col1.button("Test Add"):
    r = requests.get(f"{API_BASE}/add?a={a}&b={b}")
    st.write(r.json())

if col2.button("Test Subtract"):
    r = requests.get(f"{API_BASE}/subtract?a={a}&b={b}")
    st.write(r.json())

if col3.button("Test Multiply"):
    r = requests.get(f"{API_BASE}/multiply?a={a}&b={b}")
    st.write(r.json())

if col4.button("Test Divide"):
    try:
        r = requests.get(f"{API_BASE}/calculate?a={a}&b={b}")
        st.write(r.json())
    except:
        st.error("Error calling API")

# --- Status Section ---
st.subheader("🔍 API Status")

if st.button("Check Health"):
    r = requests.get(f"{API_BASE}/health")
    st.write(r.json())
