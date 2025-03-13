from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Subject

def user_login(request):
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
        # Process file upload here.
        # For now, simply return a message.
        return render(request, 'college/faculty/upload_material.html', {'message': 'Material uploaded successfully!'})
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
def view_class_advisors(request):
    # HOD view to see class advisors.
    advisors = CustomUser.objects.filter(role='class_advisor')
    return render(request, 'college/hod/view_class_advisors.html', {'advisors': advisors})
