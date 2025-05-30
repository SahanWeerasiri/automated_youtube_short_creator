import os
import dotenv
import asyncio
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext
)

# Load environment variables
dotenv.load_dotenv()
TOKEN = dotenv.get_key(dotenv.find_dotenv(), "BOT_TOKEN")

async def start(update: Update, context: CallbackContext) -> None:
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
        "Welcome! Choose a web app to use:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_web_app_data(update: Update, context: CallbackContext) -> None:
    """Handle data received from the web app."""
    try:
        web_app_data = update.effective_message.web_app_data
        data = json.loads(web_app_data.data)
        
        # Process the received data
        response_text = "✅ Received data from web app:\n\n"
        
        # Format the data for display
        if 'image' in data:
            response_text += "🖼️ Image data received\n"
            # You could save the image or process it further
            await update.message.reply_photo(photo=data['image'])
        elif 'text' in data:
            response_text += f"📝 Text received: {data['text']}\n"
        
        # Add raw data for debugging
        response_text += f"\nRaw data:\n{json.dumps(data, indent=2)}"
        
        await update.message.reply_text(response_text)
        
    except json.JSONDecodeError:
        await update.message.reply_text("⚠️ Received invalid data from web app")
    except Exception as e:
        await update.message.reply_text(f"❌ Error processing web app data: {str(e)}")

async def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_web_app_data))
    
    # Run the bot
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    
    print("Bot is running...")
    
    # Keep running until interrupted
    while True:
        await asyncio.sleep(3600)

if __name__ == '__main__':
    asyncio.run(main())