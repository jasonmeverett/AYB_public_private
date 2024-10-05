from crewai_tools import BaseTool
import os
import requests
import json

class ToolCaseSummarizer(BaseTool):
    name: str = "CaseSummarizerTool"
    description: str = "Summarizes an entire support case engagement given the support case id."
      
    def _fetch_summary(self, case_id):
      TOOL_API_URL = "https://modelservice." + os.getenv("CDSW_DOMAIN") + "/model?accessKey=" + os.getenv("CASE_SUMMARIZER_ACCESS_KEY")

      response = requests.post(TOOL_API_URL,
                      data='{"request":{"case_id":"%s"}}' % case_id,
                      headers={'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % os.getenv('CDSW_APIV2_KEY')})
      response_dict = response.json()
      if 'success' in response_dict:
        print(response_dict)
        return response_dict['response']
      elif 'errors' in response_dict:
        return "ERROR: " + json.dumps(response_dict['errors'])
      else:
        return "ERROR: Check application logs"

    def _run(self, request_id: str, case_id: str) -> str:
        with open('/tmp/%s' % request_id, 'w') as tools_log:
          tools_log.write('Case Summarizer Tool')
        response = self._fetch_summary(case_id)
        return response