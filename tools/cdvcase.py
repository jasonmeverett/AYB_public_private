from crewai_tools import BaseTool
import pandas as pd
import ast

class ToolCDVCaseLookup(BaseTool):
    name: str = "CDVCaseLookupTool"
    description: str = "Finds the specided number of most recent support cases filed by a customer filtered by product."
      
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
      print ('\nData Request being sent is:\n', json.dumps(json.loads(dsreq), indent=2))
      print ('\nData Response returned is:\n', json.dumps(d, indent=2))
      return d

    def _run(self, customer: str, number: int, product: str) -> str:
        with open('/tmp/crew.log', 'a') as tools_log:
          tools_log.write('...\n')
          tools_log.write('...\n')
          tools_log.write('...\n')
          tools_log.write('## Using the Recent Case Lookup Tool for this request.\n')
        dsreq = """{{"version":1,"type":"SQL","limit":{number_cases},
"dimensions":[
              {{"type":"SIMPLE","expr":"[casenumber] as 'casenumber'"}},
              {{"type":"SIMPLE","expr":"[subject] as 'subject'"}},
              {{"type":"SIMPLE","expr":"[name] as 'name'"}},
              {{"type":"SIMPLE","expr":"[createddatetime] as 'createddatetime'",
                "order":{{"asc":false,"pri":1}}
              }}
              ],
"filters":["lower([name]) LIKE '%{logo_name}%'", "lower([description]) LIKE '%{product}%'"],
"dataset_id":514}}""".format(logo_name=customer.lower(), number_cases=number, product=product.lower())
        response = self._fetch_data(dsreq)
        df = pd.DataFrame(ast.literal_eval(response['rows']), columns = response['colnames'])
        result = df.to_json(orient="table")
        return result