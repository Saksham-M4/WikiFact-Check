# 🔎 WikiFact Check
### Evidence-Based Verification of Wikipedia Infobox Facts

**WikiFact Check** is an experimental fact-verification tool that checks whether structured facts in Wikipedia infoboxes are supported by the corresponding article text. It extracts a selected infobox fact, searches the article for supporting or potentially conflicting evidence, and presents the relevant sentence to help users verify the result.

Built for **Wikimedia Open Source Day — Challenge 4**.

**Live Application:** https://wikifact-check-mfi8axlwerctayxu2yjyct.streamlit.app/

**Author:** Saksham Kumar  
**Institution:** Garden City University, Bengaluru, India

---

## ✨ Key Features

- **Live Wikipedia Integration:** Retrieves the latest available English Wikipedia article through the MediaWiki API.
- **Infobox Fact Extraction:** Identifies supported structured facts from an article's infobox.
- **Text-Based Evidence Search:** Searches the article text for sentences relevant to the selected fact.
- **Normalization and Matching:** Handles common variations in date formats and names before comparing facts.
- **Evidence-Based Results:** Displays a relevant evidence sentence alongside the article image, when available.
- **Human-in-the-Loop Verification:** Flags potential inconsistencies without automatically declaring claims false.
- **WikiWeak Dataset Integration:** Allows users to discover and select article titles from the WikiWeak dataset.

## ⚙️ How It Works

1. **Select an article:** Enter a Wikipedia article title or choose an article from the WikiWeak dataset.
2. **Retrieve the article:** Fetch the current English Wikipedia page through the MediaWiki API.
3. **Extract the fact:** Identify a supported fact from the article's infobox.
4. **Search for evidence:** Examine the article text for corresponding information.
5. **Normalize and compare:** Standardize supported values and compare the infobox fact with the text evidence.
6. **Review the result:** Display the classification, relevant evidence sentence, and article image when available.

## 🚦 Result Classification

| Result | Meaning |
|---|---|
| 🟢 **MATCH** | The implemented matching logic found agreement between the infobox fact and the article text after normalization. |
| 🟠 **POSSIBLE MISMATCH** | The article contains potentially conflicting information that requires human review. |
| ⚪ **NOT FOUND** | The system could not identify corresponding evidence in the article text. |

**Important:** These results describe what the implemented system found. They do not establish whether a claim is objectively true or false.

## 🧩 Supported Fact Types

| Fact Type | Example | Comparison Method |
|---|---|---|
| Birth Date | Narendra Modi — 17 September 1950 | Normalizes supported date formats before comparison. |
| Founder | Google — Larry Page and Sergey Brin | Normalizes names and searches the text for corresponding mentions. |
| Location | An organization or place | Compares the infobox value with relevant location information in the article. |
| Country | An entity associated with a country | Compares the infobox value with country information stated in the article. |

### Date Normalization Example

The following representations of the same date are treated as equivalent when recognized by the implementation:

- `1950-09-17`
- `17 September 1950`
- `September 17, 1950`
- `17/09/1950`

Name normalization similarly helps identify equivalent representations of supported names.

## 🚀 Getting Started

### Prerequisites

- Python 3
- Git
- An active internet connection to access the Wikimedia API

### Installation

Clone the repository:

```bash
git clone https://github.com/Saksham-M4/WikiFact-Check.git
```

Navigate to the project directory:

