from crewai_tools import BaseTool
import pandas as pd
import ast

class ToolCDVWorkloadUsageLookup(BaseTool):
    name: str = "CDVWorkloadUsageLookupTool"
    description: str = "Produces customer usage information about the chosen workload type"
      
    def _fetch_data(self, dsreq):
      host='https://hack.cdsw.edh.cloudera.com'
      path='/arc/api/data'
      import requests
      import json
      url = host+path
      headers = {
       'Authorization': 'apikey ysE7bGUsUoJlb4ZVonJG1o2q8MIClyde8pPhkST3ShX21AOH'
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
      #print ('\nData Request being sent is:\n', json.dumps(json.loads(dsreq), indent=2))
      #print ('\nData Response returned is:\n', json.dumps(d, indent=2))
      return d



    
    def _run(self, customer: str, workload: str) -> str:
        dsreq = """{{"version":1,"type":"SQL",
        "dimensions":[],
        "aggregates":[{{"expr":"sum([workload_type] LIKE '%{workload_cat}%')  * 100 / count(*) as 'percentage_of_workloads'"}}],
        "filters":["lower([account_name]) LIKE '%{logo_name}%'", "[created_at] > DATE_SUB(NOW(), 30)"],
        "dataset_id":65}}""".format(logo_name=customer.lower(), workload_cat=workload.lower())
        response = self._fetch_data(dsreq)
        df = pd.DataFrame(ast.literal_eval(response['rows']), columns = response['colnames'])
        result = df.to_json(orient="table")
        return result