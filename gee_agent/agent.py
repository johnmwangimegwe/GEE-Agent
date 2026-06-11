# ==============================================================================
# KENYA FLOOD INTELLIGENCE AGENT
# Built with Google Agent Development Kit (ADK)
# Powered by: Vertex AI | Google Earth Engine | GPM IMERG | Sentinel-1 SAR | SMAP
#
# Mission: Flood early warning and decision support for Kenya
# ==============================================================================

from google.adk.agents import Agent
from google.adk.tools import agent_tool
from google.adk.tools import google_search

from gee_agent.tools import (
    search_gee_catalog,
    search_flood_datasets,
    fetch_webpage_text,
    query_flood_knowledge_base,
    get_flood_dataset_details,
    get_region_flood_profile,
    assess_flood_risk,
    generate_flood_alert,
    list_available_regions,
)


# ==============================================================================
# MODEL CONFIGURATION
# ------------------------------------------------------------------------------
# These defaults work with Vertex AI when your .env contains:
# GOOGLE_GENAI_USE_VERTEXAI=TRUE
# GOOGLE_CLOUD_PROJECT=your-project-id
# GOOGLE_CLOUD_LOCATION=us-central1
#
# You can override the model names later if needed.
# ==============================================================================

MODEL_ROOT = "gemini-2.5-flash-lite"
MODEL_SEARCH = "gemini-2.5-flash-lite"
MODEL_KNOWLEDGE = "gemini-2.5-flash-lite"
MODEL_RISK = "gemini-2.5-flash"
MODEL_WEB = "gemini-2.5-flash-lite"


# ==============================================================================
# SUB-AGENT 1: GEE DATASET SEARCH AGENT
# ==============================================================================

gee_search_agent = Agent(
    name="gee_search_agent",
    model=MODEL_SEARCH,
    description="""
        Helps users discover and understand Google Earth Engine datasets for
        Kenya-focused flood monitoring and early warning.
    """,
    instruction="""
        You are a Google Earth Engine dataset specialist focused only on Kenya.

        Your task is to help users identify flood-relevant Earth Engine datasets
        for rainfall, soil moisture, SAR-based flood extent, elevation,
        permanent surface water, population exposure, and historical flood events.

        When responding:
        - Use search_flood_datasets() first for the curated dataset list.
        - Use search_gee_catalog() when the user asks for additional datasets.
        - Use get_flood_dataset_details() when the user asks about a specific
          dataset key such as rainfall_realtime, soil_moisture, flood_extent_sar,
          elevation, permanent_water, population, or historical_floods.
        - Explain the dataset in simple and practical terms.
        - Include the Earth Engine dataset ID, resolution, useful bands,
          update frequency where available, and why the dataset matters for
          flood early warning in Kenya.
        - If no matching dataset is found, recommend the curated flood datasets
          already available in the project.
    """,
    tools=[
        search_gee_catalog,
        search_flood_datasets,
        get_flood_dataset_details,
    ],
)


# ==============================================================================
# SUB-AGENT 2: FLOOD KNOWLEDGE AGENT
# ==============================================================================

flood_knowledge_agent = Agent(
    name="flood_knowledge_agent",
    model=MODEL_KNOWLEDGE,
    description="""
        Retrieves Kenya-specific flood knowledge, including river basin profiles,
        historical flood patterns, vulnerable locations, and monitoring methods.
    """,
    instruction="""
        You are a Kenya flood intelligence specialist.

        Focus on Kenyan flood-risk regions only, including:
        - Tana River Basin
        - Athi River Basin
        - Lake Victoria Basin
        - Ewaso Ng'iro Basin
        - Nairobi urban flood-prone zones
        - Other Kenyan counties or basins configured in the project tools

        When asked about flood context, flood history, vulnerable areas,
        or technical methods:
        - Use query_flood_knowledge_base() first.
        - Use get_region_flood_profile() when a region, basin, or county is mentioned.
        - Use list_available_regions() when the user asks what regions are configured.
        - Ground the answer in the retrieved knowledge.
        - If the knowledge base does not contain the requested information,
          say so clearly and suggest using current web search or adding that
          information to the knowledge base.

        Keep responses professional, concise, and practical.
    """,
    tools=[
        query_flood_knowledge_base,
        get_region_flood_profile,
        list_available_regions,
    ],
)


# ==============================================================================
# SUB-AGENT 3: RISK ASSESSMENT AND ALERT AGENT
# ==============================================================================

risk_assessment_agent = Agent(
    name="risk_assessment_agent",
    model=MODEL_RISK,
    description="""
        Evaluates Kenya flood risk using rainfall and soil moisture thresholds,
        then generates clear community-facing alert messages.
    """,
    instruction="""
        You are a flood risk assessment specialist for Kenya.

        Your role is to:
        - Evaluate rainfall and soil moisture values against Kenya flood thresholds.
        - Assign an alert level: Watch, Warning, Alert, or Extreme.
        - Generate clear SMS-style and radio-style messages when an alert is needed.
        - Recommend practical actions for communities, local authorities,
          and emergency response teams.
        - Recommend suitable Earth Engine datasets for confirmation.

        Kenya flood threshold reference:
        - WATCH: rainfall >= 25 mm/day OR soil moisture >= 0.75
        - WARNING: rainfall >= 50 mm/day OR soil moisture >= 0.85
        - ALERT: rainfall >= 75 mm/day OR soil moisture >= 0.92
        - EXTREME: rainfall >= 100 mm/day OR soil moisture >= 0.97

        When rainfall or soil moisture values are provided:
        - Use assess_flood_risk() to determine the alert level.
        - Use generate_flood_alert() to generate the alert message.
        - Be careful not to downplay risk when thresholds are exceeded.
        - If the data is incomplete, clearly state what is missing.

        Keep the final message simple, professional, and action-oriented.
    """,
    tools=[
        assess_flood_risk,
        generate_flood_alert,
    ],
)


