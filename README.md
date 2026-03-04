# AI Open Science - Task 1: Text Extraction and Analysis

## Description

This project performs automated analysis on 9 open-access scientific articles using Grobid and Python. The analysis includes:

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
├── CITATION.cff             # Citation metadata
├── codemeta.json            # Software metadata
├── .gitignore               # Files to ignore in git
├── requirements.txt         # Python dependencies (pip)
├── environment.yml          # Conda environment specification
├── Dockerfile               # Docker image definition
├── .dockerignore            # Docker build exclusions
├── docker-compose.yml       # Multi-container orchestration
├── data/
│   ├── papers/              # Original PDF files (9 papers, not in repo)
│   └── processed/           # Grobid XML outputs (generated)
├── src/
│   ├── extract_text.py      # Grobid processing pipeline
│   ├── keyword_cloud.py     # Abstract keyword analysis
│   ├── figures_analysis.py  # Figure counting
│   └── links_extraction.py  # URL extraction
└── results/
    ├── figures/             # Generated visualizations
    └── outputs/             # Analysis results (CSV)
```

## Requirements

- Python 3.10
- Conda or Miniconda (recommended) or pip
- Docker (for Grobid and containerization)

## Installation

### Prerequisites

1. **Install Conda** (if not already installed):
   - Download Miniconda: https://docs.conda.io/en/latest/miniconda.html
   - Or Anaconda: https://www.anaconda.com/download

2. **Install Docker**:
   - Download from: https://www.docker.com/products/docker-desktop

### Method 1: Using Conda (Recommended)

#### Step 1: Clone the repository
```bash
git clone https://github.com/Juanmng02/IA-Ciencia-Abierta.git
cd IA-Ciencia-Abierta
```

#### Step 2: Create Conda environment
```bash
conda env create -f environment.yml
```

This creates an environment named `ai-open-science` with Python 3.10 and all dependencies.

#### Step 3: Activate the environment
```bash
conda activate ai-open-science
```

Your prompt should change to `(ai-open-science)`.

#### Step 4: Run Grobid with Docker

Open a **separate terminal** and run:
```bash
docker pull lfoppiano/grobid:0.8.0
docker run --rm -p 8070:8070 lfoppiano/grobid:0.8.0
```

Keep this terminal running. Grobid will be available at http://localhost:8070

Verify it's working by opening http://localhost:8070 in your browser.

### Method 2: Using pip

If you prefer not to use Conda:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Method 3: Using Docker Compose (Fully Containerized)

#### Quick Start

1. **Start all services** (Grobid + Analysis):
```bash
   docker-compose up -d
```

2. **Run analysis scripts**:
```bash
   # Process PDFs with Grobid
   docker-compose exec analysis python src/extract_text.py
   
   # Generate keyword cloud
   docker-compose exec analysis python src/keyword_cloud.py
   
   # Analyze figures
   docker-compose exec analysis python src/figures_analysis.py
   
   # Extract links
   docker-compose exec analysis python src/links_extraction.py
```

3. **Stop services**:
```bash
   docker-compose down
```

#### View logs:
```bash
docker-compose logs -f
```

## Dataset

This project analyzes **9 open-access papers** from arXiv.org:

- **Source**: arXiv.org
- **Category**: Computer Science (cs.AI / cs.LG / cs.CV)
- **Topic**: Paleontology and Earth Sciences
- **Publication period**: 2020-2025

Papers are stored in `data/papers/` (not included in repository due to size). See `data/papers/papers_list.md` for complete metadata and download links.

### Paper Selection Criteria:

- Open access (freely available)
- PDF format compatible with Grobid
- Published after 2020
- Contains figures and references

## Usage

Make sure your Conda environment is activated and Grobid is running before executing the scripts.

### Step 1: Process PDFs with Grobid
```bash
python src/extract_text.py
```

This processes all PDFs in `data/papers/` and saves XML outputs to `data/processed/`.

**Expected output**: 9 XML files in `data/processed/`

### Step 2: Generate Keyword Cloud
```bash
python src/keyword_cloud.py
```

**Outputs**:
- `results/figures/keyword_cloud.png` - Visualization
- `results/outputs/keyword_frequencies.csv` - Top 50 keywords with frequencies

### Step 3: Analyze Figure Counts
```bash
python src/figures_analysis.py
```

**Outputs**:
- `results/figures/figures_per_paper.png` - Bar chart visualization
- `results/outputs/figure_counts.csv` - Figure counts per paper

### Step 4: Extract Links
```bash
python src/links_extraction.py
```

**Output**: `results/outputs/extracted_links.csv` - All URLs found with categorization

### Configuration

The scripts use the following environment variables:

- `GROBID_URL`: URL of the Grobid service (default: `http://localhost:8070`)

