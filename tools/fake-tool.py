from crewai_tools import BaseTool
import requests
import json

class AccountsKnowledgeGraphSearch(BaseTool):
    name: str = "AccountsQueryTool"
    description: str = "Determines the customer name in a natural language request"      
    def _fetch_data(self, query):
      host='http://hack-accounts-kg.hack-centralus.env-hack.svbr-nqvp.int.cldr.work''
      path='/api/nl-cypher-conversion'
      url = host+path
      params = { 'nl_request': nl_request }
      r = requests.get(url, headers={}, params=params)
      return r.json()

    def _run(self, nl_request: str) -> str:
        response = self._fetch_data(nl_request)
        return response
      
      
      
import tools.accounts as accountsDomain
accounts_kg_tool = accountsDomain.AccountsKnowledgeGraphSearch()