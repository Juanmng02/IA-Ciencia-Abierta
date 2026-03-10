import pytest
import xml.etree.ElementTree as ET
from pathlib import Path
from collections import Counter
from unittest.mock import patch, MagicMock
import tempfile
import os

# Import functions to test
from src.figures_analysis import count_figures_in_xml
from src.keyword_cloud import extract_abstract_from_xml, clean_text
from src.links_extraction import extract_links_from_xml, categorize_url
from src.extract_text import process_pdf_with_grobid


# ─────────────────────────────────────────────
# Fixtures: sample XML files for testing
# ─────────────────────────────────────────────

@pytest.fixture
def sample_xml_with_figures(tmp_path):
    """Create a minimal Grobid XML file with 3 figures."""
    xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <teiHeader>
    <profileDesc>
      <abstract>
        <p>This is a sample abstract about paleontology and species analysis.</p>
      </abstract>
    </profileDesc>
  </teiHeader>
  <text>
    <body>
      <figure type="figure" coords="1,100,100,200,200">
        <head>Figure 1</head>
      </figure>
      <figure type="figure" coords="2,100,100,200,200">
        <head>Figure 2</head>
      </figure>
      <figure type="table">
        <head>Table 1</head>
      </figure>
      <figure coords="3,100,100,200,200">
        <head>Figure 3</head>
      </figure>
    </body>
  </text>
</TEI>'''
    xml_file = tmp_path / "paper1.xml"
    xml_file.write_text(xml_content, encoding='utf-8')
    return xml_file


@pytest.fixture
def sample_xml_with_abstract(tmp_path):
    """Create a minimal Grobid XML file with an abstract and links."""
    xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <teiHeader>
    <profileDesc>
      <abstract>
        <p>This paper analyzes fossil species using deep learning methods for paleontology research.</p>
      </abstract>
    </profileDesc>
  </teiHeader>
  <text>
    <body>
      <p>See code at <ptr target="https://github.com/example/repo"/>.</p>
      <p>Data available at <ref target="https://doi.org/10.1234/example">DOI</ref>.</p>
      <p>More info at https://arxiv.org/abs/1234.5678</p>
    </body>
  </text>
</TEI>'''
    xml_file = tmp_path / "paper_test.xml"
    xml_file.write_text(xml_content, encoding='utf-8')
    return xml_file


@pytest.fixture
def empty_xml(tmp_path):
    """Create a minimal XML file with no figures or abstract."""
    xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <teiHeader/>
  <text><body><p>No figures or abstract here.</p></body></text>
