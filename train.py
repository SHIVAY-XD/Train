import logging
import requests
from datetime import datetime
from bs4 import BeautifulSoup
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

# Function to fetch and scrape train details
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

    # Set headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Fetch train details
    try:
        response = requests.get(url, headers=headers)
        logging.info(f"Response Status Code: {response.status_code}")

        # Check response status
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')

            # Extract train details (adjust selectors as necessary)
            trains = []
            for train in soup.find_all('div', class_='train-listing'):
                train_name = train.find('h3', class_='train-name').text.strip()
                train_number = train.find('p', class_='train-number').text.strip()
                from_time = train.find('div', class_='from-time').text.strip()
                to_time = train.find('div', class_='to-time').text.strip()
                duration = train.find('div', class_='duration').text.strip()

                trains.append(f"Train: {train_name} ({train_number})\nDeparture: {from_time}\nArrival: {to_time}\nDuration: {duration}\n")

            if trains:
                await update.message.reply_text("\n".join(trains))
            else:
                await update.message.reply_text("No trains found for your search.")
        else:
            await update.message.reply_text("Failed to fetch train details. Please try again later.")
            logging.info(f"Response Content: {response.text}")  # Log response content for debugging

    except Exception as e:
        await update.message.reply_text("An error occurred while fetching train details. Please try again.")
        logging.error(f"Error fetching train details: {e}")

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
