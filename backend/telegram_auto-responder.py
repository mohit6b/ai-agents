from telethon import TelegramClient, events
import re
from datetime import datetime, timedelta
import asyncio
import logging
import os
from dotenv import load_dotenv
import random
import requests
import json

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                   level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram API credentials
API_ID = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')
SESSION_NAME = "my_telegram_session"

# Initialize client
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# Ollama API endpoints
OLLAMA_BASE_URL = "http://localhost:11434/api"
OLLAMA_GENERATE_URL = f"{OLLAMA_BASE_URL}/generate"
OLLAMA_MODEL = "llama3"  # or whatever model name you're using locally

class MessageHandler:
    def __init__(self):
        self.context = {}  # Store conversation context per user

    async def get_llm_response(self, prompt, user_id):
        """Get response from Llama model via Ollama API"""
        try:
            full_prompt = f"""
    You are a friendly and social human, not an AI.Respond like a real person would. Avoid stating that you are an AI.

    User: {prompt}

    Respond like a natural human.
    """
            payload = {
                "model": OLLAMA_MODEL,
                "prompt": full_prompt,
                "stream": False
            }
            logger.info(f"Sending payload: {json.dumps(payload, indent=2)}")

            response = requests.post(OLLAMA_GENERATE_URL, json=payload, timeout=30)

            if response.status_code == 200:
                response_data = response.json()
                logger.info(f"Ollama response: {response_data}")
                return response_data.get("response", "I couldn't generate a response.")
            else:
                logger.error(f"Ollama API error: {response.status_code}, Response: {response.text}")
                return self.get_fallback_response(prompt)

        except Exception as e:
            logger.error(f"Error getting LLM response: {str(e)}")
            return self.get_fallback_response(prompt)

    def get_fallback_response(self, message):
        """Generate fallback response when LLM fails"""
        patterns = {
            r'(?i).*\b(lunch|eat|dining)\b.*': "How about having lunch tomorrow at 12:30 PM?",
            r'(?i).*\b(meet|meeting)\b.*': "Would you like to meet tomorrow at 2 PM?",
            r'(?i).*\b(hi|hello|hey)\b.*': "Hello! How can I help you today?",
            r'(?i).*\b(thanks|thank you)\b.*': "You're welcome! 😊",
        }
        
        for pattern, response in patterns.items():
            if re.match(pattern, message):
                return response
        
        return "I received your message. How can I help you?"

# Initialize message handler
message_handler = MessageHandler()

@client.on(events.NewMessage)
async def handle_message(event):
    """Handle incoming messages using LLM"""
    try:
        # Get the sender's information
        sender = await event.get_sender()
        message = event.message.text
        user_id = str(sender.id)
        
        # Only respond to messages in private chats or where bot has admin rights
        if event.is_private:
            # Get response from LLM
            response = await message_handler.get_llm_response(message, user_id)
            
            # Send the response
            await event.respond(response)
            logger.info(f"Sent LLM response to {sender.first_name}")
        
    except Exception as e:
        logger.error(f"Error handling message: {str(e)}")

async def main():
    """Main function to run the client."""
    try:
        logger.info("Starting Telegram auto-responder with Llama integration...")

        logger.info(f"TELEGRAM_API_ID: {API_ID}, TELEGRAM_API_HASH: {API_HASH}")
        
        # Start the client
        try:
            logger.info("Attempting to start the Telegram client...")
#            logging.getLogger('telethon').setLevel(logging.DEBUG)
            await client.start()
            logger.info("Client Started SUCCESSFULLY")
        except Exception as e:
            logger.error(f"Failed to start Telegram client: {str(e)}")
        
        # Inform that bot is running
        logger.info("Auto-responder is now running. Press Ctrl+C to stop.")
        
        # Keep the script running
        await client.run_until_disconnected()
        
    except Exception as e:
        logger.error(f"Error in main function: {str(e)}")
    finally:
        await client.disconnect()

if __name__ == '__main__':
    # Run the main function
    asyncio.run(main())