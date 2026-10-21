🔎 WikiFact Check
Checks whether a structured fact in a Wikipedia infobox is supported by the article's own text, and shows the evidence sentence so a human can verify it.
Built for Wikimedia Open Source Day, Challenge 4.
Live app: https://wikifact-check-mfi8axlwerctayxu2yjyct.streamlit.app/
What it does
Takes an article title (typed in, or picked from the WikiWeak dataset).
Fetches the current English Wikipedia article through the MediaWiki API.
Extracts a chosen fact from the infobox.
Normalizes the fact and searches the article text for corresponding evidence.
Returns one of three results, with the evidence sentence and the article image.
Result	Meaning
🟢 MATCH	The infobox fact and the article text agree after normalization.
🟠 POSSIBLE MISMATCH	The article text mentions the topic but disagrees with the infobox (e.g. 1980 vs 1981).
⚪ NOT FOUND	No corresponding information was found in the article text.
The tool never declares a fact false. A mismatch means "needs human review."
Supported fact types
Fact type	Example	How it is compared
Birth Date	Narendra Modi → 17 September 1950	Dates are normalized, so 1950-09-17, 17 September 1950, September 17, 1950 and 17/09/1950 are treated as equal.
Founder	Google → Larry Page, Sergey Brin	Names are normalized and searched in the text, so "founded by Larry Page and Sergey Brin" matches.
Location	Organization or place	Infobox value vs. location stated in the text.
Country	Entity	Infobox value vs. country stated in the text.
Quick start
bash
git clone https://github.com/Saksham-M4/WikiFact-Check.git
cd WikiFact-Check
pip install -r requirements.txt
streamlit run app.py
Open http://localhost:8501. Start the app with streamlit run app.py, not python app.py.
Requires internet access to reach the Wikimedia API.
Try it
Article	Fact type	Expected
Narendra Modi	Birth Date	MATCH
Mahendra Singh Dhoni	Birth Date	MATCH
Google	Founder	MATCH
Tests
bash
python -m pytest test_factcheck.py
test_factcheck.py holds deterministic tests for the matching logic. live_test.py runs cases against live Wikipedia, so results can change as articles are edited.
Project structure
├── app.py                # Streamlit UI and workflow
├── fact_engine.py        # Extraction, normalization, matching, evidence
├── wikiweak_results.csv  # WikiWeak article records (title column: "name")
├── test_factcheck.py     # Deterministic tests
├── live_test.py          # Live Wikipedia tests
├── requirements.txt
├── DATASET_NOTE.txt
└── IMAGE_FEATURE.md
Dataset
The WikiWeak CSV is used to discover article titles. The app detects the title column automatically (name, title, article_title, article_name, article name). The fact check itself runs against the live Wikipedia article, not the dataset's contents.
Limitations
Evidence selection is heuristic. A sentence that contains the right names does not always state the intended relationship (for example, mentioning two people near "Google" does not prove they founded it).
Infobox templates vary between articles, so extraction can fail on unusual layouts.
Wikipedia changes over time, so a result can differ between runs.
Results depend on Wikimedia API availability.
No quantitative evaluation has been run yet.
Roadmap
Relationship-aware founder detection ("founded by", "co-founded").
Evaluation on a labeled set of articles, with precision and recall.
More fact types and alias handling.
Confidence scores and multiple ranked evidence sentences.
Multilingual Wikipedia support.
Disclaimer
This is an educational, experimental project. MATCH means the implemented logic found agreement between the infobox and the article text, not that the claim is true. POSSIBLE MISMATCH and NOT FOUND are prompts for human review.
Author
Saksham Kumar, Garden City University, Bengaluru.
