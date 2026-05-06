# Udara Flood Intelligence Agent
### AI-Powered Early Warning System for Kenya, Ghana, and Africa
### Built with Google Agent Development Kit (ADK) and Google Earth Engine

---

## 📋 Overview

The **Udara Flood Intelligence Agent** is a multi-agent AI system designed to save lives through early warning of floods in Kenya, and across Africa.

This project transforms a general-purpose Google Earth Engine (GEE) dataset explorer into a **mission-critical Flood Early Warning System (EWS)** — one that monitors rainfall, soil moisture, and satellite imagery to issue community flood alerts in real time.

Built on top of **Google's Agent Development Kit (ADK)**, the system demonstrates how agentic AI can move beyond simple chatbots to become **active monitors** of environmental risk - agents that watch the watershed so communities don't have to.

**Mission:** To build equitable, community-centred AI tools that provide life-saving flood early warnings to vulnerable communities in Kenya, Ghana, and Africa — starting with the Tana River Basin and expanding continent-wide.

---

## 🏗️ Architecture

This system uses a 5-agent multi-agent architecture built with Google ADK. The root agent `flood_intelligence_agent` acts as the coordinator, sitting above five specialist sub-agents: `gee_search_agent` for finding GEE datasets, `flood_knowledge_agent` for RAG-powered flood expertise, `risk_assessment_agent` for threshold evaluation and alert generation, `web_search_agent` for current flood news, and `web_fetch_agent` for fetching full page content from URLs.

**Why two separate web agents?** This is an ADK hard rule - Google's built-in `google_search` tool cannot be combined with custom Python function tools in the same agent. So web search and web fetching must live in separate agents.

Agent roles in full:

`flood_intelligence_agent` - Root coordinator. Routes every query to the right sub-agent and formats all responses in the Udara EWS structure. Uses all sub-agents via AgentTool.

`gee_search_agent` - Finds flood-relevant GEE datasets. Tools: `search_gee_catalog`, `search_flood_datasets`, `get_flood_dataset_details`.

`flood_knowledge_agent` - RAG-powered flood expert covering Kenya, Ghana, and Africa. Tools: `query_flood_knowledge_base`, `get_region_flood_profile`, `list_available_regions`.

`risk_assessment_agent` - Evaluates rainfall and soil moisture against thresholds. Issues Watch/Warning/Alert/Extreme levels. Generates SMS and Swahili radio scripts. Tools: `assess_flood_risk`, `generate_flood_alert`.

`web_search_agent` - Searches the web for current flood news and advisories using Google Search only. Tool: `google_search` (built-in, no custom tools).

`web_fetch_agent` - Fetches full content from a specific URL. Tool: `fetch_webpage_text` (custom only, no google_search).

---

## 📡 GEE Datasets Used

The system is pre-configured with 7 flood-relevant GEE datasets:

GPM IMERG (`NASA/GPM_L3/IMERG_V06`) - 10 km resolution, updates every 30 minutes. Primary rainfall monitoring tool. Covers the globe. Key band: `precipitationCal`.

SMAP Soil Moisture (`NASA_USDA/HSL/SMAP10KM_soil_moisture`) - 10 km, daily. Measures soil saturation — the single best predictor of flood potential. Values above 0.85 mean near-saturated soil where even light rain triggers flooding.

Sentinel-1 SAR (`COPERNICUS/S1_GRD`) - 10 m resolution, 6-12 day revisit. Sees through clouds using radar — critical during Africa's rainy seasons when optical imagery is blocked. Key band: VV polarisation.

MERIT DEM (`MERIT/DEM/v1_0_3`) - 90 m, static. Digital elevation model used to model which downstream areas flood when a river overflows.

JRC Global Surface Water (`JRC/GSW1_4/GlobalSurfaceWater`) - 30 m, annual. Permanent water baseline — used to separate new flood water from rivers and lakes that are always there.

WorldPop (`WorldPop/GP/100m/pop`) - 100 m, annual. Population density — used to estimate how many people are in a flood impact zone.

Global Flood Database (`GLOBAL_FLOOD_DB/MODIS_EVENTS/V1`) - 250 m, historical events 2000-2018. Historical flood footprints used as a baseline for what a flood looks like in a given area.

