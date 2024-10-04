# from crewai_tools import BaseTool
from crewai_tools import BaseTool

class ToolEnterpriseDataHubKnowledgeGraphSearch(BaseTool):
    name: str = "EnterpriseDataHubKnowledgeGraphSearch"
    description: str = "Determines the customer name in a natural language request"
      
    def _fetch_data(self, query):
      host='http://localhost:8001' # Assuming we have self deployed the FasiAPI that acts as a facade to this tool
      path='/'
      import requests
      import json
      url = host+path
      headers = {}
      params = {
        'query': query,
      }
      r = requests.get(url, headers=headers, params=params)
      if r.status_code != 200:
        print ('Error', r.status_code, r.content)
        return
      return r.json()

    def _run(self, query: str) -> str:
        with open('/tmp/crew.log', 'a') as tools_log:
          tools_log.write('...\n')
          tools_log.write('...\n')
          tools_log.write('...\n')
          tools_log.write('## Using the CML Customer Accounts KG Query Bot for this request.\n')
        response = self._fetch_data(query)
        return response