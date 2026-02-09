def evaluate_compliance(aircraft: dict, rules: dict) -> str:
    """
    Evaluates if a specific aircraft configuration is affected by the AD rules.
    
    Returns:
        str: "Affected", "Not affected", or "Not applicable"
    """
    rule_data = rules.get('applicability_rules', {})
    
    # Normalize inputs
    ac_model = str(aircraft.get('Model', '')).strip()
    ac_mods = str(aircraft.get('Modifications', '')).strip()
    
    # Step 1: Model Matching (Partial string match)
    models_list = rule_data.get('aircraft_models', [])
    model_match = False
    
    if models_list:
        for r_model in models_list:
            if r_model in ac_model or ac_model in r_model:
                model_match = True
                break
    
    if not model_match:
        return "❌ Not applicable"

    # Step 2: Exclusion Logic
    # If the aircraft has a modification listed in the exclusions, it is NOT affected.
    exclusions = rule_data.get('excluded_if_modifications', [])
    
    for exclusion in exclusions:
        # Extract digits to ensure robust comparison (e.g., "24591" vs "Mod 24591")
        clean_excl = "".join(filter(str.isdigit, str(exclusion)))
        
        if clean_excl and clean_excl in ac_mods:
            return "❌ Not affected" 

    # Default state if model matches and no exclusions are found
    return "✅ Affected"