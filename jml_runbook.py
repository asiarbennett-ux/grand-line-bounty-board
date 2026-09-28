import os
import time
import requests
from datetime import datetime

# Microsoft Azure App Credentials (Loaded from environment variables or defined as placeholders)
TENANT_ID = os.getenv("AZURE_TENANT_ID", "dbdbd3d8-0ae7-48e8-af49-7d4cd814be33")
CLIENT_ID = os.getenv("AZURE_CLIENT_ID", "6063b0db-84bb-4019-a428-c7cd3f0b950c")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET", "YOUR_CLIENT_SECRET_HERE")

# Target user account for offboarding test
USER_UPN = "test.offboard@yourdomain.onmicrosoft.com"

def get_graph_token():
    """Authenticates to Microsoft Entra ID and returns an access token."""
    url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    payload = {
        'client_id': CLIENT_ID,
        'scope': 'https://graph.microsoft.com/.default',
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, data=payload)
    data = response.json()
    
    if 'access_token' not in data:
        print("❌ Auth Error:", data)
        return None
        
    return data.get('access_token')

def execute_leaver_workflow(token, upn):
    """Executes instant offboarding and measures execution latency."""
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    print(f"[{datetime.now().isoformat()}] Initiating Leaver Workflow for: {upn}")
    start_time = time.time()
    
    # 1. Revoke Sign-In Sessions (Instant Token Invalidation)
    revoke_url = f"https://graph.microsoft.com/v1.0/users/{upn}/revokeSignInSessions"
    revoke_resp = requests.post(revoke_url, headers=headers)
    
    # 2. Disable Account
    user_url = f"https://graph.microsoft.com/v1.0/users/{upn}"
    disable_payload = {"accountEnabled": False}
    disable_resp = requests.patch(user_url, headers=headers, json=disable_payload)
    
    end_time = time.time()
    execution_latency = round(end_time - start_time, 4)
    
    print(f"[{datetime.now().isoformat()}] Session Revocation Status: {revoke_resp.status_code}")
    print(f"[{datetime.now().isoformat()}] Account Disable Status: {disable_resp.status_code}")
    print(f"⚡ Total Offboarding Latency: {execution_latency} seconds")

if __name__ == "__main__":
    token = get_graph_token()
    if token:
        execute_leaver_workflow(token, USER_UPN)