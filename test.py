import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

def fetch_train_details(from_location, destination, travel_date_input):
    # Convert date from DD-MM-YYYY to YYYYMMDD
    try:
        travel_date = datetime.strptime(travel_date_input, "%d-%m-%Y").strftime("%Y%m%d")
    except ValueError:
        print("Please enter the date in the correct format: DD-MM-YYYY.")
        return

    # Construct the URL
    url = f"https://www.goibibo.com/trains/dsrp/{from_location}/{destination}/{travel_date}/"
    print(f"Constructed URL: {url}")

    # Set headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    }

    # Retry parameters
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print("Making request...")
            response = requests.get(url, headers=headers, timeout=30)  # Increased timeout
            response.raise_for_status()
            print("Request made successfully.")
            break
        except requests.exceptions.Timeout:
            print(f"Attempt {attempt + 1} timed out. Retrying...")
            time.sleep(2)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return

    # Process the response if successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract train details
        trains = []
        for train in soup.find_all('div', class_='train-listing'):
            train_name = train.find('h3', class_='train-name').text.strip()
            train_number = train.find('p', class_='train-number').text.strip()
            from_time = train.find('div', class_='from-time').text.strip()
            to_time = train.find('div', class_='to-time').text.strip()
            duration = train.find('div', class_='duration').text.strip()

            trains.append(f"Train: {train_name} ({train_number})\nDeparture: {from_time}\nArrival: {to_time}\nDuration: {duration}\n")

        # Print train details
        if trains:
            print("\n".join(trains))
        else:
            print("No trains found for your search.")
    else:
        print(f"Failed to fetch train details. Status Code: {response.status_code}")

# Example usage
from_location = "LTT"  # Example: Mumbai LTT
destination = "BSB"    # Example: Varanasi
travel_date_input = "01-11-2024"  # Example date

fetch_train_details(from_location, destination, travel_date_input)
