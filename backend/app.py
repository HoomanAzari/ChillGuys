from flask import Flask, request, jsonify, send_from_directory
import requests

app = Flask(__name__, static_folder="frontend")

# Replace with your actual API key
API_KEY = "AIzaSyAu4tU1Qi6kfqELFzoTAeVHWk5Y65vNwfg"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

@app.route("/")
def index():
    """Serve the updated HTML file."""
    return send_from_directory("frontend", "updated_index.html")

@app.route("/frontend/<path:filename>")
def static_files(filename):
    """Serve static files from the frontend folder."""
    return send_from_directory("frontend", filename)

@app.route("/generate-response", methods=["POST"])
def generate_response():
    """Handle POST request to generate a bot response."""
    try:
        # Get the user's message and chat history from the request
        data = request.json
        user_message = data.get("message", "")
        chat_history = data.get("chat_history", [])

        # Prepare the payload for the external API
        payload = {
            "contents": chat_history + [{"role": "user", "parts": [{"text": user_message}]}]
        }

        # Make the API request
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        api_response = response.json()

        # Extract the bot's response
        bot_response = api_response.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()

        # Return the bot's response
        return jsonify({"bot_response": bot_response})

    except Exception as e:
        # Handle errors gracefully
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)