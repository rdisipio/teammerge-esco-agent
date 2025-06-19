# teammerge-esco-agent

**A multi-agent AI assistant that explores ESCO occupations and skills to support human-centered workforce restructuring.**

This project uses LangChain, ChromaDB, and the ESCO taxonomy to simulate a collaborative AI system that assists with team planning after a company merger or restructuring. The system includes specialized agents (HR Strategist, ESCO Expert, Planner) and tools for semantic search, skill analysis, and career path planning.

---

## 🚀 Features

- 🔎 Semantic search over ESCO occupations and skills
- 🧠 Skill gap analysis based on target roles
- 🗂️ Multi-agent simulation using LangChain
- 🧰 Custom tools for reasoning over structured data
- 💬 Dialogue-driven interface for realistic team planning scenarios

---

## 📦 Installation

1. Clone the repo:

```bash
git clone https://github.com/yourusername/teammerge-esco-agent.git
cd teammerge-esco-agent
```

2. Create a virtual environment and install dependencies:

```bash
pipenv install
```

3. Download the [ESCO v1.2 datasets](https://ec.europa.eu/esco/portal/download) and place them in `./data/esco`.

---

## 🧪 Running the Notebook

Open `teammerge_agent.ipynb` in Jupyter and run through the cells to:

- Load and index ESCO data with ChromaDB
- Define the agent roles and tools
- Simulate realistic restructuring conversations

---

## 🛠️ Tools Overview

- `Skill Search`: Find ESCO skills semantically
- `Occupation Search`: Retrieve similar job roles
- `Skill Gap Analyzer`: Compare current skills with target occupations

---

## 🧠 Architecture

- Built with [`LangChain`](https://github.com/langchain-ai/langchain)
- Uses [`ChromaDB`](https://www.trychroma.com/) for fast vector search
- Embeddings via `sentence-transformers`
- Local ESCO data, no API calls required

---

## 📚 License

This project is licensed under the **MIT License** — a permissive license that allows reuse, modification, and redistribution, even for commercial purposes, as long as the original license and attribution are included.

See [LICENSE](./LICENSE) for details.

---

## ✍️ Author

Built by Riccardo Di Sipio, PhD - Dayforce HCM.
Inspired by practical questions about AI, work, and collaboration.

