def is_valid_card_number(card_number):
    """یک الگوریتم ساده برای اعتبارسنجی شماره کارت با الگوریتم لوه"""
    digits = [int(d) for d in str(card_number)]
    checksum = 0
    odd = True
    for d in reversed(digits):
        if odd:
            checksum += d
        else:
            doubled = d * 2
            checksum += doubled if doubled < 10 else doubled - 9
        odd = not odd
    return checksum % 10 == 0
