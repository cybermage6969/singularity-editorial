# Architecture Plan for "The Singularity Editorial" (MVP)

I need you to create a comprehensive implementation plan for a Python-based MVP application called **"The Singularity Editorial"**. This app simulates a one-person editorial team using 4 distinct AI Agents to process content sequentially.

## 1. Project Goal

Build a local web application where the user acts as the "Editor-in-Chief". The user inputs a raw topic or link, and the system processes it through a 4-stage AI pipeline to generate a viral, hardcore sci-fi video script and distribution strategy.

## 2. Tech Stack Requirements

| Category | Choice |
|----------|--------|
| **Language** | Python 3.9+ |
| **UI Framework** | Streamlit (must use `st.session_state` to manage the workflow pipeline) |
| **LLM Integration** | Generic OpenAI-compatible client (e.g., `openai` library) |
| **Configuration** | `python-dotenv` for API key management |

> **Crucial:**
> - Do not hardcode any keys. Use a `.env` file structure.
> - Allow the user to override the `BASE_URL` in the `.env` (to support DeepSeek / Gemini via OneAPI in the future).

## 3. The 4-Agent Pipeline (Core Logic)

Plan for 4 modular Agent classes. Each Agent takes the output of the previous step as input.

### Agent 1: The Sentinel (Information Gatherer)

- **Role:** Filters information for "High Entropy".
- **Logic:** Force-pairs the user's input with a classic **Sci-Fi motif** (e.g., *Dune*, *Three-Body Problem*) or a **Historical Parallel** (e.g., Roman Empire).
- **Output:** A structured briefing with "Reality Event" vs. "Sci-Fi Mirror".

### Agent 2: The Adversary (Logic Debater)

- **Role:** The Devil's Advocate based on Game Theory & Evolutionary Psychology.
- **Logic:** **Never** agrees with the input. Finds logical fallacies, human-centric biases, and applies "Entropy Laws" to challenge the thesis.
- **Output:** A "Refined Thesis" and a list of "Logical Loopholes".

### Agent 3: The Visual Director (Neuro-Scriptwriter)

- **Role:** Converts the thesis into a video script.
- **Logic:** Uses Neuromarketing principles. Must label script sections with target neurotransmitters:
  - **Dopamine** — Curiosity / Anticipation
  - **Oxytocin** — Empathy / Trust
  - **Endorphins** — Humor / Aha-moment

  Visual style defined as "Cyberpunk / Terminal".
- **Output:** A 2-column script (Visual Prompt vs. Audio).

### Agent 4: The Growth Hacker (Distribution)

- **Role:** Maximizes CTR and Viral Potential.
- **Logic:** Generates titles using "Curiosity Gap" and "Intellectual Offense". Designs thumbnail concepts that provoke debate.
- **Output:** 5 Titles + 3 Thumbnail descriptions + Tags.

## 4. Deliverables for this Plan

Please generate a detailed plan that includes:

1. **File Structure** — A clean, modular folder structure (e.g., separate `agents/` directory).
2. **Class Design** — Pseudocode or outlines for the Agent base class and the 4 specific subclasses.
3. **Data Flow** — How state is passed from one agent to the next in Streamlit.
4. **Configuration** — How the `.env` file and API client will be set up to allow "fill-in-the-blank" API keys later.
5. **Step-by-Step Implementation Guide** — A list of steps I can follow to build this.
