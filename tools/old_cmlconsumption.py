from crewai_tools import BaseTool
import pandas as pd
import ast

class ToolCMLConsumptionChange(BaseTool):
    name: str = "CMLConsumptionChangeTool"
    description: str = "Produces a table containing customer accounts and the amount of consumption change in CML over the last two weeks."
      
    def _fetch_data(self, dsreq):
      host='https://hack.cdsw.edh.cloudera.com'
      path='/arc/api/data'
      import requests
      import json
      url = host+path
      headers = {
       'Authorization': 'apikey xxxxxxxxxpPhkST3ShX21AOH'
      }
      params = {
        'version': 1,
        'dsreq': dsreq,
      }
      r = requests.post(url, headers=headers, data=params, verify=False)
      if r.status_code != 200:
        print ('Error', r.status_code, r.content)
        return
      raw = r.content
      d = json.loads(raw)
      print ('\nData Request being sent is:\n', json.dumps(json.loads(dsreq), indent=2))
      print ('\nData Response returned is:\n', json.dumps(d, indent=2))
      return d



    
    def _run(self) -> str:
        with open('/tmp/crew.log', 'a') as tools_log:
          tools_log.write('...\n')
          tools_log.write('...\n')
          tools_log.write('...\n')
          tools_log.write('## Using the CDP Product Consumption Trends Tool for this request.\n')
        dsreq = """{"version":1,"type":"SQL",
        "dimensions":[{"type":"SIMPLE","expr":"[account_name] as 'account_name'"},
              {"type":"SIMPLE","expr":"[diff] as 'diff'"}],
        "aggregates":[],
        "filters":["[diff] IS NOT NULL"],
        "dataset_id":517}"""
        response = self._fetch_data(dsreq)
        df = pd.DataFrame(ast.literal_eval(response['rows']), columns = response['colnames'])
        result = df.to_json(orient="table")
        return result