```bash
cd WikiFact-Check
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Launch the Streamlit application:

```bash
streamlit run app.py
```

Open the local application in your browser:

http://localhost:8501

**Note:** Start the application with `streamlit run app.py`, not `python app.py`.

## 🧪 Testing

The project includes automated tests for the fact-matching logic and a separate set of tests against live Wikipedia articles.

### Run deterministic tests

```bash
python -m pytest test_factcheck.py
```

These tests validate the implemented matching logic using predefined test cases.

### Run live Wikipedia tests

```bash
python live_test.py
```

Live tests depend on Wikipedia's current article content and API availability. Their results may change when articles are edited.

### Example Test Cases

| Article | Fact Type | Expected Result |
|---|---|---|
| Narendra Modi | Birth Date | MATCH |
| Mahendra Singh Dhoni | Birth Date | MATCH |
| Google | Founder | MATCH |

These are intended test cases; actual results depend on the current article content and the implementation's extraction and matching behavior.

## 🗂️ Project Structure

```text
WikiFact-Check/
├── app.py                 # Streamlit interface and application workflow
├── fact_engine.py         # Fact extraction, normalization, matching and evidence
├── wikiweak_results.csv   # WikiWeak article records
├── test_factcheck.py      # Deterministic matching tests
├── live_test.py           # Tests against live Wikipedia articles
├── requirements.txt       # Python dependencies
├── DATASET_NOTE.txt       # Dataset documentation
└── IMAGE_FEATURE.md       # Article image feature documentation
```

## 📚 Dataset and Data Sources

### WikiWeak Dataset

The WikiWeak CSV file is used to discover and select article titles. The application automatically detects a supported title column, including:

- `name`
- `title`
- `article_title`
- `article_name`
- `article name`

### Wikipedia and MediaWiki API

The actual fact-checking process uses the retrieved Wikipedia article rather than relying on the dataset's contents as verification evidence.

This separation allows the application to examine the article's currently available text while using WikiWeak as a source of candidate article titles.

## ⚠️ Limitations

WikiFact Check is an experimental, heuristic-based system. Its results should be interpreted with care.

- **Relationship ambiguity:** Finding two names in the same sentence does not necessarily establish a relationship such as co-founding a company.
- **Infobox variation:** Different Wikipedia templates and page structures may prevent reliable extraction of certain facts.
- **Evidence selection:** The selected sentence may mention a relevant entity without directly supporting the intended claim.
- **Normalization constraints:** Unusual date formats, aliases, abbreviations, and alternative name spellings may not be handled correctly.
- **Live data dependency:** Article edits and changes in API availability can affect results between runs.
- **Evaluation gap:** No quantitative evaluation has been conducted yet to establish precision, recall, or overall verification accuracy.

## 🛣️ Future Improvements

Planned enhancements include:

1. **Relationship-Aware Verification:** Improve founder detection by identifying relationships expressed through phrases such as “founded by” and “co-founded by.”
2. **Quantitative Evaluation:** Evaluate the system against a labeled dataset using precision, recall, and other appropriate metrics.
3. **Expanded Fact Coverage:** Support additional infobox fields and more complex fact types.
4. **Alias and Entity Resolution:** Improve handling of alternative names, abbreviations, and entity references.
5. **Confidence Scoring:** Introduce confidence estimates and multiple ranked evidence sentences.
6. **Multilingual Support:** Extend the system to additional language editions of Wikipedia.
7. **Improved Evidence Extraction:** Distinguish direct evidence from sentences that merely mention related entities.

## 🔐 Responsible Use and Disclaimer

WikiFact Check is an educational and experimental project intended to assist human review of Wikipedia content.

- A **MATCH** indicates that the implemented logic identified agreement between an infobox value and the article text. It does not independently prove that the claim is true.
- A **POSSIBLE MISMATCH** indicates a potential inconsistency that should be investigated.
- A **NOT FOUND** result means that corresponding evidence was not identified by the current implementation; it does not prove that the information is absent from all relevant sources.

The tool does not independently determine factual truth. Its output depends on the quality of the extracted data, the available article text, and the implemented matching rules. Users should consult the cited article context and authoritative sources before drawing conclusions.

## 👨‍💻 About the Author

**Saksham Kumar**  
Student at Garden City University, Bengaluru, India

WikiFact Check was developed as part of Wikimedia Open Source Day, Challenge 4, to explore how structured knowledge can be compared with article text through transparent, evidence-oriented verification.

---

**Project Repository:** https://github.com/Saksham-M4/WikiFact-Check/

**Live Demo:** https://wikifact-check-mfi8axlwerctayxu2yjyct.streamlit.app/
