from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload-material/', views.upload_material, name='upload_material'),
    path('logout/', views.user_logout, name='logout'),
    # Faculty URLs
    path('faculty/upload-material/', views.upload_material, name='upload_material'),
    path('faculty/video/', views.faculty_video_list, name='faculty_video_list'),
    path('faculty/video/edit/<int:pk>/', views.edit_video_lecture, name='edit_video_lecture'),
    path('faculty/video/delete/<int:pk>/', views.delete_video_lecture, name='delete_video_lecture'),
    path('faculty/material/', views.faculty_material_list, name='faculty_material_list'),
    path('faculty/material/edit/<int:pk>/', views.edit_material, name='edit_material'),
    path('faculty/material/delete/<int:pk>/', views.delete_material, name='delete_material'),
    path('faculty/attendance/', views.faculty_view_attendance, name='faculty_attendance'),
    # Remove add-question and view-question endpoints...
    # Class Advisor URLs
    path('class_advisor/create-student/', views.create_student, name='create_student'),
    path('class_advisor/manage-schedule/', views.manage_schedule, name='manage_schedule'),
    path('class_advisor/attendance/', views.view_attendance, name='view_attendance'),
    # HOD URLs
    path('hod/manage-faculty/', views.manage_faculty, name='manage_faculty'),
    path('hod/view-class-advisors/', views.view_class_advisors, name='view_class_advisors'),
    path('hod/view_assigned_faculties/', views.view_assigned_faculties, name='view_assigned_faculties'),
    path('hod/remove_faculty/<int:subject_id>/', views.remove_faculty_assignment, name='remove_faculty_assignment'),
    # Attendance API endpoint (for students to record attendance)
    path('attendance/', views.record_attendance, name='record_attendance'),
]
