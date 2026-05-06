# ==============================================================================
# TOOLS — Flood Intelligence Agent
# All tool functions used by sub-agents
# ==============================================================================

import requests
from gee_agent.flood_config import FLOOD_DATASETS, KENYA_REGIONS, GHANA_REGIONS, ALERT_TEMPLATES
from gee_agent.rag_store import (
    retrieve_flood_knowledge,
    get_dataset_info,
    get_region_info,       # Returns flood risk profile for a named region
    evaluate_flood_risk
)


# ==============================================================================
# GEE Catalog Tools
# ==============================================================================

def search_gee_catalog(query: str) -> str:
    """
    Searches the Google Earth Engine catalog for datasets matching a query.
    
    Args:
        query: Search terms (e.g., 'rainfall Kenya flood', 'soil moisture Africa')
    
    Returns:
        Raw search results from the GEE catalog.
    """
    search_url = (
        f"https://developers.google.com/s/results/earth-engine/datasets?q={query}"
    )
    try:
        response = requests.get(search_url, timeout=10)
        return str(response.content)
    except requests.exceptions.Timeout:
        return "GEE catalog search timed out. Try a more specific query."
    except requests.exceptions.RequestException as e:
        return f"GEE catalog search failed: {str(e)}"


def search_flood_datasets(region: str = "Kenya") -> str:
    """
    Returns pre-curated flood-relevant GEE datasets for a given region.
    Faster and more targeted than a general catalog search.
    
    Args:
        region: Target region (e.g., 'Kenya', 'Ghana', 'Africa')
    
    Returns:
        Formatted list of flood-relevant datasets with GEE IDs and details.
    """
    result = f"🌊 Pre-curated Flood Datasets for {region}:\n\n"
    for key, ds in FLOOD_DATASETS.items():
        result += f"{'='*60}\n"
        result += f"📡 {ds['name']}\n"
        result += f"   GEE ID: {ds['gee_id']}\n"
        result += f"   Resolution: {ds['resolution']} | Update: {ds['update_frequency']}\n"
        result += f"   Use Case: {ds['use_case']}\n"
        result += f"   Link: {ds['catalog_url']}\n\n"
    return result


def fetch_webpage_text(url: str) -> str:
    """
    Fetches the text content of a given webpage URL.
    
    Args:
        url: The URL of the webpage to fetch.
    
    Returns:
        Page content as string, or error message.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0 (FloodIntelligenceAgent/1.0)"}
        response = requests.get(url, timeout=8, headers=headers)
        return str(response.content[:5000])  # limit to 5000 chars to avoid token overflow
    except requests.exceptions.Timeout:
        return f"Request timed out for URL: {url}"
    except requests.exceptions.RequestException as e:
        return f"Failed to fetch URL {url}: {str(e)}"


# ==============================================================================
# RAG-Powered Knowledge Tools
# ==============================================================================

def query_flood_knowledge_base(query: str) -> str:
    """
    Queries the internal flood knowledge base using RAG retrieval.
    Returns relevant passages about flood patterns, GEE datasets, 
    and Early Warning System best practices for Kenya and Africa.
    
    Args:
        query: Natural language question about floods, datasets, or regions.
    
    Returns:
        Retrieved knowledge passages ranked by relevance.
    """
    return retrieve_flood_knowledge(query, top_k=3)


def get_flood_dataset_details(dataset_key: str) -> str:
    """
    Returns detailed technical information about a specific pre-curated flood dataset.
    
    Args:
        dataset_key: One of: rainfall_realtime, soil_moisture, flood_extent_sar,
                     elevation, permanent_water, population, historical_floods
    
    Returns:
        Full dataset metadata including GEE ID, resolution, bands, and use case.
    """
    return get_dataset_info(dataset_key)

def get_region_flood_profile(region_name: str) -> str:
    """
    Returns flood risk profile for a named region in Kenya, Ghana, or Africa.
    
    Args:
        region_name: e.g., 'tana_river_basin', 'volta_basin', 
                     'accra_coastal', 'lake_victoria_basin'
    
    Returns:
        Region flood risk profile with bounding box and key notes.
    """
#    return get_region_flood_profile(region_name)
    return get_region_info(region_name)

# ==============================================================================
# Flood Risk Assessment Tools
# ==============================================================================

def assess_flood_risk(rainfall_mm: float, soil_moisture_fraction: float = None) -> str:
    """
    Evaluates current flood risk level based on rainfall and soil moisture.
    Issues alert level (Watch / Warning / Alert / Extreme) with SMS template.
    
    Args:
        rainfall_mm: Observed or forecast daily rainfall in millimetres.
        soil_moisture_fraction: Optional — soil moisture as a fraction (0.0-1.0).
                                Values above 0.85 amplify flood risk significantly.
    
    Returns:
        Risk assessment with alert level, thresholds, and SMS alert template.
    """
    return evaluate_flood_risk(rainfall_mm, soil_moisture_fraction)


def generate_flood_alert(
    region: str,
    rainfall_mm: float,
    alert_level: str,
    affected_counties: list = None
) -> str:
    """
    Generates a formatted flood alert card and SMS message for a region.
    Suitable for display in a dashboard or sending via Africa's Talking API.
    
    Args:
        region: Name of the affected region (e.g., 'Garissa County, Tana River Basin')
        rainfall_mm: Measured or forecast rainfall in mm/day
        alert_level: One of: watch, warning, alert, extreme
        affected_counties: Optional list of affected county names
    
    Returns:
        Formatted alert card with SMS template ready for dissemination.
    """
    from gee_agent.flood_config import ALERT_TEMPLATES
    from datetime import datetime

    level = alert_level.lower()
    if level not in ALERT_TEMPLATES:
        level = "watch"

    template = ALERT_TEMPLATES[level]
    counties_str = ", ".join(affected_counties) if affected_counties else region
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    alert_card = f"""
{'='*60}
{template['emoji']}  UDARA FLOOD INTELLIGENCE SYSTEM
{template['level']}
{'='*60}
📍 Region:     {region}
📅 Issued:     {timestamp}
🌧️  Rainfall:   {rainfall_mm:.1f} mm/day observed
🏘️  Counties:   {counties_str}
{'='*60}
⚡ ACTION:     {template['action']}
{'='*60}

📱 SMS ALERT (160 chars):
"{template['emoji']} FLOOD {template['level']} - {region}. {rainfall_mm:.0f}mm rain. {template['action']} Info: udara.ews.ke | Emergency: 999"

📻 RADIO SCRIPT (Swahili):
"Tahadhari ya mafuriko katika {region}. Mvua ya {rainfall_mm:.0f}mm imerekodiwa. {template['action']}"

🔗 Data Source: NASA GPM IMERG + Sentinel-1 SAR via Google Earth Engine
📡 Powered by: Udara EWS | ADK Multi-Agent System
{'='*60}
    """.strip()

    return alert_card


def list_available_regions() -> str:
    """
    Lists all configured flood monitoring regions for Kenya and Ghana.
    
    Returns:
        Formatted list of all regions with their risk levels.
    """
    result = "🌍 Configured Flood Monitoring Regions:\n\n"

    result += "🇰🇪 KENYA:\n"
    for key, region in KENYA_REGIONS.items():
        result += f"  • {region['name']} — Risk: {region['risk_level']}\n"
        result += f"    Key: '{key}'\n"

    result += "\n🇬🇭 GHANA:\n"
    for key, region in GHANA_REGIONS.items():
        result += f"  • {region['name']} — Risk: {region['risk_level']}\n"
        result += f"    Key: '{key}'\n"

    return result