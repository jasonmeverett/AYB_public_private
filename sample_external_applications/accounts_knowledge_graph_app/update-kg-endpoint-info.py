
import cmlapi
import os
import json
import sys
from typing import Dict

if __name__ == "__main__":
    
    # Make the KG service IP address and port available as project-level 
    # environment variables, so we can instantiate clients from anywhere 
    # within the project.
    
    cml = cmlapi.default_client()
    
    project_id = os.getenv("CDSW_PROJECT_ID")
    kg_address = sys.argv[1]
    kg_port = sys.argv[2]
    
    proj: cmlapi.Project = cml.get_project(project_id)
    proj_env: Dict = json.loads(proj.environment)
    proj_env.update({
        "KG_APP_SERVICE_IP": kg_address,
        "KG_APP_SERVICE_PORT": kg_port
    })
    
    updated_project: cmlapi.Project = cmlapi.Project(
        environment= json.dumps(proj_env)
    )
    out: cmlapi.Project = cml.update_project(updated_project, project_id=project_id)
    print(out.environment)