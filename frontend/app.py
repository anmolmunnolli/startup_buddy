import streamlit as st
import requests
import pandas as pd

industry=None
# Function to send industry and dataset to the backend
def send_data_to_backend(industry, uploaded_file):
    # Prepare the files and data to send to the backend
    files = {"file": uploaded_file.getvalue()}
    data = {"industry": industry}
    
    # Send the industry and dataset (CSV file) to the backend (Flask API)
    response = requests.post("http://localhost:5000/catch_data", data=data, files=files)
    return response

# Set page config as the first command in the script
st.set_page_config(page_title="Startup Decision Support System", layout="centered")

# Title and description
st.title("Startup Decision Support System")
st.write("Enter the industry and upload your KPI data (CSV) to get startup recommendations.")

# Industry input field (text input)
industry = st.text_input("Enter Industry Name (e.g., Technology)", "")

# Dataset input (CSV file upload)
uploaded_file = st.file_uploader("Upload KPI Data (CSV)", type=["csv"])

# Button to send both industry and dataset to the backend
if st.button("Get Recommendations"):
    if industry and uploaded_file:
        # Send the industry and dataset to the backend
        response = send_data_to_backend(industry, uploaded_file)
        
        if response.status_code == 200:
            recommendations = response.json().get("recommendations")
            
            # Display Top 10 Recommendations as a bullet point list
            st.write("### Top 10 Recommendations:")
            
            for recommendation in recommendations:
                st.markdown(f"- {recommendation}")
        else:
            st.error("Error getting recommendations from the backend.")
    else:
        st.warning("Please enter an industry and upload a dataset.")


