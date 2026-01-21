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
    # Get uploaded files
    file1 = request.files.get("document1")
    file2 = request.files.get("document2")

    # Validate files
    if not file1 or not file2:
        return jsonify({"error": "Both documents are required"}), 400

    try:
        # Read file contents
        text1 = file1.read().decode("utf-8", errors="ignore")
        text2 = file2.read().decode("utf-8", errors="ignore")

        # Preprocess text
        text1 = preprocess_text(text1)
        text2 = preprocess_text(text2)

        if not text1 or not text2:
            return jsonify({"error": "Documents are empty"}), 400

        # Calculate similarity
        score = calculate_similarity(text1, text2)

        return jsonify({
            "plagiarism_percentage": score
        })

    except Exception as e:
        # Catch any unexpected error (prevents 500 crash)
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500

if __name__ == "__main__":
    app.run()
