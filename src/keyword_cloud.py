import xml.etree.ElementTree as ET
from pathlib import Path
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import re

# Configuration
INPUT_DIR = "data/processed"
OUTPUT_DIR = "results/figures"
STOPWORDS_FILE = None  # Optional: path to custom stopwords

# Common stopwords for scientific papers
STOPWORDS = set([
    'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
    'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
    'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
    'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their',
    'can', 'also', 'are', 'is', 'was', 'were', 'been', 'has', 'had',
    'using', 'used', 'use', 'paper', 'show', 'shows', 'results', 'result',
    'propose', 'proposed', 'approach', 'method', 'methods', 'based', 'work'
])

def extract_abstract_from_xml(xml_path):
    """
    Extract abstract text from Grobid XML file.
    
    Args:
        xml_path: Path to XML file
    
    Returns:
        str: Abstract text or empty string if not found
    """
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # Grobid uses TEI namespace
        ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
        
        # Find abstract in profileDesc
        abstract = root.find('.//tei:profileDesc/tei:abstract', ns)
        
        if abstract is not None:
            # Extract all text from abstract, removing XML tags
            text = ''.join(abstract.itertext())
            return text.strip()
        
        return ""
        
    except Exception as e:
        print(f"Error extracting abstract from {xml_path.name}: {e}")
        return ""

def clean_text(text):
    """
    Clean and normalize text for keyword extraction.
    
    Args:
        text: Raw text string
    
    Returns:
        list: List of cleaned words
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove non-alphabetic characters (keep spaces)
    text = re.sub(r'[^a-z\s]', ' ', text)
    
    # Split into words
    words = text.split()
    
    # Filter stopwords and short words
    words = [w for w in words if w not in STOPWORDS and len(w) > 3]
    
    return words

def generate_wordcloud(text, output_path):
    """
    Generate and save word cloud image.
    
    Args:
        text: Combined text from all abstracts
        output_path: Path to save the image
    """
    wordcloud = WordCloud(
        width=1600,
        height=800,
        background_color='white',
        colormap='viridis',
        max_words=100,
        relative_scaling=0.5,
        min_font_size=10
    ).generate(text)
    
    # Create figure
    plt.figure(figsize=(20, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Keyword Cloud from Paper Abstracts', fontsize=20, pad=20)
    plt.tight_layout(pad=0)
    
    # Save
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Word cloud saved to: {output_path}")
    plt.close()

def main():
    """Extract abstracts and generate keyword cloud."""
    
    # Create output directory
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    
    # Get all XML files
    xml_files = list(Path(INPUT_DIR).glob("*.xml"))
    
    if not xml_files:
        print(f"No XML files found in {INPUT_DIR}")
        print("Run extract_text.py first to process PDFs with Grobid")
        return
    
    print(f"Found {len(xml_files)} XML files")
    
    # Extract all abstracts
    all_abstracts = []
    all_words = []
    
    for xml_path in sorted(xml_files):
        abstract = extract_abstract_from_xml(xml_path)
        if abstract:
            all_abstracts.append(abstract)
            words = clean_text(abstract)
            all_words.extend(words)
            print(f"Extracted abstract from: {xml_path.stem} ({len(words)} words)")
        else:
            print(f"No abstract found in: {xml_path.stem}")
    
    if not all_words:
        print("No abstracts found. Cannot generate word cloud.")
        return
    
    # Statistics
    word_freq = Counter(all_words)
    print(f"\nTotal words extracted: {len(all_words)}")
    print(f"Unique words: {len(word_freq)}")
    print(f"\nTop 10 keywords:")
    for word, count in word_freq.most_common(10):
        print(f"  {word}: {count}")
    
    # Generate word cloud
    combined_text = ' '.join(all_words)
    output_path = Path(OUTPUT_DIR) / "keyword_cloud.png"
    generate_wordcloud(combined_text, output_path)
    
    # Save word frequencies to CSV
    import csv
    csv_path = Path("results/outputs") / "keyword_frequencies.csv"
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Keyword', 'Frequency'])
        for word, count in word_freq.most_common(50):
            writer.writerow([word, count])
    
    print(f"Keyword frequencies saved to: {csv_path}")

if __name__ == "__main__":
    main()