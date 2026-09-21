# 🔎 WikiFact Check

### Evidence-First Wikipedia Fact Consistency Checker

WikiFact Check is a Streamlit-based application that checks whether a structured fact from a Wikipedia article's **infobox** is supported by the corresponding **article text**.

The system is designed around an evidence-first workflow:

```text
WikiWeak Dataset
      ↓
Article Title Resolution
      ↓
Wikipedia Article Retrieval
      ↓
Infobox Fact Extraction
      ↓
Article Text Analysis
      ↓
Fact Normalization & Matching
      ↓
Match / Possible Mismatch / Not Found
      ↓
Exact Evidence Sentence + Wikipedia Article Image
```

The goal is not to judge whether an article is "good" or "bad". Instead, the application answers a focused question:

> **Does the information in the structured Wikipedia infobox agree with the information stated in the article text?**

---

# 🎯 Problem Statement

Wikipedia presents information in multiple forms.

For example, an article may contain:

- A structured infobox with a birth date
- A founder field
- A location field
- A country field
- The same information expressed naturally inside paragraphs

A simple string search can produce incorrect results when the same fact is written in a different form.

For example:

```text
Infobox:
Larry Page; Sergey Brin

Article:
Google was founded by Larry Page and Sergey Brin.
```

A basic exact-string search may fail because the wording and punctuation are different.

WikiFact Check therefore separates the problem into:

1. **Fact extraction**
2. **Normalization**
3. **Relevant article-text matching**
4. **Evidence extraction**
5. **Three-state classification**

---

# ✨ Key Features

## 1. WikiWeak Dataset Integration

The application connects to the WikiWeak article dataset and automatically detects the article-title column.

Supported title-column names include:

```text
name
title
article_title
article_name
article name
```

The current connected dataset uses:

```text
name
```

The application also displays the detected title column and the number of connected article records in the interface.

---

## 2. Wikipedia Article Retrieval

After an article title is supplied, the application retrieves the corresponding English Wikipedia article.

It obtains:

- Article title
- Infobox information
- Article text
- Wikipedia article URL
- Main article image when available

---

## 3. Multiple Fact Types

The current fact-checking workflow supports:

| Fact Type | Example |
|---|---|
| **Birth Date** | Narendra Modi → 17 September 1950 |
| **Founder** | Google → Larry Page, Sergey Brin |
| **Location** | Organization/place → stated location |
| **Country** | Entity → stated country |

The architecture is designed so additional fact types can be added later.

---

# 🧠 Fact-Matching Approach

The application does not depend only on literal string equality.

## Birth Date

Different date representations can refer to the same date:

```text
1950-09-17
17 September 1950
September 17, 1950
17/09/1950
```

These representations can be normalized before comparison.

Therefore:

```text
Infobox: 1950-09-17

Article:
Narendra Modi (born 17 September 1950) ...
```

can be classified as:

```text
MATCH
```

---

## Founder

Founder information may appear in different natural-language forms.

For example:

```text
Infobox:
Larry Page, Sergey Brin

Article:
Google was founded by Larry Page and Sergey Brin.
```

The system normalizes the names and searches the article text for supporting information instead of requiring an identical raw string.

---

# 🏷️ Three Result States

The application deliberately uses **only three final outcomes**.

## 🟢 MATCH

The structured fact and article text represent the same information and supporting evidence is available.

Example:

```text
MATCH — both information are the same.
```

---

## 🟠 POSSIBLE MISMATCH

The article contains relevant information, but it does not agree with the structured fact after normalization.

Example:

```text
Infobox: 1980
Article: 1981
```

The application reports:

```text
POSSIBLE MISMATCH
```

This wording avoids claiming more certainty than the available article evidence supports.

---

## ⚪ NOT FOUND

The requested corresponding information cannot be found in the available article text.

Example:

```text
Fact type: Country
Article: [no corresponding country information]
```

The application reports:

```text
NOT FOUND
```

---

# 📖 Evidence-First Output

A key feature of WikiFact Check is that the result is not presented as a bare label.

When supporting or conflicting evidence is found, the application displays the:

> **Exact evidence sentence from the Wikipedia article**

The interface therefore provides:

```text
Result
   ↓
Infobox information
   ↓
Exact evidence sentence
   ↓
Wikipedia article
```

This makes the result easier to inspect and demonstrate.

---

# 🖼️ Wikipedia Article Image

When Wikipedia provides a main article image, the application automatically displays it.

For example:

```text
Narendra Modi
      ↓
Wikipedia image
      ↓
Infobox birth information
      ↓
Fact-check result
      ↓
Evidence sentence
```

If an article does not have a suitable image, the fact-checking workflow can still operate normally.

---

# 🗂️ Dataset Workflow

The application uses the WikiWeak dataset primarily for **article-title discovery and dataset integration**.

The workflow is:

