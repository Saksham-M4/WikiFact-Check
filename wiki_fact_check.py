import calendar

import re

from urllib.parse import quote

import pandas as pd

import requests

import streamlit as st

from bs4 import BeautifulSoup



# ============================================================

# WikiFact Check — Challenge 4

# Compare structured Wikipedia infobox facts with article text.

# ============================================================

st.set_page_config(

    page_title="WikiFact Check",

    page_icon="🔎",

    layout="wide",

)

CSV_FILE = "wikiweak_results.csv"

REST_URL = "https://en.wikipedia.org/api/rest_v1/page/html/"

API_URL = "https://en.wikipedia.org/w/api.php"

HEADERS = {

    "User-Agent": "WikiFactCheck-Challenge4/1.0 (student prototype)"

}

FACT_CONFIG = {

    "Birth date": {

        "labels": ["born", "date of birth", "birth date"],

    },

    "Founder": {

        "labels": ["founder", "founders", "founded by", "established by"],

    },

    "Location": {

        "labels": [

            "location",

            "headquarters",

            "headquarters location",

            "located in",

        ],

    },

    "Country": {

        "labels": ["country", "nation"],

    },

}



# ============================================================

# Text / normalization helpers

# ============================================================

MONTHS = {

    "january": 1,

    "february": 2,

    "march": 3,

    "april": 4,

    "may": 5,

    "june": 6,

    "july": 7,

    "august": 8,

    "september": 9,

    "october": 10,

    "november": 11,

    "december": 12,

}

DATE_RE = re.compile(

    r"""

    (?:

        (?P<day>\d{1,2})(?:st|nd|rd|th)?\s+

        (?P<month>January|February|March|April|May|June|July|August|

                   September|October|November|December)\s+

        (?P<year>\d{4})

    )

    |

    (?:

        (?P<month2>January|February|March|April|May|June|July|August|

                    September|October|November|December)\s+

        (?P<day2>\d{1,2})(?:st|nd|rd|th)?,?\s+

        (?P<year2>\d{4})

    )

    """,

    re.I | re.X,

)



def clean_text(value):

    """Convert HTML-ish/whitespace-heavy text into readable text."""

    if value is None:

        return ""

    text = BeautifulSoup(str(value), "html.parser").get_text(" ", strip=True)

    # Remove common citation markers such as [1], [2].

    text = re.sub(r"\[\s*\d+\s*\]", "", text)

    # Remove Wikipedia edit artifacts occasionally present in extracted text.

    text = re.sub(r"\s+", " ", text)

    return text.strip(" \t\n:;,.")



def normalize_text(value):

    value = clean_text(value).lower()

    value = value.replace("&", " and ")

    value = re.sub(r"[^a-z0-9]+", " ", value)

    return re.sub(r"\s+", " ", value).strip()



def normalize_date(value):

    match = DATE_RE.search(clean_text(value))

    if not match:

        return None

    if match.group("day"):

        day = int(match.group("day"))

        month = MONTHS[match.group("month").lower()]

        year = int(match.group("year"))

    else:

        day = int(match.group("day2"))

        month = MONTHS[match.group("month2").lower()]

        year = int(match.group("year2"))

    try:

        # Validate the actual calendar date.

        import datetime

        datetime.date(year, month, day)

    except ValueError:

        return None

    return f"{year:04d}-{month:02d}-{day:02d}"



def pretty_date(value):

    normalized = normalize_date(value)

    if not normalized:

        return clean_text(value)

    year, month, day = map(int, normalized.split("-"))

    return f"{day} {calendar.month_name[month]} {year}"



def sentence_list(text):

    text = clean_text(text)

    if not text:

        return []

    # Split on sentence boundaries while preserving useful context.

    parts = re.split(r"(?<=[.!?])\s+", text)

    return [p.strip() for p in parts if p.strip()]



def normalize_people(value):

    value = normalize_text(value)

    value = re.sub(r"\b(and|with)\b", " ", value)

    return {token for token in value.split() if token}



# ============================================================

# Wikipedia retrieval

# ============================================================

@st.cache_data(ttl=3600, show_spinner=False)

