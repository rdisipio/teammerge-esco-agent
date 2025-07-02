# agents.py

import pandas as pd
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory

# Shared memory for all agents
#memory = ConversationBufferMemory(memory_key="chat_history", input_key="human_input", return_messages=True)

def build_hr_chain(llm):
    template = """You are an HR expert. Based on the following team update, describe the current and incoming team structure in 2–3 concise sentences.

Team update:
{input}
"""
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    return LLMChain(
        llm=llm,
        prompt=PromptTemplate.from_template(template),
        memory=memory,
        verbose=True
    )


def build_planner_chain(llm):
    prompt = PromptTemplate(
        input_variables=["hr", "esco"],
        template = """
You are a strategic planner helping restructure tech teams. 
Based on the following input, recommend a new team structure in under 3 sentences.
Assign a name to each new team/pod. Names can be creative but should reflect the team's focus.
Report briefly on the skills gap for each team.

HR Reported:
{hr}

ESCO Insights:
{esco}
"""
    )
    memory = ConversationBufferMemory(memory_key="chat_history", input_key="hr", return_messages=True)
    return LLMChain(
        llm=llm,
        prompt=prompt,
        memory=memory,
        verbose=True
    )

'''
def build_planner_agent(llm, tools):
    return initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        memory=memory
    )
'''

def build_esco_agent(llm, tools):
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    return initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True, # Set to True for debugging
        memory=memory,
        handle_parsing_errors=True
    )

'''
def build_hr_agent(llm, tools):
    return initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        memory=memory
    )
'''


def run_roundtable(initial_prompt, hr_agent, esco_agent, planner_agent):
    print("🟢 Initial Prompt:\n", initial_prompt)

    # Step 1: HR Agent (LLMChain)
    hr_response = hr_agent.run({"input": initial_prompt})
    print("\n🧑‍💼 HR Agent:\n", hr_response)

    # Step 2: ESCO Agent
    esco_prompt = (
        "The HR team reported: " + hr_response + "\n"
        "Use the available tools to look up 2–3 core ESCO skills for each mentioned role. "
        "Only return a final answer after using tools. Do not make up tool responses. "
        "If unsure, say you need more data."
    )
    esco_response = esco_agent.run(esco_prompt)
    print("\n📚 ESCO Agent:\n", esco_response)

    # Step 3: Planner Agent (LLMChain)
    planner_response = planner_agent.run({
        "hr": hr_response,
        "esco": esco_response
    })
    print("\n🧠 Planner Agent:\n", planner_response)

    return {
        "hr": hr_response,
        "esco": esco_response,
        "planner": planner_response
    }