import sys
sys.path.insert(0, "/home/cdsw")
import cmlapi
from cmlapi import CMLServiceApi
from sample_external_applications.accounts_knowledge_graph_app.kg.neo4j_utils import get_parent_pod_name, get_neo4j_service_name
from sample_external_applications.accounts_knowledge_graph_app.utils import update_project_envs
import os

from sample_external_applications.accounts_knowledge_graph_app.kg.neo4j_utils import (
    get_neo4j_credentails,
    is_neo4j_server_up,
    reset_neo4j_server,
    wait_for_neo4j_server,
)

def main():
    print("Resetting neo4j server...")
    reset_neo4j_server()
    print("Waiting for server to load...")
    wait_for_neo4j_server()
    
    cml: CMLServiceApi = cmlapi.default_client()
    project_id = os.getenv("CDSW_PROJECT_ID")
    updated_project_envs = update_project_envs(cml, project_id=project_id, envs={
        "KG_NEO4J_SERVICE": get_neo4j_service_name()
    })
    print(updated_project_envs)
    
    return



if __name__ == "__main__":
    main()
