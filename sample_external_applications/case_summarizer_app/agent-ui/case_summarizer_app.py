import gradio as gr
import os
import requests
import json

working_dir = "/home/cdsw"
CASE_FILE_PATH_TMPL = '%s/sample_external_applications/case_summarizer_app/data/support_cases/case-%s.json'

MODEL_SERVICE_URL = "https://modelservice." + os.getenv("CDSW_DOMAIN") + "/model?accessKey=" + os.getenv("CASE_SUMMARIZER_ACCESS_KEY")

def call_summarize_case(case_id):
    if os.path.isfile(CASE_FILE_PATH_TMPL % (working_dir, case_id)):
        with open(CASE_FILE_PATH_TMPL % (working_dir, case_id), 'r') as file:
            case_data = file.read()
    else: 
        return '{"error": "Case file for case %s not found"}' % case_id
    
    response = requests.post(MODEL_SERVICE_URL,
                      data='{"request":{"case_id":"%s"}}' % case_id,
                      headers={'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % os.getenv('CDSW_APIV2_KEY')})
    response_dict = response.json()
    if 'success' in response_dict:
      print(response_dict)
      return response_dict['response'], case_data
    elif 'errors' in response_dict:
      return "ERROR: " + json.dumps(response_dict['errors'])
    else:
      return "ERROR: Check application logs"
    
with gr.Blocks() as app:
    with gr.Row():
        gr.Markdown("# AI Support Case Summarizer")
    with gr.Row():
        with gr.Column():
            inp = gr.Textbox(label="Case ID",value="", lines=1)
            examples = gr.Examples([["981492"], ["981389"]], inputs=[inp])
            sum_btn = gr.Button("Summarize")

        with gr.Column():
            with gr.Accordion('Summary', open=True):
                sum_out = gr.Markdown()
            with gr.Accordion('Original Case Data', open=False):
                view_out = gr.JSON()

        sum_btn.click(fn=call_summarize_case, inputs=inp, outputs=[sum_out,view_out])

app.launch(server_port=int(os.getenv("CDSW_APP_PORT")), server_name="127.0.0.1",  
debug=True)