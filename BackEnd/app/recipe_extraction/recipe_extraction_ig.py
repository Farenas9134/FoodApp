import requests
import json
import os

headers = {
    "Authorization": "Bearer 6fe033d5-c088-493d-bb76-2a906187e7b3",
    "Content-Type": "application/json",
}

data = json.dumps({
    "input": [{"url":"https://www.instagram.com/reel/DXMUPlzk8xi/?stkn=ZWo3NHhkMTNsczE4","country":"US"}],
    "limit_per_input": 50,
})

response = requests.post(
    "https://api.brightdata.com/datasets/v3/scrape?dataset_id=gd_lk5ns7kz21pck8jpis&notify=false&include_errors=true",
    headers=headers,
    data=data
)

data = response.json()

# Output file path (relative to current working directory)
output_file = "test.json"

try:
    # Ensure the directory exists (optional if writing to current folder)
    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)

    # Open file in write mode and dump JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)

    print(f"JSON data successfully written to '{output_file}'")

except (OSError, TypeError) as e:
    print(f"Error writing JSON to file: {e}")

# print(response.json())