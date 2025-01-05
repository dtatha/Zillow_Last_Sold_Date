import requests
import csv
from datetime import datetime

# Function to get ZPID from an address
def get_zpid(address, api_key, api_host):
    url = "https://zillow-com1.p.rapidapi.com/locationSuggestions"
    querystring = {"q": address}
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": api_host
    }
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        results = response.json().get("results", [])
        if results:
            return results[0].get("metaData", {}).get("zpid", None)
    else:
        print(f"Error fetching ZPID for address {address}: {response.status_code}, {response.text}")
    return None

# Function to get price history for a specific ZPID
def get_price_history(zpid, api_key, api_host):
    url = "https://zillow-com1.p.rapidapi.com/valueHistory/listingPrices"
    querystring = {"zpid": zpid}
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": api_host
    }
    response = requests.get(url, headers=headers, params=querystring)
    
    if response.status_code == 200:
        # Debug print: Dump the JSON response
        print(f"Price history response for ZPID {zpid}: {response.json()}")
        
        # Extract "x" and "y" data points
        chart_data = response.json().get("chartData", [])
        if chart_data:
            points = chart_data[0].get("points", [])
            # Sort by "x" (timestamp) in descending order to get the most recent data
            sorted_points = sorted(points, key=lambda p: p["x"], reverse=True)
            return [[datetime.fromtimestamp(point["x"] / 1000).strftime('%Y-%m-%d'), point["y"]] for point in sorted_points]
    else:
        print(f"Error fetching price data for ZPID {zpid}: {response.status_code}, {response.text}")
    
    # Return an empty list if no data is available
    return []

# RapidAPI Key and Host
api_key = "ef04ceee19mshc0791fc850be0a4p1131cfjsn1093878bdab9"
api_host = "zillow-com1.p.rapidapi.com"

# List of addresses
addresses = [
    "1003 Worth Creek Ln, Katy, TX"
]

# Create CSV file with updated columns
with open('zillow_address_price_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Write header row
    writer.writerow([
        "Address", "ZPID", 
        "Date 1", "Price 1",
        "Date 2", "Price 2",
        "Date 3", "Price 3"
    ])
    
    # Process each address
    for address in addresses:
        # Get ZPID for the address
        zpid = get_zpid(address, api_key, api_host)
        
        if zpid:
            # Fetch price history for the ZPID
            price_history = get_price_history(zpid, api_key, api_host)
            
            # Get the three most recent price points or default to "No data"
            price_1 = price_history[0] if len(price_history) > 0 else ["No data", "No data"]
            price_2 = price_history[1] if len(price_history) > 1 else ["No data", "No data"]
            price_3 = price_history[2] if len(price_history) > 2 else ["No data", "No data"]
            
            # Write the row with updated data
            writer.writerow([
                address,
                zpid,
                price_1[0], price_1[1],
                price_2[0], price_2[1],
                price_3[0], price_3[1]
            ])
        else:
            print(f"ZPID not found for address: {address}")
            writer.writerow([address, "ZPID not found", "No data", "No data", "No data", "No data", "No data", "No data"])

print("Data successfully written to zillow_address_price_data.csv")