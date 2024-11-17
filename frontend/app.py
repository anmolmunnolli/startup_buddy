import streamlit as st
import requests
import pandas as pd
import re
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import matplotlib.pyplot as plt
import numpy as np

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
if uploaded_file:
    st.session_state.uploaded_file = uploaded_file
    
# Button to send both industry and dataset to the backend
if st.button("Get Recommendations"):
    if industry and uploaded_file:
        # Send the industry and dataset to the backend
        response = send_data_to_backend(industry, uploaded_file)
        
        if response.status_code == 200:
            recommendations = response.json().get("recommendations")
            llama_recommendations = response.json().get("llama_recommendations")

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

                # Reset the index to remove any additional index column
                kpis_transposed.reset_index(drop=True, inplace=True)
                # original_df = original_df.set_index('KPI')
                # Leave the first column name blank (like df1)
                # kpis_transposed.columns = [''] + kpis_transposed.columns[1:].tolist()
                # print(kpis_transposed.columns)

                # # Drop the first row which contains the 'Response' values
                kpis_transposed.drop(index=0, inplace=True)
                # kpis_transposed = kpis_transposed.drop(index=0)

                # # Remove the first unnamed column (it is now in the column 'index')
                # kpis_transposed = kpis_transposed.drop(columns=['index'])
                # kpis_transposed.to_csv("cleaned_kpi.csv",header=True)

                relevant_columns = ["Customer Acquisition Costs (CAC)", "Churn Rate (%)", "Average Order Size ($)", "Monthly Recurring Revenue (MRR) ($)", 
                            "Annual Run Rate (ARR) ($)", "Cash Runway (Months)", "Burn Rate ($/Month)", "Gross Sales ($)", 
                            "Monthly Active Users (MAU)", "Net Promoter Score (NPS)", "LTV/CAC Ratio"]
                relevant_original_df = original_df[relevant_columns] # 3rd index corresponds to the 4th column (0-based indexing)

                # # Step 2: Slice from the 2nd column onward in df2
                relevalnt_kpis_transposed = kpis_transposed[relevant_columns]  # 1st index corresponds to the 2nd column (0-based indexing)
                relevant_original_df.index.name = "KPI"


                # # Transform KPI into the index for New df2
                # kpis_transposed.set_index("KPI", inplace=True)
                # kpis_transposed.index.name = "index"

                # Print to verify
                print("Aligned df1:")
                print(relevant_original_df.head())

                print("\nAligned df2:")
                print(kpis_transposed.head())

                # Ensure that all columns are numeric in df1 and df2
                relevant_original_df = relevant_original_df.apply(pd.to_numeric, errors='coerce')
                kpis_transposed = kpis_transposed.apply(pd.to_numeric, errors='coerce')


                # Extract columns and compute mean for df1
                kpi_labels = relevant_original_df.columns
                df1_values = relevant_original_df.mean()  # Aggregating df1 values
                df2_values = kpis_transposed.iloc[0]  # Taking the first row from df2

                # Create a combined plot for all KPIs comparisons (Bar + Line Plot)
                fig, axs = plt.subplots(len(kpi_labels), 2, figsize=(14, 8 * len(kpi_labels)))

                # Loop through each KPI to create bar and line plots for all KPIs
                for i, kpi in enumerate(kpi_labels):
                    # Plot Bar chart for df1 vs df2
                    axs[i, 0].bar(kpi, df1_values[kpi], width=0.4, label='Company KPIs', align='center', color='skyblue')
                    axs[i, 0].bar(kpi, df2_values[kpi], width=0.4, label='Industry KPI Benchmark', align='edge', color='lightcoral')
                    axs[i, 0].set_title(f"{kpi} - Bar Chart Comparison")
                    axs[i, 0].set_ylabel("Values")
                    axs[i, 0].legend()

                    # Plot Line plot for df1 vs df2 (Individual KPI comparisons for both)
                    # The x-values will be the row indices of relevant_original_df (0, 1, 2, etc.)
                    x_values = np.arange(len(relevant_original_df))

                    # Plot the line for the company KPIs (actual values across rows)
                    axs[i, 1].plot(x_values, relevant_original_df[kpi], label=f"Company KPIs - {kpi}", marker='o', linestyle='-', color='blue', linewidth=2)

                    # Plot the line for the industry benchmark (constant line)
                    axs[i, 1].plot(x_values, [df2_values[kpi]] * len(x_values), label=f"Industry KPI Benchmark - {kpi}", marker='x', linestyle='--', color='red', linewidth=2)

                    # Make x-axis labels more visible and cleaner
                    axs[i, 1].set_title(f"{kpi} - Line Plot Comparison")
                    axs[i, 1].set_ylabel("Values")
                    axs[i, 1].set_xticks(x_values)  # Set the positions for x-axis labels
                    axs[i, 1].set_xticklabels(x_values, rotation=45, ha='right', fontsize=10)  # Rotate and set font size
                    axs[i, 1].grid(True, axis='x', linestyle='--', alpha=0.5)  # Add grid for better readability
                    axs[i, 1].legend()

                # Adjust layout and spacing
                plt.tight_layout()

                # Use Streamlit to display the plot
                st.pyplot(fig)


                if llama_recommendations:
                    # st.write("### LLaMA Recommendations")
                    # st.write(llama_recommendations)
                    # llama_df = pd.DataFrame(llama_recommendations).drop_duplicates()
                    st.write("### LLaMA Recommendations:")
                    st.write(llama_recommendations)
            else:
                st.write("No recommendations available.")
        else:
            st.error("Error getting recommendations from the backend.")
    else:
        st.warning("Please enter an industry and upload a dataset.")


