# 🤖 LangGraph Supervised Quickstart

A **minimal example** of a multi-agent supervisor system using LangGraph v1. Designed for easy understanding and quick setup.

![Demo](docs/assets/demo.gif?raw=true)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/LangGraph-v1.x-green.svg)](https://github.com/langchain-ai/langgraph)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![GitHub issues](https://img.shields.io/github/issues/joaomede/langgraph-supervised-quickstart)](https://github.com/joaomede/langgraph-supervised-quickstart/issues)

---

## ✨ What This Project Demonstrates

- 🎯 **Supervisor Pattern** - LLM-based routing to specialist agents
- 🔤 **Text Agent** - Entity extraction + keyword analysis (2 tools)
- 📊 **Data Agent** - Statistics + table formatting (2 tools)
- 💬 **Two CLI Modes** - Interactive chat and single-query
- 🌍 **Language-Agnostic Design** - No hardcoded stopwords
- 🐳 **Docker Ready** - Containerized setup included

---

## 🏗️ Architecture

```mermaid
graph TD
    User[👤 User Query] --> Supervisor[🎯 Supervisor LLM]
    
    Supervisor -->|Route Decision| Router{Routing Logic}
    
    Router -->|Text-related| TextAgent[🔤 Text Agent]
    Router -->|Data/numbers| DataAgent[📊 Data Agent]
    Router -->|Simple query| DirectResponse[💬 Direct Answer]
    
    TextAgent --> TextTools["🔧 extract_entities<br/>🔧 keyword_counts"]
    DataAgent --> DataTools["🔧 calculate_stats<br/>🔧 format_table"]
    
    TextTools --> Supervisor
    DataTools --> Supervisor
    DirectResponse --> User
    Supervisor --> User
    
    style Supervisor fill:#8e24aa,stroke:#e1bee7,stroke-width:3px,color:#fff
    style TextAgent fill:#558b2f,stroke:#c5e1a5,stroke-width:2px,color:#fff
    style DataAgent fill:#1976d2,stroke:#90caf9,stroke-width:2px,color:#fff
```

**How it works:**
1. **Supervisor** receives query and analyzes intent
2. **Routes** to specialist agents via tool handoff (`transfer_to_text`, `transfer_to_data`)
3. **Agents** execute tools and return results
4. **Supervisor** synthesizes final answer

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- OpenAI API key ([get one here](https://platform.openai.com/api-keys))
- (Optional) LangSmith API key for tracing ([get one here](https://smith.langchain.com/))

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/joaomede/langgraph-supervised-quickstart.git
cd langgraph-supervised-quickstart

# 2. Create virtual environment
python3.10 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 5. Verify installation
python -c "import langchain, langgraph; print('✅ Dependencies installed successfully')"
```

### Usage

**Interactive Chat Mode (default):**
```bash
PYTHONPATH=src python -m cli
```

```
╭──────────────────────────────────────────────╮
│   🤖 Multi-Agent Supervisor System           │
│   Powered by LangGraph v1                    │
╰──────────────────────────────────────────────╯

You: Extract entities from Microsoft and Google

🤔 Thinking...

╭─────────── 🤖 Assistant │ Message #1 ──────────╮
│  Entities extracted:                           │
│  • Microsoft                                   │
│  • Google                                      │
╰────────────────────────────────────────────────╯
```

**Single Query Mode:**
```bash
PYTHONPATH=src python -m cli --query "Calculate stats for: 100, 200, 300"
```

**Interactive Commands:**
- `help` - Show available commands and tips
- `clear` - Reset conversation history
- `exit` / `quit` / `bye` - End session

---

## 🐳 Docker Support

**Interactive mode:**
```bash
# Build and run
docker compose up --build

# Or using Docker directly
docker build -t langgraph-quickstart .
docker run -it --env-file .env langgraph-quickstart
```

**Single query mode:**
```bash
docker run --env-file .env langgraph-quickstart --query "Extract entities from: Tesla and SpaceX"
```

📖 **[Complete Docker Guide →](docs/DOCKER_GUIDE.md)**

---

## 💡 Example Queries

### Text Analysis
- "Extract entities from: Apple launched iPhone in California"
- "Find keywords in: artificial intelligence and machine learning"
- "Analyze text: OpenAI and LangGraph enable agentic systems"

### Data Analysis
- "Calculate statistics for: 23, 45, 67, 89, 12"
- "Compute mean and median of: 5, 15, 25, 35"
- "Show stats table for: 100, 200, 300, 400, 500"

### Multi-Agent Queries
- "Analyze 'Tesla and SpaceX' and compute stats for: 10, 20, 30"
- "Extract entities from my text and calculate averages: 5, 10, 15"

---

## 🛠️ Technology Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Orchestration** | LangGraph | v1.x | Multi-agent graph workflows |
| **LLM Framework** | LangChain | ~0.3.x | Agent creation, tool binding |
| **LLM Provider** | OpenAI GPT-4o-mini | Latest | Supervisor and agents |
| **Terminal UI** | Rich | ~13.x | Beautiful formatting |
| **Language** | Python | 3.10+ | Type hints, modern syntax |

---

## 📁 Project Structure

```
langgraph-supervised-quickstart/
├── src/
│   ├── agent/                 # Core multi-agent system
│   │   ├── graph.py           # Supervisor + routing logic
│   │   ├── agent_builders.py  # Text & Data agent factories
│   │   ├── tools.py           # 4 tools (extract_entities, keyword_counts, calculate_stats, format_table)
│   │   └── cli.py             # Single-query mode
│   └── cli.py                 # Interactive chat mode (main entry point)
├── docs/
│   └── DOCKER_GUIDE.md
├── .env.example               # Environment configuration template
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Multi-stage container build
├── docker-compose.yml         # Container orchestration
├── pyproject.toml             # Project metadata
├── LICENSE                    # MIT License
├── CONTRIBUTING.md            # Contribution guidelines
└── CODE_OF_CONDUCT.md         # Community standards
```

---

## 🤝 Contributing

This is a minimal educational example. Contributions that maintain simplicity are welcome.

**How to contribute:**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'feat: description'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 🔧 Configuration

**Environment Variables (.env):**
```bash
# Required
OPENAI_API_KEY=sk-proj-...

# Optional (recommended for debugging)
LANGSMITH_API_KEY=lsv2_...
LANGSMITH_TRACING=true

# Optional (defaults to gpt-4o-mini)
OPENAI_MODEL=gpt-4o-mini
```

**CLI Options:**
```bash
# Enable ASCII banner in interactive mode
CLI_ASCII_BANNER=true

# Enable debug mode with verbose traces
DEBUG=true
```

---

## 📊 Project Characteristics

| Aspect | Implementation |
|--------|----------------|
| **Architecture** | Supervisor + 2 Specialist Agents |
| **Routing** | LLM-based tool handoff |
| **Tools** | 4 focused tools (2 per agent) |
| **UI** | Rich terminal interface |
| **Memory** | Last 10 messages for context |
| **Language Support** | Language-agnostic processing |
| **Modes** | Interactive + Single-query |
| **Complexity** | Minimal (educational purpose) |

---

## 🎓 What You'll Learn

This minimal example covers:
- **LangGraph v1** - Graph-based agent orchestration
- **Supervisor Pattern** - Delegating to specialist agents via tools
- **Tool-based Routing** - Agent handoff using tools (not conditional edges)
- **ReAct Agents** - Reasoning and acting pattern
- **Conversation Memory** - Managing context in multi-turn dialogues

---

## 📚 Theoretical Foundation

This project implements patterns from four foundational papers in LLM agent architecture:

### 1. Chain-of-Thought Prompting (Wei et al., 2022)
**Foundation for structured reasoning**

Wei et al. demonstrated that prompting LLMs with step-by-step reasoning examples dramatically improves performance on complex tasks. This "chain-of-thought" approach forms the basis for how our supervisor and agents decompose problems.

- 📄 Paper: [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903)
- 🔍 **Applied in this project:** The supervisor uses CoT-style reasoning to analyze queries before routing to specialists

### 2. ReAct: Reasoning + Acting (Yao et al., 2022)
**Synergizing thought and action**

ReAct introduced the paradigm of interleaving reasoning traces with task-specific actions, enabling LLMs to maintain and update plans while interacting with external tools and information sources.

- 📄 Paper: [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)
- 🔍 **Applied in this project:** 
  - Supervisor loop: `Thought → Action (route to agent) → Observation (tool results) → Thought`
  - Agents execute tools and return observations that inform subsequent reasoning
  - Interactive debugging shows this reasoning trace in action

### 3. AutoGen: Multi-Agent Conversations (Wu et al., 2023)
**Conversable agents and orchestration patterns**

AutoGen demonstrated how to build LLM applications using conversable agents that can operate in multiple modes (LLM-only, human-in-loop, tool use), simplifying complex multi-agent workflows.

- 📄 Paper: [AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation](https://arxiv.org/abs/2308.08155)
- 🔍 **Applied in this project:**
  - Structured message passing between supervisor and specialist agents
  - Tool-based handoff mechanism (`transfer_to_text`, `transfer_to_data`)
  - Conversation memory for context maintenance

### 4. MetaGPT: Meta Programming for Collaboration (Hong et al., 2023)
**SOPs and role-based coordination**

MetaGPT introduced Standard Operating Procedures (SOPs) as a meta-programming approach to multi-agent collaboration, with role-based assignments and validation of intermediate outputs.

- 📄 Paper: [MetaGPT: Meta Programming for Multi-Agent Collaborative Framework](https://arxiv.org/abs/2308.00352)
- 🔍 **Applied in this project:**
  - Clear role separation: Supervisor (router) vs. Specialist Agents (executors)
  - Defined tool contracts (input/output schemas)
  - Each agent has a specific domain of expertise (text vs. data analysis)

### How These Papers Inform the Architecture

```
Chain-of-Thought → Structured reasoning in supervisor prompts
       ↓
    ReAct → Thought-Action-Observation loop for dynamic planning
       ↓
   AutoGen → Conversable agents with tool handoff mechanisms
       ↓
  MetaGPT → Role-based specialists with defined responsibilities
       ‖
   [This Project]
```

**Key Takeaway:** This minimal implementation demonstrates how modern multi-agent systems combine:
1. **Reasoning** (CoT) - Breaking down complex queries
2. **Action** (ReAct) - Executing tools and incorporating observations
3. **Coordination** (AutoGen) - Structured agent communication
4. **Specialization** (MetaGPT) - Role-based task delegation

**📖 Want to dive deeper?** See the [Research Foundations](docs/RESEARCH_FOUNDATIONS.md) document for detailed analysis of each paper, implementation examples, and future enhancement ideas.

---

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Built With

**Frameworks & Tools:**
- **[LangGraph](https://github.com/langchain-ai/langgraph)** - Graph-based agent orchestration
- **[LangChain](https://github.com/langchain-ai/langchain)** - LLM application framework
- **[Rich](https://github.com/Textualize/rich)** - Terminal formatting
- **[OpenAI](https://openai.com/)** - LLM provider

**Theoretical Foundations:**
- Wei et al. (2022) - Chain-of-Thought Prompting
- Yao et al. (2022) - ReAct: Reasoning and Acting
- Wu et al. (2023) - AutoGen Multi-Agent Framework
- Hong et al. (2023) - MetaGPT Meta Programming

See [Theoretical Foundation](#-theoretical-foundation) section for details.

---

## Troubleshooting

### Common Issues

**API Key Not Found**
```
Error: OpenAI API key not found
```
**Solution:** Ensure your `.env` file exists and contains `OPENAI_API_KEY=sk-...`

**Import Errors**
```
ModuleNotFoundError: No module named 'langchain'
```
**Solution:** Activate virtual environment and run `pip install -r requirements.txt`

**Docker Port Conflicts**
```
Error: port is already allocated
```
**Solution:** Check `docker-compose.yml` and modify port mappings if needed

**PYTHONPATH Issues**
```
ModuleNotFoundError: No module named 'agent'
```
**Solution:** Always run with `PYTHONPATH=src` prefix or add to your `.env` file

---

## Documentation

- 🐳 **[Docker Guide](docs/DOCKER_GUIDE.md)** - Complete containerization guide
- 📄 **[Research Foundations](docs/RESEARCH_FOUNDATIONS.md)** - Deep dive into the papers that inspired this architecture
- 📄 **[Contributing](CONTRIBUTING.md)** - Contribution guidelines
- 🔒 **[Security](SECURITY.md)** - Security policy
- 📖 **[Code of Conduct](CODE_OF_CONDUCT.md)** - Community standards

## 📞 Support

- 💬 Interactive help: Type `help` in interactive mode
- 🐛 Report issues: [GitHub Issues](https://github.com/joaomede/langgraph-supervised-quickstart/issues)
- 💡 Questions: [GitHub Discussions](https://github.com/joaomede/langgraph-supervised-quickstart/discussions)

---

**By [João Medeiros](https://github.com/joaomede)** - A minimal example for learning LangGraph v1 supervisor patterns.
