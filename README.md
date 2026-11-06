<<<<<<< HEAD
# Agent-Dojo-Development
Agent Dojo Development
=======
# Mini-AgentDojo

A minimal implementation of the AgentDojo framework for evaluating
prompt injection attacks and defenses for LLM agents.

Based on: **"AgentDojo: A Dynamic Environment to Evaluate Prompt
Injection Attacks and Defenses for LLM Agents"**

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure API keys in .env
cp .env.example .env   # edit with your keys

# Run the basic agent
python main.py

# Run offline tests (no API keys needed)
python test_offline.py

# Run attack demo (no API keys needed)
python test_attack.py

# Run full experiment (requires API keys)
python experiments/run_experiment.py
```

## Project Structure

```
mini-agentdojo/
├── agent/                  # LLM agent and provider abstraction
│   ├── llm_agent.py        # Simple tool-calling agent
│   ├── pipeline.py         # Defense-aware agent pipeline
│   └── providers/          # LLM provider implementations
│       ├── base_provider.py
│       ├── gemini_provider.py
│       ├── groq_provider.py
│       ├── factory.py
│       └── response.py
├── attacks/                # Prompt injection strategies
│   ├── base_attack.py
│   ├── ignore_previous.py
│   └── important_message.py
├── data/                   # Simulated environment data
│   ├── emails.json
│   ├── calendar.json
│   └── files.json
├── defenses/               # Agent defense mechanisms
│   ├── __init__.py         # Defense registry
│   ├── no_defense.py       # Baseline (no filtering)
│   ├── delimiter.py        # Data/instruction separation
│   └── detector.py         # Injection pattern detection
├── environments/           # Simulated stateful environments
│   ├── base.py
│   └── workspace.py
├── evaluation/             # Task and security evaluation
│   ├── utility.py          # Task completion scoring
│   ├── security.py         # Attack success detection
│   └── metrics.py          # Aggregate metrics (ASR, utility)
├── experiments/            # Experiment orchestration
│   ├── run_experiment.py   # Full evaluation sweep
│   └── results.json        # Output (auto-generated)
├── tasks/                  # Task definitions
│   ├── user_tasks.py       # Legitimate user tasks
│   └── injection_tasks.py  # Attacker objectives
├── tools/                  # Environment tool implementations
│   ├── tool_registry.py    # Tool dispatch and schemas
│   ├── email_tools.py
│   ├── calendar_tools.py
│   └── drive_tools.py
├── test_offline.py         # Offline test suite (12 tests)
├── test_attack.py          # Attack strategy demo
├── test_injection.py       # Single injection test
├── test_tool_injection.py  # Tool-level injection experiment
├── config.py               # Configuration loader
├── main.py                 # Simple agent entry point
└── requirements.txt        # Python dependencies
```

## Core Concepts

### Evaluation Loop

For each `(user_task, defense, attack)` combination:

1. Create a fresh environment
2. (Attack mode) Inject malicious payload into environment data
3. Snapshot environment state
4. Run the agent with the defense pipeline
5. Evaluate **utility** (did the agent complete the user's task?)
6. Evaluate **security** (did the attack succeed?)

### Metrics

- **Benign Utility** — task completion score with no attack
- **Utility Under Attack** — task completion when injection is present
- **Attack Success Rate (ASR)** — fraction of attacks that achieved the attacker's goal

### Defenses

- `no_defense` — baseline, no filtering
- `delimiter` — wraps tool output in visible delimiters
- `detector` — regex-based injection pattern detection and redaction

>>>>>>> origin/ibad-test
