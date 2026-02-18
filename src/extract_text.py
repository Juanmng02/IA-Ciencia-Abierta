import os
import requests
from pathlib import Path

# Configuration
GROBID_URL = "http://localhost:8070"
INPUT_DIR = "data/papers"
OUTPUT_DIR = "data/processed"

def process_pdf_with_grobid(pdf_path, output_path):
    """
    Process a single PDF file with Grobid.
    
    Args:
        pdf_path: Path to input PDF
        output_path: Path to save XML output
    
    Returns:
        bool: True if successful, False otherwise
    """
    url = f"{GROBID_URL}/api/processFulltextDocument"
    
    try:
        with open(pdf_path, 'rb') as pdf_file:
            files = {'input': pdf_file}
            response = requests.post(url, files=files, timeout=300)
            
            if response.status_code == 200:
                with open(output_path, 'w', encoding='utf-8') as xml_file:
                    xml_file.write(response.text)
                print(f"Successfully processed: {pdf_path.name}")
                return True
            else:
                print(f"Error processing {pdf_path.name}: Status {response.status_code}")
                return False
                
    except requests.exceptions.RequestException as e:
        print(f"Request error for {pdf_path.name}: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error for {pdf_path.name}: {e}")
        return False

def main():
    """Process all PDFs in the input directory."""
    
    # Create output directory if it doesn't exist
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    
    # Get all PDF files
    pdf_files = list(Path(INPUT_DIR).glob("*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in {INPUT_DIR}")
        return
    
    print(f"Found {len(pdf_files)} PDF files to process")
    print(f"Make sure Grobid is running at {GROBID_URL}\n")
    
    # Process each PDF
    successful = 0
    for pdf_path in sorted(pdf_files):
        output_path = Path(OUTPUT_DIR) / f"{pdf_path.stem}.xml"
        
        if process_pdf_with_grobid(pdf_path, output_path):
            successful += 1
    
    print(f"\nProcessing complete: {successful}/{len(pdf_files)} files successful")

if __name__ == "__main__":
    main()