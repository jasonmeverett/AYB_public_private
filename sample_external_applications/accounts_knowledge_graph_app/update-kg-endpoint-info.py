
import cmlapi
import os
import json
import sys
from typing import Dict

from sample_external_applications.accounts_knowledge_graph_app.utils import update_project_envs

if __name__ == "__main__":
    
    # Make the KG service IP address and port available as project-level 
    # environment variables, so we can instantiate clients from anywhere 
    # within the project.
    
    cml = cmlapi.default_client()
    
    project_id = os.getenv("CDSW_PROJECT_ID")
    kg_address = sys.argv[1]
    kg_port = sys.argv[2]
    
    updated_envs = update_project_envs(cml, project_id=project_id, envs={
        "KG_APP_SERVICE_IP": kg_address,
        "KG_APP_SERVICE_PORT": kg_port
    })
    
    print(updated_envs)