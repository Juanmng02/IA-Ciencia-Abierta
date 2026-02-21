# AI Open Science - Task 1: Text Extraction and Analysis

## Description

This project performs automated analysis on 10 open-access scientific articles using Grobid and Python. The analysis includes:

- Keyword cloud generation from abstracts
- Visualization of figure counts per article  
- Extraction of all links found in papers

## Objectives

Following best practices from the "Open Science and AI in Research Software Engineering" course, this project demonstrates:

1. **Reproducible research** - All code and data processing steps are documented
2. **Open science principles** - Using open-access papers and open-source tools
3. **FAIR principles** - Findable, Accessible, Interoperable, Reusable outputs

## Project Structure
```
ai-open-science-task1/
├── README.md                 # Project documentation
├── LICENSE                   # MIT License
├── .gitignore               # Files to ignore in git
├── requirements.txt         # Python dependencies
├── data/
│   └── processed/           # Grobid XML outputs
├── src/
│   ├── extract_text.py      # Grobid processing pipeline
│   ├── keyword_cloud.py     # Abstract keyword analysis
│   ├── figures_analysis.py  # Figure counting
│   └── links_extraction.py  # URL extraction
└── results/
    ├── figures/             # Generated visualizations
    └── outputs/             # Analysis results (CSV, TXT)
```

## Requirements

- Python 3.8+
- Docker (for Grobid)
- See `requirements.txt` for Python packages

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/[TU-USUARIO]/[TU-REPO].git
cd [TU-REPO]
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Grobid with Docker
```bash
docker pull lfoppiano/grobid:0.8.0
docker run --rm -p 8070:8070 lfoppiano/grobid:0.8.0
```

Grobid will be available at `http://localhost:8070`

## Dataset

This project analyzes **10 open-access papers** from the following source(s):

- **arXiv.org** - Category: [cs.AI / cs.LG / cs.CV]
- Topic: [Especifica el tema: ej. "Machine Learning", "Computer Vision", etc.]

Papers are stored in `data/papers/` (not included in repository due to size).

### Paper Selection Criteria:
- Open access (freely available)
- PDF format
- Published after 2020
- Related to [tu campo: AI/ML/CV/etc.]

## Usage

### Step 1: Process PDFs with Grobid
```bash
python src/extract_text.py
```

This will process all PDFs in `data/papers/` and save XML outputs to `data/processed/`.

### Step 2: Generate Keyword Cloud
```bash
python src/keyword_cloud.py
```

Output: `results/figures/keyword_cloud.png`

### Step 3: Analyze Figure Counts
```bash
python src/figures_analysis.py
```

Output: `results/figures/figures_per_paper.png` and `results/outputs/figure_counts.csv`

### Step 4: Extract Links
```bash
python src/links_extraction.py
```

Output: `results/outputs/extracted_links.csv`

## Validation

### How results were validated:

1. **Keyword Cloud**: 
   - Manual inspection of top 50 keywords
   - Comparison with paper abstracts
   - Removal of stopwords verified

2. **Figure Counts**:
   - Cross-checked with manual count in 3 sample papers
   - Accuracy: [X%]
   - Known limitations: [describe any]

3. **Link Extraction**:
   - Sample of 20 links manually verified
   - Tested link validity (HTTP status codes)
   - False positives filtered: [describe criteria]

## Results

### Summary Statistics

| Metric | Value |
|--------|-------|
| Total papers analyzed | 10 |
| Total figures found | [X] |
| Average figures per paper | [X.X] |
| Total links extracted | [X] |
| Unique keywords | [X] |

### Key Findings

[Añadir aquí tus hallazgos principales después de hacer el análisis]

## Technologies Used

- **Grobid 0.8.0** - PDF text extraction
- **Python 3.8+** - Data processing
- **WordCloud** - Keyword visualization
- **Matplotlib/Seaborn** - Data visualization
- **Pandas** - Data manipulation
- **BeautifulSoup4** - XML parsing

## References

- Grobid: https://github.com/kermitt2/grobid
- Course materials: [link a las slides si están públicas]

## Author

**[Tu Nombre]**
- Universidad Politécnica de Madrid
- Course: Open Science and AI in Research Software Engineering
- Date: February 2026

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

