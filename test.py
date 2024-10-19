import http.client
import ssl
import json

def fetch_trains(from_station, to_station, travel_date):
    conn = http.client.HTTPSConnection("www.indianrail.gov.in", context=ssl.create_default_context())
    
    url = f"/cgi_bin/inet_trnssrch.cgi?lccp=Search&from={from_station}&to={to_station}&date={travel_date}"
    try:
        conn.request("GET", url)
        res = conn.getresponse()
        data = res.read().decode()
        
        print("Raw response:", data)
        trains = parse_trains(data)
        print("Trains found:", trains)

    except Exception as e:
        print(f"Error fetching trains: {e}")
    finally:
        conn.close()

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
