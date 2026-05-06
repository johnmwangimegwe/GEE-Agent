# ==============================================================================
# RAG STORE — Retrieval Augmented Generation for Flood Intelligence
# Stores curated flood knowledge as an in-memory vector store
# Uses sentence-level embeddings via a lightweight approach
# No external vector DB needed — works fully offline for demo
# ==============================================================================

from gee_agent.flood_config import FLOOD_DATASETS, KENYA_REGIONS, GHANA_REGIONS, FLOOD_THRESHOLDS, ALERT_TEMPLATES
import json

# ==============================================================================
# Flood Knowledge Base
# This is the corpus the RAG agent retrieves from
# Add more documents here to improve agent responses
# ==============================================================================

FLOOD_KNOWLEDGE_BASE = [

    # --- Kenya-specific flood knowledge ---
    {
        "id": "ken_001",
        "title": "Tana River Basin Flood Patterns",
        "region": "Kenya",
        "content": """
            The Tana River Basin is Kenya's longest river system and most flood-prone watershed.
            Flooding occurs in two main seasons: the long rains (March-May) and short rains (October-December).
            The upper catchment in the Aberdare Range and Mount Kenya receives heavy orographic rainfall
            that causes rapid runoff into the lower basin. Garissa County downstream experiences the worst
            inundation, often lasting 2-6 weeks. The 2020 floods displaced over 100,000 people in the basin.
            Key trigger: when GPM IMERG records more than 50mm/day for 3 consecutive days in the upper catchment,
            downstream flooding in Garissa is near-certain within 72 hours.
        """,
        "tags": ["kenya", "tana", "garissa", "rainfall", "seasonal"]
    },
    {
        "id": "ken_002",
        "title": "Lake Victoria Rising Water Levels",
        "region": "Kenya",
        "content": """
            Lake Victoria water levels rose sharply from 2019-2020, reaching their highest level in 50 years.
            This caused widespread lakeshore flooding in Kisumu, Siaya, Homa Bay, and Migori counties.
            Over 200,000 people were displaced in Kenya alone. The lake level rise was driven by above-average
            rainfall across the Victoria Basin combined with reduced evaporation. JRC Global Surface Water
            dataset clearly shows the expansion of the lake boundary compared to the 1984-2015 baseline.
            Monitoring lake level anomalies using Sentinel-1 SAR is the most reliable cloud-free method.
        """,
        "tags": ["kenya", "lake victoria", "kisumu", "lakeshore", "sar"]
    },
    {
        "id": "ken_003",
        "title": "Nairobi Urban Flash Flooding",
        "region": "Kenya",
        "content": """
            Nairobi experiences severe urban flash flooding along the Mathare, Nairobi, and Ngong rivers.
            Informal settlements in Mathare, Kibera, and Mukuru are most vulnerable due to proximity to
            rivers and impermeable surfaces. Flooding can occur within 30-60 minutes of heavy rainfall onset.
            Rainfall above 30mm in 2 hours is sufficient to trigger dangerous flash flooding in low-lying areas.
            The Athi River downstream of Nairobi also floods significantly, affecting Machakos and Makueni counties.
            Population density data from WorldPop shows over 2 million people live in high-risk zones in Nairobi.
        """,
        "tags": ["kenya", "nairobi", "urban", "flash flood", "mathare", "kibera"]
    },

    # --- Ghana-specific flood knowledge ---
    {
        "id": "gha_001",
        "title": "Volta Basin Seasonal Flooding and Bagre Dam",
        "region": "Ghana",
        "content": """
            The Volta River Basin experiences predictable annual flooding from July to October.
            A critical and controversial trigger is the release of water from Bagre Dam in Burkina Faso.
            When Bagre Dam operators release water without adequate notice to Ghana, communities downstream
            in the Northern Region face sudden and severe flooding. The 2010 Bagre Dam release flooded
            half a million people in northern Ghana. Sentinel-1 SAR monitoring of the Bagre reservoir
            fill level and downstream Oti and White Volta rivers provides 48-72 hours of early warning time.
        """,
        "tags": ["ghana", "volta", "bagre dam", "northern region", "transboundary"]
    },
    {
        "id": "gha_002",
        "title": "Accra Flooding — Odaw River and Korle Lagoon",
        "region": "Ghana",
        "content": """
            Accra floods nearly every major rainfall event due to poor drainage infrastructure, 
            encroachment on flood plains, and the Odaw River and Korle Lagoon drainage system being
            overwhelmed. The June 2015 Accra floods killed over 150 people including 96 at a fuel station explosion.
            GPM IMERG data shows that rainfall exceeding 40mm in 3 hours reliably triggers dangerous flooding
            in low-lying Accra neighborhoods including Adabraka, Kokomlemle, and Alajo.
            The Korle Lagoon acts as a buffer that becomes a hazard when full.
        """,
        "tags": ["ghana", "accra", "odaw", "korle", "urban", "flash flood"]
    },

    # --- GEE Dataset technical knowledge ---
    {
        "id": "gee_001",
        "title": "GPM IMERG for Real-Time Rainfall Monitoring",
        "region": "Global",
        "content": """
            NASA's GPM IMERG (Integrated Multi-satellitE Retrievals for GPM) is the gold standard 
            for near-real-time precipitation monitoring. It provides 30-minute rainfall estimates
            at 0.1 degree (~10km) resolution globally. In Google Earth Engine, the dataset ID is
            NASA/GPM_L3/IMERG_V06. Key band: precipitationCal (calibrated precipitation in mm/hr).
            Multiply by 0.5 to convert 30-min accumulation to mm. For flood monitoring, aggregate
            to daily totals using ee.Reducer.sum() over 48 image collections per day.
            Latency is approximately 4-6 hours for Early Run, and 3 months for Final Run.
            Use Early Run for real-time monitoring and Final Run for historical analysis.
        """,
        "tags": ["gee", "gpm", "imerg", "rainfall", "technical", "realtime"]
    },
    {
        "id": "gee_002",
        "title": "Sentinel-1 SAR Flood Detection Methodology",
        "region": "Global",
        "content": """
            Sentinel-1 SAR (Synthetic Aperture Radar) can detect flood extent through clouds and at night,
            making it ideal for Africa's rainy seasons when optical imagery is often unavailable.
            In GEE, use COPERNICUS/S1_GRD. For flood detection: filter by instrumentMode='IW' and
            transmitterReceiverPolarisation containing 'VV'. Flooded areas appear as dark pixels
            (low backscatter) in VV polarization — water reflects SAR signal away from sensor.
            Algorithm: apply speckle filter (focal_median, radius 50m), then threshold VV < -15 dB
            to identify water. Mask permanent water using JRC/GSW1_4/GlobalSurfaceWater occurrence > 90.
            Sentinel-1 revisit time is 6 days (12 days for some Africa regions).
        """,
        "tags": ["gee", "sentinel-1", "sar", "flood detection", "technical", "methodology"]
    },
    {
        "id": "gee_003",
        "title": "SMAP Soil Moisture as Flood Precursor",
        "region": "Global",
        "content": """
            SMAP (Soil Moisture Active Passive) soil moisture data is one of the best predictors
            of flood potential. When soil is saturated, additional rainfall cannot be absorbed and
            runs off directly into rivers and streams. In GEE, use NASA_USDA/HSL/SMAP10KM_soil_moisture.
            Key band: smp (soil moisture profile, fraction). Values above 0.85 indicate near-saturated
            conditions where even moderate rainfall (20-30mm) can trigger flooding.
            For Kenya's Tana Basin, soil moisture consistently exceeds 0.90 before major flood events.
            Combine SMAP with GPM IMERG for a compound flood risk index: Risk = (SMAP_smp * 0.4) + 
            (GPM_normalized * 0.6). Threshold above 0.75 for flood warning issuance.
        """,
        "tags": ["gee", "smap", "soil moisture", "technical", "flood risk index"]
    },

    # --- Early Warning System knowledge ---
    {
        "id": "ews_001",
        "title": "People-Centered Early Warning System Framework",
        "region": "Africa",
        "content": """
            The WMO (World Meteorological Organization) defines an effective Early Warning System (EWS)
            as having four interconnected components: (1) Risk Knowledge — understanding who is at risk
            and why; (2) Monitoring and Warning Service — detecting hazardous conditions; 
            (3) Dissemination and Communication — reaching at-risk communities in time with actionable info;
            (4) Response Capability — communities able to act on warnings.
            For Kenya and Ghana, the last two components are often the weakest. SMS-based alerts using
            Africa's Talking API can reach feature phone users in rural areas. WhatsApp Business API
            reaches urban populations. Community radio remains the most trusted channel in rural Africa.
            Lead time target: minimum 6 hours for flash floods, 24-72 hours for river floods.
        """,
        "tags": ["ews", "warning dissemination", "africa", "sms", "community"]
    },
    {
        "id": "ews_002",
        "title": "Historical Flood Events in Kenya 2018-2024",
        "region": "Kenya",
        "content": """
            Major flood events in Kenya (2018-2024):
            - April 2018: Solai Dam collapse, Nakuru County — 47 deaths
            - May 2018: Tana River flooding — 200,000 displaced
            - October 2019: Lake Victoria floods — 100,000 displaced in western Kenya  
            - April 2020: Tana River basin — 130,000 displaced, Garissa worst affected
            - April 2023: El Niño-linked rains — nationwide flooding, 169 deaths
            - April 2024: Deadly flooding across Kenya — over 200 deaths, Mai Mahiu landslide
            Pattern: Long rains season (March-May) consistently produces worst events.
            El Niño years (2018, 2023-24) amplify flooding significantly across East Africa.
            CHIRPS and GPM retrospective data confirms above-average rainfall in all events.
        """,
        "tags": ["kenya", "historical", "events", "el nino", "deaths", "displaced"]
    }
]


