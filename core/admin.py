from django.contrib import admin
from .models import (
    Student, Department, Course, CourseRegistration,
    Exam, Mark, GradeScale, Result
)

from .utils import calculate_student_gpa, save_student_result


# =========================
# 🔥 ACTION: Generate Result
# =========================
def generate_result(modeladmin, request, queryset):
    for student in queryset:
        save_student_result(student)

generate_result.short_description = "Generate Result (CGPA)"


# =========================
# 🧑‍🎓 STUDENT ADMIN
# =========================
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'student_id', 'department', 'get_gpa')

    def get_gpa(self, obj):
        gpa, grade = calculate_student_gpa(obj)
        return f"{gpa} / 4.00 ({grade})"

    get_gpa.short_description = "CGPA"

    actions = [generate_result]


# =========================
# 📊 RESULT ADMIN
# =========================
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'cgpa', 'grade')
    readonly_fields = ('cgpa', 'grade')

    def save_model(self, request, obj, form, change):
        gpa, grade = calculate_student_gpa(obj.student)

        obj.cgpa = gpa
        obj.grade = grade

        super().save_model(request, obj, form, change)


# =========================
# 🧪 EXAM ADMIN
# =========================
class ExamAdmin(admin.ModelAdmin):
    list_display = ('course', 'exam_type', 'total_marks', 'weight')
    readonly_fields = ('weight',)

    def save_model(self, request, obj, form, change):

        if obj.exam_type == "CT":
            obj.weight = 20
        elif obj.exam_type == "MID":
            obj.weight = 30
        elif obj.exam_type == "FINAL":
            obj.weight = 50
        else:
            obj.weight = 0

        super().save_model(request, obj, form, change)


# =========================
# 🧾 MARK ADMIN (FIXED VIEW)
# =========================
class MarkAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'course',
        'exam_type_display',
        'marks_obtained',
        'total_marks_display'
    )

    list_filter = ('exam__exam_type', 'course', 'student')

    def exam_type_display(self, obj):
        return obj.exam.get_exam_type_display()

    def total_marks_display(self, obj):
        return obj.exam.total_marks

    exam_type_display.short_description = "Exam Type"
    total_marks_display.short_description = "Total Marks"


# =========================
# REGISTER MODELS
# =========================
admin.site.register(Student, StudentAdmin)
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(CourseRegistration)
admin.site.register(Exam, ExamAdmin)
admin.site.register(Mark, MarkAdmin)
admin.site.register(GradeScale)
admin.site.register(Result, ResultAdmin)