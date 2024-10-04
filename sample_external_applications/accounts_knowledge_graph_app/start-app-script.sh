#!/bin/bash


# Start up the neo4j server as a service regiestered to this
# namespace. The service will be available on some port. Also,
# port forward the neo4j browser to CDSW_APP_PORT so it's available
# in the UI for this application

# TODO: get neo4j server working on private cloud
# python sample_external_applications/accounts_knowledge_graph_app/start-neo4j.py

# Update the IP of the KG service so other sessions & pods can 
# discover. TODO: this can also be a k8s service.
KG_APP_SERVICE_IP=$CDSW_IP_ADDRESS
KG_APP_SERVICE_PORT=5678
python sample_external_applications/accounts_knowledge_graph_app/update-kg-endpoint-info.py $KG_APP_SERVICE_IP $KG_APP_SERVICE_PORT

# Serve the non-ui application endpoint. 
nohup fastapi dev sample_external_applications/accounts_knowledge_graph_app/serve.py --port $KG_APP_SERVICE_PORT &

# For now, this is a workaround hack to keep the amp long living. Ideally, we'd be able to use start-neo4j.py script
# to port forward the neo4j browser up to CDSW_APP_PORT using standard kubernetes functions in python.
python sample_external_applications/case_summarizer_app/agent-ui/case_summarizer_app.py