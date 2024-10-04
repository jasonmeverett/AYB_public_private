from fastapi import FastAPI


from sample_external_applications.accounts_knowledge_graph_app.kg.neo4j_utils import (
    get_neo4j_credentails,
    is_neo4j_server_up,
    reset_neo4j_server,
    wait_for_neo4j_server,
)

# graph = Neo4jGraph(
#     username=get_neo4j_credentails()["username"],
#     password=get_neo4j_credentails()["password"],
#     url=get_neo4j_credentails()["uri"],
# )


app = FastAPI()


@app.get("/")
async def root(query: str):
    return {
        "input":query,
        "output": {
            "message": "Hello world!"
        }
    }