---

## ⚠️ Flood Alert Thresholds

These thresholds are calibrated for Kenya's river basins based on historical GPM IMERG and SMAP data:

🟡 WATCH - Rainfall at or above 25 mm/day OR soil moisture at or above 0.75. Action: Monitor closely, prepare emergency kits.

🟠 WARNING - Rainfall at or above 50 mm/day OR soil moisture at or above 0.85. Action: Move valuables to higher ground, stay alert.

🔴 ALERT - Rainfall at or above 75 mm/day OR soil moisture at or above 0.92. Action: Evacuate low-lying areas immediately.

🚨 EXTREME - Rainfall at or above 100 mm/day OR soil moisture at or above 0.97. Action: EVACUATE NOW. Do not cross flooded roads. Call 999.

When both rainfall AND soil moisture are elevated, the risk level is automatically upgraded by one step.

---

## 🌍 Configured Monitoring Regions

**Kenya:** Tana River Basin (HIGH risk) covering Garissa, Tana River, Embu, and Kitui counties. Athi River Basin (HIGH risk) covering Nairobi, Machakos, and Makueni. Lake Victoria Basin (HIGH risk) covering Kisumu, Siaya, and Homa Bay. Ewaso Ng'iro Basin (MEDIUM risk) covering Samburu, Isiolo, and Laikipia.

---

## 🗂️ Project Structure

Your project folder should look exactly like this:

```
GEE-Agent/
│
├── README.md
├── requirements.txt
│
└── gee_agent/
        ├── __init__.py        ← already exists, do not edit
        ├── agent.py           ← root agent and all 5 sub-agents
        ├── tools.py           ← all tool functions
        ├── flood_config.py    ← regions, thresholds, dataset registry
        ├── rag_store.py       ← RAG knowledge base + retrieval
        └── .env               ← your API key
```

---

## ⚙️ Prerequisites

