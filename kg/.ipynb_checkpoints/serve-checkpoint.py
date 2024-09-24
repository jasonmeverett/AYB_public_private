from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import httpx
import json
import os
from langchain_community.graphs import Neo4jGraph

import sys
sys.path.insert(0, "/home/cdsw")
sys.path.insert(0, "/home/cdsw/CML_AMP_Knowledge_Graph_Backed_RAG")

from CML_AMP_Knowledge_Graph_Backed_RAG.utils.neo4j_utils import (
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

# From the doc
OPENAI_API_KEY=json.load(open("/tmp/jwt"))["access_token"]
OPENAI_API_BASE="https://ml-cb4a4d8b-dea.env-hack.svbr-nqvp.int.cldr.work/namespaces/serving-default/endpoints/llama-3-1-70b/v1"
OPENAI_MODEL_NAME="6lbx-oajq-2ehb-irio"


http_client = httpx.Client(verify="/etc/ssl/certs/ca-certificates.crt")
client = OpenAI(
    base_url=OPENAI_API_BASE,
    api_key=OPENAI_API_KEY,
    http_client=http_client,
)

app = FastAPI()

def chat(system_prompt, query):
    response = client.chat.completions.create(
        model=OPENAI_MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user","content": query}
        ],
    )
    return response.choices[0].message.content

@app.get("/")
async def root(query: str):

    # Hack because graph
    # query = query.lower()
    
    # Import prompt templates.
    with open("/home/cdsw/kg/input_prompt.txt", "r") as f:
        input_prompt_template = f.read()

    # with open("/home/cdsw/kg/graph_query_enrichment_prompt.txt", "r") as f:
    #     graph_query_enrichment_prompt = f.read()
    
    with open("/home/cdsw/kg/response_prompt.txt", "r") as f:
        response_prompt_template = f.read()

    input_prompt_dict = {
        "user_input":query
    }
    input_prompt = input_prompt_template

    # Make a call to openai endpoint to make the graph query.
    graph_query = chat(input_prompt, query)

    # Forcefully run a graph query enrichment to try and remove bad formatting
    # enriched_graph_query = chat(graph_query_enrichment_prompt, f"### USER_INPUT: {query}\n### BAD_GRAPH: {graph_query}")

    # Run the query.
    try:
        # res = graph.query(enriched_graph_query)
        res = graph.query(graph_query)
        response_data = res
        response_prompt = response_prompt_template
        response_text = chat(response_prompt, f"### USER INPUT:\n{query}\n\n### GRAPH QUERY:\n{graph_query}\n\n### GRAPH RESPONSE:\n{res}\n\n")
    except Exception as e:
        response_data = {}
        response_text = f"Sorry, there was an issue with running this query. Please try again with different query inputs.\nError: {e}"
    
    
    return {
        "query": query,
        "graph_query": graph_query,
        # "enriched_graph_query": enriched_graph_query,
        "response_data": response_data,
        "response_text": response_text,
    }
