import re


def _find_last4(text: str):
    for p in [r'Account Number\s*[:\s]*\*+(\d{4})', r'Acct\s*[:\s]*\*+(\d{4})', r'\*{2,}(\d{4})']:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return m.group(1)
    return None


def _find_amount(text: str):
    for p in [
        r'Total Due\s*[:\-]?\s*\$?\s*([0-9,]+\.\d{2})',
        r'New Balance\s*[:\-]?\s*\$?\s*([0-9,]+\.\d{2})',
        r'Total Amount Due\s*[:\-]?\s*\$?\s*([0-9,]+\.\d{2})',
        r'Total(?: Amount)?\s+Due\s*[:\-]?\s*\$?\s*([0-9,]+\.\d{2})',
    ]:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return m.group(1)
    return None


def parse_text(text: str) -> dict:
    out = {
        'last4': None,
        'card_name': None,
        'statement_period': None,
        'payment_due_date': None,
        'new_balance': None,
    }

    out['last4'] = _find_last4(text)

    m = re.search(r'Citi\s+([A-Za-z0-9 &-]{3,40})', text)
    if m:
        out['card_name'] = ('Citi ' + m.group(1)).strip()
    elif 'citi' in text.lower():
        out['card_name'] = 'Citi'

    m = re.search(r'Statement Period\s*:\s*([A-Za-z0-9 ,\-/]+)', text, re.IGNORECASE)
    if m:
        out['statement_period'] = m.group(1).strip()

    m = re.search(r'Payment Due Date\s*[:\-]?\s*([A-Za-z0-9, ]+\d{4})', text, re.IGNORECASE)
    if m:
        out['payment_due_date'] = m.group(1).strip()

    out['new_balance'] = _find_amount(text)
    return out
