#!/usr/bin/env python
# coding: utf-8

# In[89]:

from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from textwrap import dedent
import json
import os
import litellm
litellm.set_verbose=False
import openai
from openai import OpenAI
import httpx

import sys
#sys.stdout = open('/tmp/crew.log','wt')
#sys.stderr = open('/tmp/crew.log','wt')


OPENAI_API_KEY=json.load(open("/tmp/jwt"))["access_token"]
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

OPENAI_API_BASE="https://ml-cb4a4d8b-dea.env-hack.svbr-nqvp.int.cldr.work/namespaces/serving-default/endpoints/llama-3-1-70b/v1"
os.environ["OPENAI_API_BASE"] = OPENAI_API_BASE

OPENAI_MODEL_NAME="openai/6lbx-oajq-2ehb-irio"

os.environ["SSL_VERIFY"] = "False"
litellm.ssl_verify=False
litellm.client_session=httpx.Client(verify="/etc/ssl/certs/ca-certificates.crt")
litellm.aclient_session=httpx.AsyncClient(verify="/etc/ssl/certs/ca-certificates.crt")

log_file = "/tmp/crew.log"


llm = ChatOpenAI(
    http_client = httpx.Client(verify="/etc/ssl/certs/ca-certificates.crt"),
    model_name=OPENAI_MODEL_NAME
)

print("Importing available tools")
import tools.cdvcase as cdvcase
case_search_tool = cdvcase.ToolCDVCaseLookup()

import tools.cdvworkloadusage as cdvworkloadusage
workload_usage_tool = cdvworkloadusage.ToolCDVWorkloadUsageLookup()

import tools.cmlconsumption as cmlconsumption
cml_consumption_change_tool = cmlconsumption.ToolCMLConsumptionChange()

import tools.edhknowledgegraph as edhknowledgegraph
edh_account_info_tool = edhknowledgegraph.ToolEnterpriseDataHubKnowledgeGraphSearch()

import tools.cdxsummarizer as cdxsummarizer
cxgenius_case_summarizer = cdxsummarizer.CDXSummarizerTool()

# Agent Definitions
print("Defining Primary Agent")
agent_1 = Agent(
    role=dedent((
        """
        Customer information lookup assistant.
        """)), # Think of this as the job title
    backstory=dedent((
        """
        You are simple support case lookup assistant, attempting to proivde information about CML Customers, their deployed workspaces and entitlements, and usage information within those workspaces.
        This may include lookups of filed support cases, summaries of support cases, overall account consumption, workload consumption trends, and field information.
        """)), # This is the backstory of the agent, this helps the agent to understand the context of the task
    goal=dedent((
        """
        Perform the lookup task assigned to you by appropriate lookup tools and summarize the results found. Try to keep final answers in plain text.
        """)), # This is the goal that the agent is trying to achieve
    tools=[case_search_tool,
           workload_usage_tool,
           cml_consumption_change_tool,
           edh_account_info_tool,
           cxgenius_case_summarizer],
    allow_delegation=False,
    verbose=False,
    max_iter=3,
    max_rpm=1,
    max_retry_limit=1,
    max_retries=1,
    llm=llm
)



# In[98]:


# Task Definitions
import datetime
print("Defining Primary Task")

task_1 = Task(
    description=dedent((
        """
        Attempt to answer the user question about the customer
        ---
        User Input: "{req_input}"
        """)),
    expected_output=dedent((
        """
        Output should be a well formatted list or statement with the results of the user request.
        """)),
    agent=agent_1,
    output_file=f'output-files/agent_1-output_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
    # ↑ The output of each task iteration will be saved here
)
task_2 = Task(
    description=dedent((
        """
        Look up workload usage metrics used by the specified customer in the User Input
        ---
        User Input: "{req_input}"
        """)),
    expected_output=dedent((
        """
        Output should be a simple statement describing the usage metrics found.
        """)),
    agent=agent_1,
    output_file=f'output-files/agent_1-output_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
    # ↑ The output of each task iteration will be saved here
)



# In[99]:


def crew_launch(req_input):
    # Instantiate your crew with a sequential process
    print("Instantiating Crew")
    crew = Crew(
        agents=[agent_1],
        tasks=[task_1],
        verbose=True,  # You can set it to True or False
        # ↑ indicates the verbosity level for logging during execution.
        process=Process.sequential,
    )
    print("Setting req_input")
    inputs = {
    "req_input": req_input,
    }

    with open('/tmp/crew.log', 'a') as tools_log:
        tools_log.write('------- New Crew Request ------\n')
        tools_log.write('[' + req_input + ']\n')
        tools_log.write('# Agent: \n')
        tools_log.write('Customer information lookup assistant.\n')
        tools_log.write('## Thinking about which tool to use for this request\n')
        tools_log.write('...\n')
        tools_log.write('...\n')
    print("Kicking off crew")
    result = crew.kickoff(inputs=inputs)
    print("\n\n########################")
    print("## Here is your custom crew run result:")
    print("########################\n")
    print(result)

    with open('/tmp/crew.log', 'a') as tools_log:
        tools_log.write('-------Request Complete!------\n')
    return result



def grep_tool_usage():
  return
  
def read_logs():
    with open(log_file, "r") as f:
        return f.read()

import gradio as gr
from gradio_log import Log

example=""
print("Loading UI")

with gr.Blocks(theme='gradio/base') as demo:
    with gr.Row():
      gr.Markdown("""# All Your Bots Are Belong To Us""")
    with gr.Row():
      gr.Markdown("## Bridging Domain Silos with AI Agents")
    with gr.Row():
        with gr.Column():
          inp = gr.Textbox(label="Question",value=example, lines=2)
          btn = gr.Button("Submit")
        with gr.Column():
          out = gr.Textbox(label="Result",max_lines=12)
        #out = gr.Markdown(value="")
        btn.click(fn=crew_launch, inputs=inp, outputs=out)
    with gr.Row():
       with gr.Accordion("Agent Workflow Logging", open=False):
          logs = gr.Textbox(label="", interactive=False, lines=5, max_lines=5)

    demo.load(read_logs, None, logs, every=1)
    
demo.launch(server_port=int(os.getenv("CDSW_APP_PORT")), server_name="127.0.0.1",  debug=True)



"""gr.Interface(
    crew_launch,
    inputs=[
        gr.Textbox(lines=2, value=example, label="Question"),
    ],
    outputs=[gr.Textbox(label="Answer")],
)"""
"""Which 5 CML Accounts have had the largest drop in consumption recently?"""
"""Give me a list of the 5 most recent CML support cases filed by abbvie"""
"""Summarize the support case 1060986 for me."""

"""How often is Abbvie using workloads of type session"""
"""give me the name of the SE Manager for the abbvie-ir accounts?"""

"""who are the people that take the role of SE for the abbvie-ir accounts? give me the person, role, and account name (only the account name) for each."""

"""who are the people that take the role of SE for the AbbVie-IR-ARCH-Prod account? give me the person, role, and account name (only the account name) for each."""

"""who are the people that take the role of SE for the abbvie-ir accounts? give me the person, role, and account name (only the account name) for each."""

"""who are the solutions engineers assigned to the abbvie-ir accounts? give me the person, role, and account name (only the account name) for each."""

"""who acts as the SE Manager for the abbvie-ir accounts?"""

"""!python alex-gradio-crew.py > /tmp/crew.log 2>&1"""