# ==============================================================================
# RAG Functions
# Simple keyword + relevance scoring — no external library needed
# Works fully on free tier, no embedding API calls required
# ==============================================================================

def _score_document(doc: dict, query: str) -> float:
    """
    Scores a document's relevance to a query using keyword matching.
    Returns a float score — higher is more relevant.
    """
    query_lower = query.lower()
    query_terms = set(query_lower.split())
    score = 0.0

    # Score against title
    title_terms = set(doc["title"].lower().split())
    score += len(query_terms & title_terms) * 3.0

    # Score against tags
    for tag in doc.get("tags", []):
        if tag in query_lower:
            score += 2.0

    # Score against content
    content_lower = doc["content"].lower()
    for term in query_terms:
        if len(term) > 3:  # skip short words
            score += content_lower.count(term) * 0.5

    # Boost Kenya/Ghana specific docs for regional queries
    if "kenya" in query_lower and doc.get("region") == "Kenya":
        score *= 1.5
    if "ghana" in query_lower and doc.get("region") == "Ghana":
        score *= 1.5

    return score


def retrieve_flood_knowledge(query: str, top_k: int = 3) -> str:
    """
    Retrieves the most relevant flood knowledge documents for a given query.
    
    Args:
        query: The user's question or search query.
        top_k: Number of top documents to return.
    
    Returns:
        A formatted string of relevant knowledge passages.
    """
    scored_docs = []
    for doc in FLOOD_KNOWLEDGE_BASE:
        score = _score_document(doc, query)
        if score > 0:
            scored_docs.append((score, doc))

    # Sort by score descending
    scored_docs.sort(key=lambda x: x[0], reverse=True)
    top_docs = scored_docs[:top_k]

    if not top_docs:
        return "No specific flood knowledge found for this query. Proceeding with general GEE dataset search."

    result = f"📚 Retrieved {len(top_docs)} relevant knowledge document(s):\n\n"
    for i, (score, doc) in enumerate(top_docs, 1):
        result += f"{'='*60}\n"
        result += f"[{i}] {doc['title']} (Region: {doc['region']})\n"
        result += f"{'='*60}\n"
        result += doc["content"].strip()
        result += f"\n\nTags: {', '.join(doc.get('tags', []))}\n\n"

    return result


