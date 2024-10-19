import logging
import requests
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Global variable to hold user input
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

    # Handle responses based on the state of the conversation
    if 'from' not in user_data:
        user_data['from'] = query.message.text
        await query.edit_message_text("Please provide your destination:")
        return
    elif 'destination' not in user_data:
        user_data['destination'] = query.message.text
        await query.edit_message_text("Please provide your travel date (format: DD-MM-YYYY):")
        return
    elif 'date' not in user_data:
        user_data['date'] = query.message.text
        await fetch_train_details(query, context)

# Function to fetch train details
async def fetch_train_details(query, context):
    from_location = user_data['from'].strip().upper()
    destination = user_data['destination'].strip().upper()
    travel_date_input = user_data['date'].strip()

    # Convert date from DD-MM-YYYY to YYYYMMDD
    try:
        travel_date = datetime.strptime(travel_date_input, "%d-%m-%Y").strftime("%Y%m%d")
    except ValueError:
        await query.edit_message_text("Please enter the date in the correct format: DD-MM-YYYY.")
        return

    # Construct the URL
    url = f"https://www.goibibo.com/trains/dsrp/{from_location}/{destination}/{travel_date}/"
    
    # Fetch train details (placeholder)
    response = requests.get(url)

    # For demonstration, we'll just return the URL
    if response.status_code == 200:
        await query.edit_message_text(f"Train details URL: {url}\n\n(Parsing and displaying train details can be added here.)")
    else:
        await query.edit_message_text("Failed to fetch train details. Please try again later.")

    # Clear user data for the next search
    user_data.clear()

# Main function to run the bot
def main():
    # Replace 'YOUR_TOKEN' with your actual bot token
    application = ApplicationBuilder().token("6996568724:AAFrjf88-0uUXJumDiuV6CbVuXCJvT-4KbY").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()

if __name__ == '__main__':
    main()
