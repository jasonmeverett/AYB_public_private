import os
import sys
from dotenv import load_dotenv
from langchain.docstore.document import Document
from langchain_community.graphs import Neo4jGraph
import json
import time 
import random

import sys
sys.path.insert(0, "/home/cdsw")
sys.path.insert(0, "/home/cdsw/CML_AMP_Knowledge_Graph_Backed_RAG")

from CML_AMP_Knowledge_Graph_Backed_RAG.utils.neo4j_utils import (
    get_neo4j_credentails,
    is_neo4j_server_up,
    reset_neo4j_server,
    wait_for_neo4j_server,
)

def create_or_update_account(graph, account):
    # Merge the Account node
    query = """
        MERGE (a:Account {id: $id})
        SET a.account_name = $account_name,
            a.account_type = $account_type,
            a.industry = $industry,
            a.description = $description,
            a.geo = $geo,
            a.region = $region,
            a.subregion = $subregion,
            a.area = $area
    """
    params = {
        "id": account["id"],
        "account_name": account.get("account_name", ""),
        "account_type": account.get("account_type", ""),
        "industry": account.get("industry", ""),
        "description": account.get("description", ""),
        "geo": account.get("geo", ""),
        "region": account.get("region", ""),
        "subregion": account.get("subregion", ""),
        "area": account.get("area", ""),
    }
    graph.query(query, params=params)

def create_or_update_person(graph, person_data):
    # Merge the Person node based on email
    query = """
        MERGE (p:Person {email: $email})
        SET p.name = $name
    """
    params = {
        "email": person_data["email"],
        "name": person_data.get("name", "")
    }
    graph.query(query, params=params)

def create_or_update_role(graph, role_name):
    # Merge the Role node
    query = """
        MERGE (r:Role {name: $role_name})
    """
    params = {
        "role_name": role_name
    }
    graph.query(query, params=params)

def create_person_role_relationship(graph, email, role_name):
    # Create relationship between Person and Role
    query = """
        MATCH (p:Person {email: $email})
        MATCH (r:Role {name: $role_name})
        MERGE (p)-[:HOLDS]->(r)
    """
    params = {
        "email": email,
        "role_name": role_name
    }
    graph.query(query, params=params)

def create_account_person_relationship(graph, account_id, person_email):
    # Create relationship between Person and Account
    query = """
        MATCH (a:Account {id: $account_id})
        MATCH (p:Person {email: $email})
        MERGE (p)-[:IS_ASSOCIATED_WITH]->(a)
    """
    params = {
        "account_id": account_id,
        "email": person_email
    }
    graph.query(query, params=params)

def create_or_update_entitlement(graph, account_id, entitlement_data):
    # Create Entitlement node and relate it to the Account
    query = """
        MERGE (e:Entitlement {id: $entitlement_name})
        SET e.entitlement_type = $entitlement_type,
            e.status = $status,
            e.unit_type = $unit_type,
            e.unit_quantity = toFloat($unit_quantity)
        WITH e
        MATCH (a:Account {id: $account_id})
        MERGE (a)-[:HAS_ENTITLEMENT]->(e)
    """
    params = {
        "entitlement_name": entitlement_data["entitlement_name"],
        "entitlement_type": entitlement_data.get("entitlement_type", ""),
        "status": entitlement_data.get("status", ""),
        "unit_type": entitlement_data.get("unit_type", ""),
        "unit_quantity": entitlement_data.get("unit_quantity", "0"),
        "account_id": account_id
    }
    graph.query(query, params=params)

def create_or_update_product(graph, product_name):
    # Merge the Product node
    query = """
        MERGE (p:Product {name: $product_name})
    """
    params = {
        "product_name": product_name
    }
    graph.query(query, params=params)

def create_entitlement_product_relationship(graph, entitlement_name, product_name):
    # Create relationship between Entitlement and Product
    query = """
        MATCH (e:Entitlement {id: $entitlement_name})
        MATCH (p:Product {name: $product_name})
        MERGE (e)-[:INCLUDES_PRODUCT]->(p)
    """
    params = {
        "entitlement_name": entitlement_name,
        "product_name": product_name
    }
    graph.query(query, params=params)

    
def create_or_update_workspace(graph, workspace_data):
    # Merge the Workspace node based on 'workspace_crn'
    query = """
        MERGE (w:PublicCMLWorkspace {workspace_crn: $workspace_crn})
        SET w.account_name = $account_name,
            w.cloud_provider = $cloud_provider,
            w.control_plane = $control_plane,
            w.region = $region,
            w.workspace_name = $workspace_name,
            w.workspace_version = $workspace_version,
            w.support = $support,
            w.is_suspended = $is_suspended,
            w.current_status = $current_status
    """
    params = {
        "workspace_crn": workspace_data["workspace_crn"],
        "account_name": workspace_data.get("account_name", ""),
        "cloud_provider": workspace_data.get("cloud_provider", ""),
        "control_plane": workspace_data.get("control_plane", ""),
        "region": workspace_data.get("region", ""),
        "workspace_name": workspace_data.get("workspace_name", ""),
        "workspace_version": workspace_data.get("workspace_version", ""),
        "support": workspace_data.get("support", ""),
        "is_suspended": workspace_data.get("is_suspended", ""),
        "current_status": workspace_data.get("current_status", "")
    }
    graph.query(query, params=params)

