# Credit Card Statement PDF Parser

Simple Flask web app to upload credit card statement PDFs and extract key fields for five issuers.

Supported issuers:
- Chase
- American Express
- Capital One
- Citi
- Bank of America

Extracted fields (per statement):
- Card last 4 digits
- Card type/variant (where available)
- Billing cycle / statement period
- Payment due date
- Total balance / New balance

How to run

1. Create a Python virtualenv and activate it.
2. Install requirements:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m app
```

4. Open http://127.0.0.1:5000

Notes
- Parsers are heuristic-based and work on typical statement text. More samples will improve reliability.
