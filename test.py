import requests
from bs4 import BeautifulSoup

def find_trains(stn_from, stn_to):
    try:
        request_url = f"http://erail.in/rail/getTrains.aspx?Station_From={stn_from}&Station_To={stn_to}&DataSource=0&Language=0"
        response = requests.get(request_url)
        response.raise_for_status()
        
        trains = {}
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract train details (this part may need adjustment based on actual HTML structure)
        train_rows = soup.find_all('tr')
        for row in train_rows:
            cols = row.find_all('td')
            if len(cols) > 1:
                train_number = cols[0].text.strip()
                train_name = cols[1].text.strip()
                trains[train_number] = train_name
        
        return trains
    except Exception as e:
        print(f"Error fetching train list: {e}")
        return {}

def find_availability(args):
    post_data = {
        'lccp_day': args['day'],
        'lccp_month': args['month'],
        'lccp_year': args['year'],
        'lccp_class1': args['class'],
        'lccp_quota': args['quota'],
        'lccp_trndtl': f"{args['train_n']} {args['stn_from']} {args['stn_to']}",
        'lccp_classopt': 'ZZ',
        'lccp_age': 'ADULT_AGE'
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    request_url = "http://www.indianrail.gov.in/cgi_bin/inet_accavl_cgi1.cgi"
    
    try:
        response = requests.post(request_url, data=post_data, headers=headers, verify=False)  # Disable SSL verification for testing
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        date = f"{int(args['day']) + 1}-{args['month']}-{args['year']}"
        
        # Extract availability (adjust according to actual response structure)
        availability_info = soup.find(text=date)
        if availability_info:
            avail_status = availability_info.find_next().text.strip()
            if avail_status == 'AVAILABLE':
                avail_number = availability_info.find_next().find_next().text.strip()
                print(f"Train: {args['train_n']} - Available: {avail_number}")
            else:
                print(f"Train: {args['train_n']} - Status: {avail_status}")
    except Exception as e:
        print(f"Error fetching availability: {e}")

def lookup(trains, args):
    for train_n in trains.keys():
        args['train_n'] = train_n
        find_availability(args)

if __name__ == "__main__":
    from_station = 'GWL'  # Replace with your station
    to_station = 'MTJ'    # Replace with your destination
    trains = find_trains(from_station, to_station)
    
    args = {
        'stn_from': from_station,
        'stn_to': to_station,
        'day': '14',  # Example day
        'month': '10',  # Example month
        'year': '2024',  # Example year
        'class': '3A',  # Class of travel
        'quota': 'CK'   # Quota type
    }
    
    lookup(trains, args)
