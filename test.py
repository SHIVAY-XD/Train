import requests
import json
import re

def fetch_trains(from_station, to_station, travel_date):
    url = f"https://www.indianrail.gov.in/cgi_bin/inet_trnssrch.cgi?lccp=Search&from={from_station}&to={to_station}&date={travel_date}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        
        data = response.text
        print("Raw response:", data)

        trains = parse_trains(data)
        print("Trains found:", trains)

    except requests.exceptions.SSLError as ssl_err:
        print(f"SSL Error: {ssl_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Error fetching trains: {req_err}")

def parse_trains(data):
    # Extract train information from the raw response
    train_info_pattern = re.compile(r'~(\d+)~([^~]+)~')
    trains = {}
    
    matches = train_info_pattern.findall(data)
    for train_number, train_name in matches:
        trains[train_number] = train_name.strip()
    
    return trains

if __name__ == "__main__":
    from_station = "LTT"  # Lokmanyatilak
    to_station = "BSB"    # Varanasi Jn
    travel_date = "2024-10-19"

    print(f"Fetching trains from {from_station} to {to_station} on {travel_date}...")
    fetch_trains(from_station, to_station, travel_date)
