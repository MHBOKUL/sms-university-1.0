from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# =========================
# 👤 USER
# =========================
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),   # 🔥 ADD THIS
        ('student', 'Student'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')


# =========================
# 🏫 DEPARTMENT
# =========================
class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# =========================
# 📚 COURSE
# =========================
class Course(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"


# =========================
# 🎓 STUDENT
# =========================
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


# =========================
# 📝 MARK
# =========================
class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.course.name}"


# =========================
# 📊 RESULT
# =========================
class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    gpa = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.name} - {self.gpa}"


# =========================
# ⚡ AUTO PROFILE CREATE
# =========================
@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created and instance.role == "student":
        Student.objects.get_or_create(
            user=instance,
            defaults={"name": instance.username}
        )