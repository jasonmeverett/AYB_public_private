import requests
import os 

class KGClient:
    def __init__(self, ip_addr: str = os.getenv("KG_APP_SERVICE_IP"), port: str = os.getenv("KG_APP_SERVICE_PORT")):
        self.base_url = f"http://{ip_addr}:{port}"

    def query(self, query_str: str):
        try:
            response = requests.get(f"{self.base_url}", params={"query": query_str})
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()  # Return the JSON response
        except requests.exceptions.RequestException as e:
            print(f"Error during request: {e}")
            return None
