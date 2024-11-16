from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/catch_industry', methods=['POST'])
def catch_industry():
    # Get the industry from the frontend
    data = request.json
    industry = data['industry']

    # Process the industry (for now, we just print it)
    print(f"Received industry: {industry}")
    
    # Respond back with a success message
    return jsonify({'message': f"Industry '{industry}' received successfully!"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
