from django.db import models


# =========================
# 🏢 DEPARTMENT
# =========================
class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name} ({self.code})"


# =========================
# 🧑‍🎓 STUDENT
# =========================
class Student(models.Model):
    name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=50, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    batch = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return f"{self.name} ({self.student_id})"


# =========================
# 📚 COURSE
# =========================
class Course(models.Model):
    course_code = models.CharField(max_length=20)
    course_title = models.CharField(max_length=100)
    credit = models.FloatField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.course_title} ({self.course_code})"


# =========================
# 🧾 COURSE REGISTRATION
# =========================
class CourseRegistration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.student} - {self.course}"


# =========================
# 📝 EXAM
# =========================
class Exam(models.Model):
    EXAM_TYPES = [
        ('CT', 'Class Test'),
        ('MID', 'Mid Term'),
        ('FINAL', 'Final Exam'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    exam_type = models.CharField(max_length=10, choices=EXAM_TYPES)
    total_marks = models.IntegerField()
    weight = models.FloatField(default=0)

    def __str__(self):
        return f"{self.course} - {self.get_exam_type_display()}"


# =========================
# 📊 MARKS
# =========================
class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    marks_obtained = models.FloatField()

    def __str__(self):
        return f"{self.student} - {self.course}"


# =========================
# 🎯 GRADE SCALE
# =========================
class GradeScale(models.Model):
    min_marks = models.FloatField()
    max_marks = models.FloatField()
    grade = models.CharField(max_length=2)
    point = models.FloatField()

    def __str__(self):
        return f"{self.grade} ({self.point})"


# =========================
# 🏆 RESULT
# =========================
class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    cgpa = models.FloatField()
    grade = models.CharField(max_length=5)
    semester = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.cgpa}"


# =========================
# 📢 NOTICE BOARD (DASHBOARD)
# =========================
class Notice(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# =========================
# 💬 CHAT / MESSAGES
# =========================
class Message(models.Model):
    user = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}: {self.text[:20]}"


# =========================
# 📅 EVENTS (CALENDAR)
# =========================
class Event(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


# =========================
# 🔔 NOTIFICATIONS (OPTIONAL SAAS FEATURE)
# =========================
class Notification(models.Model):
    user = models.CharField(max_length=100)
    text = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text