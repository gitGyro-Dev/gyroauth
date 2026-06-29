import requests
from dotenv import load_dotenv
import os

load_dotenv()

OWNER = "gitGyro-Dev"
REPO = "gyroauth"
TOKEN = os.getenv("GITHUB_TOKEN")

url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/README.md"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

r = requests.get(url, headers=headers)

print(r.status_code)

data = r.json()

print(data["sha"])