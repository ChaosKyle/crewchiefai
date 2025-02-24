import requests
import csv
import os
from datetime import datetime
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def fetch_iracing_data(api_key, output_folder):
    """Fetch all available historical iRacing data using the API and save it as CSV."""
    url = "https://members-ng.iracing.com/data/telemetry/all"  # Updated endpoint to fetch all data
    headers = {"Authorization": f"Bearer {api_key}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        file_path = save_to_csv(data, output_folder)
        upload_to_google_drive(file_path)
    else:
        print(f"Failed to fetch data: {response.status_code} - {response.text}")


def save_to_csv(data, output_folder):
    """Save all iRacing telemetry data to a CSV file in the specified folder."""
    os.makedirs(output_folder, exist_ok=True)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    file_path = os.path.join(output_folder, f'iracing_all_data_{timestamp}.csv')

    # Dynamically get all available keys for CSV header
    fieldnames = set()
    for entry in data:
        fieldnames.update(entry.keys())

    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=sorted(fieldnames))
        writer.writeheader()
        for entry in data:
            writer.writerow(entry)

    print(f"All telemetry data saved to {file_path}")
    return file_path


def upload_to_google_drive(file_path):
    """Upload the CSV file to Google Drive."""
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Authenticate via browser
    drive = GoogleDrive(gauth)

    file = drive.CreateFile({'title': os.path.basename(file_path)})
    file.SetContentFile(file_path)
    file.Upload()
    print(f"File uploaded to Google Drive: {file['title']}")


if __name__ == "__main__":
    API_KEY = os.getenv("IRACING_API_KEY")  # Use environment variable for security
    OUTPUT_FOLDER = "./iracing_data"

    if API_KEY:
        fetch_iracing_data(API_KEY, OUTPUT_FOLDER)
    else:
        print("Please set the IRACING_API_KEY environment variable.")