</TEI>'''
    xml_file = tmp_path / "empty.xml"
    xml_file.write_text(xml_content, encoding='utf-8')
    return xml_file


# ─────────────────────────────────────────────
# Tests: figures_analysis.py
# ─────────────────────────────────────────────

class TestCountFigures:

    def test_counts_explicit_type_figures(self, sample_xml_with_figures):
        """Should count figures with type='figure', excluding tables."""
        count = count_figures_in_xml(sample_xml_with_figures)
        assert count == 2  # 2 explicit type="figure", 1 table excluded

    def test_returns_zero_for_empty_xml(self, empty_xml):
        """Should return 0 when no figures are present."""
        count = count_figures_in_xml(empty_xml)
        assert count == 0

    def test_returns_zero_for_missing_file(self, tmp_path):
        """Should return 0 gracefully when file does not exist."""
        missing = tmp_path / "nonexistent.xml"
        count = count_figures_in_xml(missing)
        assert count == 0

    def test_returns_integer(self, sample_xml_with_figures):
        """Return value should always be an integer."""
        count = count_figures_in_xml(sample_xml_with_figures)
        assert isinstance(count, int)


# ─────────────────────────────────────────────
# Tests: keyword_cloud.py
# ─────────────────────────────────────────────

class TestExtractAbstract:

    def test_extracts_abstract_text(self, sample_xml_with_abstract):
        """Should extract non-empty abstract text."""
        abstract = extract_abstract_from_xml(sample_xml_with_abstract)
        assert len(abstract) > 0
        assert "paleontology" in abstract.lower()

    def test_returns_empty_string_when_no_abstract(self, empty_xml):
        """Should return empty string when abstract is missing."""
        abstract = extract_abstract_from_xml(empty_xml)
        assert abstract == ""

    def test_returns_empty_string_for_missing_file(self, tmp_path):
        """Should return empty string gracefully for missing files."""
        missing = tmp_path / "nonexistent.xml"
        abstract = extract_abstract_from_xml(missing)
        assert abstract == ""


class TestCleanText:

    def test_removes_stopwords(self):
        """Common stopwords should be filtered out."""
        words = clean_text("the analysis of the species is based on methods")
        assert "the" not in words
        assert "is" not in words
        assert "based" not in words

    def test_removes_short_words(self):
        """Words with 3 or fewer characters should be removed."""
        words = clean_text("a an the and use big analysis")
        assert "a" not in words
        assert "an" not in words
        assert "and" not in words

    def test_converts_to_lowercase(self):
        """All output words should be lowercase."""
        words = clean_text("Paleontology SPECIES Analysis")
        assert all(w == w.lower() for w in words)

    def test_returns_list(self):
        """clean_text should return a list."""
        result = clean_text("sample abstract text for testing purposes")
        assert isinstance(result, list)

    def test_empty_string_returns_empty_list(self):
        """Empty input should produce empty list."""
        result = clean_text("")
        assert result == []

    def test_keeps_relevant_keywords(self):
        """Domain-relevant words should be preserved."""
        words = clean_text("fossil paleontology species analysis genus")
        assert "fossil" in words
        assert "paleontology" in words
        assert "species" in words


# ─────────────────────────────────────────────
# Tests: links_extraction.py
# ─────────────────────────────────────────────

class TestExtractLinks:

    def test_extracts_ptr_links(self, sample_xml_with_abstract):
        """Should extract links from <ptr> elements."""
        links = extract_links_from_xml(sample_xml_with_abstract)
        urls = [l['url'] for l in links]
        assert any("github.com" in url for url in urls)

    def test_extracts_ref_links(self, sample_xml_with_abstract):
        """Should extract links from <ref> elements."""
        links = extract_links_from_xml(sample_xml_with_abstract)
        urls = [l['url'] for l in links]
        assert any("doi.org" in url for url in urls)

    def test_extracts_text_links(self, sample_xml_with_abstract):
        """Should extract links found in plain text via regex."""
        links = extract_links_from_xml(sample_xml_with_abstract)
        urls = [l['url'] for l in links]
        assert any("arxiv.org" in url for url in urls)

    def test_returns_empty_list_for_empty_xml(self, empty_xml):
        """Should return empty list when no links are present."""
        links = extract_links_from_xml(empty_xml)
        assert links == []

    def test_returns_empty_list_for_missing_file(self, tmp_path):
        """Should return empty list gracefully for missing files."""
        missing = tmp_path / "nonexistent.xml"
        links = extract_links_from_xml(missing)
        assert links == []

    def test_no_duplicate_urls(self, sample_xml_with_abstract):
        """Should not return duplicate URLs."""
        links = extract_links_from_xml(sample_xml_with_abstract)
        urls = [l['url'] for l in links]
        assert len(urls) == len(set(urls))


class TestCategorizeUrl:

    def test_github_is_code_repository(self):
        assert categorize_url("https://github.com/user/repo") == "code_repository"

    def test_gitlab_is_code_repository(self):
        assert categorize_url("https://gitlab.com/user/repo") == "code_repository"

    def test_doi_is_doi(self):
        assert categorize_url("https://doi.org/10.1234/test") == "doi"

    def test_arxiv_is_arxiv(self):
        assert categorize_url("https://arxiv.org/abs/1234.5678") == "arxiv"

    def test_unknown_domain_is_other(self):
        assert categorize_url("https://somerandompublisher.com/paper") == "other"

    def test_returns_string(self):
        result = categorize_url("https://github.com/test/repo")
        assert isinstance(result, str)


# ─────────────────────────────────────────────
# Tests: extract_text.py
# ─────────────────────────────────────────────

class TestProcessPdfWithGrobid:

    def test_returns_true_on_success(self, tmp_path):
        """Should return True when Grobid responds with 200."""
        pdf_path = tmp_path / "test.pdf"
        pdf_path.write_bytes(b"%PDF-1.4 fake content")
        output_path = tmp_path / "test.xml"

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<TEI>fake xml</TEI>"

        with patch("src.extract_text.requests.post", return_value=mock_response):
            result = process_pdf_with_grobid(pdf_path, output_path)

        assert result is True
        assert output_path.exists()

    def test_returns_false_on_error_status(self, tmp_path):
        """Should return False when Grobid responds with non-200 status."""
        pdf_path = tmp_path / "test.pdf"
        pdf_path.write_bytes(b"%PDF-1.4 fake content")
        output_path = tmp_path / "test.xml"

        mock_response = MagicMock()
        mock_response.status_code = 500

        with patch("src.extract_text.requests.post", return_value=mock_response):
            result = process_pdf_with_grobid(pdf_path, output_path)

        assert result is False

    def test_returns_false_on_connection_error(self, tmp_path):
        """Should return False gracefully when Grobid is unreachable."""
        import requests as req
        pdf_path = tmp_path / "test.pdf"
        pdf_path.write_bytes(b"%PDF-1.4 fake content")
        output_path = tmp_path / "test.xml"

        with patch("src.extract_text.requests.post", side_effect=req.exceptions.ConnectionError):
            result = process_pdf_with_grobid(pdf_path, output_path)

        assert result is False