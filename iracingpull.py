import requests
import csv
import os
import hashlib
import base64
from datetime import datetime
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def authenticate_iracing(email, password):
    """Authenticate with the iRacing API using Base64 encoded SHA256 hash."""
    email_lower = email.lower()
    hash_value = hashlib.sha256((password + email_lower).encode('utf-8')).digest()
    encoded_password = base64.b64encode(hash_value).decode('utf-8')

    login_url = "https://members-ng.iracing.com/auth"
    payload = {"email": email, "password": encoded_password}
    headers = {'Content-Type': 'application/json'}

    session = requests.Session()
    response = session.post(login_url, json=payload, headers=headers)

    if response.status_code == 200:
        print("Authentication successful")
        return session
    else:
        print(f"Failed to authenticate: {response.status_code} - {response.text}")
        return None

def fetch_iracing_data(session, output_folder):
    """Fetch all available historical iRacing data using the API and save it as CSV."""
    url = "https://members-ng.iracing.com/data/telemetry/all"
    response = session.get(url)

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
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    file = drive.CreateFile({'title': os.path.basename(file_path)})
    file.SetContentFile(file_path)
    file.Upload()
    print(f"File uploaded to Google Drive: {file['title']}")

if __name__ == "__main__":
    EMAIL = os.getenv("IRACING_EMAIL")
    PASSWORD = os.getenv("IRACING_PASSWORD")
    OUTPUT_FOLDER = "./iracing_data"

    if EMAIL and PASSWORD:
        session = authenticate_iracing(EMAIL, PASSWORD)
        if session:
            fetch_iracing_data(session, OUTPUT_FOLDER)
    else:
        print("Please set the IRACING_EMAIL and IRACING_PASSWORD environment variables.")