def create_workspace_account_relationship(graph, workspace_crn, account_id):
    query = """
        MATCH (w:PublicCMLWorkspace {workspace_crn: $workspace_crn})
        MATCH (a:Account {id: $account_id})
        MERGE (a)-[:HAS_WORKSPACE]->(w)
    """
    params = {
        "workspace_crn": workspace_crn,
        "account_id": account_id
    }
    graph.query(query, params=params)
    
def create_or_update_cloud_provider(graph, provider_name):
    query = """
        MERGE (cp:CloudProvider {name: $provider_name})
    """
    params = {
        "provider_name": provider_name
    }
    graph.query(query, params=params)

def create_workspace_provider_relationship(graph, workspace_crn, provider_name):
    query = """
        MATCH (w:PublicCMLWorkspace {workspace_crn: $workspace_crn})
        MATCH (cp:CloudProvider {name: $provider_name})
        MERGE (w)-[:DEPLOYED_ON]->(cp)
    """
    params = {
        "workspace_crn": workspace_crn,
        "provider_name": provider_name
    }
    graph.query(query, params=params)


def clear_graph(graph: Neo4jGraph):
    graph.query("MATCH (n) DETACH DELETE n")
    return


def populate_database(graph: Neo4jGraph):
    kg_data = json.load(open(os.path.join(os.getenv("HOME"), "kg_data.json")))
    random.shuffle(kg_data)
    kg_data_with_cloud = list(filter(lambda x: x["public_cloud_cml_workspaces"], kg_data))
    
    # Clear out the existing graph
    # print("Clearing existing graph...")
    # clear_graph(graph)

    idx0 = 0
    idxf = 10000

    stuff_to_add = kg_data_with_cloud + kg_data[idx0:idxf]

    # Add data
    print("Beginning population...")
    t0 = time.time()
    for ii, account in enumerate(stuff_to_add):
        print(f"{ii}: {account['account_name']}")
        create_or_update_account(graph, account)
        for person in account["account_team"]:
            create_or_update_person(graph, person)
            create_or_update_role(graph, person["team_role"])
            create_person_role_relationship(graph, person["email"], person["team_role"])
            create_account_person_relationship(graph, account["id"], person["email"])
        for entitlement in account["entitlements"]:
            print(f"  - account '{account['account_name']}' has entitlement '{entitlement['entitlement_name']}'.")
            create_or_update_entitlement(graph, account["id"], entitlement)
            create_or_update_product(graph, entitlement["products"])
            create_entitlement_product_relationship(graph, entitlement["entitlement_name"], entitlement["products"]) 
        for workspace in account["public_cloud_cml_workspaces"]:
            print(f"  - account '{account['account_name']}' has a Public CML cloud workspace '{workspace['workspace_name']}'.")
            create_or_update_workspace(graph, workspace)
            create_workspace_account_relationship(graph, workspace["workspace_crn"], account["id"])
            create_or_update_cloud_provider(graph, workspace["cloud_provider"])
            create_workspace_provider_relationship(graph, workspace["workspace_crn"], workspace["cloud_provider"])
            
    tf = time.time()
    print("Graph indexing complete!")
    print(f"Elapsed time: {tf-t0} seconds")
    print(f"Doc rate: {(idxf - idx0)/(tf - t0)} docs/sec")
    
    return


def main():
    # print("Resetting neo4j server...")
    # reset_neo4j_server()
    # print("Waiting for server to load...")
    # wait_for_neo4j_server()

    # Get the graph client
    graph = Neo4jGraph(
        username=get_neo4j_credentails()["username"],
        password=get_neo4j_credentails()["password"],
        url=get_neo4j_credentails()["uri"],
    )

    populate_database(graph)

    # # Test a query
    # res = graph.query("""
    #     MATCH (p:Person)-[:IS_ASSOCIATED_WITH]->(a:Account)
    #     OPTIONAL MATCH (p)-[:HOLDS]->(r:Role)
    #     WITH p, collect(DISTINCT r.name) AS roles, count(DISTINCT a) AS accountCount
    #     WHERE accountCount > 1
    #     RETURN p.name, roles, accountCount;
    #     """)
    # # print(res)
    # for hit in res:
    #     print(hit)

    # abbive
    # exon
    
    
    return



if __name__ == "__main__":
    main()
