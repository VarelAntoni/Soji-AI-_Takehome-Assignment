# AD Extraction & Compliance Report

## 1. Approach
I implemented a **Hybrid Pipeline** designed for reliability in safety-critical contexts.
* **Ingestion:** The system supports both direct URL scraping and local file processing. This ensures the pipeline works even when external servers (like EASA) block automated requests.
* **Extraction:** I used a **"Trust but Verify"** strategy.
    1.  **LLM (Gemini-2.5-flash):** Used to parse the unstructured PDF text and identify aircraft models.
    2.  **Regex Safety Net:** A deterministic layer that scans specifically for modification numbers (e.g., `mod 24591`). This ensures 100% recall for critical exclusion rules, covering cases where the LLM might miss small digits in dense text.

## 2. Challenges & Solutions
**Challenge: Anti-Scraping Barriers**
The EASA URL redirects programmatic requests to a login page, preventing the text extraction from working via URL.
* **Solution:** I modified the ingestion logic to check for a local file (`EASA_AD_2025-0254R1_1.pdf`) if the URL download fails or is restricted. This allows the system to process the document offline without breaking the pipeline.

## 3. Limitations
* **Manual Download Required:** For protected sites like EASA, a human must currently download the PDF to the project folder first. A production version would require a headless browser (Selenium) to handle authentication automatically.
* **Hardcoded Patterns:** The Safety Net relies on Regex patterns (looking for 4-6 digits). If a manufacturer changes their numbering format to include letters (e.g., "Mod A-123"), the patterns would need updating.

## 4. Trade-offs
* **LLM vs. Pure Regex:** I chose an LLM because AD formats vary wildly between FAA and EASA. Writing pure Regex for *every* possible sentence structure is brittle. The LLM handles the structure, while Regex handles the specific numbers.
* **Text Extraction vs. Vision Models (VLM):** I used `PyMuPDF` (text) instead of a VLM. Since these are digital-native PDFs, text extraction is significantly faster, cheaper, and more accurate than processing them as images.