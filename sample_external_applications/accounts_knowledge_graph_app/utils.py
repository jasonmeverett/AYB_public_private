import cmlapi
import os 
import sys 
from typing import Dict 
import json
from cmlapi import CMLServiceApi


def update_project_envs(cml: CMLServiceApi, project_id: str, envs: Dict) -> Dict:
    """
    Update CML project environment with a new key-value dict.
    """

    proj: cmlapi.Project = cml.get_project(project_id)
    proj_env: Dict = json.loads(proj.environment)
    proj_env.update(envs)
    
    updated_project: cmlapi.Project = cmlapi.Project(
        environment= json.dumps(proj_env)
    )
    out: cmlapi.Project = cml.update_project(updated_project, project_id=project_id)
    return json.loads(proj.environment)


def get_project_envs(cml: CMLServiceApi, project_id: str) -> Dict:
    """
    Get project environment variables as a key-value dict.
    """
    
    proj: cmlapi.Project = cml.get_project(project_id)
    return json.loads(proj.environment)