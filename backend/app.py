from flask import Flask, request, jsonify
# from assistant import CarDealershipAssistant, vehicles
from assistant import ChillGuyChatbot

# Initialize the Assistant with the vehicle data
# vehicles_list = vehicles.Vehicle.get_objects("../vehicles.json")
# assistant = CarDealershipAssistant(vehicles_list)
assistant = ChillGuyChatbot()

app = Flask(__name__, static_folder="../frontend")


@app.route("/")
def index():
    """Serve the main HTML page."""
    return app.send_static_file("updated_index.html")


@app.route("/generate-response", methods=["POST"])
def generate_response_route():
    """
    Handle POST requests to generate a bot response using the Assistant.
    """
    try:
        # Parse the request JSON
        data = request.json
        latest_message = data.get("message", "")
        chat_history = data.get("chat_history", [])

        # Convert chat history into `Interaction` objects
        past_interactions = [
            assistant.Interaction(
                source=assistant.Interaction.Source.HUMAN
                if chat["role"] == "user" else
                assistant.Interaction.Source.AI,
                message=chat["text"]) for chat in chat_history
        ]

        # Use prompt_bot to generate the bot response
        bot_response = assistant.prompt_bot(past_interactions, latest_message)

        # Return the generated response
        return jsonify({"bot_response": bot_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
