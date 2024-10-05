from fastapi import FastAPI
from litellm import completion
import os
from langchain_community.graphs import Neo4jGraph

from sample_external_applications.accounts_knowledge_graph_app.kg.neo4j_utils import (
    get_neo4j_credentails,
    is_neo4j_server_up,
    reset_neo4j_server,
    wait_for_neo4j_server,
)

graph = Neo4jGraph(
    username=get_neo4j_credentails()["username"],
    password=get_neo4j_credentails()["password"],
    url=get_neo4j_credentails()["uri"],
)


app = FastAPI()


@app.get("/")
async def root(query: str):
    
    with open("sample_external_applications/accounts_knowledge_graph_app/kg/input_prompt.txt") as fin:
        input_prompt = str(fin.read())
        
    messages = [
        {"role": "system", "content": input_prompt},
        {"role": "user", "content": f"{query}"},
    ]
    graph_query = completion(
        model = os.getenv("AWS_BEDROCK_MODEL"),
        messages = messages
    )['choices'][0]['message']['content']
    
    graph_output = graph.query(graph_query)
    
    return {
        "query":query,
        "graph_query": graph_query,
        "graph_output": graph_output
    }