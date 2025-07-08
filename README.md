VOICE AGENT
===========

A modern, interactive voice agent powered by OpenAI Gemini models, supporting real-time speech-to-text (STT), text-to-speech (TTS), and multi-agent workflows. Built with Python, Textual UI, and the openai-agents framework.

---

FEATURES
--------
- **Real-time Voice Interaction:**
  - Speak to the agent and receive instant, spoken responses.
  - Uses OpenAI Gemini models for both STT and TTS.
- **Multi-Agent Workflow:**
  - Supports agent handoff (e.g., English/Urdu language detection).
  - Customizable workflow logic (see `agent1.py`).
- **Function Calling:**
  - Example tool: `get_weather(city)` for dynamic responses.
- **Modern Terminal UI:**
  - Built with [Textual](https://textual.textualize.io/) for a beautiful, interactive experience.
- **Extensible:**
  - Easily add new tools, agents, or workflows.

---

INSTALLATION
------------

1. **Clone the repository:**
   git clone <your-repo-url>
   cd voice_agent

2. **Install Python dependencies:**
   Requires Python 3.11+
   pip install .
   # or, for development:
   pip install -e .

   *Dependencies (from `pyproject.toml`):*
   - numpy
   - openai-agents[voice]
   - python-dotenv
   - sounddevice
   - textual

3. **Set up environment variables:**
   - Copy `.env.example` to `.env` (if provided) or create a `.env` file.
   - Add your Google/OpenAI API key:
     GOOGLE_API_KEY=sk-...

---

USAGE
-----

To start the voice agent UI:

    voice-agent

- Press **K** to start/stop recording.
- Speak into your microphone; the agent will transcribe and respond.
- Press **Q** to quit.

---

PROJECT STRUCTURE
-----------------

- `main.py`         : Entry point, launches the Textual UI and voice pipeline.
- `agent1.py`       : Example workflow and agent logic (customizable).
- `src/voice_agent/`: Package directory (minimal, can be extended).
- `pyproject.toml`  : Project metadata and dependencies.

---

CONFIGURATION
-------------
- **API Keys:** Set `GOOGLE_API_KEY` in your `.env` file.
- **Models:**
  - STT: `gemini-2.5-flash`
  - TTS: `gemini-2.5-flash-preview-tts`
  - Chat: `gemini-2.5-flash`
- **Custom Workflow:** Edit `agent1.py` to change agent logic, tools, or handoff behavior.

---

CONTRIBUTING
------------
1. Fork the repo and create a feature branch.
2. Make your changes (add features, fix bugs, improve docs).
3. Submit a pull request with a clear description.

---

CREDITS
-------
- Built by MuhammadAbdullah95
- Powered by [openai-agents](https://github.com/openai/openai-agents) and [Textual](https://textual.textualize.io/)

---