def get_dataset_info(dataset_key: str) -> str:
    """
    Returns pre-curated information about a specific flood dataset.
    
    Args:
        dataset_key: Key from FLOOD_DATASETS config
                     (e.g., 'rainfall_realtime', 'flood_extent_sar')
    
    Returns:
        Formatted dataset information string.
    """
    if dataset_key not in FLOOD_DATASETS:
        available = ", ".join(FLOOD_DATASETS.keys())
        return f"Dataset key '{dataset_key}' not found. Available: {available}"

    ds = FLOOD_DATASETS[dataset_key]
    return f"""
📡 Dataset: {ds['name']}
GEE ID: {ds['gee_id']}
Resolution: {ds['resolution']}
Update Frequency: {ds['update_frequency']}
Coverage: {ds['coverage']}
Key Bands: {', '.join(ds['key_bands'])}
Use Case: {ds['use_case']}
Catalog: {ds['catalog_url']}
    """.strip()


def get_region_info(region_name: str) -> str:
    """
    Returns flood risk information for a named region.
    
    Args:
        region_name: e.g. 'tana_river_basin', 'volta_basin', 'accra_coastal'
    
    Returns:
        Formatted region information string.
    """
    all_regions = {**KENYA_REGIONS, **GHANA_REGIONS}

    # Try exact match first
    if region_name in all_regions:
        region = all_regions[region_name]
    else:
        # Try fuzzy match
        region_name_lower = region_name.lower()
        matched = None
        for key, val in all_regions.items():
            if region_name_lower in key or region_name_lower in val["name"].lower():
                matched = val
                break
        if not matched:
            return f"Region '{region_name}' not found. Try: {', '.join(all_regions.keys())}"
        region = matched

    bbox = region["bbox"]
    return f"""
🌍 Region: {region['name']}
Risk Level: {region['risk_level']}
Bounding Box: [{bbox[0]}°E, {bbox[1]}°N] to [{bbox[2]}°E, {bbox[3]}°N]
Notes: {region['notes']}
    """.strip()


