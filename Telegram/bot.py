import os
import dotenv
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import json
import http
# Load environment variables
dotenv.load_dotenv()
TOKEN = dotenv.get_key(dotenv.find_dotenv(), "BOT_TOKEN")
SECOND_BOT_TOKEN = dotenv.get_key(dotenv.find_dotenv(), "SECOND_BOT_TOKEN")  # Add this to your .env file

# Create uploads directory structure
UPLOAD_FOLDER = "bot_uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global variable to store the target chat ID
target_chat_id = None

async def send_keep_alive_message():
    """Send keep alive message to the second bot using stored chat ID."""
    global target_chat_id
    
    if target_chat_id is None:
        print("No target chat ID set yet - skipping keep alive message")
        return
        
    try:
        conn = http.client.HTTPSConnection("api.telegram.org")
        url = f"/bot{SECOND_BOT_TOKEN}/sendMessage"
        payload = json.dumps({
            'chat_id': target_chat_id,
            'text': 'Keep alive - bot is running'
        })
        headers = {
            'Content-Type': 'application/json'
        }
        conn.request("POST", url, body=payload, headers=headers)
        response = conn.getresponse()
        resp_data = response.read().decode()
        if response.status != 200:
            print(f"Error sending keep alive message: {resp_data}")
        else:
            print("Keep alive message sent successfully")
        conn.close()
    except Exception as e:
        print(f"Error in send_keep_alive_message: {e}")


async def start(update: Update, _context: CallbackContext) -> None:
    """Send welcome message with web app buttons."""
    keyboard = [
        [InlineKeyboardButton(
            "AI Image Generator", 
            web_app=WebAppInfo(url="https://perchance.org/unrestricted-ai-image-generator")
        )],
        [InlineKeyboardButton(
            "Base64 Image Processor", 
            web_app=WebAppInfo(url="https://v0-next-js-image-upload-gamma.vercel.app")
        )]
    ]
    
    await update.message.reply_text(
        "Welcome! Choose an option below:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def second_bot_start(update: Update, _context: CallbackContext) -> None:
    """Handle the start command for the second bot."""
    global target_chat_id
    target_chat_id = update.message.chat.id  # Store the chat ID for keep alive messages
    await update.message.reply_text("Second bot started! Keep alive messages will be sent to this chat.")

async def start_second_bot() -> None:
    """Start and run the second bot."""
    application = Application.builder().token(SECOND_BOT_TOKEN).build()
    
    # Add your second bot's handlers here
    application.add_handler(CommandHandler("start", second_bot_start))
    
    await application.initialize()
    await application.start()

    await application.updater.start_polling()  # or webhook if you prefer
    # Send keep alive message every 5 minutes
    while True:
        await send_keep_alive_message()
        await asyncio.sleep(3600)  # Sleep for 1 hour

async def main() -> None:
    """Start both bots simultaneously."""
    # Create and configure the first bot
    first_bot = Application.builder().token(TOKEN).build()
    first_bot.add_handler(CommandHandler("start", start))
    
    # Initialize both bots
    await first_bot.initialize()
    await first_bot.start()
    await first_bot.updater.start_polling()
    
    # Start the second bot in parallel
    await start_second_bot()
    
    # Keep running until interrupted
    while True:
        await asyncio.sleep(3600)  # Sleep for 1 hour and repeat

if __name__ == '__main__':
    asyncio.run(main())