def time_series_forecasting(df, column_name, freq='M', periods=12):
    # Ensure the data has a datetime index
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])  # Remove rows with invalid dates
    df = df.set_index('Date')

    # Resample to ensure consistent monthly frequency
    ts_data = df[column_name].resample(freq).mean()

    # Check if there are enough data points
    if len(ts_data.dropna()) < 2 * periods:
        st.error(f"Not enough data points to forecast {periods} months ahead.")
        return None, None

    # Fit the Exponential Smoothing model
    model = ExponentialSmoothing(ts_data, seasonal='add', seasonal_periods=12)
    fit = model.fit()

    # Forecast the next 'periods' months
    forecast = fit.forecast(periods)

    return ts_data, forecast


# Step 1: Persist file and selected column in session state
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

if "selected_column" not in st.session_state:
    st.session_state.selected_column = None

# Step 3: Process uploaded file
if st.session_state.uploaded_file:
    original_df = pd.read_csv(st.session_state.uploaded_file)
    # List numeric columns for selection
    numeric_columns = original_df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    # Step 4: Column selection
    selected_column = st.selectbox("Select a column for forecasting", numeric_columns, key="selected_column")

    # Step 5: Perform forecasting when the button is clicked
    if st.button("Perform Time Series Forecasting"):
        if 'Date' in original_df.columns:
            ts_data, forecast = time_series_forecasting(original_df, selected_column)

            if ts_data is not None and forecast is not None:
                # Plot the original time series and forecast
                fig, ax = plt.subplots(figsize=(10, 6))
                ts_data.plot(ax=ax, label="Historical Data")
                forecast.plot(ax=ax, label="Forecast", linestyle="--")
                plt.legend()
                plt.title(f"Time Series Forecast for {selected_column}")
                plt.xlabel("Date")
                plt.ylabel(selected_column)
                st.pyplot(fig)

                # Display the forecast data
                forecast_df = pd.DataFrame({
                    'Date': forecast.index,
                    'Forecast': forecast.values
                })
                st.dataframe(forecast_df)
                st.download_button(
                    label="Download Forecast as CSV",
                    data=forecast_df.to_csv(index=False),
                    file_name=f"{selected_column}_forecast.csv",
                    mime='text/csv'
                )
        else:
            st.error("The data must include a 'Date' column for time series analysis.")