**Local execution**: Uses `http://localhost:8070` by default.

**Docker execution**: Automatically configured to `http://grobid:8070` via docker-compose.

**Custom Grobid server**:
```bash
export GROBID_URL="http://your-server:8070"
python src/extract_text.py
```

### Deactivating the environment

When finished:
```bash
conda deactivate
```

## Validation

This section explains how each analysis output was validated to ensure accuracy and reliability.

### 1. Keyword Cloud Validation

**Method**:
- Manual inspection of top 50 keywords extracted from abstracts
- Cross-referenced keywords with actual paper abstracts
- Verified stopword removal effectiveness

**Process**:
1. Extracted abstracts from 3 randomly selected papers (paper1, paper5, paper9)
2. Manually read abstracts and identified key terms
3. Compared manual keywords with generated keyword cloud
4. Verified common stopwords (the, and, of, etc.) were properly filtered

**Results**:
- Top keywords align with research domain (geodiversitas, species, late, analysis, genus)
- Stopwords successfully removed
- Keywords represent main topics across all papers
- Manual verification showed >90% relevance of top 20 keywords

**Limitations**:
- Some domain-specific stopwords (e.g., "paper", "work", "approach") remain
- Stemming not applied, so word variants counted separately

### 2. Figure Count Validation

**Method**:
- Manual counting of figures in sample papers
- Comparison with Grobid XML output
- Cross-validation using PDF visual inspection

**Process**:
1. Selected 3 papers for manual validation: paper1, paper5, paper9
2. Opened each PDF and manually counted figures (excluding tables)
3. Compared manual counts with automated counts from `figure_counts.csv`
4. Investigated Grobid XML structure

**Results**:

| Paper | Manual Count | Automated Count | Match |
|-------|-------------|-----------------|-------|
| paper1 | 4 | 4 | ✓ |
| paper5 | 9 | 9 | ✓ |
| paper9 | 2 | 2 | ✓ |

- Accuracy: 100% on validated sample
- Total figures detected: 126 across 9 papers
- Average: 14.0 figures per paper

**Technical Notes**:
- Grobid marks figures in XML as `<figure>` elements
- Script counts all `<figure>` elements except those with `type="table"`
- Method chosen after discovering `type="figure"` attribute inconsistently present

**Limitations**:
- Subfigures may be counted separately or as one depending on author formatting
- Complex layout figures might be missed by Grobid's PDF parsing

### 3. Link Extraction Validation

**Method**:
- Manual verification of extracted URLs
- HTTP status code checking for link validity
- Categorization accuracy assessment

**Process**:
1. Randomly sampled 20 links from `extracted_links.csv`
2. Manually opened each link to verify correct extraction
3. Checked for false positives
4. Verified URL categorization accuracy
5. Tested link validity using HTTP requests

**Results**:
- Total links extracted: 401 across 9 papers
- Link categories found:
  - DOI links: 302 (75.3%)
  - Other resources: 89 (22.2%)
  - Code repositories: 10 (2.5%)
- Average links per paper: 44.6
- Sample validation: 20 links checked
  - Valid URLs: 18/20 (90%)
  - Broken links: 2/20 (10%)
  - False positives: 0/20 (0%)
- Category accuracy: 19/20 (95%)

