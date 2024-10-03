import os
def crew_launch(input_str):
  return input_str

import gradio as gr
example="Show me the 4 most recent support cases from abbvie"
gr.Interface(
    crew_launch,
    inputs=[
        gr.Textbox(lines=2, value=example, label="Question"),
    ],
    outputs=[gr.Textbox(label="Answer")],
).launch(server_port=int(os.getenv("CDSW_APP_PORT")), server_name="127.0.0.1",  debug=True)