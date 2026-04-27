from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=50, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    batch = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Course(models.Model):
    course_code = models.CharField(max_length=20)
    course_title = models.CharField(max_length=100)
    credit = models.FloatField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.course_title


class CourseRegistration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.student.name} - {self.course.course_title}"


class Exam(models.Model):

    EXAM_TYPES = [
        ('CT', 'Class Test'),
        ('MID', 'Mid Term'),
        ('FINAL', 'Final Exam'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    exam_type = models.CharField(max_length=10, choices=EXAM_TYPES)
    total_marks = models.IntegerField()

    # 🔥 NEW FIELD
    weight = models.FloatField(help_text="Enter percentage weight (e.g. 20, 30, 50)")

    def __str__(self):
        return f"{self.course.course_title} - {self.exam_type}"


class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    marks_obtained = models.FloatField()

    def __str__(self):
        return f"{self.student.name} - {self.course.course_title}"


class GradeScale(models.Model):
    min_marks = models.FloatField()
    max_marks = models.FloatField()
    grade = models.CharField(max_length=2)
    point = models.FloatField()

    def __str__(self):
        return self.grade


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    cgpa = models.FloatField()
    grade = models.CharField(max_length=5)
    semester = models.CharField(max_length=20, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.cgpa}"