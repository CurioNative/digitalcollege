from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Subject, Question, Choice, VideoLecture, Material, Attendance
from datetime import timedelta
from .forms import VideoLectureForm, MaterialForm
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def user_login(request):
    # If the user is already logged in, redirect to dashboard.
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.role in ['faculty', 'class_advisor', 'hod']:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'college/login.html', {'error': 'Invalid credentials or not authorized'})
    return render(request, 'college/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    # For example, if the user is a faculty member, fetch the subjects assigned to them.
    context = {}
    if request.user.role == 'faculty':
        context['subjects'] = Subject.objects.filter(faculty=request.user)
    return render(request, 'college/dashboard.html', context)

@login_required
def upload_material(request):
    # Handle file uploads for faculty.
    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        video_title = request.POST.get('video_title')  # Get the video title from the form
        video_url = request.POST.get('video_url')
        resource_url = request.POST.get('resource_url')
        material_file = request.FILES.get('material_file')

        # Create or update the VideoLecture
        subject = Subject.objects.get(id=subject_id)
        video_lecture = VideoLecture.objects.create(
            subject=subject,
            title=video_title,  # Use the video title from the form
            video_url=video_url,
            video_file=material_file  # If you want to allow file uploads as well
        )

        # Create or update the Material
        Material.objects.create(
            subject=subject,
            video_lecture=video_lecture,
            title="Material Title",  # You may want to get this from the form as well
            resource_url=resource_url,
            resource_file=material_file  # If you want to allow file uploads as well
        )

        return render(request, 'college/faculty/upload_material.html', {'message': 'Material uploaded successfully!', 'subjects': Subject.objects.filter(faculty=request.user)})

    # Pass in subjects for the dropdown.
    context = {'subjects': Subject.objects.filter(faculty=request.user)}
    return render(request, 'college/faculty/upload_material.html', context)

@login_required
def create_student(request):
    # Only class advisors can create students.
    if request.method == 'POST':
        # Here, you would process form data to create a new student user.
        # For demonstration, we simply return a success message.
        return render(request, 'college/class_advisor/create_student.html', {'message': 'Student account created successfully!'})
    return render(request, 'college/class_advisor/create_student.html')

@login_required
def manage_schedule(request):
    # Handle schedule management for class advisors.
    return render(request, 'college/class_advisor/manage_schedule.html')

@login_required
def manage_faculty(request):
    # Only HODs can assign faculty.
    if request.method == 'POST':
        # Process the assignment here.
        return render(request, 'college/hod/manage_faculty.html', {'message': 'Faculty assigned successfully!'})
    # Provide list of subjects and faculty for dropdowns.
    context = {
        'subjects': Subject.objects.all(),
        'faculty_list': CustomUser.objects.filter(role='faculty')
    }
    return render(request, 'college/hod/manage_faculty.html', context)

@login_required
def remove_faculty_assignment(request, subject_id):
    # Only allow HODs to perform this action.
    if request.user.role != 'hod':
        return HttpResponseForbidden("You are not allowed to perform this action.")

    # Ensure the subject belongs to the HOD's department.
    subject = get_object_or_404(Subject, id=subject_id, department=request.user.department)
    
    if request.method == 'POST':
        subject.faculty = None
        subject.save()
        return redirect('manage_faculty')
    
    return render(request, 'college/hod/confirm_remove_faculty.html', {'subject': subject})

@login_required
def view_class_advisors(request):
    # HOD view to see class advisors.
    advisors = CustomUser.objects.filter(role='class_advisor')
    return render(request, 'college/hod/view_class_advisors.html', {'advisors': advisors})

@login_required
def faculty_video_list(request):
    """
    List all video lectures for subjects taught by the logged-in faculty.
    """
    video_lectures = VideoLecture.objects.filter(subject__faculty=request.user)
    return render(request, 'college/faculty/video_list.html', {'video_lectures': video_lectures})

@login_required
def edit_video_lecture(request, pk):
    """
    Allow faculty to edit a video lecture.
    Only allows editing if the lecture belongs to a subject taught by the faculty.
    """
    video = get_object_or_404(VideoLecture, pk=pk, subject__faculty=request.user)
    if request.method == 'POST':
        form = VideoLectureForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            return redirect('faculty_video_list')
    else:
        form = VideoLectureForm(instance=video)
    return render(request, 'college/faculty/edit_video_lecture.html', {'form': form, 'video': video})

@login_required
def faculty_material_list(request):
    """
    List all materials for subjects taught by the logged-in faculty.
    """
    materials = Material.objects.filter(subject__faculty=request.user)
    return render(request, 'college/faculty/material_list.html', {'materials': materials})

@login_required
def edit_material(request, pk):
    """
    Allow faculty to edit a material.
    Only allows editing if the material belongs to a subject taught by the faculty.
    """
    material = get_object_or_404(Material, pk=pk, subject__faculty=request.user)
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES, instance=material)
        if form.is_valid():
            form.save()
            return redirect('faculty_material_list')
    else:
        form = MaterialForm(instance=material)
    return render(request, 'college/faculty/edit_material.html', {'form': form, 'material': material})

