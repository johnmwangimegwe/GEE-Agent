# ==============================================================================
# FLOOD INTELLIGENCE AGENT - Geographic & Threshold Configuration
# Tailored for Kenya, Ghana, and Africa-wide EWS
# ==============================================================================

# Key watersheds and regions of interest for Kenya
KENYA_REGIONS = {
    "tana_river_basin": {
        "name": "Tana River Basin",
        "counties": ["Tharaka-Nithi", "Embu", "Kitui", "Tana River", "Garissa"],
        "bbox": [37.0, -1.5, 41.0, 1.5],  # [min_lon, min_lat, max_lon, max_lat]
        "risk_level": "HIGH",
        "notes": "Most flood-prone basin in Kenya. Seasonal flooding affects Garissa County."
    },
    "athi_river_basin": {
        "name": "Athi River Basin",
        "counties": ["Nairobi", "Machakos", "Makueni", "Kajiado", "Kwale"],
        "bbox": [36.5, -4.0, 39.5, -0.5],
        "risk_level": "HIGH",
        "notes": "Urban flooding risk in Nairobi. Flash floods in lower reaches."
    },
    "lake_victoria_basin": {
        "name": "Lake Victoria Basin",
        "counties": ["Kisumu", "Siaya", "Homa Bay", "Migori", "Busia"],
        "bbox": [33.5, -1.5, 35.5, 0.5],
        "risk_level": "HIGH",
        "notes": "Rising lake levels since 2019. Lakeshore communities at risk."
    },
    "ewaso_ngiro_basin": {
        "name": "Ewaso Ng'iro Basin",
        "counties": ["Samburu", "Isiolo", "Laikipia", "Marsabit"],
        "bbox": [36.0, 0.5, 39.0, 3.0],
        "risk_level": "MEDIUM",
        "notes": "Flash floods in arid/semi-arid regions. Affects pastoralist communities."
    }
}

# Ghana regions for flood monitoring
GHANA_REGIONS = {
    "volta_basin": {
        "name": "Volta River Basin",
        "regions": ["Northern", "Upper East", "Upper West", "Oti"],
        "bbox": [-2.5, 6.5, 1.0, 11.0],
        "risk_level": "HIGH",
        "notes": "Annual flooding. Bagre Dam releases amplify downstream flooding."
    },
    "accra_coastal": {
        "name": "Accra Coastal Zone",
        "regions": ["Greater Accra"],
        "bbox": [-0.5, 5.4, 0.2, 5.8],
        "risk_level": "HIGH",
        "notes": "Urban flooding from Odaw and Densu rivers. June-September peak risk."
    }
}

# Africa-wide high-risk zones
AFRICA_HIGH_RISK_ZONES = {
    "sahel_belt": {
        "name": "Sahel Flood Belt",
        "countries": ["Niger", "Nigeria", "Chad", "Mali", "Burkina Faso"],
        "bbox": [-6.0, 10.0, 24.0, 20.0],
        "risk_level": "HIGH",
        "notes": "Paradox region — drought and flash floods. August-September peak."
    },
    "mozambique_coast": {
        "name": "Mozambique Coastal Zone",
        "countries": ["Mozambique", "Zimbabwe", "Malawi"],
        "bbox": [30.0, -25.0, 40.0, -10.0],
        "risk_level": "VERY HIGH",
        "notes": "Cyclone-driven flooding. Cyclone Idai (2019) reference event."
    },
    "south_sudan_sudd": {
        "name": "South Sudan Sudd Wetlands",
        "countries": ["South Sudan"],
        "bbox": [28.0, 5.0, 34.0, 10.0],
        "risk_level": "VERY HIGH",
        "notes": "Persistent multi-year flooding since 2019. Humanitarian crisis."
    }
}

# ==============================================================================
# Flood Threshold Configuration
# Based on historical percentiles for East Africa
# ==============================================================================

FLOOD_THRESHOLDS = {
    "rainfall": {
        "watch":   25,   # mm/day — monitor closely
        "warning": 50,   # mm/day — elevated risk
        "alert":   75,   # mm/day — high risk, prepare communities
        "extreme": 100,  # mm/day — imminent danger, issue warnings now
    },
    "soil_moisture": {
        "watch":   0.75,  # fraction of saturation
        "warning": 0.85,
        "alert":   0.92,
        "extreme": 0.97,
    },
    "river_anomaly": {
        # Z-score above historical mean
        "watch":   1.5,
        "warning": 2.0,
        "alert":   2.5,
        "extreme": 3.0,
    }
}

