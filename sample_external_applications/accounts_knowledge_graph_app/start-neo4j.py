import sys
sys.path.insert(0, "/home/cdsw")

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
    return



if __name__ == "__main__":
    main()
