import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Global variables to hold user input
user_data = {}

# Function to start the bot and greet the user
def start(update: Update, context: CallbackContext) -> None:
    keyboard = [[InlineKeyboardButton("Search Trains", callback_data='search_trains')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Welcome! Click the button below to search for trains.", reply_markup=reply_markup)

# Function to handle button clicks
def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == 'search_trains':
        query.edit_message_text("Please provide your 'from' location:")
        return

    # Handle responses based on the state of the conversation
    if 'from' not in user_data:
        user_data['from'] = query.message.text
        query.edit_message_text("Please provide your destination:")
        return
    elif 'destination' not in user_data:
        user_data['destination'] = query.message.text
        query.edit_message_text("Please provide your travel date (format: YYYYMMDD):")
        return
    elif 'date' not in user_data:
        user_data['date'] = query.message.text
        fetch_train_details(query, context)

# Function to fetch train details
def fetch_train_details(query, context):
    from_location = user_data['from'].strip().upper()
    destination = user_data['destination'].strip().upper()
    travel_date = user_data['date'].strip()

    if len(travel_date) != 8 or not travel_date.isdigit():
        query.edit_message_text("Please enter the date in the format YYYYMMDD.")
        return

    # Construct the URL
    url = f"https://www.goibibo.com/trains/dsrp/{from_location}/{destination}/{travel_date}/"
    
    # Fetch train details (placeholder)
    response = requests.get(url)

    # For demonstration, we'll just return the URL
    if response.status_code == 200:
        query.edit_message_text(f"Train details URL: {url}\n\n(Parsing and displaying train details can be added here.)")
    else:
        query.edit_message_text("Failed to fetch train details. Please try again later.")

    # Clear user data for the next search
    user_data.clear()

# Main function to run the bot
def main():
    # Replace 'YOUR_TOKEN' with your actual bot token
    updater = Updater("6996568724:AAFrjf88-0uUXJumDiuV6CbVuXCJvT-4KbY")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
