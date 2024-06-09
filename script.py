import json
import requests
import time
from colorama import init, Fore
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Initialize colorama
init(autoreset=True)

# Load data from JSON file
with open('data.json', 'r') as file:
    shops_data = json.load(file)

# Base URL for Shopify API version
api_version = '2024-04'

# Webhook callback URLs
OLD_WEBHOOK_CALLBACK_URL = 'old-webhook-callback-url.herokuapp.com'
NEW_WEBHOOK_CALLBACK_URL = 'new-webhook-callback-url.herokuapp.com'

# Retry strategy
retry_strategy = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS", "PUT"]
)

adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)

# Iterate over each shop in the JSON data
for shop_data in shops_data:
    # Check if 'shop' and 'accessToken' fields are present
    if 'shop' not in shop_data or 'accessToken' not in shop_data:
        print(Fore.YELLOW + f"Skipping object because it is missing 'shop' or 'accessToken': {shop_data}")
        continue

    shop = shop_data['shop']
    access_token = shop_data['accessToken']

    print(f"Processing shop: {shop}")

    # First API call to get webhooks
    url = f'https://{shop}/admin/api/{api_version}/webhooks.json'
    headers = {
        'X-Shopify-Access-Token': access_token
    }

    try:
        response = http.get(url, headers=headers)
        if response.status_code != 200:
            print(Fore.RED + f"Failed to get webhooks for shop {shop}: {response.status_code}, {response.text}")
            continue

        print(f"Response for GET {url}: {response.status_code}, {response.json()}")
        webhooks = response.json().get('webhooks', [])

        # Iterate over each webhook in the response
        for webhook in webhooks:
            webhook_id = webhook['id']
            new_address = webhook['address'].replace(OLD_WEBHOOK_CALLBACK_URL, NEW_WEBHOOK_CALLBACK_URL)

            # Second API call to update each webhook
            update_url = f'https://{shop}/admin/api/{api_version}/webhooks/{webhook_id}.json'
            update_headers = {
                'X-Shopify-Access-Token': access_token,
                'Content-Type': 'application/json'
            }
            update_data = {
                "webhook": {
                    "id": webhook_id,
                    "address": new_address
                }
            }

            update_response = http.put(update_url, headers=update_headers, json=update_data)
            if update_response.status_code != 200:
                print(Fore.RED + f"Failed to update webhook {webhook_id} for shop {shop}: {update_response.status_code}, {update_response.text}")
            else:
                print(f"Successfully updated webhook {webhook_id} for shop {shop}: {update_response.status_code}, {update_response.json()}")

            # Delay to prevent rate limiting
            time.sleep(1)
        print(f'----------- Store Execution Complete --------------')

    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Request failed for shop {shop}: {e}")

print("Script execution completed.")
