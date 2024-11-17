import streamlit as st
import requests
import pandas as pd
import re
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
                    "KPI": ["Customer Acquisition Costs (CAC)", "Churn Rate (%)", "Average Order Size ($)", "Monthly Recurring Revenue (MRR) ($)", 
                            "Annual Run Rate (ARR) ($)", "Cash Runway (Months)", "Burn Rate ($/Month)", "Gross Sales ($)", 
                            "Monthly Active Users (MAU)", "Net Promoter Score (NPS)", "LTV/CAC Ratio"],
                    "Response": recommendations
                })
                
                st.write("### KPI Responses:")
                st.dataframe(kpi_df)  # Display as a table
                kpi_df.to_csv(f"{industry}.csv", index=False)  # Save DataFrame to a CSV file


                original_df = pd.read_csv(f"../backend/original_{industry}.csv")
                print(original_df.columns, kpi_df.columns)




                # Function to clean and convert the values in Response column
                def clean_and_convert(value):
                    # Remove dollar signs, commas, quotes, and percentages
                    value = re.sub(r'[\$,"]', '', value)  # Remove $, commas, and quotes
                    value = value.strip()  # Remove leading/trailing spaces
                    
                    # Convert words like million, billion into numbers
                    if 'million' in value.lower():
                        value = re.sub(r'million', '', value, flags=re.IGNORECASE)
                        value = float(value) * 1e6  # Multiply by 1 million
                    elif 'billion' in value.lower():
                        value = re.sub(r'billion', '', value, flags=re.IGNORECASE)
                        value = float(value) * 1e9  # Multiply by 1 billion
                    elif 'tens of millions' in value.lower():
                        value = 1e7  # Assign a value for "tens of millions"
                    
                    # Check if the value is a percentage, convert to decimal if necessary
                    elif value.endswith('%'):
                        value = float(value.rstrip('%')) / 100  # Convert percentage to decimal

                    # Attempt to convert the value to a float or int
                    try:
                        value = float(value)
                    except ValueError:
                        pass  # If conversion fails, leave the value as is (string)

                    return value

                # Apply the cleaning function to the 'Response' column
                kpi_df['Cleaned_Response'] = kpi_df['Response'].apply(clean_and_convert)

                # Now, the cleaned responses will be numeric or appropriate values
                # print(kpi_df)


                kpis_transposed = kpi_df.set_index('KPI').T
                print(kpis_transposed.columns)
                kpis_transposed.reset_index(inplace=True)

                # Drop the first row which contains the 'Response' values
                # kpis_transposed.drop(index=0, inplace=True)
                kpis_transposed = kpis_transposed.drop(index=0)

                # Remove the first unnamed column (it is now in the column 'index')
                kpis_transposed = kpis_transposed.drop(columns=['index'])
                kpis_transposed.to_csv("cleaned_kpi.csv",header=True)


                # # Step 2: Align the column names of kpis_transposed to match df1's relevant columns
                # kpis_transposed.columns = original_df.columns[3:]  # Align to df1 columns starting from the 4th column
                

                # print(kpis_transposed.columns, original_df.columns)
                # # Step 3: Compare both DataFrames (df1 and kpis_transposed)
                # # For simplicity, we will just add both DataFrames together based on the common KPI columns.
                # comparison_df = pd.concat([original_df.iloc[:, 3:], kpis_transposed], axis=1)

                # # Optional: Rename the columns for clarity if needed
                # comparison_df.columns = [col + ' - df1' if i < len(original_df.columns[3:]) else col + ' - kpis_df' 
                #                         for i, col in enumerate(comparison_df.columns)]

                # # Show the result
                # print(comparison_df)

                # comparison_df.to_csv("compare.csv", header=True)


            else:
                st.write("No recommendations available.")
        else:
            st.error("Error getting recommendations from the backend.")
    else:
        st.warning("Please enter an industry and upload a dataset.")