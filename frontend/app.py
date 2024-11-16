import streamlit as st
import requests
import pandas as pd

industry = None

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
            
            # Display recommendations as a dataframe (table)
            if recommendations:
                # Create a pandas DataFrame for the KPI responses
                kpi_df = pd.DataFrame({
                    "KPI": ["Customer Acquisition Costs", "Average order size", "Cash Runway", "K-factor", 
                            "Churn Rate", "Monthly Recurring Revenue", "Annual Run Rate", "Burn Rate", 
                            "LTV/CAC ratio", "Gross sales", "Monthly active users", "Net Promoter Score"],
                    "Response": recommendations
                })
                
                st.write("### KPI Responses:")
                st.dataframe(kpi_df)  # Display as a table
            else:
                st.write("No recommendations available.")
        else:
            st.error("Error getting recommendations from the backend.")
    else:
        st.warning("Please enter an industry and upload a dataset.")
