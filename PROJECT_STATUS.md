# PROJECT STATUS — Mini-AgentDojo

**Last Updated:** 2026-11-04

## Objective

Implement a minimal reproduction of the AgentDojo framework for evaluating
prompt injection attacks and defenses for LLM agents.

## Architecture

```
main.py ──────► LLMAgent (legacy) ──► Provider ──► Tool Loop
                                         │
experiments/run_experiment.py             │
    └── AgentPipeline ──► Defense ──► Provider ──► Tool Loop
            │                                         │
            ▼                                         ▼
    WorkspaceEnvironment ◄────────── tool_registry.py
            │
            ▼
    Evaluation (utility + security + metrics)
```

## Completed and Verified Features

- [x] WorkspaceEnvironment with state snapshots and from_snapshot
- [x] 4 read tools + 1 write tool (send_email)
- [x] Tool registry with OpenAI-compatible schemas
- [x] LLMAgent with Gemini/Groq provider fallback
- [x] BaseProvider abstraction (Gemini + Groq)
- [x] 3 user tasks, 2 injection tasks
- [x] 2 attack strategies (IgnorePrevious, ImportantMessage)
- [x] 3 defense mechanisms (NoDefense, Delimiter, Detector)
- [x] AgentPipeline with defense integration
- [x] Utility evaluation (email, calendar, file categories)
- [x] Security evaluation (file disclosure, instruction following)
- [x] Metrics aggregation (benign utility, attack utility, ASR)
- [x] Experiment runner with full sweep orchestration
- [x] Offline test suite — 12 tests, all passing
- [x] README documentation
- [x] Dependencies installed (google-genai, groq, python-dotenv)

## Incomplete / Not Yet Verified

- [ ] Live LLM integration test (requires API key validation)
- [ ] Full experiment run with real LLM responses
- [ ] Result visualization / plots
- [ ] Additional attack strategies (composite, parameterized)
- [ ] Additional user tasks and injection tasks
- [ ] Git version control initialization

## Important Decisions

- The `LLMAgent` class (original) is preserved for backward compatibility.
  New experiments should use `AgentPipeline`.
- Defenses operate on serialized tool output (JSON text), not structured data.
- Environment state is captured before and after agent runs for evaluation.
- API keys are in `.env` and are never committed or logged.

## How to Run

```bash
# Offline tests (no API keys)
python test_offline.py

# Attack demo
python test_attack.py

# Basic agent (needs API keys)
python main.py

# Full experiment (needs API keys)
python experiments/run_experiment.py
```

## Next Task

Run a full end-to-end experiment with a live LLM provider to validate
the entire pipeline, collect real metrics, and verify evaluation correctness.

## Known Blockers

- Experiment runner and agent pipeline require valid API keys
  to produce meaningful results.
- No result visualization yet.

