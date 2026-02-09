import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())

# API Configuration
SOJI_API_KEY = os.getenv("SOJI_API_KEY")
SOJI_BASE_URL = os.getenv("SOJI_BASE_URL")
MODEL_NAME = 'gemini/gemini-2.5-flash' 

# Document Sources
# Implements a hybrid approach: URLs for accessible documents, 
# and local file paths for documents behind authentication walls (e.g., EASA).
AD_SOURCES = [
    "https://ad.easa.europa.eu/ad/US-2025-23-53",  # FAA AD 
    "EASA_AD_2025-0254R1_1.pdf"                     # EASA AD (Local file bypass)
    # "https://ad.easa.europa.eu/ad/2025-0254"  # EASA AD
]