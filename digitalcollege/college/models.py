from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

class Department(models.Model):
    """
    Represents a college department.
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    """
    Custom user model with additional fields:
    - role: Determines if the user is a faculty, class advisor, HOD, or student.
    - department: The department the user belongs to (compulsory for students).
    - semester: For students, indicates the current semester (1 to 8).
    """
    ROLE_CHOICES = (
        ('faculty', 'Faculty'),
        ('class_advisor', 'Class Advisor'),
        ('hod', 'Head of Department'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True,
        help_text="Department to which the user belongs. (Required for students)"
    )
    # Only applicable for students
    semester = models.PositiveSmallIntegerField(
        null=True, blank=True, help_text="Semester number for student (1-8)"
    )

    def clean(self):
        """
        Ensures that students are assigned to a department.
        """
        if self.role == 'student' and not self.department:
            raise ValidationError("Students must be assigned to a department.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Call clean() before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

class Subject(models.Model):
    """
    Represents a subject offered in the college.
    It is linked to a department and may have a faculty member assigned.
    """
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    faculty = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
        limit_choices_to={'role': 'faculty'},
        help_text="Faculty assigned to teach this subject."
    )

    def __str__(self):
        return f"{self.name} ({self.department.name})"

class VideoLecture(models.Model):
    """
    Represents a video lecture associated with a subject.
    A video lecture can be stored as an external URL or as an uploaded file.
    """
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    video_url = models.URLField(blank=True, null=True, help_text="URL to the video lecture")
    video_file = models.FileField(upload_to='videos/', blank=True, null=True, help_text="Upload video file if applicable")

    def __str__(self):
        return f"{self.title} - {self.subject.name}"

class Material(models.Model):
    """
    Represents downloadable resources related to a subject and a specific video lecture.
    These could be lecture notes, slides, PDFs, etc.
    """
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    video_lecture = models.ForeignKey(VideoLecture, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=200)
    resource_url = models.URLField(blank=True, null=True, help_text="URL to the downloadable resource")
    resource_file = models.FileField(upload_to='materials/', blank=True, null=True, help_text="Upload file if available")

    def __str__(self):
        return f"{self.title} for {self.video_lecture.title}"

class Question(models.Model):
    """
    Represents a question that pops up during a video lecture.
    The time_stamp indicates when (relative to the start of the video) the question should appear.
    """
    video = models.ForeignKey(VideoLecture, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    time_stamp = models.DurationField(help_text="Time (HH:MM:SS) when the question pops up")

    def __str__(self):
        return f"Question for {self.video.title}"

class Answer(models.Model):
    """
    Stores a student's answer to a question during a video lecture.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    student = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'student'},
        help_text="Student who answered the question"
    )
    answer_text = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer by {self.student.username} for {self.question}"
