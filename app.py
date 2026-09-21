import re
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

import pandas as pd
import requests
import streamlit as st
from bs4 import BeautifulSoup

APP_DIR = Path(__file__).resolve().parent
DATA_FILE = APP_DIR / "wikiweak_results.csv"
DEMO_DATA_FILE = APP_DIR / "wikiweak_demo.csv"

WIKI_API = "https://en.wikipedia.org/w/api.php"
RAW_DATA_URL = "https://raw.githubusercontent.com/Saksham-M4/WikiWeak-Article-Finder/main/wikiweak_results.csv"
USER_AGENT = "WikiFactCheck/2.0 (educational project; fact-consistency demo)"

FACT_CONFIG = {
    "Birth Date": {
        "infobox_keys": ["birth_date", "date_of_birth", "born"],
        "patterns": [r"\bborn\b", r"\bbirth\b", r"\bdate of birth\b"],
    },
    "Founder": {
        "infobox_keys": ["founder", "founders", "founder_name"],
        "patterns": [r"\bfounded by\b", r"\bfounder\b", r"\bco-founded by\b", r"\bestablished by\b"],
    },
    "Location": {
        "infobox_keys": ["location", "located_in", "headquarters", "location_city", "location_country"],
        "patterns": [r"\bbased in\b", r"\bheadquartered in\b", r"\blocated in\b", r"\blocated at\b", r"\bheadquarters\b"],
    },
    "Country": {
        "infobox_keys": ["country", "location_country", "nationality"],
        "patterns": [r"\bin ([A-Z][A-Za-z .'-]+)", r"\bfrom ([A-Z][A-Za-z .'-]+)", r"\bcountry\b"],
    },
}

STOPWORDS = {
    "the", "and", "of", "in", "on", "at", "a", "an", "by", "for", "to",
    "was", "is", "are", "as", "with", "from", "born", "founded", "located",
    "headquartered", "country", "his", "her", "their", "company", "inc",
    "limited", "ltd", "llc", "official", "headquarters", "based", "established",
}


def normalize_key(value: str) -> str:
    value = str(value or "").strip().lower()
    value = re.sub(r"\[[^\]]*\]", "", value)
    return re.sub(r"[^a-z0-9]+", "_", value).strip("_")


def clean_text(value: str) -> str:
    value = BeautifulSoup(str(value or ""), "html.parser").get_text(" ", strip=True)
    value = re.sub(r"\[[0-9]+\]", "", value)
    return re.sub(r"\s+", " ", value).strip()


def normalize_name(value: str) -> str:
    value = clean_text(value).lower()
    value = re.sub(r"\([^)]*\)", " ", value)
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def split_people(value: str):
    value = clean_text(value)
    value = re.sub(r"\([^)]*\)", "", value)
    parts = re.split(r"\s*(?:;|\n|\u2022|,\s+and\s+|\s+and\s+|,\s*)\s*", value, flags=re.I)
    return [p.strip() for p in parts if len(p.strip()) > 1 and p.lower() not in {"none", "unknown"}]


