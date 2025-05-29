import requests
import time
import os

# URLs of your deployed Render services
# Replace with your actual Render service URLs after deployment
API_URL = os.environ.get("RENDER_API_URL") # Example: "https://your-api-service-name.onrender.com/health"
STREAMLIT_URL = os.environ.get("RENDER_STREAMLIT_URL") # Example: "https://your-streamlit-service-name.onrender.com/_stcore/health"

# Interval in seconds to send keep-alive requests (e.g., every 5 minutes)
KEEP_ALIVE_INTERVAL = 300  # 5 minutes

def send_keep_alive_request(url, service_name):
    """Sends a GET request to the specified URL to keep the service alive."""
    if not url:
        print(f"URL for {service_name} is not set. Skipping keep-alive ping.")
        return

    try:
        response = requests.get(url, timeout=10) # 10-second timeout
        if response.status_code == 200:
            print(f"Successfully pinged {service_name} at {url}. Status: {response.status_code}")
        else:
            print(f"Failed to ping {service_name} at {url}. Status: {response.status_code}, Response: {response.text[:200]}")
    except requests.exceptions.RequestException as e:
        print(f"Error pinging {service_name} at {url}: {e}")

if __name__ == "__main__":
    print("Starting keep-alive script...")
    if not API_URL and not STREAMLIT_URL:
        print("RENDER_API_URL and RENDER_STREAMLIT_URL environment variables are not set.")
        print("Please set them to your deployed Render service URLs.")
        print("Exiting keep-alive script.")
    else:
        while True:
            if API_URL:
                send_keep_alive_request(API_URL, "API Service")
            if STREAMLIT_URL:
                send_keep_alive_request(STREAMLIT_URL, "Streamlit App")
            print(f"Sleeping for {KEEP_ALIVE_INTERVAL} seconds...")
            time.sleep(KEEP_ALIVE_INTERVAL)