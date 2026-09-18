# WikiFact Check — Challenge 4

This project implements the minimum Challenge 4 flow:

1. Select an article.
2. Extract a structured fact from its Wikipedia infobox.
3. Search the article text for the corresponding information.
4. Compare the two extracted values.
5. Identify a possible difference.
6. Display both values.
7. Clearly report **Possible mismatch detected** when they differ.

## Run locally

```bash
pip install -r requirements.txt
streamlit run wiki_fact_check.py
```

## Demo

Choose **Enter article title**, type an article title such as:

`Albert Einstein`

Select:

`Birth date`

Then click **Compare Fact**.

## Important source note

The original WikiWeak CSV contains the article list and scoring fields, but it does
not contain the full infobox values and article prose needed for Challenge 4.
Therefore this app uses the selected English Wikipedia article to obtain those two
pieces of information. This is deliberately stated in the UI rather than pretending
the summary CSV contains data that it does not.

The official Wikimedia Structured Contents dataset does contain parsed `infoboxes`
and `sections`, which are the appropriate fields for a dataset-native implementation.