# ==============================================================================
# GEE Flood-Relevant Dataset Registry
# Pre-curated for the Flood Intelligence Agent
# ==============================================================================

FLOOD_DATASETS = {
    "rainfall_realtime": {
        "gee_id": "NASA/GPM_L3/IMERG_V06",
        "name": "GPM IMERG — Global Precipitation Measurement",
        "resolution": "10 km",
        "update_frequency": "30 minutes",
        "coverage": "Global (60°N to 60°S)",
        "key_bands": ["precipitationCal", "precipitationUncal"],
        "use_case": "Primary rainfall monitoring for flood triggers",
        "catalog_url": "https://developers.google.com/earth-engine/datasets/catalog/NASA_GPM_L3_IMERG_V06"
    },
    "soil_moisture": {
        "gee_id": "NASA_USDA/HSL/SMAP10KM_soil_moisture",
        "name": "SMAP — Soil Moisture Active Passive",
        "resolution": "10 km",
        "update_frequency": "Daily",
        "coverage": "Global",
        "key_bands": ["ssm", "susm", "smp"],
        "use_case": "Soil saturation monitoring — key pre-flood indicator",
        "catalog_url": "https://developers.google.com/earth-engine/datasets/catalog/NASA_USDA_HSL_SMAP10KM_soil_moisture"
    },
    "flood_extent_sar": {
        "gee_id": "COPERNICUS/S1_GRD",
        "name": "Sentinel-1 SAR GRD — Flood Extent Mapping",
        "resolution": "10 m",
        "update_frequency": "6-12 days",
        "coverage": "Global",
        "key_bands": ["VV", "VH"],
        "use_case": "Cloud-penetrating flood extent detection — critical during storms",
        "catalog_url": "https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S1_GRD"
    },
    "elevation": {
        "gee_id": "MERIT/DEM/v1_0_3",
        "name": "MERIT DEM — Multi-Error-Removed Improved Terrain",
        "resolution": "90 m",
        "update_frequency": "Static",
        "coverage": "Global",
        "key_bands": ["dem"],
        "use_case": "Downstream inundation modelling and flow direction analysis",
        "catalog_url": "https://developers.google.com/earth-engine/datasets/catalog/MERIT_DEM_v1_0_3"
    },
    "permanent_water": {
        "gee_id": "JRC/GSW1_4/GlobalSurfaceWater",
        "name": "JRC Global Surface Water",
        "resolution": "30 m",
        "update_frequency": "Annual",
        "coverage": "Global",
        "key_bands": ["occurrence", "change_abs", "seasonality", "max_extent"],
        "use_case": "Baseline water mask — separates new floods from permanent water",
        "catalog_url": "https://developers.google.com/earth-engine/datasets/catalog/JRC_GSW1_4_GlobalSurfaceWater"
    },
    "population": {
        "gee_id": "WorldPop/GP/100m/pop",
        "name": "WorldPop — Population Density",
        "resolution": "100 m",
        "update_frequency": "Annual",
        "coverage": "Global",
        "key_bands": ["population"],
        "use_case": "Estimating affected population in flood impact zones",
        "catalog_url": "https://developers.google.com/earth-engine/datasets/catalog/WorldPop_GP_100m_pop"
    },
    "historical_floods": {
        "gee_id": "GLOBAL_FLOOD_DB/MODIS_EVENTS/V1",
        "name": "Global Flood Database — MODIS Events",
        "resolution": "250 m",
        "update_frequency": "Per-event (2000-2018)",
        "coverage": "Global",
        "key_bands": ["flooded", "duration", "clear_views", "jrc_perm_water"],
        "use_case": "Historical flood footprints for risk baseline and model training",
        "catalog_url": "https://developers.google.com/earth-engine/datasets/catalog/GLOBAL_FLOOD_DB_MODIS_EVENTS_V1"
    }
}

# ==============================================================================
# Alert Message Templates
# ==============================================================================

ALERT_TEMPLATES = {
    "watch": {
        "emoji": "🟡",
        "level": "FLOOD WATCH",
        "action": "Monitor conditions closely. Prepare emergency kits."
    },
    "warning": {
        "emoji": "🟠",
        "level": "FLOOD WARNING",
        "action": "Move valuables to higher ground. Stay alert for updates."
    },
    "alert": {
        "emoji": "🔴",
        "level": "FLOOD ALERT",
        "action": "Evacuate low-lying areas immediately. Contact local authorities."
    },
    "extreme": {
        "emoji": "🚨",
        "level": "EXTREME FLOOD DANGER",
        "action": "EVACUATE NOW. Do not attempt to cross flooded roads. Call 999."
    }
}