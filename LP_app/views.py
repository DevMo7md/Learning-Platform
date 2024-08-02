from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.http import JsonResponse
from .models import MonthlySubscription
from .tasks import update_monthly_subscriptions
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

# Create your views here.
def landing(request):
    return render(request, 'LP_app/landing.html')

def home(request):

    categories = Category.objects.all()
    if hasattr(request.user, 'teachers'):
        teacher = Teachers.objects.get(user=request.user)
        dashboard_url = reverse('dashboard', kwargs={'pk': teacher.pk})
    else:
        dashboard_url = None

    context = {
            'categories': categories,
            'dashboard_url': dashboard_url,
            }
    return render(request, 'LP_app/home.html', context)

def video(request, pk):

    lesson = Lesson.objects.get(id=pk)
    categories = Category.objects.all()

    video = get_object_or_404(Lesson, id=pk)
    video.views += 1  # زيادة عدد المشاهدات
    video.save()

    # dashboard
    if hasattr(request.user, 'teachers'):
        teacher = Teachers.objects.get(user=request.user)
        dashboard_url = reverse('dashboard', kwargs={'pk': teacher.pk})
    else:
        dashboard_url = None


    context = {
        'lesson':lesson,
        'categories': categories,
        'video':video,
        'dashboard_url': dashboard_url,
    }
    return render(request, 'LP_app/video.html', context)

def teachers_home(request, foo):

    foo = foo.replace('-', ' ')
    
    try:
        category = Category.objects.get(name=foo)
    except Category.DoesNotExist:
        messages.error(request, "الفئة المطلوبة غير موجودة!")
        return redirect('home')  # Redirect to main page if category doesn't exist

    teachers = Teachers.objects.filter(subject=category)
    categories = Category.objects.all()

    # dashboard
    if hasattr(request.user, 'teachers'):
        teacher = Teachers.objects.get(user=request.user)
        dashboard_url = reverse('dashboard', kwargs={'pk': teacher.pk})
    else:
        dashboard_url = None

    context = {
        'teachers': teachers,
        'categories': categories,
        'dashboard_url': dashboard_url,        
    }
    return render(request, 'LP_app/teachers_home.html', context)


def lessons(request, pk):

    try:
        videos = Lesson.objects.filter(teacher=pk)
        categories = Category.objects.all()

        # dashboard
        if hasattr(request.user, 'teachers'):
            teacher = Teachers.objects.get(user=request.user)
            dashboard_url = reverse('dashboard', kwargs={'pk': teacher.pk})
        else:
            dashboard_url = None

        context = {
            'videos': videos,
            'categories': categories,
            'dashboard_url': dashboard_url,
        }
        return render(request, 'LP_app/lessons.html', context)
    except:
        messages.error(request, "الفيديو المطلوب غير موجود!")
        return redirect('home')  # Redirect to main page if video doesn't exist
    
def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "تم تسجيل الدخول بنجاح")
            return redirect('home')
        else:
            messages.warning(request, "عذراً اسم المستخدم او كلمة المرور غير صحيحه الرجاء المحاوله مره اخرى")
            return redirect('login')
        
    return render(request, 'LP_app/login.html', {})


def register(request):

    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        second_name = request.POST['second_name']
        third_name = request.POST['third_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone_num = request.POST['phone_num']
        dad_num = request.POST['dad_num']
        mom_num = request.POST['mom_num']
        school = request.POST['school']
        dad_job = request.POST['dad_job']
        government = request.POST['government']
        alsaf = request.POST['alsaf']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'عذراً كلمة المرور لا تتوافق مع بعضها')
            
            else:
                user = User.objects.create_user(username=username, email=email, password=password1, first_name=first_name, last_name=last_name)
                user.save()
                student = Student.objects.create(
                        user=user,
                        first_name=first_name,
                        second_name=second_name,
                        third_name=third_name,
                        last_name=last_name,
                        phone_num=phone_num,
                        dad_num=dad_num,
                        mom_num=mom_num,
                        school=school,
                        dad_job=dad_job,
                        government=government,
                        alsaf=alsaf,)
                student.save()
                login(request, user)
                messages.success(request, 'لقد تم انشاء حسابك بنجاح ')
                return redirect('home')
        else:
            messages.error(request, 'عذراً كلمة المرور غير متوافقة')
    return render(request, 'LP_app/register.html')

def logout_user (request):
    logout(request)
    messages.success(request, 'تم تسجيل الخروج بنجاح')
    return redirect('/')  # Redirect to main page after logout

