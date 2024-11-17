import requests
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
# from frontend.app import industry
# Function to fetch `industry` dynamically
def get_industry():
    try:
        response = requests.get("http://127.0.0.1:5000/get-industry")
        if response.status_code == 200:
            return response.json().get("industry")
        else:
            print("Failed to fetch industry from Flask app")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching industry: {e}")
        return None

industry = get_industry()

kpis = ["Customer Acquisition Costs (CAC)", "Churn Rate (%)", "Average Order Size ($)", "Monthly Recurring Revenue (MRR) ($)", 
                            "Annual Run Rate (ARR) ($)", "Cash Runway (Months)", "Burn Rate ($/Month)", "Gross Sales ($)", 
                            "Monthly Active Users (MAU)", "Net Promoter Score (NPS)", "LTV/CAC Ratio"]

model_name = "google/flan-t5-large"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

if industry:
    for kpi in kpis:
        prompt = f"What is the average {kpi} for a {industry} company?"
        inputs = tokenizer(prompt, return_tensors="pt")
        outputs = model.generate(inputs.input_ids, max_length=50)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"Model response for kpi- {kpi} in {industry}: {response}")
else:
    print("Industry variable is not set. Please ensure the Flask app is running and the variable is set.")

