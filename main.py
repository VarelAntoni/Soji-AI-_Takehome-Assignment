import pandas as pd
import time
from src.config import AD_SOURCES
from src.ingestion import get_pdf_text
from src.extraction import ADExtractor
from src.evaluation import evaluate_compliance

# Test Fleet Configuration
FLEET_DATA = [
    # Validation Cases
    {"Model": "MD-11F", "MSN": "48400", "Modifications": "None"},
    {"Model": "A320-214", "MSN": "4500", "Modifications": "mod 24591 (production)"}, 
    {"Model": "A320-214", "MSN": "4500", "Modifications": "None"},
    # Additional Test Cases
    {"Model": "MD-11", "MSN": "48123", "Modifications": "None"},
    {"Model": "DC-10-30F", "MSN": "47890", "Modifications": "None"},
    {"Model": "Boeing 737-800", "MSN": "30123", "Modifications": "None"},
    {"Model": "A320-232", "MSN": "6789", "Modifications": "mod 24591 (production)"},
    {"Model": "A321-112", "MSN": "364", "Modifications": "mod 24977 (production)"},
]

def main():
    print("Starting AD Compliance Pipeline...")
    
    extractor = ADExtractor()
    extracted_rules_db = []

    # Phase 1: Ingestion and Extraction
    print("\n[PHASE 1] Document Processing")
    for source in AD_SOURCES:
        text = get_pdf_text(source)
        if text:
            data = extractor.extract_rules(text)
            if data:
                extracted_rules_db.append(data)
                ad_id = data.get('ad_id', 'Unknown ID')
                print(f"[SUCCESS] Extracted rules for: {ad_id}")
            else:
                print(f"[WARN] Extraction returned empty data for {source}")
        else:
            print(f"[ERROR] Failed to retrieve text from {source}")
            
        time.sleep(1) 

    if not extracted_rules_db:
        print("\n[CRITICAL] No rules extracted. Aborting pipeline.")
        return

    # Phase 2: Evaluation
    print("\n[PHASE 2] Fleet Evaluation")
    results = []
    
    for ac in FLEET_DATA:
        row = {
            "Model": ac['Model'],
            "MSN": ac['MSN'],
            "Mods": ac['Modifications']
        }
        
        for rule in extracted_rules_db:
            # Dynamically determine column name based on AD ID
            ad_id_raw = str(rule.get('ad_id', ''))
            if "US" in ad_id_raw or "FAA" in ad_id_raw:
                col_name = "FAA Result"
            else:
                col_name = "EASA Result"
            
            row[col_name] = evaluate_compliance(ac, rule)
            
        results.append(row)

    # Phase 3: Reporting
    df = pd.DataFrame(results)
    
    # Ensure column ordering
    cols = ["Model", "MSN", "Mods", "FAA Result", "EASA Result"]
    existing_cols = [c for c in cols if c in df.columns]
    df = df[existing_cols]

    print("\n" + "="*80)
    print("FINAL COMPLIANCE REPORT")
    print("="*80)
    print(df.to_string(index=False))
    
    output_file = "compliance_results.csv"
    df.to_csv(output_file, index=False)
    print(f"\n[INFO] Results saved to '{output_file}'")

if __name__ == "__main__":
    main()