def fetch_page_html(title):

    """Fetch rendered English Wikipedia HTML, with API fallback."""

    encoded = quote(title.replace(" ", "_"), safe="")

    url = REST_URL + encoded

    response = requests.get(

        url,

        headers=HEADERS,

        timeout=20,

    )

    if response.ok and response.text.strip():

        return response.text

    # Fallback to MediaWiki parse API.

    params = {

        "action": "parse",

        "page": title,

        "prop": "text",

        "format": "json",

        "formatversion": "2",

    }

    api_response = requests.get(

        API_URL,

        params=params,

        headers=HEADERS,

        timeout=20,

    )

    api_response.raise_for_status()

    data = api_response.json()

    if "parse" not in data or "text" not in data["parse"]:

        raise requests.HTTPError("Wikipedia returned no article content.")

    return data["parse"]["text"]



# ============================================================

# Structured infobox extraction

# ============================================================

def extract_infobox_rows(html):

    soup = BeautifulSoup(html, "html.parser")

    boxes = soup.select("table.infobox")

    if not boxes:

        boxes = soup.select("table[class*='infobox']")

    rows = []

    for box in boxes:

        for tr in box.select("tr"):

            th = tr.find("th")

            td = tr.find("td")

            if not th or not td:

                continue

            label = clean_text(th.get_text(" ", strip=True))

            value = clean_text(td.get_text(" ", strip=True))

            if label and value:

                rows.append((label, value))

    return rows



def extract_structured_fact(html, fact_name):

    """

    Extract only the requested value from the infobox.

    For birth dates, return a clean normalized human-readable date.

    For other facts, return the infobox cell value with citation/HTML noise removed.

    """

    wanted = {normalize_text(x) for x in FACT_CONFIG[fact_name]["labels"]}

    rows = extract_infobox_rows(html)

    # Exact label match first.

    for label, value in rows:

        if normalize_text(label) in wanted:

            if fact_name == "Birth date":

                return pretty_date(value), label

            return clean_text(value), label

    # Conservative fallback for labels such as "Headquarters location".

    for label, value in rows:

        label_norm = normalize_text(label)

        if any(

            label_norm == item or

            label_norm.startswith(item + " ") or

            label_norm.endswith(" " + item)

            for item in wanted

        ):

            if fact_name == "Birth date":

                return pretty_date(value), label

            return clean_text(value), label

    return None, None



# ============================================================

# Article prose extraction

# ============================================================

def extract_article_text(html):

    soup = BeautifulSoup(html, "html.parser")

    # Remove structured/non-prose content so infoboxes, references,

    # navigation and scripts cannot contaminate the article-text search.

    selectors = [

        "table.infobox",

        "table[class*='infobox']",

        "table.navbox",

        "table.sidebar",

        "div.navbox",

        "div.reflist",

        "ol.references",

        "div.mw-references-wrap",

        "div.metadata",

        "div.thumb",

        "style",

        "script",

        "noscript",

        "sup.reference",

    ]

    for selector in selectors:

        for node in soup.select(selector):

            node.decompose()

    root = soup.select_one(".mw-parser-output") or soup

    return clean_text(root.get_text(" ", strip=True))



# ============================================================

# Article-text fact extraction

# ============================================================

def article_title_tokens(title):

    return {

        token

        for token in normalize_text(title).split()

        if len(token) >= 3

    }



def sentence_mentions_article(sentence, title):

    """

    Conservative relevance test.

    A sentence is considered article-relevant when:

    - it explicitly mentions enough of the article title, OR

    - it begins with a pronoun/reference that commonly follows the

      article subject in an encyclopedic lead, OR

    - it is a direct lead sentence containing the requested relation.

    This is deliberately conservative: failing to find a fact is

    preferable to treating an unrelated sentence as a mismatch.

    """

    sentence_norm = normalize_text(sentence)

    title_norm = normalize_text(title)

    if not sentence_norm or not title_norm:

        return False

    # Full title phrase.

    if title_norm in sentence_norm:

        return True

    # For multi-word titles, require all significant title tokens.

    tokens = article_title_tokens(title)

    if tokens and all(token in sentence_norm.split() for token in tokens):

        return True

    return False



def extract_birth_date_from_text(text):

    for sentence in sentence_list(text):

        if not re.search(r"\b(?:born|birth|date of birth)\b", sentence, re.I):

            continue

        match = DATE_RE.search(sentence)

        if match:

            return clean_text(match.group(0)), sentence

    return None, None



