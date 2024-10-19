import requests
from bs4 import BeautifulSoup
from datetime import datetime

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
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Fetch train details
    try:
        response = requests.get(url, headers=headers)
        print(f"Response Status Code: {response.status_code}")

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')
            trains = []

            for train in soup.find_all('div', class_='train-listing'):
                train_name = train.find('h3', class_='train-name').text.strip()
                train_number = train.find('p', class_='train-number').text.strip()
                from_time = train.find('div', class_='from-time').text.strip()
                to_time = train.find('div', class_='to-time').text.strip()
                duration = train.find('div', class_='duration').text.strip()

                trains.append(f"Train: {train_name} ({train_number})\nDeparture: {from_time}\nArrival: {to_time}\nDuration: {duration}\n")

            if trains:
                print("\n".join(trains))
            else:
                print("No trains found for your search.")
        else:
            print("Failed to fetch train details. Please try again later.")

    except Exception as e:
        print(f"An error occurred while fetching train details: {e}")

# Example usage
from_location = "LTT"  # Example: Mumbai LTT
destination = "BSB"    # Example: Varanasi
travel_date_input = "01-11-2024"  # Example date

fetch_train_details(from_location, destination, travel_date_input)
