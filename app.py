from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Example compatibility data (1-3 scale)
compatibility_data = {
    "Aries": {"Aries": 2, "Taurus": 1, "Gemini": 3},  # Add full data here
    "Taurus": {"Aries": 1, "Taurus": 3, "Gemini": 2},
    "Gemini": {"Aries": 3, "Taurus": 2, "Gemini": 3}
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate_compatibility():
    data = request.json
    people = data.get("people", [])
    
    results = []
    for i in range(len(people)):
        for j in range(i+1, len(people)):
            person1, person2 = people[i], people[j]
            sun_score = compatibility_data.get(person1["sun"], {}).get(person2["sun"], 2)
            moon_score = compatibility_data.get(person1["moon"], {}).get(person2["moon"], 2)
            rising_score = compatibility_data.get(person1["rising"], {}).get(person2["rising"], 2)
            avg_score = (sun_score + moon_score + rising_score) / 3
            status = "disaster" if avg_score < 1.5 else "okay" if avg_score < 2.5 else "awesome"
            results.append({"pair": [person1["name"], person2["name"]], "score": avg_score, "status": status})
    
    return jsonify(results)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use dynamic port for Render
    app.run(debug=True, host='0.0.0.0', port=port)