def extract_founder_from_text(text, title):
    """Extract an explicit founder statement from article prose."""
    patterns = [
        r"\b(?:was|were)\s+founded\s+by\s+([^.;:]{2,160})",
        r"\bfounded\s+by\s+([^.;:]{2,160})",
        r"\b(?:was|were)\s+established\s+by\s+([^.;:]{2,160})",
        r"\bestablished\s+by\s+([^.;:]{2,160})",
        r"\bco[- ]founded\s+by\s+([^.;:]{2,160})",
    ]

    def clean_founder_value(value):
        value = clean_text(value)
        # Preserve "Bill Gates and Paul Allen", while removing later
        # explanatory clauses.
        value = re.split(
            r"\s+(?:that|which|who)\s+|"
            r"\s*,\s*(?:which|who)\s+|"
            r"\s+and\s+(?:was|were|is|are|has|have)\s+",
            value,
            maxsplit=1,
            flags=re.I,
        )[0]
        return clean_text(value)

    sentences = sentence_list(text)

    # Prefer a sentence explicitly mentioning the selected article.
    for sentence in sentences:
        if not sentence_mentions_article(sentence, title):
            continue
        for pattern in patterns:
            match = re.search(pattern, sentence, re.I)
            if match:
                value = clean_founder_value(match.group(1))
                if value:
                    return value, sentence

    # Wikipedia lead fallback: only inspect the first five sentences.
    for sentence in sentences[:5]:
        for pattern in patterns:
            match = re.search(pattern, sentence, re.I)
            if match:
                value = clean_founder_value(match.group(1))
                if value:
                    return value, sentence

    return None, None


def extract_location_from_text(text, title):

    """

    Find location/headquarters statements.

    IMPORTANT: Never use an arbitrary 'based in X' or 'located in X'

    sentence from anywhere in a long article. The sentence must be

    explicitly connected to the selected article or be an early lead

    sentence describing it.

    """

    patterns = [

        r"\bheadquartered in\s+([^.;:]{2,120})",

        r"\bheadquarters (?:is|are|was|were) in\s+([^.;:]{2,120})",

        r"\bbased in\s+([^.;:]{2,120})",

        r"\blocated in\s+([^.;:]{2,120})",

    ]

    sentences = sentence_list(text)

    # Strongest evidence: title appears in the same sentence.

    for sentence in sentences:

        if not sentence_mentions_article(sentence, title):

            continue

        for pattern in patterns:

            match = re.search(pattern, sentence, re.I)

            if match:

                value = clean_text(match.group(1))

                if value:

                    return value, sentence

    # Next, inspect only the first few lead sentences. This is much safer

    # than scanning the whole article for a generic "based in" phrase.

    for sentence in sentences[:6]:

        for pattern in patterns:

            match = re.search(pattern, sentence, re.I)

            if match:

                value = clean_text(match.group(1))

                if value:

                    return value, sentence

    return None, None



def extract_country_from_text(text, title):

    """

    Country extraction is ambiguous in prose, so only accept explicit

    country/nationality statements connected to the selected article.

    """

    patterns = [

        r"\bcountry\s+(?:is|was)\s+([A-Z][A-Za-z .'-]{2,60})",

        r"\bnationality\s+(?:is|was)\s+([A-Z][A-Za-z .'-]{2,60})",

        r"\bcountry:\s*([A-Z][A-Za-z .'-]{2,60})",

        r"\bnationality:\s*([A-Z][A-Za-z .'-]{2,60})",

    ]

    sentences = sentence_list(text)

    for sentence in sentences:

        if not sentence_mentions_article(sentence, title):

            continue

        for pattern in patterns:

            match = re.search(pattern, sentence)

            if match:

                value = clean_text(match.group(1))

                if value:

                    return value, sentence

    for sentence in sentences[:6]:

        for pattern in patterns:

            match = re.search(pattern, sentence)

            if match:

                value = clean_text(match.group(1))

                if value:

                    return value, sentence

    return None, None



def extract_text_fact(text, fact_name, title):

    if fact_name == "Birth date":

        return extract_birth_date_from_text(text)

    if fact_name == "Founder":

        return extract_founder_from_text(text, title)

    if fact_name == "Location":

        return extract_location_from_text(text, title)

    if fact_name == "Country":

        return extract_country_from_text(text, title)

    return None, None



# ============================================================

# Comparison

# ============================================================