```text
WikiWeak CSV
     ↓
Detect title column
     ↓
Load article titles
     ↓
Select / enter article
     ↓
Retrieve current Wikipedia article
     ↓
Extract structured fact
     ↓
Compare against article text
```

The application does not assume that the dataset itself contains the final answer to every fact-check.

Instead, it uses the article title to locate the corresponding Wikipedia article and perform the consistency check.

---

# 🏗️ System Architecture

```text
                    WikiWeak Dataset
                           │
                           ▼
                 Article Title Loader
                           │
                           ▼
                Title Column Detection
                           │
                           ▼
                 Wikipedia API Client
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
           Infobox     Article Text   Page Image
              │            │            │
              ▼            ▼            │
        Fact Extraction  Evidence      │
              │            │            │
              └──────┬─────┘            │
                     ▼                  │
              Normalization            │
                     │                  │
                     ▼                  │
               Fact Matching            │
                     │                  │
          ┌──────────┼──────────┐       │
          ▼          ▼          ▼       │
       MATCH    MISMATCH    NOT FOUND   │
          │          │          │       │
          └──────────┼──────────┘       │
                     ▼                  ▼
              Evidence Sentence    Article Image
                     │                  │
                     └────────┬─────────┘
                              ▼
                       Streamlit UI
```

---

# 🛠️ Technology Stack

### Programming Language

- Python

### User Interface

- Streamlit

### Data Processing

- Pandas

### Wikipedia Integration

- Wikimedia MediaWiki API

### Data Source

- WikiWeak dataset
- English Wikipedia

### Development

- Visual Studio Code
- macOS / Linux / Windows-compatible Python environment

---

# 📁 Project Structure

```text
WikiFactCheck/
│
├── app.py
├── fact_engine.py
├── wikiweak_results.csv
├── requirements.txt
├── README.md
├── test_factcheck.py
├── live_test.py
├── IMAGE_FEATURE.md
└── DATASET_NOTE.txt
```

### `app.py`

Contains the Streamlit user interface and application workflow.

### `fact_engine.py`

Contains the fact extraction, normalization, matching, and evidence logic.

### `wikiweak_results.csv`

Contains the WikiWeak article records used by the application.

### `test_factcheck.py`

Contains deterministic tests for the fact-checking logic.

### `live_test.py`

Contains live Wikipedia-oriented test cases.

### `requirements.txt`

Contains the Python dependencies required to run the application.

---

# 🚀 How to Run

## 1. Extract the Project

Extract the project ZIP into your Downloads folder or another working directory.

---

## 2. Open Terminal

Move into the project directory:

```bash
cd ~/Downloads/WikiFactCheck_TeacherReady_v2
```

---

## 3. Install Dependencies

```bash
python3 -m pip install -r requirements.txt
```

---

## 4. Start Streamlit

Use:

```bash
python3 -m streamlit run app.py
```

Do **not** start the Streamlit application using:

```bash
python3 app.py
```

---

## 5. Open the Application

Streamlit normally provides:

```text
http://localhost:8501
```

Open that address in a browser.

---

# 🧪 Recommended Demonstration Tests

The following tests cover the major requirements of the project.

## Test 1 — Birth Date Match

```text
Article: Narendra Modi
Fact Type: Birth Date
```

Expected:

```text
MATCH
```

The application should show:

- Narendra Modi article image
- Infobox birth date
- Evidence sentence
- Wikipedia article link

---

## Test 2 — Founder Match

```text
Article: Google
Fact Type: Founder
```

Expected:

```text
MATCH
```

The application should show:

- Google article image
- Founder information
- Supporting evidence sentence
- Wikipedia article link

---

## Test 3 — Another Article

Example:

```text
Article: Mahendra Singh Dhoni
Fact Type: Birth Date
```

Expected:

```text
MATCH
```

This demonstrates that the application is not hard-coded only for Narendra Modi.

---

## Test 4 — Possible Mismatch

Use an article/fact combination where the structured information and article evidence disagree.

Expected:

```text
POSSIBLE MISMATCH
```

The application should display the relevant evidence when available.

---

## Test 5 — Not Found

Choose a fact type for which the corresponding information is unavailable in the article.

Expected:

```text
NOT FOUND
```

This demonstrates that the system distinguishes missing information from an actual mismatch.

---

# 👩‍🏫 Teacher Requirement Coverage

The implementation is designed to address the following requirements:

| Requirement | Implementation |
|---|---|
| Correct WikiWeak dataset | WikiWeak CSV integration |
| Article title column | Automatic column detection |
| Narendra Modi birth date | Normalized date comparison |
| Natural-language founder matching | Normalized entity/name matching |
| Exactly three outcomes | Match / Possible Mismatch / Not Found |
| Evidence display | Exact Wikipedia evidence sentence |
| Multiple articles | Article title input + dataset selection |
| Multiple fact types | Birth Date / Founder / Location / Country |
| Article image | Wikipedia PageImages retrieval |
| Interactive interface | Streamlit dashboard |

---

