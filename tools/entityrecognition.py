from crewai_tools import BaseTool
import pandas as pd
import ast

class ToolCustomerNameEntity(BaseTool):
    name: str = "CustomerNameEntity"
    description: str = "Determines the customer name in a natural language request"
      
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
      print ('\nData Request being sent is:\n', \
            json.dumps(json.loads(dsreq), indent=2))
      print ('\nData Response returned is:\n', json.dumps(d, indent=2))
      return d

    def _run(self, argument: str) -> str:
        dsreq = """{{"version":1,"type":"SQL","limit":5,
"dimensions":[
              {{"type":"SIMPLE","expr":"[casenumber] as 'casenumber'"}},
              {{"type":"SIMPLE","expr":"[subject] as 'subject'"}},
              {{"type":"SIMPLE","expr":"[name] as 'name'"}},
              {{"type":"SIMPLE","expr":"[status] as 'status'"}},
              {{"type":"SIMPLE","expr":"[createddatetime] as 'createddatetime'",
                "order":{{"asc":false,"pri":1}}
              }}
              ],
"filters":["lower([name]) LIKE '%{logo_name}%'"],
"dataset_id":514}}""".format(logo_name=argument)
        response = self._fetch_data(dsreq)
        df = pd.DataFrame(ast.literal_eval(response['rows']), columns = response['colnames'])
        result = df.to_json(orient="table")
        return result