import xml.etree.ElementTree as ET
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Configuration
INPUT_DIR = "data/processed"
OUTPUT_DIR = "results/figures"

def count_figures_in_xml(xml_path):
    """
    Count the number of figures in a Grobid XML file.
    
    Args:
        xml_path: Path to XML file
    
    Returns:
        int: Number of figures found
    """
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # Grobid uses TEI namespace
        ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
        
        # Find all figure elements
        figures = root.findall('.//tei:figure', ns)
        
        # Debug: print what we find in first file
        if xml_path.stem == 'paper1':
            print(f"\nDEBUG for {xml_path.name}:")
            print(f"  Total <figure> elements: {len(figures)}")
            if figures:
                print(f"  Sample types: {[f.get('type') for f in figures[:5]]}")
                print(f"  Sample coords: {[f.get('coords') is not None for f in figures[:5]]}")
        
        # Strategy: Try multiple counting methods
        
        # Method 1: Explicit type="figure"
        type_figure = [f for f in figures if f.get('type') == 'figure']
        
        # Method 2: Has coords attribute (indicates image/graphic)
        with_coords = [f for f in figures if f.get('coords')]
        
        # Method 3: All figures except tables
        not_tables = [f for f in figures if f.get('type') != 'table']
        
        # Choose the best count
        if len(type_figure) > 0:
            return len(type_figure)
        elif len(with_coords) > 0:
            return len(with_coords)
        elif len(not_tables) > 0:
            return len(not_tables)
        else:
            # Last resort: count all figure elements
            return len(figures)
        
    except Exception as e:
        print(f"Error counting figures in {xml_path.name}: {e}")
        return 0

def create_visualization(data, output_path):
    """
    Create bar chart of figure counts.
    
    Args:
        data: DataFrame with paper names and figure counts
        output_path: Path to save the visualization
    """
    # Set style
    sns.set_style("whitegrid")
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Create bar plot
    bars = ax.bar(data['Paper'], data['Figures'], color='steelblue', edgecolor='black')
    
    # Customize
    ax.set_xlabel('Paper', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Figures', fontsize=12, fontweight='bold')
    ax.set_title('Number of Figures per Paper', fontsize=14, fontweight='bold', pad=20)
    
    # Rotate x labels for better readability
    plt.xticks(rotation=45, ha='right')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=10)
    
    # Add grid
    ax.yaxis.grid(True, linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)
    
    # Tight layout
    plt.tight_layout()
    
    # Save
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Visualization saved to: {output_path}")
    plt.close()

def main():
    """Analyze figure counts and create visualization."""
    
    # Create output directories
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    Path("results/outputs").mkdir(parents=True, exist_ok=True)
    
    # Get all XML files
    xml_files = list(Path(INPUT_DIR).glob("*.xml"))
    
    if not xml_files:
        print(f"No XML files found in {INPUT_DIR}")
        print("Run extract_text.py first to process PDFs with Grobid")
        return
    
    print(f"Found {len(xml_files)} XML files")
    
    # Count figures in each paper
    results = []
    for xml_path in sorted(xml_files):
        count = count_figures_in_xml(xml_path)
        results.append({
            'Paper': xml_path.stem,
            'Figures': count
        })
        print(f"{xml_path.stem}: {count} figures")
    
    # Create DataFrame
    df = pd.DataFrame(results)
    
    # Statistics
    print(f"\nStatistics:")
    print(f"Total figures: {df['Figures'].sum()}")
    print(f"Average figures per paper: {df['Figures'].mean():.2f}")
    print(f"Min figures: {df['Figures'].min()}")
    print(f"Max figures: {df['Figures'].max()}")
    
    # Save to CSV
    csv_path = Path("results/outputs") / "figure_counts.csv"
    df.to_csv(csv_path, index=False)
    print(f"\nFigure counts saved to: {csv_path}")
    
    # Create visualization
    output_path = Path(OUTPUT_DIR) / "figures_per_paper.png"
    create_visualization(df, output_path)

if __name__ == "__main__":
    main()