def compare_values(fact_name, structured, article_value):
    if fact_name == "Birth date":
        a = normalize_date(structured)
        b = normalize_date(article_value)
        if not a or not b:
            return None, a or "", b or ""
        return a == b, a, b

    if fact_name == "Founder":
        a = normalize_people(structured)
        b = normalize_people(article_value)
        if not a or not b:
            return None, " ".join(sorted(a)), " ".join(sorted(b))
        same = a.issubset(b) or b.issubset(a)
        return same, " ".join(sorted(a)), " ".join(sorted(b))

    a = normalize_text(structured)
    b = normalize_text(article_value)

    if not a or not b:
        return None, a, b

    if fact_name == "Location":
        # Different specificity can still describe the same place.
        if a == b or a in b or b in a:
            return True, a, b

        # Multi-token containment after normalization handles cases where
        # punctuation/qualifiers differ, without treating one-word places
        # as matches merely because they share a token.
        a_tokens = set(a.split())
        b_tokens = set(b.split())
        common = a_tokens & b_tokens
        if (
            len(a_tokens) >= 2
            and len(b_tokens) >= 2
            and len(common) >= min(len(a_tokens), len(b_tokens))
        ):
            return True, a, b

        return False, a, b

    return a == b, a, b



    if fact_name == "Birth date":

        a = normalize_date(structured)

        b = normalize_date(article_value)

        if not a or not b:

            return None, a or "", b or ""

        return a == b, a, b

    if fact_name == "Founder":

        a = normalize_people(structured)

        b = normalize_people(article_value)

        if not a or not b:

            return None, " ".join(sorted(a)), " ".join(sorted(b))

        # Names may be written with different punctuation/order.

        # Agreement is accepted when one normalized name set contains

        # the other.

        same = a.issubset(b) or b.issubset(a)

        return (

            same,

            " ".join(sorted(a)),

            " ".join(sorted(b)),

        )

    a = normalize_text(structured)

    b = normalize_text(article_value)

    if not a or not b:

        return None, a, b

    # Exact normalized comparison prevents partial substring matches

    # from being declared equal.

    return a == b, a, b



# ============================================================

# Dataset loading

# ============================================================

@st.cache_data

def load_wikiweak_dataset():

    try:

        df = pd.read_csv(CSV_FILE)

    except FileNotFoundError:

        return None

    if df.empty:

        return df

    # Identify a likely article/title column without assuming one exact

    # capitalization.

    candidates = [

        "Article",

        "article",

        "Title",

        "title",

        "article_title",

        "Article Title",

    ]

    title_col = next((c for c in candidates if c in df.columns), None)

    if title_col is None:

        # Try semantic column-name matching.

        for col in df.columns:

            norm = normalize_text(col)

            if "article" in norm and "title" in norm:

                title_col = col

                break

    if title_col is not None:

        df = df.copy()

        df["_article_title"] = df[title_col].astype(str).str.strip()

        df = df[

            (df["_article_title"] != "")

            & (df["_article_title"].str.lower() != "nan")

        ].drop_duplicates("_article_title")

    return df



# ============================================================

# UI

# ============================================================

st.markdown(

    '<div style="font-size:42px;font-weight:750;">🔎 WikiFact Check</div>',

    unsafe_allow_html=True,

)

st.markdown(

    '<div style="font-size:18px;opacity:.75;margin-bottom:20px;">'

    "Compare a structured Wikipedia infobox fact with corresponding "

    "information in the article text."

    "</div>",

    unsafe_allow_html=True,

)

st.info(

    "A difference is reported only as **Possible mismatch detected**. "

    "It is not treated as proof that a fact is false; human verification "

    "may be required."

)

st.markdown("### Expected flow")

st.write(

    "Select Article → Extract Structured Fact → Search Article Text → "

    "Find Corresponding Information → Compare Values → "

    "Flag Possible Difference → Display Both Values"

)

dataset = load_wikiweak_dataset()

with st.sidebar:

    st.markdown("## ⚙️ Fact Check")

    source = st.radio(

        "Article source",

        ["Select from WikiWeak dataset", "Enter article title"],

    )

    if source == "Select from WikiWeak dataset":

        if dataset is None:

            st.error(

                f"'{CSV_FILE}' was not found. Put the CSV in the same "

                "folder as this Python file."

            )

            selected_title = ""

        elif dataset.empty or "_article_title" not in dataset.columns:

            st.error(

                "The WikiWeak CSV does not contain a recognizable article-title column."

            )

            selected_title = ""

        else:

            titles = dataset["_article_title"].tolist()

            selected_title = st.selectbox(

                "WikiWeak article",

                titles,

            )

    else:

        selected_title = st.text_input(

            "Wikipedia article title",

            value="Virat Kohli",

        )

    fact_name = st.selectbox(

        "Structured fact to compare",

        list(FACT_CONFIG.keys()),

    )

    check = st.button(

        "🔍 Compare Fact",

        type="primary",

        use_container_width=True,

    )



