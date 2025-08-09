# team.py — CrewAI x Ollama (DeepSeek Coder 6.7B)
# Fully UTF-8 safe for Windows, telemetry disabled, writes to crew_output.md

import os, sys
from crewai import Agent, Task, Crew, LLM

# --- Force UTF-8 and silence noisy logs ---
os.environ.update({
    "CREWAI_TELEMETRY_OPT_OUT": "1",
    "DO_NOT_TRACK": "1",
    "OTEL_SDK_DISABLED": "true",
    "NO_COLOR": "1",
    "TERM": "dumb",
})
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# --- Local LLM via Ollama ---
local_model = LLM(
    model="ollama/deepseek-coder:6.7b",   # provider prefix required
    base_url="http://localhost:11434",
    api_key="ollama",                     # dummy, not used by Ollama
)

# --- Agents ---
eng_director = Agent(
    name="Engineering Director",
    role="Architecture & Code Quality",
    goal="Keep the pipeline vision aligned and hardened before any code ships.",
    backstory="Seasoned architect; enforces maintainable patterns, tests, and logging.",
    llm=local_model,
    verbose=False,
)

backend = Agent(
    name="Backend",
    role="Slides→Notion Pipeline",
    goal="Implement Google Slides → Notion with idempotent upserts (slide hash) and solid retries.",
    backstory="APIs, parsing, and resilience-first coding.",
    llm=local_model,
    verbose=False,
)

qa = Agent(
    name="QA",
    role="Test & Harden",
    goal="Design pytest coverage to catch empty slides, rate limits, and idempotency issues.",
    backstory="Finds failure modes before users do.",
    llm=local_model,
    verbose=False,
)

# --- Tasks ---
t1 = Task(
    agent=eng_director,
    description="Outline a high-level 5–10 step plan for Google Slides → Notion. Include open questions.",
    expected_output="• Bullet plan\n• Unknowns checklist",
)

t2 = Task(
    agent=backend,
    description="Propose Python module layout and function skeletons for the pipeline, with logging & retries.",
    expected_output="• Module tree\n• Python skeletons\n• Notes on hashing, pagination, and error handling",
)

t3 = Task(
    agent=qa,
    description="Draft a pytest suite for edge cases and idempotency validation.",
    expected_output="• Test file list\n• Example pytest stubs",
)

# --- Crew Run ---
crew = Crew(agents=[eng_director, backend, qa], tasks=[t1, t2, t3])

if __name__ == "__main__":
    result = crew.kickoff()
    with open("crew_output.md", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(result))
    print("OK: wrote crew_output.md")
