import logging
import requests
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Global variable to hold user data
user_data = {}

# Function to start the bot and greet the user
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton("Search Trains", callback_data='search_trains')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome! Click the button below to search for trains.", reply_markup=reply_markup)

# Function to handle button clicks
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'search_trains':
        await query.edit_message_text("Please provide your 'from' location:")
        return

# Function to handle user text input
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id

    if user_id not in user_data:
        user_data[user_id] = {}

    if 'from' not in user_data[user_id]:
        user_data[user_id]['from'] = update.message.text
        await update.message.reply_text("Please provide your destination:")
    elif 'destination' not in user_data[user_id]:
        user_data[user_id]['destination'] = update.message.text
        await update.message.reply_text("Please provide your travel date (format: DD-MM-YYYY):")
    elif 'date' not in user_data[user_id]:
        user_data[user_id]['date'] = update.message.text
        await fetch_train_details(update, context, user_id)

# Function to fetch train details
async def fetch_train_details(update, context, user_id):
    from_location = user_data[user_id]['from'].strip().upper()
    destination = user_data[user_id]['destination'].strip().upper()
    travel_date_input = user_data[user_id]['date'].strip()

    # Convert date from DD-MM-YYYY to YYYYMMDD
    try:
        travel_date = datetime.strptime(travel_date_input, "%d-%m-%Y").strftime("%Y%m%d")
    except ValueError:
        await update.message.reply_text("Please enter the date in the correct format: DD-MM-YYYY.")
        return

    # Construct the URL
    url = f"https://www.goibibo.com/trains/dsrp/{from_location}/{destination}/{travel_date}/"
    logging.info(f"Constructed URL: {url}")
    
    # Fetch train details
    response = requests.get(url)
    logging.info(f"Response Status Code: {response.status_code}")

    # Check response status
    if response.status_code == 200:
        await update.message.reply_text(f"Train details URL: {url}\n\n(Parsing and displaying train details can be added here.)")
    else:
        await update.message.reply_text("Failed to fetch train details. Please try again later.")
        logging.info(f"Response Content: {response.text}")  # Log response content for debugging

    # Clear user data for the next search
    del user_data[user_id]

# Main function to run the bot
def main():
    # Replace 'YOUR_TOKEN' with your actual bot token
    application = ApplicationBuilder().token("6996568724:AAFrjf88-0uUXJumDiuV6CbVuXCJvT-4KbY").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    application.run_polling()

if __name__ == '__main__':
    main()
