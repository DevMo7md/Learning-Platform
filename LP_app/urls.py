from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('home/', views.home, name='home'),
    path('video/<int:pk>/', views.video, name='video'),
    path('lessons/<int:pk>/',views.lessons, name='lessons' ),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
    path('dashboard/<int:pk>/', views.dashboard, name='dashboard'),
    path('api/get-subscription-stats/', views.get_subscription_stats, name='get_subscription_stats'),
    path('stat-dashboard/', views.stat_dashboard, name='stat_dashboard'),
    path('edit-lesson/<int:pk>/', views.edit_lesson, name='edit_lesson'),
    path('delete_lesson/<int:pk>/', views.delete_lesson, name='delete_lesson'),
    path('teacher-video/<int:pk>/', views.teacher_video, name='teacher_video'),
    path('teachers-home/<str:foo>/',views.teachers_home, name='teachers_home' ),

]
