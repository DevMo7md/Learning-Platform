from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='cat_images', null=True, blank=False)
    
    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    second_name = models.CharField(max_length=255, null=True, blank=True)
    third_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone_num = models.CharField(max_length=20, null=True, blank=True)
    dad_num = models.CharField(max_length=255, null=True, blank=True)
    mom_num = models.CharField(max_length=255, null=True, blank=True)
    school = models.CharField(max_length=255, null=True, blank=True)
    dad_job = models.CharField(max_length=255, null=True, blank=True)
    government = models.CharField(max_length=255, null=True, blank=True)
    alsaf = models.CharField(max_length=255, null=True, blank=True)
    enrolled_courses = models.ManyToManyField(Category, related_name='students')
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name} - username: {self.user.username}'


class Teachers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, related_name='teachers', blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    second_name = models.CharField(max_length=255, null=True, blank=True)
    third_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone_num = models.CharField(max_length=20, null=True, blank=True)
    government = models.CharField(max_length=255, null=True, blank=True)
    id_card = models.ImageField(upload_to='teachers ids', null=True, blank=True)
    photo = models.ImageField(upload_to='teachers photos', null=True, blank=True)
    subject = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__ (self):
        return f'{self.first_name} {self.last_name} - {self.user.username}'


class Lesson(models.Model):
    teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE, null=True, blank=False)
    title = models.CharField(max_length=200, null=True, blank=True)
    discrebtion = models.TextField(null=True, blank=True)
    lesson = models.FileField(upload_to='lessons', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    thumnale_image = models.ImageField(upload_to='thumnales', null=True, blank=True)
    added_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    views = models.PositiveIntegerField(default=0)  # حقل عدد المشاهدات

    def __str__(self):
        return self.title

class MonthlySubscription(models.Model):
    month = models.CharField(max_length=50, null=True, blank=True)  # تعديل نوع الحقل ليكون CharField
    new_subscribers = models.PositiveIntegerField(null=True, blank=True)
    teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE, null=True, blank=True)  # إضافة العلاقة مع Teacher

    def __str__(self):
        return f"{self.month} - {self.new_subscribers} subscribers"