Before you begin make sure you have: Python 3.9 or higher, a Google Account, a Google AI Studio API Key (free - get one at https://aistudio.google.com), and Git installed on your machine.

---

## 🚀 Installation & Setup

**Step 1 - Clone the repository**

```bash
git clone https://github.com/johnmwangimegwe/GEE-Agent.git
cd GEE-Agent
```

**Step 2 - Create a virtual environment**

On Windows (Git Bash):
```bash
python -m venv venv
source venv/Scripts/activate
```

On Mac or Linux:
```bash
python -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal prompt confirming it is active.

**Step 3 - Install dependencies**

```bash
pip install -r requirements.txt
```

**Step 4 - Get your Google AI Studio API Key**

Go to https://aistudio.google.com, click Get API Key in the top left, then click Create API Key. Copy the key - it starts with `AIzaSy...`

Free tier gives you 15-20 requests per day per model at no cost. For workshops or production use, add $5 billing at https://aistudio.google.com/billing - this gives you thousands of requests and removes all quota errors.

**Step 5 - Create your .env file**

Create a file called `.env` inside the `gee_agent/` folder with this single line:

```
GOOGLE_API_KEY=your_actual_api_key_here
```

Never commit this file to GitHub. The `.gitignore` in this repo already excludes it.

**Step 6 - Verify the installation**

Run this from the project root:

```bash
python -c "from gee_agent.agent import root_agent; print('OK:', root_agent.name)"
```

You should see: `OK: flood_intelligence_agent`

If you see an error, check the Troubleshooting section at the bottom of this file.

---

## ▶️ Running the Agent

**Web UI:**

```bash
adk web
```

Open your browser and go to `http://localhost:8000`. Select `gee_agent` from the dropdown in the top left and start chatting.

**Command Line — for quick testing:**

```bash
adk run gee_agent
```

This starts an interactive chat session directly in your terminal.

---

## Try out some prompts
```bash
1. List all flood monitoring regions configured for Kenya.
```

```bash
2. Show me all GEE datasets for flood monitoring in Kenya's Tana River Basin.
```

```bash
3. What do you know about flooding patterns in the Tana River Basin and Garissa County?
```

```bash
4. Rainfall of 85mm detected in Garissa today. Soil moisture is 0.91. Issue a flood alert.
```

```bash
5. Find the latest flood news for Kenya this week.
```

```
What is the flood risk in Nairobi, Kenya during the rainy season?
Explain how Sentinel-1 SAR detects floods through clouds
Rainfall of 120mm in the Volta Basin, Ghana. Issue an extreme alert.
```

---

## 🧠 How RAG Works in This System

This project implements Retrieval Augmented Generation without any external vector database — making it fully runnable offline and on the free tier.

The knowledge base in `rag_store.py` contains 10 curated flood documents covering: Kenya flood patterns (Tana River, Lake Victoria, Nairobi urban floods), Ghana flood patterns (Volta Basin, Accra), GEE technical methodology (GPM IMERG, Sentinel-1, SMAP), Early Warning System design for African communities, and historical flood events in Kenya from 2018 to 2024.

Retrieval uses keyword scoring — no embedding API calls needed. Each document is scored against the user query using term frequency, with regional boosts for Kenya and Ghana-specific queries. The top 3 most relevant documents are returned to the agent which synthesises them into its response.

To add new knowledge documents, open `rag_store.py` and add an entry to `FLOOD_KNOWLEDGE_BASE` following this pattern:

```python
{
    "id": "ken_004",
    "title": "Your Document Title",
    "region": "Kenya",
    "content": """
        Your knowledge here. Be specific — include numbers,
        dates, river names, and actionable thresholds.
    """,
    "tags": ["kenya", "your", "tags", "here"]
}
```

---

## 🔧 Troubleshooting

**`404 NOT_FOUND: models/gemini-pro is not found`**

`gemini-pro` is deprecated. Run this to fix all occurrences at once:
```bash
sed -i 's/gemini-pro/gemini-2.5-flash-lite/g' gee_agent/agent.py
```

**`429 RESOURCE_EXHAUSTED`**

You have hit the free tier daily quota of 20 requests per day per model. Options: wait for quota to reset at midnight Pacific Time, add $5 billing at https://aistudio.google.com/billing, or check your current usage at https://ai.dev/rate-limit.

**`503 UNAVAILABLE`**

Google's servers are under high load — common during Google IO season. Wait 2-5 minutes and try again. If it persists, swap to a different model in `agent.py` and restart `adk web`.

**`400 INVALID_ARGUMENT: Built-in tools and Function Calling cannot be combined`**

This means `google_search` and a custom Python tool are in the same agent. Ensure `web_search_agent` uses only `google_search` and `web_fetch_agent` uses only `fetch_webpage_text`. Never put both in the same agent.

**Agent gives blank response on the first prompt**

Normal ADK cold start behaviour. Send a warmup message first, wait for a response, then run your actual prompts. All subsequent prompts in the same session respond correctly first time.

---

## 🗺️ Roadmap

What this project can become with further development: real GEE integration connecting to live GPM IMERG and SMAP data via the Earth Engine Python API, SMS alerts via Africa's Talking API to reach rural communities on feature phones, WhatsApp integration via Twilio for urban populations, automated Sentinel-1 SAR flood extent computation using the Otsu thresholding algorithm, Swahili and French radio script generation for community broadcast, expansion to full Africa coverage including the Sahel, Mozambique, and South Sudan, a Mesop chat frontend with live map visualisation, and agent-to-agent communication with NASA OpenScapes via the A2A protocol.

---

## 📚 Acknowledgements

This project builds on the work of Eric Abelson and Kristopher Overholt who built the original GEE ADK dataset explorer, Renee Johnston who created the first GEE vector and text embedding search tool, the Google Science Team for Earth Engine community experiments, and the Google ADK Team for the Agent Development Kit framework at https://google.github.io/adk-docs/.

---

## 👨‍💻 Author

**John M. Megwe**

Data Scientist and postgraduate student specialising in Graph Neural Networks and Reinforcement Learning, with research centred on building equitable AI systems for healthcare resource allocation in high-scarcity African environments. Beyond research, John is an active voice in the tech community, serving as a co-organizer for GDG Google Earth Engine.

LinkedIn: https://www.linkedin.com/in/john-megwe-539982222/

GitHub: https://github.com/johnmwangimegwe

---

Powered by Google ADK | Google Earth Engine | Udara EWS

*Built for the community. Saving lives through early warning.*

**We are what we build together.**