#!/bin/bash

# Get kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl

# Start up the neo4j server as a service regiestered to this
# namespace. The service will be available on some port. Also,
# port forward the neo4j browser to CDSW_APP_PORT so it's available
# in the UI for this application

# TODO: get neo4j server working on private cloud
python sample_external_applications/accounts_knowledge_graph_app/start-neo4j.py

# Populate the graph content.
python sample_external_applications/accounts_knowledge_graph_app/kg/graphs.py

# Forward the neo4j browser and bolt port up to application pod
# Right now this isn't doing much of anything, since we can only expose CDSW_APP_PORT
# and neo4j browser expects the client to connect directly to the neo4j service.
./kubectl port-forward svc/cml-neo4j-$CDSW_ENGINE_ID 7474:7474 -v=9 &
./kubectl port-forward svc/cml-neo4j-$CDSW_ENGINE_ID 7687:7687 -v=9 &

# Update the IP of the KG service so other sessions & pods can 
# discover. This is automatically configured through the KGClient() class.
KG_APP_SERVICE_IP=$CDSW_IP_ADDRESS
KG_APP_SERVICE_PORT=50051
python sample_external_applications/accounts_knowledge_graph_app/update-kg-endpoint-info.py $KG_APP_SERVICE_IP $KG_APP_SERVICE_PORT

# Serve the non-ui application endpoint. 
uvicorn sample_external_applications.accounts_knowledge_graph_app.serve:app --reload --port $KG_APP_SERVICE_PORT --host 0.0.0.0 & 

# Port forward the neo4j browser
python sample_external_applications/accounts_knowledge_graph_app/start-ui.py
