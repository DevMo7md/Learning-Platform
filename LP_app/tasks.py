from celery import shared_task
from datetime import datetime
from LP_app.models import MonthlySubscription, Teachers, User

@shared_task
def update_monthly_subscriptions(teacher_id=None):
    print("Starting task...")
    current_month = datetime.now().strftime('%B')
    current_year = datetime.now().year
    start_of_month = datetime(current_year, datetime.now().month, 1)

    if teacher_id:
        teacher_ids = [teacher_id]
    else:
        teacher_ids = Teachers.objects.values_list('id', flat=True)

    for teacher_id in teacher_ids:
        try:
            teacher = Teachers.objects.get(id=teacher_id)
            print(f"Processing teacher: {teacher_id}")
        except Teachers.DoesNotExist:
            print(f"Teacher not found: {teacher_id}")
            continue

        new_subscribers = User.objects.filter(
            date_joined__gte=start_of_month,
            student__teachers=teacher
        ).count()

        subscription, created = MonthlySubscription.objects.update_or_create(
            month=current_month,
            defaults={'new_subscribers': new_subscribers}
        )
        print(f"Updated subscription: {subscription}")
