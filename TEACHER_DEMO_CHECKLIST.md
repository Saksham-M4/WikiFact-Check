# Teacher demo checklist

1. Start with `python3 -m streamlit run app.py`.
2. Confirm the sidebar says `WikiWeak connected: 10,000+ articles` and shows `Article-title column: name`.
3. Search `Narendra Modi`, choose `Birth Date`, and run the check. Expected: `MATCH`, evidence sentence, and article image when available.
4. Search `Google`, choose `Founder`, and run the check. Test natural wording such as “Google was founded by Larry Page and Sergey Brin.”
5. Test an intentionally different fact. Expected: `POSSIBLE MISMATCH` when a competing relevant value is found.
6. Test a fact unavailable from the article. Expected: `NOT FOUND`.
7. Repeat with at least 5–10 different articles and fact types: Birth Date, Founder, Location, Country.
