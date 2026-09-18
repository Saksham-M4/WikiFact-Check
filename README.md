# 🔎 WikiFact Check

## Wikimedia Open Source Day — Challenge 4

> Compare structured Wikipedia facts with corresponding information in article text and flag possible mismatches for human verification.

---

## 📌 Overview

**WikiFact Check** is an interactive web application developed for **Wikimedia Open Source Day — Challenge 4: WikiFact Check**.

Wikipedia articles can contain information in two forms:

- **Structured information** — available through the article infobox
- **Unstructured information** — written in the main article text

These two representations may sometimes contain different values.

WikiFact Check extracts a selected fact from the structured infobox, searches the article text for corresponding information, compares the extracted values, and reports a **possible mismatch** when a difference is detected.

> ⚠️ A detected difference is **not proof that a fact is false**. The result is intended for human verification.

---

## 🎯 Challenge Objective

The project implements the Challenge 4 workflow:

1. Select an article
2. Extract structured information
3. Search the article text
4. Find corresponding information
5. Compare the values
6. Identify possible differences
7. Display both values
8. Clearly indicate a possible mismatch

---

## 🔄 Application Workflow

```text
Select Article
      ↓
Fetch Wikipedia Page
      ↓
Extract Structured Infobox Fact
      ↓
Search Article Text
      ↓
Find Corresponding Information
      ↓
Normalize Values
      ↓
Compare Values
      ↓
┌─────────────────────────┐
│ Same Information?       │
└────────────┬────────────┘
       ┌─────┴─────┐
       ↓           ↓
      YES          NO
       ↓           ↓
No Difference   Possible
Detected        Mismatch
                   ↓
             Human Verification
             ✨ Key Features
📄 Article Selection
Users can select an article from the WikiWeak dataset article list or enter a Wikipedia article title manually.
🧩 Structured Fact Extraction
The application extracts selected information from the Wikipedia infobox.
Supported fact types include:

Birth date
Founder
Location
Country
🔍 Article Text Search
The application searches the main article prose for corresponding information.
Structured and non-prose elements such as infoboxes, navigation boxes, references, scripts, and metadata are removed before searching.

⚖️ Value Comparison
Extracted values are normalized before comparison.
The application handles:

Date normalization
Text normalization
Founder-name normalization
Location differences in specificity
⚠️ Possible Mismatch Detection
When extracted values differ, the application displays:
⚠️ Possible mismatch detected.
The application does not automatically declare either value false.
📝 Evidence Display
The article-text evidence used for the comparison is displayed to help a human review the result.
🔢 Normalized Comparison
The application can display the normalized values used by its comparison logic.
✅ Requirement Checklist
The interface includes a Challenge 4 requirement checklist showing the implemented workflow.
🧪 Example
Birth Date Comparison
Example:
Structured infobox:
15 May 1980

Article text:
16 May 1980
The application reports:
⚠️ Possible mismatch detected.
Both values and the supporting article-text evidence are displayed for review.
🛡️ Interpretation of Results
WikiFact Check is a consistency-checking tool, not an automatic truth detector.
A difference between structured information and article text does not necessarily mean that one value is incorrect.

Possible reasons include:

Different levels of specificity
Different formatting
Different wording
Missing information
Historical changes
Extraction limitations
Therefore, the application deliberately uses:
Possible mismatch detected
instead of:
This fact is false
Human verification may be required.
🗂️ Dataset Usage
The project uses the WikiWeak dataset supplied for the Wikimedia Open Source Day activity to provide and select article titles.
For the selected article, the application reads the corresponding English Wikipedia page to obtain:

Structured infobox information
Main article text
The dataset is therefore part of the article-selection workflow, while the selected Wikipedia page provides the two representations being compared.
🧰 Technologies Used
Technology	Purpose
Python	Core application logic
Streamlit	Interactive web interface
Pandas	Dataset loading and processing
Requests	Wikipedia data retrieval
BeautifulSoup	HTML parsing and text extraction
Regular Expressions	Fact and pattern extraction
Wikipedia REST API	Article HTML retrieval
MediaWiki API	Fallback article retrieval
CSV	WikiWeak dataset article selection
🏗️ Project Structure
WikiFact-Check/
│
├── wiki_fact_check.py
├── wikiweak_results.csv
├── requirements.txt
└── README.md
wiki_fact_check.py
Contains the main Streamlit application, including:
Wikipedia retrieval
Infobox extraction
Article-text extraction
Fact extraction
Normalization
Comparison logic
Possible mismatch detection
User interface
wikiweak_results.csv
Contains the WikiWeak dataset used for article selection.
requirements.txt
Contains the Python dependencies required to run the application.
⚙️ Installation
1. Clone the repository
git clone https://github.com/YOUR-USERNAME/WikiFact-Check.git
2. Enter the project directory
cd WikiFact-Check
3. Create a virtual environment
python3 -m venv .venv
4. Activate the virtual environment
macOS / Linux
source .venv/bin/activate
Windows
.venv\Scripts\activate
5. Install dependencies
pip install -r requirements.txt
▶️ Run the Application
Run:
streamlit run wiki_fact_check.py
The application will open in the browser.
🧪 Testing
The application should be tested with different articles and fact types.
Matching Information
When both representations describe the same information:
✅ No difference detected between the extracted values.
Possible Difference
When the extracted values differ:
⚠️ Possible mismatch detected.
Missing Information
If the requested information is unavailable in one representation, it is not automatically treated as a mismatch.
Missing information ≠ Confirmed mismatch
📊 Challenge 4 Requirement Mapping
Requirement	Implementation
1. Allow user to select an article	Article selector / title input
2. Extract relevant structured information	Wikipedia infobox extraction
3. Search article text	Main article prose extraction
4. Compare information	Normalization and comparison logic
5. Identify possible differences	Difference detection
6. Display both values	Side-by-side comparison
7. Clearly indicate a possible mismatch	"Possible mismatch detected"
🔬 Comparison Logic
Birth Date
Dates are converted into a common normalized format before comparison.
Example:

15 May 1980
becomes:
1980-05-15
This allows different date formatting to be compared consistently.
Founder
Founder names are normalized to reduce differences caused by punctuation, conjunctions, or ordering.
For example:

Bill Gates and Paul Allen
can be compared with equivalent founder information represented differently.
Location
Location information can appear at different levels of specificity.
For example:

Microsoft campus, Redmond, Washington, U.S.
and:
Redmond, Washington
may describe the same location.
The application therefore accounts for meaningful location specificity rather than relying only on exact string equality.

⚠️ Limitations
WikiFact Check is an educational prototype.
Wikipedia articles can vary significantly in:

Infobox structure
Wording
Available information
Sentence construction
Fact representation
Therefore, the application may not extract every possible fact from every article.
The tool reports possible mismatches rather than automatically determining which value is correct.

🚀 Future Improvements
Possible future enhancements include:
NLP-based information extraction
Named Entity Recognition (NER)
Advanced date normalization
Semantic similarity matching
Confidence scores
AI-assisted comparison
Highlighting mismatched text
Multiple fact comparison
Automated comparison reports
Support for additional Wikipedia infobox templates
Improved extraction accuracy
🎓 Learning Outcomes
This project demonstrates practical application of:
Structured data processing
Web data retrieval
HTML parsing
Text processing
Regular expressions
Data normalization
Information comparison
Interactive web application development
Human-in-the-loop verification
🌐 Project Information
Event: Wikimedia Open Source Day
Challenge: Challenge 4 — WikiFact Check

Difficulty: Advanced

Project Type: Interactive Web Application

Dataset: Wikimedia Structured Wikipedia Dataset / WikiWeak article dataset

👨‍💻 Contribution
Saksham
Responsibilities included:
Problem analysis
Solution design
Python implementation
Wikipedia data extraction
Infobox processing
Article-text processing
Comparison logic
Streamlit interface
Testing and debugging
Prototype preparation
🔗 Project Links
GitHub Repository
https://github.com/YOUR-USERNAME/WikiFact-Check
Live Demo
YOUR-STREAMLIT-LIVE-DEMO-LINK
📜 Disclaimer
WikiFact Check is an educational prototype developed for Wikimedia Open Source Day.
It is designed to identify possible inconsistencies between structured Wikipedia information and article prose.

A detected difference should be reviewed by a human and should not automatically be interpreted as proof that either value is incorrect.

⭐ Project Summary
Structured Wikipedia Fact
          ↓
      Article Text
          ↓
       Extraction
          ↓
      Normalization
          ↓
       Comparison
          ↓
 ┌────────┴─────────┐
 ↓                  ↓
Match          Difference
 ↓                  ↓
No Difference   Possible
Detected        Mismatch
                    ↓
              Human Review
🔎 WikiFact Check
Compare • Detect • Review
