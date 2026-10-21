# 🔎 WikiFact Check
### Evidence-Based Verification of Wikipedia Infobox Facts

**WikiFact Check** is an experimental fact-verification tool that checks whether structured facts in Wikipedia infoboxes are supported by the corresponding article text. It compares infobox values with information found in the article and presents relevant evidence to help users identify potential inconsistencies.

Built for **Wikimedia Open Source Day — Challenge 4**.

<p align="center">
  <a href="https://wikifact-check-mfi8axlwerctayxu2yjyct.streamlit.app/">
    <strong>🚀 Live Demo</strong>
  </a>
  &nbsp; • &nbsp;
  <a href="https://github.com/Saksham-M4/WikiFact-Check">
    <strong>💻 Source Code</strong>
  </a>
</p>

---

## 📌 Table of Contents

- [Overview](#-overview)
- [How It Works](#-how-it-works)
- [Key Features](#-key-features)
- [Result Classification](#-result-classification)
- [Supported Fact Types](#-supported-fact-types)
- [Technology Stack](#-technology-stack)
- [Getting Started](#-getting-started)
- [Running Tests](#-running-tests)
- [Project Structure](#-project-structure)
- [Dataset and Data Sources](#-dataset-and-data-sources)
- [Limitations](#️-limitations)
- [Future Improvements](#-future-improvements)
- [Contributing](#-contributing)
- [Disclaimer](#️-disclaimer)
- [Author](#-author)

---

## 📖 Overview

Wikipedia articles contain structured information in infoboxes, including dates, founders, locations, and countries. However, these facts may not always be explicitly supported by the text of the corresponding article.

WikiFact Check helps address this problem by comparing a selected infobox fact with the article's own text and presenting a relevant evidence sentence for human review.

Instead of automatically declaring information true or false, the system classifies the comparison into three outcomes:

- **MATCH** — The fact and article text agree according to the implemented matching logic.
- **POSSIBLE MISMATCH** — Potentially conflicting information was identified.
- **NOT FOUND** — Corresponding evidence could not be identified.

The goal is to make Wikipedia fact verification more transparent, interpretable, and easier to review.

## 🔄 How It Works

WikiFact Check follows an evidence-based verification workflow.

1. **Enter an article title:** Type a Wikipedia article title or select one from the WikiWeak dataset.
2. **Fetch the article:** Retrieve the current English Wikipedia article using the MediaWiki API.
3. **Extract the infobox:** Identify available structured fields from the article.
4. **Select a fact type:** Choose a supported category, such as Birth Date or Founder.
5. **Normalize the fact:** Standardize supported values, including date formats and names.
6. **Search the article text:** Look for information corresponding to the selected fact.
7. **Identify evidence:** Select a relevant sentence from the article.
8. **Compare the information:** Determine whether the extracted fact agrees with the identified evidence or whether a potential conflict exists.
9. **Display the result:** Present the classification, evidence sentence, and article image when available.

### System Flowchart

<!-- Add the WikiFact Check flowchart image here -->

The flowchart illustrates the complete workflow, including the three possible result paths and the final evidence display.

## ✨ Key Features

- **Live Wikipedia Retrieval** — Retrieves article content through the MediaWiki API.
- **Infobox Fact Extraction** — Extracts supported structured facts from Wikipedia infoboxes.
- **Fact Normalization** — Handles recognized variations in date formats and names.
- **Evidence Sentence Identification** — Presents relevant article text for human verification.
- **Potential Mismatch Detection** — Flags conflicting information for further investigation.
- **Multiple Fact Categories** — Supports birth dates, founders, locations, and countries.
- **WikiWeak Dataset Integration** — Provides article-title discovery through a CSV dataset.
- **Article Image Display** — Shows the associated article image when available.
- **Human-in-the-Loop Approach** — Supports manual review rather than claiming automatic truth verification.
- **Automated Testing** — Includes deterministic tests and tests against live Wikipedia content.

## 🚦 Result Classification

| Result | Description |
|---|---|
| 🟢 MATCH | The infobox fact and article text agree after the implemented normalization and matching process. |
| 🟠 POSSIBLE MISMATCH | The article text contains potentially conflicting information that requires human review. |
| ⚪ NOT FOUND | The system could not identify corresponding evidence in the article text. |

**Example:** If an infobox lists a birth year as 1980 but the article text mentions 1981, the system may flag a possible mismatch if its matching logic detects the conflicting values.

A result is an indication produced by the system, not a final judgment about factual accuracy.

## 🧩 Supported Fact Types

| Fact Type | Example | Verification Approach |
|---|---|---|
| Birth Date | Narendra Modi — 17 September 1950 | Normalizes supported date representations before comparison. |
| Founder | Google — Larry Page and Sergey Brin | Searches for normalized names and corresponding textual evidence. |
| Location | An organization or place | Compares the infobox value with location information in the article text. |
| Country | An entity associated with a country | Compares the infobox value with country information found in the text. |

### Example: Date Normalization

The following formats represent the same date when recognized by the implementation:

```text
1950-09-17
17 September 1950
September 17, 1950
17/09/1950
```

Normalization helps the system compare equivalent representations without treating formatting differences as factual disagreements.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Interactive web application |
| MediaWiki API | Retrieval of Wikipedia article content |
| Pandas / CSV | Dataset handling, where used by the implementation |
| Pytest | Automated testing |
| WikiWeak dataset | Article-title discovery |

## 🚀 Getting Started

Follow these instructions to run WikiFact Check locally.

### Prerequisites

- Python 3
- Git
- An internet connection to access the Wikimedia API

### 1. Clone the Repository

```bash
git clone https://github.com/Saksham-M4/WikiFact-Check.git
```

### 2. Navigate to the Project Directory

```bash
cd WikiFact-Check
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch the Application

```bash
streamlit run app.py
```

### 5. Open the Application

Visit the following address in your browser:

```text
http://localhost:8501
```

**Important:** Run the application using `streamlit run app.py`, not `python app.py`.

The application requires internet access to retrieve current article content from Wikipedia.

## 🧪 Running Tests

WikiFact Check includes tests for the matching logic and a separate script for testing against live Wikipedia articles.

### Run Deterministic Tests

```bash
python -m pytest test_factcheck.py
```

This runs predefined tests for the fact-checking logic.

### Run Live Wikipedia Tests

```bash
python live_test.py
```

Live test results can change when Wikipedia articles are edited or when the Wikimedia API is unavailable.

### Example Test Cases

| Article | Fact Type | Expected Result |
|---|---|---|
| Narendra Modi | Birth Date | MATCH |
| Mahendra Singh Dhoni | Birth Date | MATCH |
| Google | Founder | MATCH |

These are intended test cases, not guaranteed outcomes. Actual results depend on the current article content and the implemented extraction and matching rules.

## 📁 Project Structure

```text
WikiFact-Check/
│
├── app.py                  # Streamlit interface and workflow
├── fact_engine.py          # Extraction, normalization, matching and evidence
├── wikiweak_results.csv    # WikiWeak article records
├── test_factcheck.py       # Deterministic matching tests
├── live_test.py            # Live Wikipedia tests
├── requirements.txt        # Project dependencies
├── DATASET_NOTE.txt        # Dataset documentation
└── IMAGE_FEATURE.md        # Article image feature documentation
```

## 📚 Dataset and Data Sources

### WikiWeak Dataset

The WikiWeak CSV file helps users discover and select article titles. The application detects supported title columns, including:

- `name`
- `title`
- `article_title`
- `article_name`
- `article name`

### Wikipedia MediaWiki API

The actual fact-checking process uses the retrieved Wikipedia article rather than treating the dataset's contents as verification evidence.

This separates article discovery from the comparison of infobox facts with article text.

## ⚠️ Limitations

WikiFact Check is an experimental system based on heuristic matching. Its results have several important limitations.

- **Relationship ambiguity:** Mentioning two people in the same sentence does not prove that they founded an organization together.
- **Infobox variability:** Unusual templates and page structures may cause fact extraction to fail.
- **Evidence selection:** A selected sentence may mention a topic without directly supporting the claim.
- **Normalization constraints:** Unrecognized date formats, aliases, and name variations may not be handled correctly.
- **Live content changes:** Wikipedia edits can change the results between runs.
- **API dependency:** Retrieval depends on Wikimedia API availability and network access.
- **Evaluation limitations:** No quantitative evaluation has yet established the system's precision, recall, or overall verification accuracy.

These limitations mean that the system should assist human reviewers rather than replace them.

## 🛣️ Future Improvements

Potential improvements include:

- **Relationship-Aware Verification:** Better detection of explicit relationships such as “founded by” and “co-founded by.”
- **Quantitative Evaluation:** Evaluate performance on a labeled dataset using precision, recall, and F1-score.
- **Expanded Fact Coverage:** Support more infobox fields and additional fact categories.
- **Entity Resolution:** Improve handling of aliases, alternative names, and abbreviations.
- **Confidence Scoring:** Provide confidence estimates and multiple ranked evidence sentences.
- **Improved Evidence Extraction:** Distinguish direct supporting evidence from sentences that merely mention related entities.
- **Multilingual Support:** Extend verification to additional language editions of Wikipedia.
- **Regression Testing:** Expand deterministic tests to cover unusual article structures and conflicting values.

## 🤝 Contributing

Contributions, suggestions, and bug reports are welcome.

If you would like to improve WikiFact Check:

1. Fork the repository.
2. Create a feature branch.
3. Make your changes and add appropriate tests.
4. Run the existing tests.
5. Submit a pull request describing your changes.

For significant changes, consider opening an issue first to discuss the proposed improvement.

## ⚖️ Disclaimer

WikiFact Check is an educational and experimental project designed to assist with reviewing structured Wikipedia information.

- **MATCH** means the implemented logic found agreement between the infobox and the article text. It does not independently establish that a claim is true.
- **POSSIBLE MISMATCH** identifies a potential inconsistency that requires human review.
- **NOT FOUND** means that the current implementation did not identify corresponding evidence. It does not prove that no supporting information exists.

The tool does not independently determine factual truth. Its results depend on article content, fact extraction, normalization, and matching logic. Users should review the evidence and consult authoritative sources before drawing conclusions.

Wikipedia content changes over time, so results may differ between runs.

## 👨‍💻 Author

**Saksham Kumar**

Student at Garden City University, Bengaluru, India.

Developed for **Wikimedia Open Source Day — Challenge 4**.

- **GitHub:** https://github.com/Saksham-M4/WikiFact-Check
- **Live Application:** https://wikifact-check-mfi8axlwerctayxu2yjyct.streamlit.app/

---

<p align="center">
  <strong>WikiFact Check</strong><br>
  ![WikiFact Check system flowchart](assets/wikifact-check-flowchart.png)
  Making structured knowledge easier to inspect, compare, and verify.
</p>