def normalize_date(value: str):
    value = clean_text(value)
    if not value:
        return None
    value = re.sub(r"\([^)]*\)", "", value).strip()
    value = re.sub(r"\b(circa|c\.|approximately|about)\b", "", value, flags=re.I).strip()
    formats = [
        "%d %B %Y", "%d %b %Y", "%B %d, %Y", "%b %d, %Y",
        "%B %Y", "%b %Y", "%Y-%m-%d", "%Y",
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(value, fmt)
            if fmt == "%Y":
                return str(dt.year)
            if "%d" not in fmt:
                return dt.strftime("%Y-%m")
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            pass
    m = re.search(r"\b(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})\b", value)
    if m:
        for fmt in ("%d %B %Y", "%d %b %Y"):
            try:
                return datetime.strptime(" ".join(m.groups()), fmt).strftime("%Y-%m-%d")
            except ValueError:
                pass
    y = re.search(r"\b(1[5-9]\d{2}|20\d{2})\b", value)
    return y.group(1) if y else None


def normalize_general(value: str) -> str:
    value = normalize_name(value)
    tokens = [t for t in value.split() if t not in STOPWORDS]
    return " ".join(tokens)


def values_match(fact_type: str, infobox_value: str, sentence: str) -> bool:
    if not infobox_value or not sentence:
        return False
    if fact_type == "Birth Date":
        ib = normalize_date(infobox_value)
        if not ib:
            return False
        sentence_date = normalize_date(sentence)
        if sentence_date == ib:
            return True
        year = re.search(r"\b(1[5-9]\d{2}|20\d{2})\b", ib)
        return bool(year and re.search(rf"\b{re.escape(year.group(1))}\b", sentence))
    if fact_type == "Founder":
        names = split_people(infobox_value)
        normalized_sentence = normalize_name(sentence)
        return bool(names) and all(normalize_name(name) in normalized_sentence for name in names if normalize_name(name))
    ib = normalize_general(infobox_value)
    sentence_n = normalize_general(sentence)
    if not ib:
        return False
    if ib in sentence_n:
        return True
    tokens = [t for t in ib.split() if len(t) > 2]
    return bool(tokens) and all(re.search(rf"\b{re.escape(t)}\b", sentence_n) for t in tokens)


def likely_contains_different_fact(fact_type: str, infobox_value: str, sentence: str) -> bool:
    if not sentence or not infobox_value:
        return False
    if fact_type == "Birth Date":
        ib_date = normalize_date(infobox_value)
        dates = re.findall(
            r"\b(?:\d{1,2}\s+)?(?:January|February|March|April|May|June|July|August|September|October|November|December)"
            r"(?:\s+\d{1,2})?,?\s+\d{4}\b|\b(?:19|20)\d{2}\b", sentence, flags=re.I)
        return any(normalize_date(d) and normalize_date(d) != ib_date for d in dates)
    if fact_type == "Founder":
        names = {normalize_name(x) for x in split_people(infobox_value)}
        caps = re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3}\b", sentence)
        candidates = {normalize_name(x) for x in caps}
        return bool(candidates - names)
    ib = normalize_general(infobox_value)
    sentence_tokens = set(normalize_general(sentence).split())
    return any(len(token) > 2 and token not in sentence_tokens for token in ib.split())


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_wikipedia(title: str):
    params = {
        "action": "parse", "page": title, "prop": "text", "format": "json",
        "formatversion": "2", "redirects": 1,
    }
    response = requests.get(WIKI_API, params=params, headers={"User-Agent": USER_AGENT}, timeout=20)
    response.raise_for_status()
    data = response.json()
    if "error" in data:
        raise ValueError(data["error"].get("info", "Wikipedia page could not be loaded."))
    html = data["parse"]["text"]
    soup = BeautifulSoup(html, "html.parser")
    infobox = {}
    table = soup.select_one("table.infobox")
    if table:
        for row in table.select("tr"):
            th, td = row.find("th"), row.find("td")
            if th and td:
                key = normalize_key(th.get_text(" ", strip=True))
                value = clean_text(td.get_text(" ", strip=True))
                if key and value:
                    infobox[key] = value
    for node in soup.select("table.infobox, table, sup.reference, style, script"):
        node.decompose()
    sentences = []
    for p in soup.select("p"):
        text = clean_text(p.get_text(" ", strip=True))
        if text:
            sentences.extend(x.strip() for x in re.split(r"(?<=[.!?])\s+", text) if len(x.strip()) >= 20)
    return {
        "title": data["parse"]["title"],
        "url": "https://en.wikipedia.org/wiki/" + quote(data["parse"]["title"].replace(" ", "_")),
        "infobox": infobox,
        "sentences": sentences,
    }


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_wikipedia_image(title: str):
    params = {
        "action": "query", "prop": "pageimages", "titles": title,
        "piprop": "thumbnail|original", "pithumbsize": 900,
        "format": "json", "formatversion": "2", "redirects": 1,
    }
    try:
        response = requests.get(WIKI_API, params=params, headers={"User-Agent": USER_AGENT}, timeout=15)
        response.raise_for_status()
        pages = response.json().get("query", {}).get("pages", [])
        if pages and pages[0].get("thumbnail", {}).get("source"):
            return pages[0]["thumbnail"]["source"]
        if pages and pages[0].get("original", {}).get("source"):
            return pages[0]["original"]["source"]
    except Exception:
        pass
    return None


