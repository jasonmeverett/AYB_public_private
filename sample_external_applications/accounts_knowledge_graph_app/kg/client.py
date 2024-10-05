import requests
import os 
import cmlapi
from sample_external_applications.accounts_knowledge_graph_app.utils import get_project_envs

class KGClient:
    def __init__(self):
        self.cml = cmlapi.default_client()
        self.project_id = os.getenv("CDSW_PROJECT_ID")
        envs = get_project_envs(self.cml, self.project_id)
        self.base_url = f"http://{envs['KG_APP_SERVICE_IP']}:{envs['KG_APP_SERVICE_PORT']}"

    def query(self, query_str: str) -> dict:
        out = {
            "neo4j_url": self.base_url,
            "query": query_str
        }
        try:
            response = requests.get(f"{self.base_url}", params={"query": query_str})
            response.raise_for_status()  # Raise an exception for HTTP errors
            out.update(response.json())
            return out
        except requests.exceptions.RequestException as e:
            print(f"Error during request: {e}")
            out.update({
                "error": str(e)
            })
            return out
