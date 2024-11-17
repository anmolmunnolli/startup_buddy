from flask import Flask, request, jsonify
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM
import requests
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)

# Function to fetch KPI responses
def generate_kpi_responses(industry, kpis):
    model_name = "google/flan-t5-large"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    kpi_responses = []
    for kpi in kpis:
        prompt = f"What is the average {kpi} for a {industry} company?"
        inputs = tokenizer(prompt, return_tensors="pt")
        outputs = model.generate(inputs.input_ids, max_length=50)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        kpi_responses.append(response)
    return kpi_responses

@app.route("/catch_data", methods=["POST"])
def catch_data():
    global industry
    industry = request.form.get("industry")
    
    file = request.files.get("file")
    
    if industry and file:
        print(f"Received industry: {industry}")
        print(f"Received file: {file.filename}")

        try:
            df = pd.read_csv(file)
            df.to_csv(f"original_{industry}.csv")
            print(f"CSV data preview:\n{df.head()}")
        except Exception as e:
            return jsonify({"error": f"Error reading CSV file: {str(e)}"}), 400

        kpis = ["Customer Acquisition Costs (CAC)", "Churn Rate (%)", "Average Order Size ($)", "Monthly Recurring Revenue (MRR) ($)", 
                            "Annual Run Rate (ARR) ($)", "Cash Runway (Months)", "Burn Rate ($/Month)", "Gross Sales ($)", 
                            "Monthly Active Users (MAU)", "Net Promoter Score (NPS)", "LTV/CAC Ratio"]

        kpi_responses = generate_kpi_responses(industry, kpis)

        kpis_data = {}
        for kpi in kpis:
            if kpi in df.columns:
                kpis_data[kpi] = df[kpi].mean()  # Example: Calculate average values for KPIs

        # Step 3: Generate LLaMA-based recommendations
        llama_recommendations = generate_kpi_recommendations(industry, kpis_data)

        return jsonify({"recommendations": kpi_responses,
                    "llama_recommendations": llama_recommendations})
    else:
        return jsonify({"error": "Missing industry or file"}), 400


@app.route('/get-industry', methods=['GET'])
def get_industry():
    global industry
    return jsonify({"industry": industry})

def get_recommendations_from_llama(industry, kpis_data):
    # URL of the separate LLaMA recommendation service
    llama_service_url = "http://localhost:5001/generate_recommendations"
    
    payload = {
        "industry": industry,
        "kpis_data": kpis_data
    }

    response = requests.post(llama_service_url, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Error in fetching recommendations from LLaMA service"}

def generate_kpi_recommendations(industry, kpis_data):
    model_name = "meta-llama/Llama-3.2-1B"  # You can adjust the model as per your preference
    hf_token = os.getenv("HF_TOKEN") # Replace this with your actual token

    tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=hf_token)
    model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=hf_token)

    recommendations = []
    

        # Build the KPI list dynamically
    kpi_list = ""
    for kpi, value in kpis_data.items():
        kpi_list += f"- {kpi}: {value}\n"

    # Construct the final prompt
    prompt = (
        f"You are a business expert providing actionable recommendations for improving key performance indicators (KPIs) "
        f"in a company operating in the {industry} industry. Below are the KPIs and their current values:\n{kpi_list}\n\n"
        f"### Recommendations:\n"
    )


    # Generate recommendations
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        inputs.input_ids,
        max_length=1000,
        attention_mask=inputs.attention_mask,
        pad_token_id=tokenizer.pad_token_id,
        num_return_sequences=1,
        temperature=0.7,
        top_k=40,
        top_p=0.8
    )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    response = response[len(prompt):].strip()
    print(response)

    # Loop through KPIs and create prompts to generate recommendations
    # for kpi, value in kpis_data.items():
    #     prompt = f"Given the KPI {kpi} with a value of {value} for a {industry} company, what actions or recommendations can improve this KPI?"
    #     inputs = tokenizer(prompt, return_tensors="pt")
    #     outputs = model.generate(inputs.input_ids, max_length=150,    attention_mask=inputs.attention_mask,    pad_token_id=tokenizer.pad_token_id , num_return_sequences=1)
    #     response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    recommendations.append({"KPI": kpi, "Recommendation": response})
    
    return recommendations

if __name__ == "__main__":
    app.run(debug=True)