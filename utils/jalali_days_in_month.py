from persiantools.jdatetime import JalaliDate


def jalali_month_days(year, month):
    """
    تعداد روزهای ماه شمسی رو بر اساس تقویم هجری شمسی برمی‌گردونه.
    ماه‌های 1 تا 6: 31 روز
    ماه‌های 7 تا 11: 30 روز
    ماه 12 (اسفند): 29 روز در سال عادی و 30 روز در سال کبیسه
    """
    if month <= 6:
        return 31
    elif month <= 11:
        return 30
    else:
        # اسفند: اگر سال کبیسه باشه، 30 روز، در غیر این صورت 29 روز
        return 30 if JalaliDate.is_leap(year) else 29



