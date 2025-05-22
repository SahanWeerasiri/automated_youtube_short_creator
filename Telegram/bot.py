import os
import dotenv
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Load environment variables
dotenv.load_dotenv()
TOKEN = dotenv.get_key(dotenv.find_dotenv(), "BOT_TOKEN")
SECOND_BOT_TOKEN = dotenv.get_key(dotenv.find_dotenv(), "SECOND_BOT_TOKEN")  # Add this to your .env file

# Create uploads directory structure
UPLOAD_FOLDER = "bot_uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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

async def start_second_bot() -> None:
    """Start and run the second bot."""
    application = Application.builder().token(SECOND_BOT_TOKEN).build()
    
    # Add your second bot's handlers here
    # application.add_handler(CommandHandler("start", second_bot_start))
    
    await application.initialize()
    await application.start()
    await application.updater.start_polling()  # or webhook if you prefer

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