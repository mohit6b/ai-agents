from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes and all origins (you can configure it more specifically if needed)
CORS(app, origins=["http://localhost:5173"])  # Allow only your frontend origin

# Store user sessions (basic in-memory approach; consider persistent storage for production)
user_sessions = {}

class FoodOrderingAgent:
    def __init__(self):
        self.user_context = {}  # Store context like user preferences, address, etc.

    def process_user_message(self, user_id, message):
        """Process user instructions and respond accordingly."""
        if user_id not in self.user_context:
            self.user_context[user_id] = {"stage": "greeting"}

        context = self.user_context[user_id]
        stage = context["stage"]

        if stage == "greeting":
            response = "Hi! What food would you like to order today? 😊"
            context["stage"] = "food_query"
            return response

        elif stage == "food_query":
            food_choice = message.strip()
            context["food_choice"] = food_choice
            context["stage"] = "address_query"
            return f"Great choice! You want to order {food_choice}. Can you provide your delivery address?"

        elif stage == "address_query":
            address = message.strip()
            context["address"] = address
            context["stage"] = "payment_query"
            return "Thanks! Now, could you provide your payment details (e.g., card number)?"

        elif stage == "payment_query":
            payment = message.strip()
            context["payment"] = payment
            context["stage"] = "order_confirmation"
            return f"Thank you! I have your order and payment details. Should I go ahead and place the order? (yes/no)"

        elif stage == "order_confirmation":
            if "yes" in message.lower():
                food_choice = context["food_choice"]
                address = context["address"]
                payment = context["payment"]

                # Mock order placement
                order_status = self.place_order(food_choice, address, payment)
                if order_status:
                    self.user_context[user_id] = {"stage": "greeting"}  # Reset the session
                    return f"Your order for {food_choice} has been successfully placed! It will arrive soon. 🍔"
                else:
                    return "Sorry, there was an issue placing your order. Please try again later."
            else:
                self.user_context[user_id] = {"stage": "greeting"}  # Reset the session
                return "Okay, let me know if you'd like to order anything else!"

    def place_order(self, food, address, payment_details):
        """Mock order placement."""
        try:
            # Simulating a successful order placement
            return True
        except Exception as e:
            logger.error(f"Error placing order: {e}")
            return False

# Initialize the agent
agent = FoodOrderingAgent()

@app.route('/ai-agent', methods=['POST'])
def ai_agent():
    """Endpoint to interact with the AI agent."""
    try:
        user_id = request.json.get("user_id")  # Unique user identifier
        message = request.json.get("message")  # User input message

        if not user_id or not message:
            return jsonify({"error": "user_id and message are required"}), 400

        response = agent.process_user_message(user_id, message)
        return jsonify({"response": response}), 200
    except Exception as e:
        logger.error(f"Error in /ai-agent: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
