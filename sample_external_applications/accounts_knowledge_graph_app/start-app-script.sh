#!/bin/bash


# Start up the neo4j server as a service regiestered to this
# namespace. The service will be available on some port. Also,
# port forward the neo4j browser to CDSW_APP_PORT so it's available
# in the UI for this application
python sample_external_applications/accounts_knowledge_graph_app/start-neo4j.py

# Update the IP of the KG service so other sessions & pods can 
# discover. TODO: this can also be a k8s service.
KG_APP_SERVICE_IP=$CDSW_IP_ADDRESS
KG_APP_SERVICE_PORT=5678
python sample_external_applications/accounts_knowledge_graph_app/update-kg-endpoint-info.py $KG_APP_SERVICE_IP $KG_APP_SERVICE_PORT

# Serve the non-ui application endpoint. 
fastapi dev sample_external_applications/accounts_knowledge_graph_app/serve.py --port $KG_APP_SERVICE_PORT