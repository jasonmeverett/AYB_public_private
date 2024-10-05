import gradio as gr
import os
import requests
import json

working_dir = "/home/cdsw"

MODEL_SERVICE_URL = "https://modelservice." + os.getenv("CDSW_DOMAIN") + "/model?accessKey=" + os.getenv("USAGE_CONSUMPTION_ACCESS_KEY")

def call_consumption_trends(product):
    response = requests.post(MODEL_SERVICE_URL,
                      data='{"request":{"product":"%s"}}' % product,
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
        gr.Markdown("# Usage Consumption Trend Delta Tool")
    with gr.Row():
        with gr.Column():
            inp = gr.Textbox(label="Product",value="", lines=1)
            examples = gr.Examples([["Cloudera Machine Learning"]], inputs=[inp])
            sum_btn = gr.Button("Submit")
        with gr.Column():
            table = gr.JSON()

        sum_btn.click(fn=call_consumption_trends, inputs=inp, outputs=[table])

app.launch(server_port=int(os.getenv("CDSW_APP_PORT")), server_name="127.0.0.1",  
debug=True)