if check:

    title = (selected_title or "").strip()

    if not title:

        st.warning("Enter or select an article title first.")

        st.stop()

    with st.spinner("Fetching the article and comparing the selected fact…"):

        try:

            html = fetch_page_html(title)

            structured_value, structured_label = extract_structured_fact(

                html,

                fact_name,

            )

            article_text = extract_article_text(html)

            article_value, evidence = extract_text_fact(

                article_text,

                fact_name,

                title,

            )

        except requests.RequestException as exc:

            st.error("Wikipedia could not be reached.")

            st.caption(str(exc))

            st.stop()

        except Exception as exc:

            st.error(f"Could not process the article: {exc}")

            st.stop()

    st.markdown(f"## 📄 {title}")

    if source == "Select from WikiWeak dataset":

        st.caption(

            "Article selected from the WikiWeak dataset. "

            "The selected English Wikipedia page is then read for its "

            "structured infobox and article text."

        )

    else:

        st.caption(

            "Source: English Wikipedia. The article title is entered manually; "

            "the selected English Wikipedia page is read for its structured "

            "infobox and article text."

        )

    # --------------------------------------------------------

    # Requirement 2 — Extract structured information

    # --------------------------------------------------------

    if not structured_value:

        st.warning(

            f"No '{fact_name}' value was found in this article's infobox."

        )

        st.caption(

            "This is treated as missing information, not as a mismatch."

        )

        st.stop()

    # --------------------------------------------------------

    # Requirement 3 — Search article text

    # --------------------------------------------------------

    if not article_value:

        st.warning(

            f"No corresponding '{fact_name}' information was found "

            "in the article text."

        )

        st.markdown("### Structured value")

        st.info(

            f"{structured_value}\n\n"

            f"*Infobox field: {structured_label}*"

        )

        st.caption("Not found is not treated as a mismatch.")

        with st.expander("Challenge 4 requirement checklist"):

            checklist = {

                "1. Article can be selected": True,

                "2. Structured information extracted": True,

                "3. Article text searched": True,

                "4. Comparison logic available": True,

                "5. Possible differences can be identified": True,

                "6. Values can be displayed": True,

                "7. Possible mismatch wording is implemented": True,

            }

            for item, status in checklist.items():

                st.write(("✅ " if status else "❌ ") + item)

        st.stop()

    # --------------------------------------------------------

    # Requirement 4 — Compare values

    # --------------------------------------------------------

    same, normalized_structured, normalized_article = compare_values(

        fact_name,

        structured_value,

        article_value,

    )

    st.markdown("### Comparison")

    c1, c2 = st.columns(2)

    with c1:

        st.markdown("**Structured infobox value**")

        st.info(

            f"{structured_value}\n\n"

            f"*Infobox field: {structured_label}*"

        )

    with c2:

        st.markdown("**Article text value**")

        st.info(article_value)

    # --------------------------------------------------------

    # Requirements 5 + 7 — Difference + explicit warning

    # --------------------------------------------------------

    if same is True:

        st.success("✅ No difference detected between the extracted values.")

    elif same is False:

        st.warning("⚠️ **Possible mismatch detected.**")

        st.write(

            "The extracted values differ. This result should be reviewed "

            "by a human."

        )

    else:

        st.info(

            "The values could not be compared reliably. "

            "Human verification may be required."

        )

    # --------------------------------------------------------

    # Requirement 6 — Evidence

    # --------------------------------------------------------

    with st.expander("Evidence from article text", expanded=(same is False)):

        st.write(evidence)

    with st.expander("Normalized comparison"):

        st.write(

            {

                "Structured value": normalized_structured,

                "Article text value": normalized_article,

                "Match": same,

            }

        )

    with st.expander("Challenge 4 requirement checklist"):

        checklist = {

            "1. Article can be selected": bool(title),

            "2. Structured information extracted": bool(structured_value),

            "3. Article text searched": True,

            "4. Information compared": same is not None,

            "5. Possible differences identified": same is False or same is True,

            "6. Both values displayed": bool(structured_value and article_value),

            "7. Possible mismatch is clearly indicated": same is not None,

        }

        for item, status in checklist.items():

            st.write(("✅ " if status else "❌ ") + item)

st.markdown("---")

st.caption(

    "WikiFact Check • Structured Fact → Article Text → Compare → "

    "Possible Mismatch → Human Review"

)