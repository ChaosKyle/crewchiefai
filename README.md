# CrewChief_AI iRacing AI Crew Chief - Open Source Project

Pulling data
# iRacing Data Export Script

This script pulls historical telemetry data from the iRacing API, saves it as a CSV file, and uploads the file to Google Drive. It uses Base64 encoded SHA256 hashing for authentication, as per iRacing's latest requirements.

## Prerequisites
- Python 3.8 or later
- Required libraries: `requests`, `pydrive`, `hashlib`, `base64`
- Google Drive API credentials configured for `pydrive`

## Installation
```bash
pip install requests pydrive
```

## Setup
1. **Environment Variables:** Set the following environment variables:
```bash
export IRACING_EMAIL="your_email@example.com"
export IRACING_PASSWORD="your_password"
```
2. **Google Drive Authentication:**
   - Ensure you have a `client_secrets.json` file from your Google API Console.
   - The first time you run the script, a browser window will open to authenticate your Google Drive.

## Usage
```bash
python iracing_data_export.py
```

## Output
- Data is saved locally in the `./iracing_data` directory with a timestamp.
- A copy is uploaded to your Google Drive.

## Next Steps
After exporting your data, you can configure Grafana Alloy to ingest the CSV files from Google Drive and push the data to Grafana Cloud or a local deployment.









## Overview
This project uses Grafana's open-source tools (Alloy, Mimir, Loki, Tempo, and Grafana) to provide real-time telemetry feedback and after-race analysis for iRacing. It includes AI agents that act as a virtual race team to help improve performance. Deployment starts with **local Kubernetes** and will expand to **cloud providers** and **Grafana Cloud** in future versions.

### Features
- **Real-time telemetry feedback** using Alloy and Mimir
- **Event logging** with Loki
- **Race traces** with Tempo
- **Visual dashboards** in Grafana
- **Post-race AI analysis** using Python AI agents
- **Local Kubernetes deployment** using manifests and Helm charts (primary focus)
- **Secure-by-default configuration following DevOps best practices

---

## Prerequisites
- [Docker](https://www.docker.com/get-started) and Kubernetes installed
- Helm CLI installed for Kubernetes deployments
- Basic command line usage (no coding required)

---

## Quick Start (Local Kubernetes Deployment)

1. **Clone the Repository**
```bash
git clone https://github.com/your-repo/iracing-ai-crew-chief.git
cd iracing-ai-crew-chief
```

2. **Deploy to Kubernetes**
```bash
kubectl apply -f k8s-manifests/
helm install ai-crew-chief helm/
```

3. **Access the Tools:**
- Grafana: [http://localhost:3000](http://localhost:3000)
- Loki Logs: Integrated into Grafana
- Mimir Metrics: Integrated into Grafana
- Tempo Traces: Integrated into Grafana

4. **Default Credentials:**
- Username: `admin`
- Password: `admin`

---

## Security Best Practices
- **RBAC:** Kubernetes Role-Based Access Control is enabled by default
- **Network Policies:** Restrict pod-to-pod communication for sensitive components
- **Minimal Permissions:** Alloy, Mimir, Loki, and Tempo run with least privilege

---

## AI Agents

- **Crew Chief:** Provides real-time performance feedback, alerts on car issues, and suggests adjustments.
- **Race Engineer:** Monitors tire wear, fuel usage, and pit strategy.
- **Analyst:** Reviews post-race telemetry, compares lap times, and highlights performance trends.

### AI Script Example
```python
import json
import requests

def analyze_telemetry(data_file):
    with open(data_file, 'r') as f:
        telemetry = json.load(f)
        avg_speed = sum(lap['speed'] for lap in telemetry['laps']) / len(telemetry['laps'])
        print(f"Average Speed: {avg_speed} km/h")

if __name__ == "__main__":
    analyze_telemetry('./telemetry_data/sample_race.json')
```

---

## Example Telemetry Data
- Located in the `telemetry_data` folder.
- Includes sample race telemetry files with lap times, sector splits, and incidents.

---

## Grafana Dashboards
- Dashboards are pre-configured and located in the `dashboards` folder.
- Import them into Grafana via **Configuration > Dashboards > Import**.

---

## Development Roadmap
- **Phase 1:** Local Kubernetes deployment with DevOps best practices (current focus)
- **Phase 2:** Cloud deployment using Terraform for AWS, GCP, and Azure
- **Phase 3:** Grafana Cloud integration with simplified setup

---

## Documentation
- Beginner-friendly, step-by-step guides for local Kubernetes deployment
- Advanced setup for cloud and Grafana Cloud coming soon

---

## Contributing
Contributions are welcome! Please submit a pull request with your improvements.

---

## License
This project is licensed under the MIT License.
