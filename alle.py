import requests
import json
from threading import Thread

def fetch_item_mapping():
    url = 'https://prices.runescape.wiki/api/v1/osrs/mapping'
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        return {item['id']: item['name'] for item in data}
    else:
        return {}

def fetch_hourly_trading_data():
    url = 'https://prices.runescape.wiki/api/v1/osrs/1h'
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        # Assuming the data format is {'data': {'item_id': {'lowPriceVolume': volume, ...}, ...}}
        return {int(item_id): details for item_id, details in data['data'].items() if details.get('lowPriceVolume', 0) > 20}
    else:
        return {}

def fetch_item_data(item_id, all_data, item_mapping, trading_data):
    headers = {'User-Agent': 'findingmerches-#Teh_Jack#2746'}
    url = f'https://prices.runescape.wiki/api/v1/osrs/latest?id={item_id}'
    try:
        if item_id in trading_data:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = json.loads(response.text)
                if str(item_id) in data['data']:
                    item_info = data['data'][str(item_id)]
                    low_price = item_info['low']
                    high_price = item_info['high']
                    if low_price is not None and high_price is not None and low_price > 300000 and high_price > 300000:
                        profit = high_price - low_price
                        roi = (profit / low_price) * 100
                        item_name = item_mapping.get(item_id, f'Item {item_id}')
                        all_data.append((item_name, item_id, profit, roi))
    except Exception as e:
        pass

# Fetch item mapping and hourly trading data
item_mapping = fetch_item_mapping()
trading_data = fetch_hourly_trading_data()

# Variables
num_threads = 10
batch_size = 500
all_data = []

# Process items in batches
for batch_start in range(1, 50001, batch_size):
    threads = []
    for item_id in range(batch_start, batch_start + batch_size):
        thread = Thread(target=fetch_item_data, args=(item_id, all_data, item_mapping, trading_data))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # Sort all_data by ROI
    sorted_data = sorted(all_data, key=lambda x: x[3], reverse=True)

    # Print top items by ROI
    print(f"Top items by ROI for item IDs {batch_start} to {batch_start + batch_size - 1}:")
    for name, item_id, profit, roi in sorted_data[:10]:
        formatted_profit = f"{profit / 1000:.1f}K" if profit > 10000 else str(profit)
        print(f"  {name} (ID: {item_id}): Profit {formatted_profit} coins ({roi:.2f}%)")

# Print final top items by ROI
print("Final Top Items by ROI:")
for name, item_id, profit, roi in sorted_data[:10]:
    formatted_profit = f"{profit / 1000:.1f}K" if profit > 10000 else str(profit)
    print(f"  {name} (ID: {item_id}): Profit {formatted_profit} coins ({roi:.2f}%)")
