import requests
import json

def fetch_item_price(item_id, price_type):
    headers = {
        'User-Agent': 'findingmerches-#Teh_Jack#2746',
    }
    url = f'https://prices.runescape.wiki/api/v1/osrs/latest?id={item_id}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = json.loads(response.text)
        return data['data'][str(item_id)][price_type]
    else:
        return None

potion_variants = {
    "Stamina Potion": {
        1: 12631,
        2: 12629,
        3: 12627,
        4: 12625,
    },
    "Prayer Potion": {
        1: 143,
        2: 141,
        3: 139,
        4: 2434,
    },
    "Super Strength": {
        1: 161,
        2: 159,
        3: 157,
        4: 2440,
    },
    "Super Restore": {
        1: 3028,
        2: 3026,
        3: 3024,
        4: 3024,
    },
    "Super Combat": {
        1: 12701,
        2: 12699,
        3: 12697,
        4: 12695,
    },
    "Saradomin Brew": {
        1: 6691,
        2: 6689,
        3: 6687,
        4: 6685,
    },
    "Super Energy": {
        1: 3018,
        2: 3016,
        3: 3014,
        4: 3012,
    },
   "Bastion Potion": {
        1: 22470,
        2: 22467,
        3: 22464,
        4: 22461,
    },
    "Sanfew Serum": {
        1: 10931,
        2: 10929,
        3: 10927,
        4: 10925,
    },
    "Divine Bastion Potion": {
        1: 24644,
        2: 24641,
        3: 24638,
        4: 24635,
    },
    "Sanfew Serum": {
        1: 10931,
        2: 10929,
        3: 10927,
        4: 10925,
    },
    "Divine Battlemage Potion": {
        1: 24632,
        2: 24629,
        3: 24626,
        4: 24623,
    },
    "Divine Super Combat Potion": {
        1: 23694,
        2: 23691,
        3: 23688,
        4: 23685,
    },
    "Super Antifire Potion": {
        1: 21987,
        2: 21984,
        3: 21981,
        4: 21978,
    },
    "Anti-venom+": {
        1: 12919,
        2: 12917,
        3: 12915,
        4: 12913,
    },
    "Antidote++": {
        1: 5958,
        2: 5956,
        3: 5954,
        4: 5952,
    },
    "Guthix Rest": {
        1: 4423,
        2: 4421,
        3: 4419,
        4: 4417,
    },
    "Extended Super Antifire": {
        1: 22218,
        2: 22215,
        3: 22212,
        4: 22209,
    },
}

for potion_name, potion_ids in potion_variants.items():
    print(f"{potion_name}:")
    potion_prices = {}
    for doses, item_id in potion_ids.items():
        price_type = 'high' if doses == 4 else 'low'
        price = fetch_item_price(item_id, price_type)
        if price is not None:
            potion_prices[doses] = price

    potion_4_dose_price = potion_prices[4] / 4
    for doses, price in potion_prices.items():
        dose_price = price / doses
        price_difference = (potion_4_dose_price - dose_price) / potion_4_dose_price
        if price_difference > 0.05:
            print(f"  Price per dose of {potion_name} ({doses}): {dose_price:.2f}")
            print(f"  {potion_name} ({doses}) is more than 5% cheaper: {price_difference * 100:.2f}%")
    print()


# Add the correct item IDs for the godsword components and completed godswords
godsword_parts = {
    "Godsword Blade": 11818,  # Corrected item ID for Godsword Blade
    "Armadyl Hilt": 11810,
    "Bandos Hilt": 11812,
    "Saradomin Hilt": 11814,
    "Zamorak Hilt": 11816,
    "Ancient Hilt": 26370,  # Item ID for Ancient Hilt (example, please verify)
    "Armadyl Godsword": 11802,
    "Bandos Godsword": 11804,
    "Saradomin Godsword": 11806,
    "Zamorak Godsword": 11808,
    "Ancient Godsword": 26233,  # Item ID for Ancient Godsword (example, please verify)
}

# Define a function for formatting the price and profit
def format_price(value):
    return f"{value / 1000:.1f}K" if value > 10000 else str(value)

# Fetch prices and calculate profits and ROI
godsword_prices = {}
profits_and_roi = []
for part, item_id in godsword_parts.items():
    price = fetch_item_price(item_id, 'low' if 'Hilt' in part else 'high')
    if price is not None:
        godsword_prices[part] = price

for hilt in ["Armadyl Hilt", "Bandos Hilt", "Saradomin Hilt", "Zamorak Hilt", "Ancient Hilt"]:
    blade_price = godsword_prices.get("Godsword Blade", 0)
    hilt_price = godsword_prices.get(hilt, 0)
    combined_cost = blade_price + hilt_price
    godsword_name = f"{hilt.split(' ')[0]} Godsword"
    selling_price = godsword_prices.get(godsword_name, 0)

    profit = selling_price - combined_cost
    roi = (profit / combined_cost) * 100 if combined_cost else 0
    profits_and_roi.append((godsword_name, profit, hilt_price, roi))

# Sort by profit and print
profits_and_roi.sort(key=lambda x: x[1], reverse=True)
print("Godsword Profitability Analysis:")
for godsword, profit, hilt_price, roi in profits_and_roi:
    formatted_profit = format_price(profit)
    formatted_hilt_price = format_price(hilt_price)
    formatted_roi = f"{roi:.1f}%"
    print(f"{godsword}: Hilt price {formatted_hilt_price} coins, Profit {formatted_profit} coins, ROI {formatted_roi}")
