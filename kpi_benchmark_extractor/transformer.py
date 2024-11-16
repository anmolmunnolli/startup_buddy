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

kpis = ["Churn Rate", "Monthly Recurring Revenue", "Annual Run Rate", "Burn Rate", "LTV/CAC ratio"]

model_name = "google/flan-t5-large"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

if industry:
    prompt = f"What is the average gross sales for {industry} business?"
    inputs = tokenizer(prompt, return_tensors="pt")

    outputs = model.generate(inputs.input_ids, max_length=50)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"Model response for {industry}: {response}")
else:
    print("Industry variable is not set. Please ensure the Flask app is running and the variable is set.")

