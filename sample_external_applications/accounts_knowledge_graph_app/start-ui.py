import gradio as gr
import json
import os
from sample_external_applications.accounts_knowledge_graph_app.kg.client import KGClient

kg = KGClient()

# Function to handle the query and pretty-print the result
def handle_query(input_text):
    response = kg.query(input_text)
    return json.dumps(response, indent=4)

# Get the port number from the environment variable
port = int(os.getenv("CDSW_APP_PORT"))

# Define the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Knowledge Graph Query Tool")

    input_text = gr.Textbox(label="Enter your query", placeholder="Type something...")
    output_text = gr.Textbox(label="Response", interactive=False)

    query_button = gr.Button("Submit")
    query_button.click(fn=handle_query, inputs=input_text, outputs=output_text)

# Launch the Gradio app on the specific port
demo.launch(server_port=port)