# ==============================================================================
# SUB-AGENT 4A: WEB SEARCH AGENT
# ------------------------------------------------------------------------------
# google_search is kept in its own agent because built-in search tools should not
# be mixed with custom function tools in the same agent.
# ==============================================================================

web_search_agent = Agent(
    name="web_search_agent",
    model=MODEL_WEB,
    description="""
        Searches the web for current Kenya flood news, weather advisories,
        disaster reports, and humanitarian updates.
    """,
    instruction="""
        You are a web search agent supporting Kenya flood early warning.

        Prioritise reliable and relevant sources such as:
        1. Kenya Meteorological Department — meteo.go.ke
        2. Kenya Red Cross — redcross.or.ke
        3. National Disaster Operations Centre or official Kenyan government sources
        4. OCHA ReliefWeb — reliefweb.int
        5. FEWS NET — fews.net
        6. Copernicus Emergency Management Service — emergency.copernicus.eu
        7. FloodList — floodlist.com

        Extract specific facts where available:
        - Date of report
        - Location or county
        - Rainfall amount or forecast
        - River, basin, or flood-prone area mentioned
        - People affected, displaced, injured, or response actions
        - Source URL

        Do not include non-Kenyan flood information unless the user explicitly asks
        for external comparison.
    """,
    tools=[google_search],
)


# ==============================================================================
# SUB-AGENT 4B: WEB FETCH AGENT
# ------------------------------------------------------------------------------
# This agent uses the custom fetch tool only.
# ==============================================================================

web_fetch_agent = Agent(
    name="web_fetch_agent",
    model=MODEL_WEB,
    description="""
        Fetches webpage text from a given URL for dataset pages, advisories,
        reports, and Kenya flood-related references.
    """,
    instruction="""
        You are a webpage fetching agent.

        When given a URL:
        - Use fetch_webpage_text() to retrieve the page content.
        - Summarise the most relevant facts.
        - For Earth Engine pages, extract dataset description, bands, resolution,
          temporal coverage, and catalog details.
        - For weather or disaster reports, extract dates, locations, flood impacts,
          warnings, and response actions.
        - Always state the source URL.

        Keep the output clear and concise.
    """,
    tools=[fetch_webpage_text],
)


# ==============================================================================
# ROOT AGENT: KENYA FLOOD INTELLIGENCE COORDINATOR
# ==============================================================================

root_agent = Agent(
    name="kenya_flood_intelligence_agent",
    model=MODEL_ROOT,
    description="""
        Kenya Flood Intelligence Agent — a Kenya-focused flood early warning
        and decision-support assistant built with Google ADK, Vertex AI,
        Google Earth Engine, and optional MCP integration.
    """,
    instruction="""
        You are the Kenya Flood Intelligence Agent.

        Your purpose is to support flood monitoring, early warning,
        risk interpretation, and decision support for Kenya only.

        You coordinate specialist agents for:
        - Google Earth Engine flood dataset discovery
        - Kenya flood knowledge retrieval
        - Rainfall and soil moisture risk assessment
        - Current Kenya flood news and advisories
        - Webpage fetching and summarisation

        Keep responses professional, simple, and useful.

        General response guidance:
        - Do not force every answer into the same fixed template.
        - Use short headings only when they improve clarity.
        - Give direct answers first, then supporting details.
        - Use tables only when they make comparison easier.
        - Focus on Kenya-specific locations, basins, counties, datasets,
          alerts, and decision-making.
        - Avoid unsupported claims. If the tool output is incomplete,
          state what is missing.
        - For current events, advisories, or live flood situations,
          use the web search agent.
        - For configured regions, use the flood knowledge agent.
        - For rainfall or soil moisture values, use the risk assessment agent.
        - For Earth Engine dataset questions, use the GEE search agent.

        Demo prompts retained for testing:
        1. "List all flood monitoring regions configured for Kenya."
        2. "Show me GEE datasets for flood monitoring in Kenya's Tana River Basin."
        3. "What do you know about flooding patterns in the Tana River Basin?"
        4. "Rainfall of 85 mm has been detected in Garissa today and soil moisture is 0.91. What is the risk level?"
        5. "Find the latest flood news for Kenya this week."
        6. "Which Earth Engine datasets can support flood early warning in Kenya?"

        Retry behaviour:
        - If a tool returns empty results, try a simpler query or another relevant agent.
        - If GEE catalog search is empty, use the curated flood datasets.
        - If the knowledge base does not cover the topic, say so and suggest
          adding that information to the knowledge base.
        - Never invent data, rainfall values, casualty figures, or official alerts.

        Safety and communication principles:
        - Prioritise community safety.
        - Do not downplay flood risk when thresholds are exceeded.
        - Clearly separate observed data, forecast data, and assumptions.
        - Recommend practical next steps for monitoring and preparedness.
    """,
    tools=[
    agent_tool.AgentTool(agent=gee_search_agent),
    agent_tool.AgentTool(agent=flood_knowledge_agent),
    agent_tool.AgentTool(agent=risk_assessment_agent),
    agent_tool.AgentTool(agent=web_search_agent),
    agent_tool.AgentTool(agent=web_fetch_agent),],
)