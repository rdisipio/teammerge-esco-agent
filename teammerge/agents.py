# agents.py

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory

from .tools import get_skill_tool, get_occupation_tool, get_skill_gap_tool

# Shared memory for all agents
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# --- HR Strategist Agent ---
def build_hr_agent(llm):
    hr_prompt = PromptTemplate.from_template("You are an experienced HR strategist. {input}")
    return LLMChain(llm=llm, prompt=hr_prompt, memory=memory)

# --- ESCO Expert Agent (with tools) ---
def build_esco_agent(llm, tools=[]):
    esco_tools = [get_skill_tool, get_occupation_tool, get_skill_gap_tool]
    all_tools = tools + esco_tools
    return initialize_agent(
        tools=all_tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        memory=memory
    )

# --- Planner Agent (with tools) ---
def build_planner_agent(llm, tools=[]):
    return initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        memory=memory
    )