@login_required
def delete_video_lecture(request, pk):
    """
    Allow faculty to delete a video lecture.
    Only allows deletion if the lecture belongs to a subject taught by the faculty.
    A confirmation page is displayed before deletion.
    """
    video = get_object_or_404(VideoLecture, pk=pk, subject__faculty=request.user)
    if request.method == 'POST':
        video.delete()
        return redirect('faculty_video_list')
    return render(request, 'college/faculty/delete_video_lecture.html', {'video': video})

@login_required
def delete_material(request, pk):
    """
    Allow faculty to delete a material.
    Only allows deletion if the material belongs to a subject taught by the faculty.
    A confirmation page is displayed before deletion.
    """
    material = get_object_or_404(Material, pk=pk, subject__faculty=request.user)
    if request.method == 'POST':
        material.delete()
        return redirect('faculty_material_list')
    return render(request, 'college/faculty/delete_material.html', {'material': material})

@login_required
def view_assigned_faculties(request):
    # Only HODs can access this view.
    if request.user.role != 'hod':
        return redirect('dashboard')
    # Get subjects within the HOD's department that have an assigned faculty member.
    subjects = Subject.objects.filter(department=request.user.department, faculty__isnull=False)
    return render(request, 'college/hod/view_assigned_faculties.html', {'subjects': subjects})

@login_required
@csrf_exempt  # If you're calling via API; alternatively, ensure proper CSRF tokens are sent
def record_attendance(request):
    """
    Records attendance for a video lecture.
    Expects a POST with JSON data containing 'video_id'.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            video_id = data.get('video_id')
            video = get_object_or_404(VideoLecture, id=video_id)
            # Create attendance record for the logged-in student.
            Attendance.objects.create(
                student=request.user,
                video=video
            )
            return JsonResponse({'status': 'success', 'message': 'Attendance recorded'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@login_required
def view_attendance(request):
    """
    Allows a class advisor to view attendance records of students in their department.
    """
    if request.user.role != 'class_advisor':
        return HttpResponseForbidden("Not allowed")
    
    # Assuming class advisor is assigned a department, filter attendance by that department.
    attendance_records = Attendance.objects.filter(student__department=request.user.department)
    return render(request, 'college/class_advisor/attendance.html', {'attendance_records': attendance_records})

@login_required
def faculty_view_attendance(request):
    """
    Allows a faculty member to view attendance records for the videos of the subjects they teach.
    """
    if request.user.role != 'faculty':
        return HttpResponseForbidden("You are not allowed to access this page.")
    
    # Filter attendance records by the faculty assigned to the video's subject.
    attendance_records = Attendance.objects.filter(video__subject__faculty=request.user)
    return render(request, 'college/faculty/attendance.html', {'attendance_records': attendance_records})