import xml.etree.ElementTree as ET
from pathlib import Path
import re
import csv
from urllib.parse import urlparse

# Configuration
INPUT_DIR = "data/processed"
OUTPUT_DIR = "results/outputs"

def extract_links_from_xml(xml_path):
    """
    Extract all URLs from a Grobid XML file.
    
    Args:
        xml_path: Path to XML file
    
    Returns:
        list: List of dictionaries with link information
    """
    links = []
    
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # Grobid uses TEI namespace
        ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
        
        # Method 1: Find all <ptr> elements (pointers/links in TEI)
        for ptr in root.findall('.//tei:ptr', ns):
            target = ptr.get('target')
            if target and (target.startswith('http://') or target.startswith('https://')):
                links.append({
                    'url': target,
                    'type': 'ptr_element',
                    'context': ptr.get('type', 'unknown')
                })
        
        # Method 2: Find all <ref> elements with target attribute
        for ref in root.findall('.//tei:ref', ns):
            target = ref.get('target')
            if target and (target.startswith('http://') or target.startswith('https://')):
                links.append({
                    'url': target,
                    'type': 'ref_element',
                    'context': ref.get('type', 'unknown')
                })
        
        # Method 3: Search for URLs in text using regex
        text_content = ''.join(root.itertext())
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        found_urls = re.findall(url_pattern, text_content)
        
        for url in found_urls:
            # Clean URL (remove trailing punctuation)
            url = re.sub(r'[.,;:!?)\]]+$', '', url)
            
            # Avoid duplicates
            if not any(link['url'] == url for link in links):
                links.append({
                    'url': url,
                    'type': 'text_extracted',
                    'context': 'body_text'
                })
        
    except Exception as e:
        print(f"Error extracting links from {xml_path.name}: {e}")
    
    return links

def categorize_url(url):
    """
    Categorize URL by domain type.
    
    Args:
        url: URL string
    
    Returns:
        str: Category name
    """
    try:
        domain = urlparse(url).netloc.lower()
        
        if 'github.com' in domain or 'gitlab.com' in domain:
            return 'code_repository'
        elif 'arxiv.org' in domain:
            return 'arxiv'
        elif 'doi.org' in domain or 'dx.doi.org' in domain:
            return 'doi'
        elif any(x in domain for x in ['google.com', 'scholar.google']):
            return 'google'
        elif any(x in domain for x in ['wikipedia.org', 'wiki']):
            return 'wikipedia'
        elif 'youtube.com' in domain or 'youtu.be' in domain:
            return 'video'
        else:
            return 'other'
            
    except:
        return 'unknown'

def main():
    """Extract links from all papers and save results."""
    
    # Create output directory
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    
    # Get all XML files
    xml_files = list(Path(INPUT_DIR).glob("*.xml"))
    
    if not xml_files:
        print(f"No XML files found in {INPUT_DIR}")
        print("Run extract_text.py first to process PDFs with Grobid")
        return
    
    print(f"Found {len(xml_files)} XML files")
    
    # Extract links from all papers
    all_links = []
    
    for xml_path in sorted(xml_files):
        links = extract_links_from_xml(xml_path)
        
        for link in links:
            link['paper'] = xml_path.stem
            link['category'] = categorize_url(link['url'])
            all_links.append(link)
        
        print(f"{xml_path.stem}: {len(links)} links found")
    
    if not all_links:
        print("No links found in any papers")
        return
    
    # Save to CSV
    csv_path = Path(OUTPUT_DIR) / "extracted_links.csv"
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['paper', 'url', 'category', 'type', 'context']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_links)
    
    print(f"\nTotal links extracted: {len(all_links)}")
    print(f"Links saved to: {csv_path}")
    
    # Statistics by category
    from collections import Counter
    categories = Counter(link['category'] for link in all_links)
    
    print("\nLinks by category:")
    for category, count in categories.most_common():
        print(f"  {category}: {count}")
    
    # Statistics by paper
    by_paper = Counter(link['paper'] for link in all_links)
    print(f"\nAverage links per paper: {len(all_links) / len(xml_files):.1f}")

if __name__ == "__main__":
    main()