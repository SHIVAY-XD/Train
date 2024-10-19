import requests
import re
from bs4 import BeautifulSoup

def find_trains(stn_from, stn_to):
    url = f"http://erail.in/rail/getTrains.aspx?Station_From={stn_from}&Station_To={stn_to}&DataSource=0&Language=0"
    response = requests.get(url)
    response.raise_for_status()
    
    re_train_item = re.compile(r'\^\d+\~[A-Za-z0-9 ]+')
    re_train_name = re.compile(r'~[A-Za-z0-9 ]+')
    re_train_number = re.compile(r'\^\d+')
    
    trains = {}
    train_items = re_train_item.findall(response.text)
    
    for train_item in train_items:
        train_number = re_train_number.search(train_item).group()[1:]
        train_name = re_train_name.search(train_item).group()[1:]
        trains[train_number] = train_name
    
    return trains

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
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    request_url = "http://www.indianrail.gov.in/cgi_bin/inet_accavl_cgi1.cgi"
    response = requests.post(request_url, data=post_data, headers=headers)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    date = f"{int(args['day']) + 1}-{args['month']}-{args['year']}"
    
    tds = soup.find(text=re.compile('S.No.'))
    try:
        td_text = tds.parent.parent.parent.find(text=re.compile(date)).next.next.next
    except Exception as e:
        print(f"Error finding availability: {e}")
        return
    
    avail_text = td_text
    avail_stat = re.search(r'\w+', avail_text).group()
    
    if avail_stat == 'AVAILABLE':
        avail_n = re.search(r'\d+', avail_text).group()
        print(f"{args['train_n']} {avail_n}")
    
    return

def lookup(trains, args):
    for train_n in trains.keys():
        args['train_n'] = train_n
        find_availability(args)

# Example usage
trains = find_trains('GWL', 'MTJ')
args = {
    'stn_from': 'KYN',
    'stn_to': 'GWL',
    'day': '14',
    'month': '10',
    'year': '2023',
    'class': '3A',
    'quota': 'CK'
}
lookup(trains, args)