def evaluate_flood_risk(rainfall_mm: float, soil_moisture: float = None) -> str:
    """
    Evaluates flood risk level based on rainfall and optional soil moisture.
    
    Args:
        rainfall_mm: Daily rainfall in mm
        soil_moisture: Soil moisture fraction (0-1), optional
    
    Returns:
        Formatted risk assessment string with alert level.
    """
    from gee_agent.flood_config import FLOOD_THRESHOLDS, ALERT_TEMPLATES

    thresholds = FLOOD_THRESHOLDS["rainfall"]

    # Determine base alert level from rainfall
    if rainfall_mm >= thresholds["extreme"]:
        level = "extreme"
    elif rainfall_mm >= thresholds["alert"]:
        level = "alert"
    elif rainfall_mm >= thresholds["warning"]:
        level = "warning"
    elif rainfall_mm >= thresholds["watch"]:
        level = "watch"
    else:
        template = ALERT_TEMPLATES.get("watch")
        return f"""
✅ NORMAL CONDITIONS
Rainfall: {rainfall_mm:.1f} mm/day — below watch threshold ({thresholds['watch']} mm/day)
No flood risk elevated at this time. Continue routine monitoring.
        """.strip()

    # Upgrade level if soil moisture also high
    upgrade_note = ""
    if soil_moisture is not None:
        sm_thresholds = FLOOD_THRESHOLDS["soil_moisture"]
        if soil_moisture >= sm_thresholds["extreme"] and level in ["watch", "warning"]:
            level = "alert"
            upgrade_note = f"\n⚠️  Risk upgraded: Soil moisture ({soil_moisture:.2f}) near saturation amplifies flood risk."
        elif soil_moisture >= sm_thresholds["alert"] and level == "watch":
            level = "warning"
            upgrade_note = f"\n⚠️  Risk upgraded: High soil moisture ({soil_moisture:.2f}) reduces infiltration capacity."

    template = ALERT_TEMPLATES[level]

    result = f"""
{template['emoji']} {template['level']}
{'='*50}
Rainfall: {rainfall_mm:.1f} mm/day (Threshold: {thresholds[level]} mm/day)
"""
    if soil_moisture is not None:
        result += f"Soil Moisture: {soil_moisture:.2f} (fraction of saturation)\n"

    result += f"""
Recommended Action: {template['action']}
{upgrade_note}

📱 Alert SMS Template:
"FLOOD {template['level']} | Rainfall: {rainfall_mm:.0f}mm detected. {template['action']} Call 999 for emergencies. -Kenya Met Dept"
    """.strip()

    return result