def dashboard(request, pk):
    teacher = get_object_or_404(Teachers, user=request.user)

    if request.method == 'POST':
        title = request.POST.get('title')
        lesson_file = request.FILES.get('lesson')
        category_id = request.POST.get('category')
        thumnale_image = request.FILES.get('thumnale_image')
        discrebtion = request.POST.get('discrebtion')

        if not title or not lesson_file or not category_id or not thumnale_image or not discrebtion:
            messages.error(request, "يرجى ملء جميع الحقول.")
            return redirect('dashboard', pk=pk)

        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            messages.error(request, "التصنيف المحدد غير موجود.")
            return redirect('dashboard', pk=pk)

        Lesson.objects.create(
            teacher=teacher,
            title=title,
            lesson=lesson_file,
            category=category,
            thumnale_image=thumnale_image,
            discrebtion=discrebtion,
        )

        messages.success(request, 'تم حفظ الدرس بنجاح')
        return redirect('dashboard', pk=pk)

    # الحصول على فيديوهات المدرس المحدد
    lessons = Lesson.objects.filter(teacher=teacher)
    lesson_titles = [lesson.title for lesson in lessons]
    lesson_views = sum([lesson.views for lesson in lessons])  # افترض أن لديك حقل views في نموذج Lesson
    lesson_num = len(lessons)
    categories = Category.objects.all()

    context = {
        'teacher': teacher,
        'lesson_titles': lesson_titles,
        'lesson_views': lesson_views,
        'lesson_num': lesson_num,
        'categories': categories,
        'lessonss':lessons,
    }
    print(request.user.username)# who is teacher
    return render(request, 'LP_app/dashboard.html', context)

def stat_dashboard(request):
    teacher = get_object_or_404(Teachers, user=request.user)


    # الاحصائيات
    context = {
        'teacher': teacher,
    }
    return render(request, 'LP_app/statstic.html', context)

def get_subscription_stats(request):
    stats = MonthlySubscription.objects.all().values('month', 'new_subscribers', 'teacher__user__username')
    data = {
        'labels': [f"{item['month']} - {item['teacher__user__username']}" for item in stats],
        'datasets': [{
            'label': 'الجدد في المنصة',
            'data': [item['new_subscribers'] for item in stats],
            'backgroundColor': "#eeb5ff",
            'borderColor': "#c507ff",
            'borderWidth': 0.5,
        }]
    }
    return JsonResponse(data)


def edit_lesson(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    if request.method == 'POST':
        title = request.POST.get('title')
        lesson_file = request.FILES.get('lesson')
        category_id = request.POST.get('category')
        thumnale_image = request.FILES.get('thumnale_image')
        discrebtion = request.POST.get('discrebtion')

        # التحقق من أن جميع الحقول قد تم ملؤها
        if not title or not discrebtion or not category_id:
            messages.error(request, "يرجى ملء جميع الحقول.")
            return redirect('edit_lesson', pk=pk)

        # الحصول على التصنيف بناءً على معرف التصنيف
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            messages.error(request, "التصنيف المحدد غير موجود.")
            return redirect('edit_lesson', pk=pk)

        # تحديث الدرس
        lesson.title = title
        lesson.lesson = lesson_file if lesson_file else lesson.lesson
        lesson.category = category
        lesson.thumnale_image = thumnale_image if thumnale_image else lesson.thumnale_image
        lesson.discrebtion = discrebtion
        lesson.save()

        messages.success(request, 'تم تعديل الفيديو بنجاح')
        return redirect('dashboard', pk=lesson.teacher.id)

    # إذا كان الطلب GET، املأ النموذج بالبيانات الحالية
    categories = Category.objects.all()
    context = {
        'lesson': lesson,
        'categories': categories,
    }
    return render(request, 'LP_app/edit_lesson.html', context)

def delete_lesson(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    
    if request.method == 'POST':
        lesson.delete()
        messages.success(request, 'تم حذف الفيديو بنجاح')
        return redirect('dashboard', pk=lesson.teacher.id)

    return render(request, 'LP_app/delete_lesson.html', {'lesson' : lesson})


def teacher_video(request, pk):
    teacher = get_object_or_404(Teachers, user=request.user)
    lessons = Lesson.objects.filter(teacher=teacher)
    categories = Category.objects.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        lesson_file = request.FILES.get('lesson')
        category_id = request.POST.get('category')
        thumnale_image = request.FILES.get('thumnale_image')
        discrebtion = request.POST.get('discrebtion')

        if not title or not lesson_file or not category_id or not thumnale_image or not discrebtion:
            messages.error(request, "يرجى ملء جميع الحقول.")
            return redirect('dashboard', pk=pk)

        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            messages.error(request, "التصنيف المحدد غير موجود.")
            return redirect('dashboard', pk=pk)

        Lesson.objects.create(
            teacher=teacher,
            title=title,
            lesson=lesson_file,
            category=category,
            thumnale_image=thumnale_image,
            discrebtion=discrebtion,
        )

        messages.success(request, 'تم حفظ الدرس بنجاح')
        return redirect('teacher_video', pk=pk)

    context = {
        'lessons':lessons,
        'teacher':teacher,
        'categories':categories
    }
    return render(request, 'LP_app/teachers_videos.html', context)
