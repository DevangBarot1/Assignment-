import re


def _find_last4(text: str):
    # try several common patterns
    patterns = [
        r'Account\s+ending\s+in\s+(\d{4})',
        r'Card\s+ending\s+in\s+(\d{4})',
        r'Account Number\s*[:\s]*\*+(\d{4})',
        r'Acct(?:\.|ount)?(?: Number)?\s*[:\s]*\*+(\d{4})',
        r'\*{2,}(\d{4})',
        r'\b(\d{4})\b'  # fallback - last 4 digit group
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return m.group(1)
    return None


def _find_card_name(text: str):
    # look for a Chase product line - capture Chase + up to 4 words (e.g., Chase Sapphire Reserve)
    m = re.search(r'^(.*Chase(?: [A-Za-z0-9&-]+){0,4}?)\s*$', text, re.IGNORECASE | re.MULTILINE)
    if m:
        # prefer lines that contain 'Card' or known product names
        line = m.group(1).strip()
        if 'card' in line.lower() or any(k in line.lower() for k in ['sapphire', 'freedom', 'slate', 'ink', 'reserve']):
            return line

    # looser: find 'Chase' followed by words
    m = re.search(r'Chase\s+[A-Za-z0-9 &-]{3,40}', text)
    if m:
        return m.group(0).strip()
    return None


def _find_amount(text: str):
    # Look for common balance labels and capture dollar amounts
    patterns = [
        r'New Balance\s*[:\-]?\s*\$?\s*([0-9,]+\.\d{2})',
        r'New balance\s*[:\-]?\s*\$?\s*([0-9,]+\.\d{2})',
        r'Current Balance\s*[:\-]?\s*\$?\s*([0-9,]+\.\d{2})',
        r'Total Due\s*[:\-]?\s*\$?\s*([0-9,]+\.\d{2})',
        r'Total Amount Due\s*[:\-]?\s*\$?\s*([0-9,]+\.\d{2})',
        r'Amount Due\s*[:\-]?\s*\$?\s*([0-9,]+\.\d{2})',
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return m.group(1)
    return None


def parse_text(text: str) -> dict:
    # Heuristics for Chase statements (more robust)
    out = {
        'last4': None,
        'card_name': None,
        'statement_period': None,
        'payment_due_date': None,
        'new_balance': None,
    }

    # prefer explicit Card Number patterns
    out['last4'] = _find_last4(text)
    if not out['last4']:
        m = re.search(r'Card Number\s*[:\s]*\*+(\d{4})', text, re.IGNORECASE)
        if m:
            out['last4'] = m.group(1)

    out['card_name'] = _find_card_name(text)
    if not out['card_name'] and 'chase' in text.lower():
        out['card_name'] = 'Chase'

    # match the colon form to avoid matching header lines (e.g. a separate 'STATEMENT PERIOD' title)
    m = re.search(r'Statement Period\s*:\s*([A-Za-z0-9 ,\-/]+)', text, re.IGNORECASE)
    if m:
        out['statement_period'] = m.group(1).strip()

    m = re.search(r'Payment Due Date\s*[:\-]?\s*([A-Za-z0-9, ]+\d{4})', text, re.IGNORECASE)
    if m:
        out['payment_due_date'] = m.group(1).strip()

    out['new_balance'] = _find_amount(text)

    return out

