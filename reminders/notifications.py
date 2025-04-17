def send_reminder(user, message):
    if user.email:
        # ارسال ایمیل
        print(f"Sending email to {user.email}: {message}")
    if hasattr(user, 'phone_number'):
        # ارسال SMS فرضی
        print(f"Sending SMS to {user.phone_number}: {message}")
