import ssl
import requests

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

    # Create a new SSL context
    ssl_context = ssl.create_default_context()
    ssl_context.options |= ssl.OP_NO_SSLv3  # Disable SSLv3

    request_url = "https://www.indianrail.gov.in/cgi_bin/inet_accavl_cgi1.cgi"

    try:
        response = requests.post(request_url, data=post_data, headers=headers, verify=ssl_context)
        response.raise_for_status()
        print(f"Response received for {args['train_n']}: {response.text[:100]}...")  # Print first 100 chars for brevity
    except requests.RequestException as e:
        print(f"Error checking availability: {e}")
