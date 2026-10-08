import json
import os
import requests
import time

from api_key_ig import API_KEY

def main():
    
    headers = {
        "Authorization": "Bearer " + API_KEY,
        "Content-Type": "application/json",
    }

    data = json.dumps({
        "input": [{"url":"https://www.tiktok.com/@herbi.app/video/7693531155685215521","country":""}],
        "limit_per_input": 1,
    })

    response = requests.post(
        "https://api.brightdata.com/datasets/v3/scrape?dataset_id=gd_lu702nij2f790tmv9h&notify=false&include_errors=true",
        headers=headers,
        data=data
    )

    max_attempts = 2
    num_attempts = 0
    snapshot_id = ""

    # In case snapshot is not ready to be downloaded yet
    if response.status_code == 202:
        snapshot_id = response.json()['snapshot_id']
        print("Snapshot is not quite ready to download, trying again in 30 seconds")

    # Wait for 1 minute if snapshot not ready to be downloaded
    while response.status_code == 202 and num_attempts < max_attempts:
        time.sleep(30)
        num_attempts += 1

        print(f"Job is running with Snapshot ID: {snapshot_id}")
        # print("Trying again...")

        url = f"https://api.brightdata.com/datasets/v3/snapshot/{snapshot_id}"

        headers = {"Authorization": "Bearer " + API_KEY}

        response = requests.get(url, headers=headers)

    # In case scraping takes too long, will modify timeout time later
    if num_attempts == max_attempts:
        print("Scraping took too long, try again later")
        exit(1)
    
    data = response.json()

    # Output file path (relative to current working directory)
    output_file = "tiktok_recipe.json"

    try:
        # Ensure the directory exists (optional if writing to current folder)
        os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)

        # Open file in write mode and dump JSON
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)

        print(f"JSON data successfully written to '{output_file}'")

    except (OSError, TypeError) as e:
        print(f"Error writing JSON to file: {e}")

if __name__ == "__main__":
    main()