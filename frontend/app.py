import streamlit as st
import requests

# Function to send industry input to the backend
def send_industry_to_backend(industry):
    # Send the industry to the backend (Flask API)
    response = requests.post("http://localhost:5000/catch_industry", json={'industry': industry})
    return response


# Set up the Streamlit page configuration
st.set_page_config(page_title="Startup Decision Support System", layout="centered")

# Title and description
st.title("Startup Decision Support System")
st.write("Enter the industry to send to the backend.")

# Industry input field (text input)
industry = st.text_input("Enter Industry Name (e.g., Technology)", "")

# Button to send industry to the backend
if st.button("Send Industry"):
    if industry:
        # Send the industry to the backend
        response = send_industry_to_backend(industry)
        if response.status_code == 200:
            st.success(f"Industry '{industry}' has been successfully sent to the backend.")
        else:
            st.error("Error sending data to the backend.")
    else:
        st.warning("Please enter an industry.")


