from crewai_tools import BaseTool
import os
import requests
import json
import time

class ToolCaseLookup(BaseTool):
    name: str = "CaseLookupTool"
    description: str = "Finds recent support cases filed by the requested customer name"
      
    def _fetch_data(self, customer):
      TOOL_API_URL = "https://modelservice." + os.getenv("CDSW_DOMAIN") + "/model?accessKey=" + os.getenv("CASE_LOOKUP_ACCESS_KEY")

      response = requests.post(TOOL_API_URL,
                      data='{"request":{"case_id":"%s"}}' % customer,
                      headers={'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % os.getenv('CDSW_APIV2_KEY')})
      response_dict = response.json()
      if 'success' in response_dict:
        print(response_dict)
        return response_dict['response']
      elif 'errors' in response_dict:
        return "ERROR: " + json.dumps(response_dict['errors'])
      else:
        return "ERROR: Check application logs"

    def _run(self, customer: str) -> str:
        with open('/tmp/crew.log', 'w') as tools_log:
          tools_log.write('## Using the *Recent Case Lookup Tool* for this request...\n')
        time.sleep(2)
        response = self._fetch_data(customer)
        return response