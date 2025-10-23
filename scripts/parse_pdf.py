#!/usr/bin/env python
import sys
import json
import fitz
from parsers import chase, amex, capone, citi, boa

PARSERS = {
    'chase': chase,
    'amex': amex,
    'capone': capone,
    'citi': citi,
    'boa': boa,
}

ISSUER_DISPLAY = {
    'chase': 'Chase',
    'amex': 'American Express',
    'capone': 'Capital One',
    'citi': 'Citi',
    'boa': 'Bank of America',
}


def extract_text(path: str) -> str:
    doc = fitz.open(path)
    return "\n".join(page.get_text() for page in doc)


def main(argv):
    if len(argv) < 3:
        print('Usage: parse_pdf.py <issuer> <pdf-path>')
        print('issuers:', ', '.join(PARSERS.keys()))
        return 2
    issuer = argv[1]
    path = argv[2]
    if issuer not in PARSERS:
        print('Unknown issuer:', issuer)
        return 3
    text = extract_text(path)
    result = PARSERS[issuer].parse_text(text)
    if not result.get('card_name'):
        result['card_name'] = ISSUER_DISPLAY.get(issuer, issuer.title())
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
