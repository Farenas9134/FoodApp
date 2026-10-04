import requests
import json
import os

from api_key_ig import API_KEY

headers = {
    "Authorization": "Bearer" + API_KEY,
    "Content-Type": "application/json",
}

data = json.dumps({
    "input": [{"url":"https://www.instagram.com/reel/DXMUPlzk8xi/?stkn=ZWo3NHhkMTNsczE4"},{"url":"https://www.instagram.com/catsofinstagram/p/CesFC7JLyFl/?img_index=1"},{"url":"https://www.instagram.com/cats_of_instagram/reel/C2TmNOVMSbG/","exclude_comments":["18334942807171235","18077653106575592"]}],
    "limit_per_input": 50,
})

response = requests.post(
    "https://api.brightdata.com/datasets/v3/scrape?dataset_id=gd_ltppn085pokosxh13&notify=false&include_errors=true",
    headers=headers,
    data=data
)

data = response.json()

# Output file path (relative to current working directory)
output_file = "comments.json"

try:
    # Ensure the directory exists (optional if writing to current folder)
    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)

    # Open file in write mode and dump JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)

    print(f"JSON data successfully written to '{output_file}'")

except (OSError, TypeError) as e:
    print(f"Error writing JSON to file: {e}")