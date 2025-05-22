from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Updater, CommandHandler, CallbackContext
import dotenv
from telegram.ext import Application, CommandHandler

dotenv.load_dotenv()
TOKEN = dotenv.get_key(dotenv.find_dotenv(), "BOT_TOKEN")

async def start(update: Update, _context: CallbackContext) -> None:
    # Create a button that opens the Web App
    keyboard = [
        [InlineKeyboardButton(
            "Open Full Screen", 
            web_app=WebAppInfo(url="https://gameforge.com/en-US/littlegames/monster-up/#")
        )]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Click below to open full screen view:",
        reply_markup=reply_markup
    )
def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

if __name__ == '__main__':
    main()