import pandas as pd
import ast

def _fetch_data(dsreq):
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

"""
SELECT sum(workload_type LIKE '%job%') * 100 / count(*) as percentage_workloads
FROM flex_ml.cml_workloads
WHERE LOWER(account_name) LIKE '%abbvie%'
AND created_at > DATE_SUB(NOW(), 30);
"""

dsreq = """{{"version":1,"type":"SQL","limit":{number_cases},
"dimensions":[
              {{"type":"SIMPLE","expr":"[casenumber] as 'casenumber'"}},
              {{"type":"SIMPLE","expr":"[subject] as 'subject'"}},
              {{"type":"SIMPLE","expr":"[name] as 'name'"}},
              {{"type":"SIMPLE","expr":"[status] as 'status'"}},
              {{"type":"SIMPLE","expr":"[createddatetime] as 'createddatetime'",
                "order":{{"asc":false,"pri":1}}
              }}
              ],
"filters":["lower([name]) LIKE '%{logo_name}%'", "lower([description]) LIKE '%{product}%'"
           ],
"dataset_id":514}}""".format(logo_name="abbvie", number_cases=4, product="cml")
response = _fetch_data(dsreq)
df = pd.DataFrame(ast.literal_eval(response['rows']), columns = response['colnames'])
result = df.to_json(orient="table")