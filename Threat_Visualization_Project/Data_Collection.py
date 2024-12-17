import requests
import json

# AlienVault OTX API Key and URL
API_KEY = "f07aa431b2375f66b36a350eb5428ce547fae4a495afda739d2c5b4777c2e870"  # Replace with your API key
BASE_URL = "https://otx.alienvault.com/api/v1/pulses/subscribed"
HEADERS = {"X-OTX-API-KEY": API_KEY}
OUTPUT_FILE = "indicators.json"

def fetch_and_save_indicators():
    indicators = []
    page = 1

    while True:
        print(f"Fetching page {page}...")
        response = requests.get(f"{BASE_URL}?page={page}", headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            if not data or "results" not in data or len(data["results"]) == 0:
                print("No more indicators to fetch.")
                break

            for result in data["results"]:
                for indicator in result.get("indicators", []):
                    indicators.append({
                        "indicator": indicator["indicator"],
                        "type": indicator.get("type", "Unknown"),
                        "description": indicator.get("description", "N/A")
                    })
            page += 1
        else:
            print(f"Error: {response.status_code}")
            print("Response:", response.text)
            break

    print(f"Total indicators fetched: {len(indicators)}")

    with open("indicators.json", "w") as file:
        json.dump(indicators, file, indent=4)
    print(f"Indicators saved to {OUTPUT_FILE}")


#Gives the total available number of indicators for IPV4 and CVE
def analyze_data():
    with open("indicators.json", "r") as file:
        data = json.load(file)

    # Count the total number of indicators
    print(f"Total indicators: {len(data)}")

    # Optionally categorize based on basic characteristics
    ipv4_count = sum(1 for i in data if i.count('.') == 3)  # Rough check for IPv4 addresses
    cve_count = sum(1 for i in data if i.startswith("CVE-"))

    print(f"IPv4 Indicators: {ipv4_count}")
    print(f"CVE Indicators: {cve_count}")


if __name__ == "__main__":
    fetch_and_save_indicators()
    analyze_data()
    
