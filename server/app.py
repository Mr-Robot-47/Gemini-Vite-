import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai
from flask import Flask, request, Response, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

def api_key():
    load_dotenv()
    key = os.getenv("API_KEY")
    if not key:
        raise EnvironmentError("Missing API_KEY in environment.")
    return key

def model():
    genai.configure(api_key=api_key())
    return genai.GenerativeModel("gemini-2.5-flash-lite")

def generate_stream(prompt):
    m = model()
    m.start_chat()
    for chunk in m.generate_content(prompt, stream=True):
        yield chunk.text

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "Missing prompt"}), 400
    return Response(generate_stream(prompt), mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)