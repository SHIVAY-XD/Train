import requests

def fetch_trains(from_station, to_station, travel_date):
    url = f"https://www.indianrail.gov.in/cgi_bin/inet_trnssrch.cgi?lccp=Search&from={from_station}&to={to_station}&date={travel_date}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an error for bad responses
        raw_data = response.text
        print("Raw response:", raw_data)

        trains = parse_trains(raw_data)
        print("Trains found:", trains)
        return trains

    except requests.exceptions.SSLError as ssl_err:
        print(f"SSL Error: {ssl_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Error fetching trains: {req_err}")

def parse_trains(raw_data):
    trains = {}
    lines = raw_data.split('^')
    
    for line in lines:
        details = line.split('~')
        if len(details) > 1:
            train_number = details[1]
            train_name = details[2]
            trains[train_number] = train_name
            
    return trains

if __name__ == "__main__":
    from_station = "LTT"  # Lokmanyatilak
    to_station = "BSB"    # Varanasi Junction
    travel_date = "2024-10-19"

    print(f"Fetching trains from {from_station} to {to_station} on {travel_date}...")
    fetch_trains(from_station, to_station, travel_date)
