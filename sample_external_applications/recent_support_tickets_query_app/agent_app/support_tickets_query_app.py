import gradio as gr
import os
import requests
import json

working_dir = "/home/cdsw"

MODEL_SERVICE_URL = "https://modelservice." + os.getenv("CDSW_DOMAIN") + "/model?accessKey=" + os.getenv("TICKET_QUERY_ACCESS_KEY")

def call_case_lookup(account_name):
    response = requests.post(MODEL_SERVICE_URL,
                      data='{"request":{"account":"%s"}}' % account_name,
                      headers={'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % os.getenv('CDSW_APIV2_KEY')})
    response_dict = response.json()
    if 'success' in response_dict:
      print(response_dict)
      return response_dict['response']
    elif 'errors' in response_dict:
      return "ERROR: " + json.dumps(response_dict['errors'])
    else:
      return "ERROR: Check application logs"
    
with gr.Blocks() as app:
    with gr.Row():
        gr.Markdown("# Recent Support Case Lookup Tool")
    with gr.Row():
        with gr.Column():
            inp = gr.Textbox(label="Case ID",value="", lines=1)
            examples = gr.Examples([["Main Street Bank"], ["Evolve Pharma"]], inputs=[inp])
            sum_btn = gr.Button("Submit")

        with gr.Column():
            with gr.Accordion('Recent Case Data', open=True):
                view_out = gr.JSON()

        sum_btn.click(fn=call_case_lookup, inputs=inp, outputs=[view_out])

app.launch(server_port=int(os.getenv("CDSW_APP_PORT")), server_name="127.0.0.1",  
debug=True)