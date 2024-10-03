import gradio as gr
import os
from litellm import completion

#working_dir = "/Users/mecha_alex/work/code/CML_AMP_AYB"
working_dir = "/home/cdsw"
CASE_FILE_PATH_TMPL = '%s/sample_external_applications/case_summarizer_app/data/support_cases/case-%s.json'


if os.getenv("AWS_ACCESS_KEY_ID") is None:
    pass
if os.getenv("AWS_SECRET_ACCESS_KEY") is None:
    pass
if os.getenv("AWS_REGION_NAME") is None:
    pass

def summarize_case(case_id):
    if os.path.isfile(CASE_FILE_PATH_TMPL % (working_dir, case_id)):
        with open(CASE_FILE_PATH_TMPL % (working_dir, case_id), 'r') as file:
            case_data = file.read()
    else: 
        return '{"error": "Case file for case %s not found"}' % case_id
    
    messages = [
        {"role": "system", "content": "You are a helpful and truthful support case summarization assistant. Create a very brief and concise summary of the support case represented by a json formatted file. Include the case number in the title. Include a conclusion at the end indicating the status of the case. Use markdown formatting wherever applicable."},
        {"role": "user", "content": "%s"%case_data},
    ]
    response = completion(
        model = "anthropic.claude-3-5-sonnet-20240620-v1:0",
        messages = messages
    )
    return (response['choices'][0]['message']['content'], case_data)

with gr.Blocks() as app:
    with gr.Row():
        gr.Markdown("# AI Support Case Summarizer")
    with gr.Row():
        with gr.Column():
            inp = gr.Textbox(label="Case ID",value="", lines=1)
            examples = gr.Examples([["981492"], ["981492"], ["981492"]], inputs=[inp])
            sum_btn = gr.Button("Summarize")

        with gr.Column():
            with gr.Accordion('Summary', open=True):
                sum_out = gr.Markdown()
            with gr.Accordion('Original Case Data', open=False):
                view_out = gr.JSON()

        sum_btn.click(fn=summarize_case, inputs=inp, outputs=[sum_out,view_out])

app.launch(server_port=int(os.getenv("CDSW_APP_PORT")), server_name="127.0.0.1",  
debug=True)