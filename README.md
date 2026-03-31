# Vibe Coding

> **Built entirely with natural language. Zero manual coding.**

---

## 🚀 What is Vibe Coding?

Vibe Coding is a new paradigm of software development where you **describe what you want in plain English** and AI builds it for you.

- ❌ No memorizing syntax
- ❌ No debugging semicolons for hours
- ✅ You are the architect — AI is the engineer

The barrier to building software is no longer technical skill.
**It is the clarity of your thinking.**

---

## 🛫 Project Overview

This is a **web-based AI Flight Search System** built using a multi-agent architecture — powered by **Google Gemini 2.5 Flash** and the **Duffel API**.

You type something like:

```
"I want to fly from Montreal to Toronto next Friday under $300"
```

And the system:
- ✅ Understands your intent using AI
- ✅ Converts it into a structured search query automatically
- ✅ Queries live flight data from real airline databases
- ✅ Returns flights with prices, times & stops
- ✅ Displays everything in a clean two-panel web interface

No forms. No dropdowns. No manual filters. Just talk to it like a human.

---

## 🏗️ System Architecture

```
User (Natural Language)
        │
        ▼
┌─────────────────────────────────┐
│     Agent 1 — Orchestration     │
│       Gemini 2.5 Flash (LLM)    │
│                                 │
│  Perception → Intent Parsing    │
│  → Structured JSON Output       │
│  { origin, destination,         │
│    departure_date, passengers,  │
│    price_limit }                │
└────────────────┬────────────────┘
                 │ Structured JSON
                 ▼
┌─────────────────────────────────┐
│     Agent 2 — Flight Search     │
│                                 │
│  Request Handler → API Caller   │
│  → Raw Flight Results           │
└────────────────┬────────────────┘
                 │ API Call
                 ▼
        ┌────────────────┐
        │   Duffel API   │
        │ (Live Flights) │
        └────────────────┘
                 │ Results
                 ▼
┌─────────────────────────────────┐
│     Web UI — Flask + Python     │
│  Left: Flight Results Cards     │
│  Right: AI Chat Interface       │
└─────────────────────────────────┘
```

---

## ⚙️ Tech Stack

| Component | Technology |
|---|---|
| LLM (AI Brain) | Google Gemini 2.5 Flash |
| Flight Data | Duffel API |
| Backend | Python + Flask |
| AI Development Tool | Gemini CLI |
| Config Management | `.env` file |

---

## 📦 Getting Started

### Prerequisites
- Python 3.10+
- A [Gemini API Key](https://aistudio.google.com/)
- A [Duffel API Key](https://duffel.com/)

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/iamkarandeepsingh/Vibe-Coding-
cd Vibe-Coding-
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set up your API keys**

Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
DUFFEL_API_KEY=your_duffel_api_key_here
```

**4. Run the application**
```bash
python app.py
```

**5. Open in your browser**
```
http://localhost:5000
```

---

## 💬 Example Queries

```
"I want to fly from Montreal to Toronto next Monday"
"Find me a flight from London to Paris this weekend under $200"
"I need a return flight from New York to LA, departing March 20"
```

---

## 📁 Project Structure

```
Vibe-Coding-/
├── app.py                  # Main Flask application
├── agents/
│   ├── agent_1_intent_parser.py   # Orchestration agent
│   └── agent_2_flight_search.py   # Flight search agent
├── templates/              # HTML web interface
├── static/                 # CSS and JS assets
├── requirements.txt        # Python dependencies
└── .env                    # API keys (not committed)
```

---

## 🔑 API Notes

- **Gemini API** — Free tier includes 1,000 requests/day via [Google AI Studio](https://aistudio.google.com/)
- **Duffel API** — Test mode provides sandbox flight data. Sign up at [duffel.com](https://duffel.com/)

> ⚠️ Never commit your `.env` file or share your API keys publicly.

---

## 💡 Key Takeaway

This project is proof that in the AI era, **anyone with a clear idea and the ability to communicate it can build production-level software.**

> *"The builders of tomorrow won't be the ones who memorized the most syntax.*
> *They'll be the ones who asked the best questions."* 🧠

---

## 📄 License

MIT License — feel free to use, modify, and build on this project.

---

## 🙌 Acknowledgements

- [Google Gemini](https://deepmind.google/technologies/gemini/) — for the LLM powering the agents
- [Duffel](https://duffel.com/) — for the real-time flight data API
- [Gemini CLI](https://github.com/google-gemini/gemini-cli) — the vibe coding tool used to build this entire project
