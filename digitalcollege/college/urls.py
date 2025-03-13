from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload-material/', views.upload_material, name='upload_material'),
    path('logout/', views.user_logout, name='logout'),
    # Faculty URL
    path('faculty/upload-material/', views.upload_material, name='upload_material'),
    # Class Advisor URLs
    path('class_advisor/create-student/', views.create_student, name='create_student'),
    path('class_advisor/manage-schedule/', views.manage_schedule, name='manage_schedule'),
    # HOD URLs
    path('hod/manage-faculty/', views.manage_faculty, name='manage_faculty'),
    path('hod/view-class-advisors/', views.view_class_advisors, name='view_class_advisors'),
    # Add additional URLs as needed.
]