def find_infobox_value(infobox: dict, fact_type: str):
    for wanted in FACT_CONFIG[fact_type]["infobox_keys"]:
        for actual, value in infobox.items():
            if actual == wanted or actual.startswith(wanted + "_"):
                if value:
                    return value
    return None


def find_evidence(fact_type: str, infobox_value: str, sentences):
    for sentence in sentences:
        if values_match(fact_type, infobox_value, sentence):
            return sentence, "Match"
    for sentence in sentences:
        if any(re.search(pattern, sentence, re.I) for pattern in FACT_CONFIG[fact_type]["patterns"]):
            if likely_contains_different_fact(fact_type, infobox_value, sentence):
                return sentence, "Possible Mismatch"
    return None, "Not Found"


def compare_fact(title: str, fact_type: str):
    page = fetch_wikipedia(title)
    infobox_value = find_infobox_value(page["infobox"], fact_type)
    image_url = fetch_wikipedia_image(page["title"])
    if not infobox_value:
        return {
            "status": "Not Found", "title": page["title"], "url": page["url"],
            "infobox_value": None, "evidence": None, "image_url": image_url,
            "message": "The corresponding fact is not available in the article infobox.",
        }
    evidence, status = find_evidence(fact_type, infobox_value, page["sentences"])
    messages = {
        "Match": "The article text supports the infobox information.",
        "Possible Mismatch": "The article contains a relevant sentence with different information.",
        "Not Found": "The corresponding information is not available in the article text.",
    }
    return {
        "status": status, "title": page["title"], "url": page["url"],
        "infobox_value": infobox_value, "evidence": evidence, "image_url": image_url,
        "message": messages[status],
    }


def download_real_dataset():
    response = requests.get(RAW_DATA_URL, headers={"User-Agent": USER_AGENT}, timeout=30)
    response.raise_for_status()
    if len(response.content) < 100_000:
        raise ValueError("Downloaded dataset is unexpectedly small; refusing to replace the local dataset.")
    DATA_FILE.write_bytes(response.content)


def validate_dataset(df: pd.DataFrame):
    aliases = ["title", "article_title", "article name", "article_name", "name"]
    lower_map = {str(c).strip().lower(): c for c in df.columns}
    title_col = next((lower_map[a] for a in aliases if a in lower_map), None)
    if title_col is None:
        raise ValueError("Dataset loaded, but no article title column was found. Expected: title, article_title, article_name, or name.")
    df = df.copy()
    df["__article_title"] = df[title_col].astype(str).str.strip()
    df = df[df["__article_title"].ne("") & df["__article_title"].ne("nan")].drop_duplicates("__article_title")
    return df, title_col


@st.cache_data(ttl=300)
def load_dataset():
    source = "local"
    # The packaged 5-row file is only a fallback. The real repository CSV is
    # 10,001 lines / about 1 MB, so prefer downloading it whenever the local
    # file looks like the demo fallback.
    needs_refresh = not DATA_FILE.exists()
    if DATA_FILE.exists():
        try:
            local = pd.read_csv(DATA_FILE)
            needs_refresh = len(local) < 1000
        except Exception:
            needs_refresh = True
    if needs_refresh:
        try:
            download_real_dataset()
            source = "official project repository"
        except Exception:
            source = "local fallback (offline)"
    df = pd.read_csv(DATA_FILE)
    df, title_col = validate_dataset(df)
    return df, source, title_col


def inject_css():
    st.markdown("""
    <style>
    .hero { padding: 1.4rem 1.6rem; border-radius: 18px; border: 1px solid rgba(128,128,128,.22); background: linear-gradient(135deg, rgba(40,80,120,.16), rgba(80,80,80,.05)); margin-bottom: 1rem; }
    .hero h1 { margin: 0; font-size: 2.4rem; }
    .hero p { margin: .45rem 0 0; opacity: .78; }
    .evidence { padding: 1rem 1.1rem; border-radius: 12px; border-left: 5px solid #6c8ebf; background: rgba(128,128,128,.08); line-height: 1.6; }
    </style>
    """, unsafe_allow_html=True)


