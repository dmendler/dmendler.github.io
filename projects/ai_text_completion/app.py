from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import cohere

load_dotenv()
API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.ClientV2(API_KEY)

app = Flask(__name__)

@app.route('/complete', methods=['POST'])
def complete():
    data = request.get_json()
    prompt = data.get("prompt")
    temp = data.get("temperature")
    max_tokens = data.get("max_tokens")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        response = co.chat(
            model="command-a-03-2025",
            messages=[{"role": "user", "content": prompt}],
            temperature=float(temp) if temp else None,
            max_tokens=int(max_tokens) if max_tokens else None,
        )
        for item in response.message.content:
            if item.type == "text":
                return jsonify({"completion": item.text})
        return jsonify({"completion": "No text response found."})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
