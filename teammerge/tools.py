# tools.py

from langchain.tools import Tool
from .utils import calculate_skill_gap


# --- Skill Search Tool ---
def search_skills_semantic(query, vectorstore, top_k=5):
    results = vectorstore.similarity_search(query, k=top_k)
    if not results:
        return "No similar skills found."
    return "\n".join([f"{r.metadata['label']}: {r.page_content}" for r in results])

def get_skill_tool(vectorstore):
    return Tool(
        name="Skill Search",
        func=lambda q: search_skills_semantic(q, vectorstore),
        description="Search ESCO skills related to a concept using semantic similarity."
    )

# --- Occupation Search Tool ---
def search_occupations_semantic(query, vectorstore, top_k=5):
    results = vectorstore.similarity_search(query, k=top_k)
    if not results:
        return "No similar occupations found."
    return "\n".join([f"{r.metadata['label']}: {r.page_content}" for r in results])

def get_occupation_tool(vectorstore):
    return Tool(
        name="Occupation Search",
        func=lambda q: search_occupations_semantic(q, vectorstore),
        description="Search ESCO occupations related to a concept using semantic similarity."
    )

# --- Skill Gap Tool ---
def skill_gap_tool_func(query, calculate_skill_gap):
    try:
        parts = dict(part.strip().split("=") for part in query.split(";"))
        occupation = parts["occupation"].strip()
        user_skills = [s.strip() for s in parts["skills"].split(",")]
    except:
        return "Please format input as: occupation=<job>; skills=<comma-separated skills>"

    gap = calculate_skill_gap(user_skills, occupation)
    if isinstance(gap, str):
        return gap

    return (
        f"Missing essential skills for '{occupation}':\n- " +
        "\n- ".join(gap['missing_essential']) + "\n\n" +
        f"Missing optional skills:\n- " +
        "\n- ".join(gap['missing_optional'])
    )

def get_skill_gap_tool(calculate_skill_gap):
    return Tool(
        name="Skill Gap Analyzer",
        func=lambda q: skill_gap_tool_func(q, calculate_skill_gap),
        description="Compare known skills with the requirements for a given occupation. Format: occupation=<job>; skills=<comma-separated skills>"
    )
