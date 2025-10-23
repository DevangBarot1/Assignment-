from flask import Flask, render_template, request, redirect, url_for
import fitz  # PyMuPDF
import os
from parsers import chase, amex, capone, citi, boa

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024

PARSERS = {
    'chase': chase,
    'amex': amex,
    'capone': capone,
    'citi': citi,
    'boa': boa,
}

# friendly display names for the UI
ISSUER_DISPLAY = {
    'chase': 'Chase',
    'amex': 'American Express',
    'capone': 'Capital One',
    'citi': 'Citi',
    'boa': 'Bank of America',
}


def extract_text_from_pdf(stream):
    # load pdf from file-like object
    doc = fitz.open(stream=stream.read(), filetype='pdf')
    text = []
    for page in doc:
        text.append(page.get_text())
    return "\n".join(text)


@app.route('/')
def index():
    # pass list of (id, display)
    issuers = [(k, ISSUER_DISPLAY.get(k, k)) for k in PARSERS.keys()]
    return render_template('index.html', issuers=issuers)


@app.route('/parse', methods=['POST'])
def parse():
    issuer = request.form.get('issuer')
    f = request.files.get('pdf')
    if not issuer or issuer not in PARSERS:
        return redirect(url_for('index'))
    if not f:
        return redirect(url_for('index'))

    text = extract_text_from_pdf(f.stream)
    parser = PARSERS[issuer]
    result = parser.parse_text(text)
    # fallback: if parser couldn't find a card_name, use the selected issuer's display name
    if not result.get('card_name'):
        result['card_name'] = ISSUER_DISPLAY.get(issuer, issuer.title())
    show_raw = bool(request.form.get('debug'))

    return render_template('result.html', issuer=issuer, result=result, raw_text=(text if show_raw else None), issuer_display=ISSUER_DISPLAY.get(issuer, issuer))


if __name__ == '__main__':
    app.run(debug=True)
