from crewai_tools import BaseTool
import os
import requests
import json
import time

class TicketListingTool(BaseTool):
    name: str = "TicketListingTool"
    description: str = "Finds recent support tickets filed by the requested customer name"
      
    def _fetch_data(self, customer):
      TOOL_API_URL = "https://modelservice." + os.getenv("CDSW_DOMAIN") + "/model?accessKey=" + os.getenv("TICKET_QUERY_ACCESS_KEY")

      response = requests.post(TOOL_API_URL,
                      data='{"request":{"account":"%s"}}' % customer,
                      headers={'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % os.getenv('CDSW_APIV2_KEY')})
      response_dict = response.json()
      if 'success' in response_dict:
        print(response_dict)
        return response_dict['response']
      elif 'errors' in response_dict:
        return "ERROR: " + json.dumps(response_dict['errors'])
      else:
        return "ERROR: Check application logs"

    def _run(self, request_id: str, customer: str) -> str:
        with open('/tmp/%s' % request_id, 'w') as tools_log:
          tools_log.write('Ticket DB Query Agent')
        time.sleep(2)
        response = self._fetch_data(customer)
        return response