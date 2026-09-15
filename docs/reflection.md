# Project Reflection

### Architecture
I structured the phases primarily as deterministic workflows with LLMs used for specific, constrained tasks (extraction, summarization) rather than free-wheeling agentic loops. This decision was driven by cost control, reliability, and the need for predictable JSON outputs. Phase 3 incorporates a slight hybrid approach where the legitimacy "agent" dynamically uses tools, but its final output is still strictly constrained.

### Prompt Engineering
The most impactful prompt engineering choice was defining the exact date in the system prompt (`Today's date is {today}`) and giving explicit instructions on how to calculate `posting_age_days`. Before doing this, the LLM would frequently hallucinate ages or leave the field null.

### Legitimacy Agent
The legitimacy agent relies on two main tools: Tavily (web presence) and WHOIS (domain age). I prioritized domain age because scammers rarely use aged domains (10+ years old) for quick phishing operations. A limitation is that scammers can impersonate real companies using free email providers, so checking if the contact email matches the domain is critical.

### Models and Cost
I primarily used `google/gemini-2.5-flash` via OpenRouter. This model is incredibly cheap and surprisingly good at adhering to Pydantic schemas when used with the `instructor` library. It kept total API costs practically negligible during development.

### Coding Agent Process
I used the Antigravity coding agent to build the core infrastructure.
- **Initial instructions**: Build all 3 phases based on the assignment spec, focusing on Pydantic schemas and the Instructor library.
- **Iterations**: It took about 3 iterations. The agent initially tried to use `gemini-2.0-flash-001` which isn't available on OpenRouter, causing 404 errors. I had to manually guide it to use `gemini-2.5-flash`.
- **Manual fixes**: I had to manually resolve a Windows console encoding issue (`cp1252` crashing on emojis) by adding `sys.stdout.reconfigure(encoding='utf-8')` to the entry points, a problem I had learned how to fix during Lab 1.
- **Agent performance**: The agent was excellent at scaffolding the boilerplate and Pydantic schemas, but struggled slightly with external API idiosyncrasies (like the OpenRouter model naming conventions).
