#!/usr/bin/env python
# coding: utf-8

# In[89]:

from crewai import Agent, Task, Crew, Process, LLM
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
llm = LLM(model="bedrock/" + os.getenv("AWS_BEDROCK_MODEL"))
log_file = "/tmp/crew.log"

print("Importing available tools")
import tools.tool_case_lookup as tool_case_lookup
case_search_tool = tool_case_lookup.ToolCaseLookup()

#import tools.cdvworkloadusage as cdvworkloadusage
#workload_usage_tool = cdvworkloadusage.ToolCDVWorkloadUsageLookup()

#import tools.old_cmlconsumption as old_cmlconsumption
#cml_consumption_change_tool = old_cmlconsumption.ToolCMLConsumptionChange()

#import tools.old_edhknowledgegraph as old_edhknowledgegraph
#edh_account_info_tool = old_edhknowledgegraph.ToolEnterpriseDataHubKnowledgeGraphSearch()

import tools.tool_case_summarizer as tool_case_summarizer
cxgenius_case_summarizer = tool_case_summarizer.ToolCaseSummarizer()

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
           cxgenius_case_summarizer],
    allow_delegation=False,
    verbose=False,
    max_iter=3,
    max_rpm=1,
    max_retry_limit=1,
    max_retries=1,
    llm=llm
)

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