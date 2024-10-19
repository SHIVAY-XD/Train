import requests
from datetime import datetime

# Constants
BASE_URL = "https://www.indianrail.gov.in"
TRAIN_SEARCH_URL = f"{BASE_URL}/cgi_bin/inet_trnssrch.cgi"
AVAILABILITY_URL = f"{BASE_URL}/cgi_bin/inet_accavl_cgi1.cgi"

def fetch_trains(source, destination, date):
    print(f"Fetching trains from {source} to {destination} on {date}...")
    params = {
        "lccp": "Search",
        "from": source,
        "to": destination,
        "date": date,
    }
    try:
        response = requests.get(TRAIN_SEARCH_URL, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        print(f"Response status code: {response.status_code}")
        print(f"Raw response: {response.content.decode()}")
        
        trains = parse_trains(response.text)
        print(f"Trains found: {trains}")
        return trains
    except requests.exceptions.RequestException as e:
        print(f"Error fetching trains: {e}")
        return {}

def parse_trains(response_text):
    # Sample parsing logic (replace with your actual logic)
    trains = {}
    raw_trains = response_text.split('~')[1:]  # Adjust based on actual response format
    for train in raw_trains:
        details = train.split('~')
        if len(details) > 2:
            train_number = details[0]
            train_name = details[1]
            trains[train_number] = train_name
    return trains

def check_availability(train_number):
    print(f"Checking availability for {train_number}...")
    params = {
        "trainno": train_number,
        # Add other necessary params here
    }
    try:
        response = requests.get(AVAILABILITY_URL, params=params)
        response.raise_for_status()
        print(f"Response status code: {response.status_code}")
        # Parse availability logic here
    except requests.exceptions.RequestException as e:
        print(f"Error checking availability: {e}")

def main():
    source = "LTT"  # Lokmanyatilak Terminus
    destination = "BSB"  # Varanasi Junction
    date = datetime.now().strftime("%Y-%m-%d")  # Today's date in YYYY-MM-DD format

    trains = fetch_trains(source, destination, date)
    for train_number in trains.keys():
        check_availability(train_number)

if __name__ == "__main__":
    main()
