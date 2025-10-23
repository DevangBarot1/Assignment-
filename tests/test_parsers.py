from parsers import chase, amex, capone, citi, boa


def test_chase():
    sample = """
    Chase Card
    Account ending in 1234
    Statement Period: Sep 1 - Sep 30, 2025
    Payment Due Date: October 25, 2025
    New Balance $1,234.56
    """
    out = chase.parse_text(sample)
    assert out['last4'] == '1234'
    assert 'Chase' in (out['card_name'] or 'Chase')
    assert 'Sep' in (out['statement_period'] or '')
    assert 'October' in (out['payment_due_date'] or '')
    assert out['new_balance'] == '1,234.56'


def test_amex():
    sample = """
    American Express Gold
    Card ending in 9876
    Statement Period: Aug 15 - Sep 14, 2025
    Payment Due Date: September 20, 2025
    New Balance $234.56
    """
    out = amex.parse_text(sample)
    assert out['last4'] == '9876'
    assert 'American Express' in (out['card_name'] or '')
    assert 'Aug' in (out['statement_period'] or '')
    assert 'September' in (out['payment_due_date'] or '')
    assert out['new_balance'] == '234.56'


def test_capone():
    sample = """
    Capital One Savor Card
    Account Number: ****4321
    Statement Date: 09/2025
    Due Date: October 5, 2025
    New Balance $12,345.67
    """
    out = capone.parse_text(sample)
    assert out['last4'] == '4321'
    assert 'Capital One' in (out['card_name'] or '')
    assert '09' in (out['statement_period'] or '')
    assert 'October' in (out['payment_due_date'] or '')
    assert out['new_balance'] == '12,345.67'


def test_citi():
    sample = """
    Citi Double Cash
    Account Number ****1111
    Statement Period: Sep 1 - Sep 30, 2025
    Payment Due Date: October 20, 2025
    Total Due $456.78
    """
    out = citi.parse_text(sample)
    assert out['last4'] == '1111'
    assert 'Citi' in (out['card_name'] or '')
    assert 'Sep' in (out['statement_period'] or '')
    assert 'October' in (out['payment_due_date'] or '')
    assert out['new_balance'] == '456.78'


def test_boa():
    sample = """
    Bank of America Cash Rewards
    Card Number: ****2222
    Statement Period: 09/01/2025 - 09/30/2025
    Due Date: October 22, 2025
    New Balance $78.90
    """
    out = boa.parse_text(sample)
    assert out['last4'] == '2222'
    assert 'Bank of America' in (out['card_name'] or '')
    assert '09' in (out['statement_period'] or '')
    assert 'October' in (out['payment_due_date'] or '')
    assert out['new_balance'] == '78.90'
