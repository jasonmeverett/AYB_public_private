import os
from litellm import completion
import cml.models_v1 as models

working_dir = "/home/cdsw"
CASE_FILE_PATH_TMPL = '%s/sample_external_applications/case_summarizer_app/data/support_cases/case-%s.json'


if os.getenv("AWS_ACCESS_KEY_ID") is None:
    pass
if os.getenv("AWS_SECRET_ACCESS_KEY") is None:
    pass
if os.getenv("AWS_REGION_NAME") is None:
    pass

@models.cml_model
def summarize_case(args):
    case_id = args["case_id"]
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
    return (response['choices'][0]['message']['content'])