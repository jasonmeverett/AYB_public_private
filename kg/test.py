import requests
import sys
import json

from tools.edhknowledgegraph import ToolEnterpriseDataHubKnowledgeGraphSearch

# Define the query parameter
query_param = sys.argv[1] if len(sys.argv) > 1 else "hello"

tool = ToolEnterpriseDataHubKnowledgeGraphSearch()

out = tool._run(query_param)
print(json.dumps(out, indent=2))