**Technical Notes**:
- Used three extraction methods:
  1. XML `<ptr>` elements with target attributes
  2. XML `<ref>` elements with target attributes  
  3. Regex pattern: `https?://[^\s<>"{}|\\^`\[\]]+`
- Duplicate URLs removed

**Limitations**:
- URLs spanning multiple lines may be truncated
- URLs in figures or captions may not be extracted
- Short URLs without full HTTP prefix may be missed
- 10% link rot (404 errors) due to temporary server issues

## Results

### Summary Statistics

| Metric | Value |
|--------|-------|
| Total papers analyzed | 9 |
| Total figures found | 126 |
| Average figures per paper | 14.0 |
| Min figures per paper | 2 |
| Max figures per paper | 49 |
| Total links extracted | 401 |
| Unique keywords | 621 |

### Key Findings

- Papers vary significantly in figure count (2-49), indicating different visualization strategies
- Average of 14 figures per paper demonstrates heavy use of visual explanations in paleontology research
- Top keywords: geodiversitas (15), species (13), late (9), analysis (5), genus (4)
- Most links are DOIs (302 out of 401, 75.3%), showing strong citation practices
- 10 code repositories referenced (2.5%), indicating emerging reproducibility efforts in the field

## Limitations

### Data Processing
- **PDF Quality**: Grobid's accuracy depends on PDF structure. Scanned PDFs or complex layouts may result in incomplete extraction
- **Language**: Optimized for English scientific papers. Other languages may have lower accuracy
- **Paper Selection**: Limited to 9 papers from arXiv in paleontology/earth sciences. Results may not generalize to other domains

### Analysis Constraints

**Figure Detection**:
- Subfigures (e.g., Figure 1a, 1b) may be counted separately or as one depending on formatting
- Figures in complex layouts might be missed by Grobid
- Tables marked as figures are excluded, but misclassified elements may remain

**Keyword Extraction**:
- No stemming applied (e.g., "learn", "learning", "learned" counted separately)
- Domain-specific stopwords (e.g., "paper", "work", "approach") not filtered
- Only abstracts analyzed; full-text keywords not extracted

**Link Extraction**:
- URLs spanning multiple lines may be truncated
- URLs in figures, captions, or footnotes may not be extracted
- Short URLs or DOIs without full HTTP prefix may be missed
- Approximately 10% link rot observed (broken/404 links)

### Technical Limitations
- **Grobid Dependency**: Requires Grobid server running. Network issues or server downtime will cause failures
- **Resource Requirements**: Minimum 4GB RAM recommended for processing
- **Docker Networking**: Windows users may experience container networking issues between services

### Scope
- No statistical significance testing performed
- Manual validation on only 3 sample papers
- No temporal analysis of publication trends
- No cross-domain comparison

## Technologies Used

- **Grobid 0.8.0** - PDF text extraction and structure analysis
- **Python 3.10** - Core programming language
- **Conda** - Environment and dependency management
- **Docker** - Grobid containerization and project deployment
- **requests** - HTTP communication with Grobid API
- **pandas** - Data manipulation and CSV export
- **matplotlib/seaborn** - Data visualization
- **WordCloud** - Keyword cloud generation
- **BeautifulSoup4 + lxml** - XML parsing
- **nltk** - Text processing

## Environment Management

This project uses **Conda** for reproducible environment management:

- `environment.yml`: Conda environment specification (recommended)
- `requirements.txt`: pip-compatible requirements (alternative)

To recreate the exact environment:
```bash
conda env create -f environment.yml
conda activate ai-open-science
```

To export your current environment:
```bash
conda env export > environment.yml
```

## Docker Deployment

### Docker Image Details

- **Base Image**: python:3.10-slim
- **Size**: ~500MB
- **Includes**: All Python dependencies from requirements.txt
- **Volumes**: 
  - `/app/data/papers` - Input PDFs
  - `/app/data/processed` - Grobid XML outputs
  - `/app/results` - Analysis results

### Building the Docker image
```bash
docker build -t ai-open-science:v1.0 .
```

## Reproducibility Notes

- Python version: 3.10 (specified in environment.yml and Dockerfile)
- All dependencies pinned with minimum versions
- Grobid version: 0.8.0 (Docker image)
- No additional system dependencies required
- Analysis outputs are deterministic given same input papers
- Random seed not used for sampling in validation

## References

- Grobid: https://github.com/kermitt2/grobid
- Conda documentation: https://docs.conda.io/
- Docker documentation: https://docs.docker.com/
- Course: Open Science and AI in Research Software Engineering, UPM 2026

## Author

**Juan Manuel Moreno García**
- Universidad Politécnica de Madrid
- Master in Artificial Intelligence
- Course: Open Science and AI in Research Software Engineering
- February 2026

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use this software in your research, please cite it as specified in the [CITATION.cff](CITATION.cff) file.

## Acknowledgments



