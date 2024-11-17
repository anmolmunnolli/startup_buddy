from flask import Flask, request, jsonify
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

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
        return jsonify({"recommendations": kpi_responses})
    else:
        return jsonify({"error": "Missing industry or file"}), 400


@app.route('/get-industry', methods=['GET'])
def get_industry():
    global industry
    return jsonify({"industry": industry})

if __name__ == "__main__":
    app.run(debug=True)