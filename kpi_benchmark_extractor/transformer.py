from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = "google/flan-t5-large"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

prompt = "What is the average customer acquisition cost for big clothing company in the USA?"
inputs = tokenizer(prompt, return_tensors="pt")

outputs = model.generate(inputs.input_ids, max_length=50)
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(f"Model response: {response}")
