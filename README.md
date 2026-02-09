# Automated AD Compliance Pipeline

## Overview
This tool automates the extraction of rules from Aviation Airworthiness Directives (ADs) to determine if aircraft are **Affected**, **Not Affected**, or **Not Applicable**. It uses a hybrid approach (LLM + Regex) to ensure high accuracy.

## ⚙️ Setup & Installation

**1. Install Dependencies**

pip install -r requirements.txt

**2. Configure Environment Create a .env file in the root directory:**

SOJI_API_KEY=your_api_key_here

SOJI_BASE_URL=[https://llm.soji.ai/v1](https://llm.soji.ai/v1)

**3. Required EASA Document** 
Due to EASA website restrictions, you must ensure the file EASA_AD_2025-0254R1_1.pdf is present in this root directory. The script will read it locally.

**4. Execute the main script:**

python main.py
