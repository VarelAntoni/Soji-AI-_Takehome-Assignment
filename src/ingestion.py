import requests
import fitz  # PyMuPDF
import os

def get_pdf_text(source: str) -> str:
    """
    Retrieves raw text content from a PDF source.
    Supports both remote URLs and local file paths.

    Args:
        source (str): The URL or local file path of the PDF.

    Returns:
        str: Extracted text content. Returns an empty string on failure.
    """
    doc = None
    try:
        # Case 1: Remote URL
        if source.lower().startswith("http"):
            print(f"[INFO] Downloading document: {source}")
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124"
            }
            try:
                response = requests.get(source, headers=headers, timeout=15)
                if response.status_code == 200:
                    doc = fitz.open(stream=response.content, filetype="pdf")
                else:
                    print(f"[ERROR] Download failed. Status code: {response.status_code}")
                    return ""
            except Exception as e:
                print(f"[ERROR] Connection error: {e}")
                return ""
                
        # Case 2: Local File
        else:
            print(f"[INFO] Reading local file: {source}")
            if os.path.exists(source):
                doc = fitz.open(source)
            else:
                print(f"[ERROR] File not found: {source}")
                return ""

        # Extract text from all pages
        full_text = ""
        for page in doc:
            full_text += page.get_text()
            
        return full_text

    except Exception as e:
        print(f"[ERROR] Failed to process PDF: {e}")
        return ""