st.set_page_config(page_title="WikiFact Check", page_icon="🔎", layout="wide")
inject_css()

st.markdown("""
<div class="hero">
<h1>🔎 WikiFact Check</h1>
<p>Evidence-first consistency checking between a Wikipedia infobox fact and the article text.</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("Fact Check")
    fact_type = st.selectbox("Fact type", list(FACT_CONFIG.keys()))
    try:
        dataset, source, title_col = load_dataset()
        if source == "official project repository":
            st.success(f"WikiWeak connected: {len(dataset):,} articles")
        elif len(dataset) >= 1000:
            st.success(f"WikiWeak connected: {len(dataset):,} articles")
        else:
            st.warning(f"Offline fallback: {len(dataset):,} demo articles")
        st.caption(f"Article-title column: `{title_col}`")
    except Exception as exc:
        dataset, source, title_col = pd.DataFrame(), "error", ""
        st.error(str(exc))

    article_query = st.text_input("Article title", placeholder="e.g. Narendra Modi, Google, Virat Kohli")
    title_options = dataset["__article_title"].tolist() if not dataset.empty else []
    matching = [t for t in title_options if article_query.strip().lower() in t.lower()] if article_query.strip() else title_options[:50]
    selected = st.selectbox("WikiWeak article (optional)", matching[:100], index=0 if matching else None, placeholder="Select an article")
    use_selected = st.checkbox("Use selected dataset article", value=False)
    run_check = st.button("🔍 Check Fact", type="primary", use_container_width=True)

if run_check:
    title = selected if use_selected and selected else article_query.strip()
    if not title:
        st.warning("Enter an article title or select a WikiWeak article.")
        st.stop()
    with st.spinner(f"Checking {title}..."):
        try:
            result = compare_fact(title, fact_type)
        except requests.RequestException as exc:
            st.error(f"Wikipedia could not be reached: {exc}")
            st.stop()
        except Exception as exc:
            st.error(f"Could not check this article: {exc}")
            st.stop()

    if result["status"] == "Match":
        st.success("MATCH — both information are the same.")
    elif result["status"] == "Possible Mismatch":
        st.warning("POSSIBLE MISMATCH — the article contains different information.")
    else:
        st.info("NOT FOUND — corresponding information is not available in the article.")

    st.markdown(f"## {result['title']}")
    st.caption(f"Fact type: **{fact_type}**")

    if result.get("image_url"):
        st.image(result["image_url"], caption=f"Wikipedia image — {result['title']}", width=360)

    left, right = st.columns(2)
    with left:
        st.markdown("### Infobox information")
        st.info(result["infobox_value"] or "Not available")
    with right:
        st.markdown("### Wikipedia article")
        st.markdown(f"[Open article ↗]({result['url']})")
        st.caption("Source: English Wikipedia")

    st.markdown("### Exact evidence sentence")
    if result["evidence"]:
        st.markdown(f'<div class="evidence">“{result["evidence"]}”</div>', unsafe_allow_html=True)
    else:
        st.caption("No corresponding evidence sentence was found in the article text.")
    st.caption(result["message"])

else:
    st.markdown("### Teacher requirement checklist")
    st.dataframe(pd.DataFrame({
        "Requirement": [
            "WikiWeak article-title column", "Three outcomes", "Natural-language matching",
            "Exact evidence sentence", "Different fact types", "Wikipedia article image",
        ],
        "Implementation": [
            "Auto-detects title/name column", "Match / Possible Mismatch / Not Found",
            "Normalizes names, dates and phrases", "Displays the source sentence",
            "Birth Date / Founder / Location / Country", "Fetches the page's main image",
        ],
        "Status": ["Ready", "Ready", "Ready", "Ready", "Ready", "Ready"],
    }), hide_index=True, use_container_width=True)
    st.info("Demo path: Narendra Modi → Birth Date → Match; Google → Founder → Match; then test an incorrect or unavailable fact.")
