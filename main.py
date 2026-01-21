from flask import Flask, request, jsonify
from flask_cors import CORS
from preprocess import preprocess_text
from similarity import calculate_similarity

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Render backend running"})

@app.route("/check", methods=["POST"])
def check_plagiarism():
    data = request.get_json()

    text1 = preprocess_text(data.get("text1", ""))
    text2 = preprocess_text(data.get("text2", ""))

    if not text1 or not text2:
        return jsonify({"error": "Both texts are required"}), 400

    if len(text1) > 5000 or len(text2) > 5000:
        return jsonify({"error": "Text too long"}), 400

    score = calculate_similarity(text1, text2)

    return jsonify({
        "plagiarism_percentage": score
    })

if __name__ == "__main__":
    app.run()
