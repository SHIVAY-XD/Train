import requests
from bs4 import BeautifulSoup

def find_trains(stn_from, stn_to):
    print(f"Fetching trains from {stn_from} to {stn_to}...")
    try:
        response = requests.get(f"http://erail.in/rail/getTrains.aspx?Station_From={stn_from}&Station_To={stn_to}&DataSource=0&Language=0")
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching trains: {e}")
        return {}
    
    # Print the raw response for debugging
    print("Raw response:", response.text[:1000])  # Print first 1000 chars for brevity
    
    soup = BeautifulSoup(response.content, 'html.parser')
    trains = {}
    
    # Adjust the following selector based on the actual HTML structure
    for train in soup.select('tr'):
        columns = train.find_all('td')
        if len(columns) >= 2:
            train_number = columns[1].text.strip()
            train_name = columns[2].text.strip()
            trains[train_number] = train_name
    
    return trains

def find_availability(args):
    print(f"Checking availability for {args['train_n']}...")
    post_data = {
        'lccp_day': args['day'],
        'lccp_month': args['month'],
        'lccp_year': args['year'],
        'lccp_class1': args['class'],
        'lccp_quota': args['quota'],
        'lccp_trndtl': f"{args['train_n']} {args['stn_from']} {args['stn_to']}",
        'lccp_age': 'ADULT_AGE',
        'lccp_conc': 'ZZZZZZ'
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    request_url = "http://www.indianrail.gov.in/cgi_bin/inet_accavl_cgi1.cgi"
    
    try:
        response = requests.post(request_url, data=post_data, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        print(f"Response received for {args['train_n']}: {response.text[:100]}...")  # Print first 100 chars for brevity
    except requests.RequestException as e:
        print(f"Error checking availability: {e}")
        return

    # Check for availability based on the actual response format
    available = soup.find(text='Available')
    if available:
        print(f"{args['train_n']} is available!")
    else:
        print(f"{args['train_n']} is not available.")

def lookup(trains, args):
    for train_n in trains.keys():
        args['train_n'] = train_n
        find_availability(args)

if __name__ == "__main__":
    from_station = 'LTT'  # Example starting station
    to_station = 'BSB'    # Example destination station
    trains = find_trains(from_station, to_station)
    print("Trains found:", trains)
    
    args = {
        'stn_from': from_station,
        'stn_to': to_station,
        'day': '01',
        'month': '11',
        'year': '2024',
        'class': '3A',
        'quota': 'GN'
    }
    
    if trains:
        lookup(trains, args)
    else:
        print("No trains found.")
