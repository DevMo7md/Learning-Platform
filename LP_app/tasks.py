from celery import shared_task
from datetime import datetime
from celery.schedules import crontab
from celery import Celery
from django.utils import timezone
from django.contrib.auth.models import User
from .models import MonthlySubscription, Teachers

app = Celery('LP_project')

app.conf.beat_schedule = {
    'update-monthly-statistics': {
        'task': 'LP_app.tasks.update_monthly_statistics',
        'schedule': crontab(minute='*/1'),  # يتم تشغيله في اليوم الأول من كل شهر
    },
}

@shared_task
def update_monthly_subscriptions(teacher_id=None):
    # حساب الشهر الحالي
    current_month = datetime.now().strftime('%B')
    current_year = datetime.now().year
    start_of_month = datetime(current_year, datetime.now().month, 1)

    # If teacher_id is provided, update stats for that teacher; otherwise, for all teachers
    if teacher_id:
        teacher_ids = [teacher_id]
    else:
        teacher_ids = Teachers.objects.values_list('id', flat=True)

    for teacher_id in teacher_ids:
        try:
            teacher = Teachers.objects.get(id=teacher_id)
        except Teachers.DoesNotExist:
            continue

        # تصفية المستخدمين الذين انضموا بعد بداية الشهر
        new_subscribers = User.objects.filter(
            date_joined__gte=start_of_month,
            student__teachers__id=teacher.id
        ).count()

        # تحديث أو إنشاء سجل الشهر الحالي
        subscription, created = MonthlySubscription.objects.update_or_create(
            month=current_month,
            teacher=teacher,
            defaults={'new_subscribers': new_subscribers}
        )

        '''
from celery import shared_task
from django.utils import timezone
from datetime import datetime
from LP_app.models import MonthlySubscription, Teachers, User

@shared_task
def update_monthly_subscriptions(teacher_id=None):
    print("Starting task...")
    current_month = timezone.now().strftime('%B')
    current_year = timezone.now().year
    start_of_month = timezone.make_aware(datetime(current_year, timezone.now().month, 1))

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
            student__teachers__id=teacher.id
        ).count()

        subscription, created = MonthlySubscription.objects.update_or_create(
            month=current_month,
            teacher=teacher,
            defaults={'new_subscribers': new_subscribers}
        )
        print(f"Updated subscription: {subscription}, New subscribers: {new_subscribers}")

'''