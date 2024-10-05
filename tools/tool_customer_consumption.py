from crewai_tools import BaseTool
import os
import requests
import json
import time

class ConsumptionMetricsTool(BaseTool):
    name: str = "ConsumptionMetricsTool"
    description: str = "Finds recent support tickets filed by the requested customer name"
      
    def _fetch_data(self, product):
      TOOL_API_URL = "https://modelservice." + os.getenv("CDSW_DOMAIN") + "/model?accessKey=" + os.getenv("USAGE_CONSUMPTION_ACCESS_KEY")

      response = requests.post(TOOL_API_URL,
                      data='{"request":{"product":"%s"}}' % product,
                      headers={'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % os.getenv('CDSW_APIV2_KEY')})
      response_dict = response.json()
      if 'success' in response_dict:
        print(response_dict)
        return response_dict['response']
      elif 'errors' in response_dict:
        return "ERROR: " + json.dumps(response_dict['errors'])
      else:
        return "ERROR: Check application logs"

    def _run(self, request_id: str, product: str) -> str:
        with open('/tmp/%s' % request_id, 'w') as tools_log:
          tools_log.write('Consumption Metrics Agent')
        time.sleep(2)
        response = self._fetch_data(product)
        return response