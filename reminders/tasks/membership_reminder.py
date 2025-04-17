
@shared_task
def daily_membership_reminder_check():
    today = jdatetime.date.today()
    target_date = today + timedelta(days=7)

    profiles = UserProfile.objects.filter(next_payment_date=target_date)

    for profile in profiles:
        send_reminder(profile.user, "یادآوری پرداخت حق عضویت: موعد پرداخت شما نزدیک است!")
        Reminder.objects.get_or_create(
            user=profile.user,
            reminder_type='membership_fee',
            due_date=profile.next_payment_date,
            defaults={'sent': True}
        )

