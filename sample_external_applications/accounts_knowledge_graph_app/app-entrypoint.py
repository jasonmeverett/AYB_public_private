import subprocess
import os 

# Start up bash
out = subprocess.run([f"bash ./sample_external_applications/accounts_knowledge_graph_app/start-app-script.sh"], shell=True, check=True)
print(out)

print("App start script is complete.")