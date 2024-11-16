from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

@app.route("/catch_data", methods=["POST"])
def catch_data():
    # Get the industry from the form data
    global industry
    industry = request.form.get("industry")
    
    # Get the uploaded CSV file from the request
    file = request.files.get("file")
    
    if industry and file:
        # Log the received data in the backend terminal
        print(f"Received industry: {industry}")
        print(f"Received file: {file.filename}")

        # Read the CSV file to check its content
        try:
            df = pd.read_csv(file)
            print(f"CSV data preview:\n{df.head()}")
        except Exception as e:
            return jsonify({"error": f"Error reading CSV file: {str(e)}"}), 400
        
        # Here, you would apply your transformer or AI model to the data
        # For now, let's just return dummy recommendations
        recommendations = ["Recommendation 1", "Recommendation 2", "Recommendation 3"]
        
        return jsonify({"recommendations": recommendations})
    else:
        return jsonify({"error": "Missing industry or file"}), 400


@app.route('/get-industry', methods=['GET'])
def get_industry():
    global industry
    return jsonify({"industry": industry})


if __name__ == "__main__":
    app.run(debug=True)
