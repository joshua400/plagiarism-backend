from flask import Flask, request, jsonify
from flask_cors import CORS
from preprocess import preprocess_text
from similarity import calculate_similarity

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Render backend running"})

@app.route("/check-plagiarism", methods=["POST"])
def check_plagiarism():
    text1 = request.form.get("document1", "")
    text2 = request.form.get("document2", "")

    text1 = preprocess_text(text1)
    text2 = preprocess_text(text2)

    if not text1 or not text2:
        return jsonify({"error": "Both documents are required"}), 400

    score = calculate_similarity(text1, text2)

    return jsonify({
        "plagiarism_percentage": score
    })

if __name__ == "__main__":
    app.run()
