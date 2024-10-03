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


OPENAI_API_KEY=json.load(open("/tmp/jwt"))["access_token"]
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

OPENAI_API_BASE="https://ml-cb4a4d8b-dea.env-hack.svbr-nqvp.int.cldr.work/namespaces/serving-default/endpoints/llama-3-1-70b/v1"
os.environ["OPENAI_API_BASE"] = OPENAI_API_BASE

OPENAI_MODEL_NAME="openai/6lbx-oajq-2ehb-irio"

os.environ["SSL_VERIFY"] = "False"
litellm.ssl_verify=False
litellm.client_session=httpx.Client(verify="/etc/ssl/certs/ca-certificates.crt")
litellm.aclient_session=httpx.AsyncClient(verify="/etc/ssl/certs/ca-certificates.crt")

llm = ChatOpenAI(
    http_client = httpx.Client(verify="/etc/ssl/certs/ca-certificates.crt"),
    model_name=OPENAI_MODEL_NAME
)


# In[90]:


from importlib import reload
import tools.cdvcase as cdvcase

import tools.cdvworkloadusage as cdvworkloadusage


case_search_tool = cdvcase.ToolCDVCaseLookup()
workload_usage_tool = cdvworkloadusage.ToolCDVWorkloadUsageLookup()


# In[97]:


# Agent Definitions

agent_1 = Agent(
    role=dedent((
        """
        Customer information lookup assistant.
        """)), # Think of this as the job title
    backstory=dedent((
        """
        You are simple support case lookup assistant, attempting to proivde information about customers.
        This may include lookups of filed support cases, or information about customer workload usage.
        
        """)), # This is the backstory of the agent, this helps the agent to understand the context of the task
    goal=dedent((
        """
        Perform the lookup task assigned to you by appropriate lookup tools and summarize the results found.
        """)), # This is the goal that the agent is trying to achieve
    tools=[case_search_tool, workload_usage_tool],
    allow_delegation=False,
    verbose=False,
    max_iter=1,
    max_rpm=1,
    max_retry_limit=1,
    max_retries=1,
    llm=llm
)



# In[98]:


# Task Definitions
import datetime
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
        process=Process.sequential
        # ↑ the process flow that the crew will follow (e.g., sequential, hierarchical).
    )
    print("Setting req_input")
    inputs = {
    "req_input": req_input,
    }

    print("Kicking off crew")
    result = crew.kickoff(inputs=inputs)
    print("\n\n########################")
    print("## Here is your custom crew run result:")
    print("########################\n")
    print(result)
    
    return result