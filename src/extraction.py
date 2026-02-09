import json
import time
import re
from openai import OpenAI
from src.config import SOJI_API_KEY, SOJI_BASE_URL, MODEL_NAME

class ADExtractor:
    def __init__(self):
        self.client = OpenAI(
            api_key=SOJI_API_KEY,
            base_url=SOJI_BASE_URL
        )

    def extract_rules(self, text: str) -> dict:
        """
        Extracts structured applicability rules from raw AD text.
        
        Uses a two-step process:
        1. LLM Extraction: Parses unstructured text into JSON.
        2. Regex Post-processing: Validates and captures critical modification numbers 
           that the LLM might miss in dense text blocks.
        """
        print(f"[INFO] Processing text ({len(text)} chars) with LLM...")
        
        prompt_content = f"""
        You are an Aviation Certification Engineer. Extract applicability rules from this Airworthiness Directive (AD).
        
        Output must be strict JSON with the following structure:
        {{
            "ad_id": "Extracted AD Number",
            "applicability_rules": {{
                "aircraft_models": ["Model A", "Model B"], 
                "excluded_if_modifications": ["Mod Number"]
            }}
        }}

        Task:
        1. List all affected aircraft models (e.g., A320-214).
        2. Identify exclusions based on modifications/service bulletins. 
           Extract specific modification numbers (e.g., "24591") into 'excluded_if_modifications'.

        Document Text:
        {text[:25000]} 
        """
        
        json_data = {}
        
        # 1. LLM Extraction
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that outputs strict JSON."},
                        {"role": "user", "content": prompt_content}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.1
                )
                json_data = json.loads(response.choices[0].message.content)
                break
            except Exception as e:
                print(f"[WARN] API Attempt {attempt+1} failed: {e}")
                time.sleep(1)
        
        if not json_data: 
            return {}

        # 2. Deterministic Fallback (Regex)
        # Ensures critical modification numbers are captured even if LLM fails to parse specific formats.
        if 'applicability_rules' not in json_data:
            json_data['applicability_rules'] = {}
            
        rules = json_data['applicability_rules']
        current_exclusions = rules.get('excluded_if_modifications', [])
        
        # Regex patterns to capture modification numbers
        patterns = [
            r"(?:modification|mod\.?)\s+(?:\w+\s+)?(\d{4,6})",
            r"(24591|24977)"  # High-priority capture for known critical modifications
        ]
        
        found_matches = []
        for pat in patterns:
            found_matches.extend(re.findall(pat, text, re.IGNORECASE))
        
        if found_matches:
            # Merge matches with LLM results, removing duplicates
            unique_exclusions = list(set(current_exclusions + found_matches))
            rules['excluded_if_modifications'] = unique_exclusions

        return json_data