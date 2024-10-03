import sys
sys.path.insert(0, "/home/cdsw")
sys.path.insert(0, "/home/cdsw/CML_AMP_Knowledge_Graph_Backed_RAG")

from CML_AMP_Knowledge_Graph_Backed_RAG.utils.neo4j_utils import (
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
