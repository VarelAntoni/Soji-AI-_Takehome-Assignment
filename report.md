# AD Extraction & Compliance Report

## 1. Approach: Why Hybrid?
* **Ingestion** I started by trying to scrape everything via URL. However, I quickly hit a wall with the EASA website—it redirected my bot to a login page. Instead of over-engineering a web scraper to bypass their security (which could break easily), I built a fallback: if the URL fails, look for a local file. It’s a pragmatic solution to keep the pipeline running.
* **Extraction (LLM + Regex):** I treated the LLM as a "Reader" and the Regex as a "Validator." The LLM is great at understanding the messy structure of different PDFs (FAA vs EASA), but I didn't trust it 100% with the specific numbers. That's why I added the Regex layer.

## 2. The Hardest Part: Edge Cases
The biggest challenge wasn't the coding, but the data logic.

I encountered a critical edge case with the EASA document. The text clearly stated the AD applies to the A320 except those with modification **24591**.
* **The Problem:** In my early tests, the LLM correctly identified the aircraft as an A320 but sometimes hallucinated or missed the "24591" exclusion because it was buried in a dense paragraph. This resulted in a False Positive (marking a safe plane as affected).
* **The Solution** I realized I couldn't rely on probabilistic AI for exact integer matching. I implemented a deterministic Regex pass (`mod\s+(\d+)`) to forcibly capture these numbers. If the code sees "24591", it overrides the LLM's initial impression.

## 3. Limitations
* **Manual Download:** Currently, the EASA file requires a human to download it first. Ideally, I would implement a headless browser (like Selenium) to handle the login flow automatically, but the "Local File" fallback works perfectly for this assignment context.
* **Regex Rigidity:** My "Safety Net" looks for standard number formats (4-6 digits). If Airbus decides to change their modification numbers to alphanumeric (e.g., "Mod-A123"), my Regex would fail.

## 4. Trade-offs
* **Why not just Regex?** Writing Regex for *every* sentence variation in ADs is a nightmare and very brittle. I used the LLM to handle the "unstructured" mess and Regex only for the "structured" critical data. Best of both worlds.
* **Why not Vision Models (VLM)?** I stuck to text extraction (`PyMuPDF`) because it's faster and cheaper. VLMs are cool, but for digital-native PDFs, converting text to pixels and back to text introduces unnecessary OCR errors.