# 🔍 Example Workflow

Suppose the user selects:

```text
Article:
Narendra Modi

Fact:
Birth Date
```

The application performs:

```text
1. Resolve article title
        ↓
2. Retrieve Wikipedia article
        ↓
3. Extract infobox birth date
        ↓
4. Extract article text
        ↓
5. Normalize date representations
        ↓
6. Search for supporting evidence
        ↓
7. Compare information
        ↓
8. Return MATCH
        ↓
9. Display evidence sentence
        ↓
10. Display article image
```

---

# 🔐 Design Principles

## Evidence Before Conclusion

The application attempts to provide supporting article evidence rather than displaying only a result label.

## Normalization Before Comparison

Equivalent representations should be normalized before deciding whether information differs.

## Three-State Classification

The system separates:

```text
Same
Different
Unavailable
```

into:

```text
MATCH
POSSIBLE MISMATCH
NOT FOUND
```

## Explainability

The user can inspect:

- The structured infobox information
- The article evidence
- The Wikipedia source
- The article image

---

# ⚠️ Limitations

WikiFact Check is an experimental fact-consistency checker and should not be treated as an authoritative fact-verification system.

### 1. Wikipedia Can Change

Wikipedia content may be edited after a result is produced.

### 2. Natural Language Is Complex

A sentence can contain information that requires context beyond simple matching.

### 3. Infoboxes Are Structured Differently

Different Wikipedia articles may use different infobox templates and field formats.

### 4. Evidence Selection

A sentence containing the relevant names or values does not always establish the exact semantic relationship intended by the fact type. Evidence matching is therefore an area for continued improvement.

### 5. API Availability

The application depends on access to Wikimedia services for live article retrieval and images.

---

# 🔮 Future Improvements

Possible future improvements include:

- Stronger semantic sentence matching
- Relationship-aware founder detection
- More fact types
- Better handling of aliases and alternate names
- Multilingual Wikipedia support
- Confidence indicators
- Evidence ranking
- Multiple evidence sentences
- Historical Wikipedia revision comparison
- Automated evaluation across a larger test set
- Improved entity recognition
- More robust infobox template handling

---

# 📊 Evaluation Strategy

A meaningful evaluation should test different:

### Articles

```text
People
Companies
Organizations
Places
Historical subjects
```

### Fact Types

```text
Birth Date
Founder
Location
Country
```

### Outcomes

```text
MATCH
POSSIBLE MISMATCH
NOT FOUND
```

The evaluation should include both straightforward and naturally worded examples.

---

# 🎓 Project Demonstration Flow

For a short classroom demonstration:

### Step 1
Show the WikiWeak connection:

```text
WikiWeak connected
Article-title column: name
```

### Step 2
Search:

```text
Narendra Modi
```

Select:

```text
Birth Date
```

Show:

```text
MATCH
```

and the evidence sentence.

### Step 3
Search:

```text
Google
```

Select:

```text
Founder
```

Show:

```text
MATCH
```

and the article evidence.

### Step 4
Explain the three outcomes:

```text
MATCH
POSSIBLE MISMATCH
NOT FOUND
```

### Step 5
Explain the key technical idea:

> **“We do not compare raw strings only. We normalize the structured fact and look for corresponding evidence in the article text.”**

---

# 📌 Project Status

**Completed Prototype**

Current implementation includes:

- WikiWeak dataset integration
- Automatic article-title column detection
- Wikipedia article retrieval
- Infobox fact extraction
- Fact normalization
- Article-text comparison
- Three-state result classification
- Exact evidence sentence display
- Wikipedia article image display
- Multiple fact types
- Streamlit interface
- Test utilities
- Local execution support
- Project documentation

---

# 👤 Author

**Saksham Kumar**

Garden City University, Bengaluru

Areas of interest:

- Python
- Artificial Intelligence
- Data Science
- Open Source
- Wikimedia technologies
- Software Development

---

# 📜 Disclaimer

WikiFact Check is an educational and experimental software project.

A `MATCH` result means that the implemented comparison logic found supporting agreement between the selected structured fact and available article evidence. It does not independently establish the ultimate truth of a claim.

A `POSSIBLE MISMATCH` indicates that the available structured information and article evidence did not agree under the implemented matching rules.

A `NOT FOUND` result means the requested corresponding information was not found in the available article text.

---

# ⭐ Summary

WikiFact Check combines:

```text
WikiWeak Dataset
       +
Wikipedia Structured Data
       +
Natural-Language Article Text
       +
Fact Normalization
       +
Evidence Matching
       +
Three-State Classification
       +
Exact Evidence Display
       +
Article Images
       +
Interactive Streamlit UI
```

### Core Idea

```text
Retrieve
   ↓
Extract
   ↓
Normalize
   ↓
Compare
   ↓
Classify
   ↓
Show Evidence
```

**WikiFact Check — making Wikipedia fact consistency easier to inspect, understand, and demonstrate.**
