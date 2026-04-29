from django.contrib import admin
from .models import (
    Student, Department, Course, CourseRegistration,
    Exam, Mark, GradeScale, Result, Notice, Message, Event,
)

from .utils import calculate_student_gpa, save_student_result


# =========================
# 🎨 BRANDING
# =========================
admin.site.site_header = "🎓 University SMS Admin Panel"
admin.site.site_title = "SMS Admin"
admin.site.index_title = "Smart Academic Dashboard"


# =========================
# 🏢 DEPARTMENT
# =========================
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')


# =========================
# 📚 COURSE
# =========================
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'course_title', 'credit', 'department')
    search_fields = ('course_code', 'course_title')
    list_filter = ('department',)


# =========================
# 🧑‍🎓 STUDENT
# =========================
class CourseRegistrationInline(admin.TabularInline):
    model = CourseRegistration
    extra = 1


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'student_id', 'department', 'batch')
    search_fields = ('name', 'student_id')
    list_filter = ('department',)

    inlines = [CourseRegistrationInline]


# =========================
# 🧪 EXAM
# =========================
@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('course', 'exam_type', 'total_marks', 'weight')
    list_filter = ('exam_type', 'course')


# =========================
# 🧾 MARK
# =========================
@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'exam', 'marks_obtained')
    list_filter = ('course', 'student', 'exam')
    search_fields = ('student__name', 'course__course_title')
    list_editable = ('marks_obtained',)


# =========================
# 🏆 RESULT
# =========================
@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'cgpa', 'grade', 'created_at')
    search_fields = ('student__name',)
    readonly_fields = ('cgpa', 'grade', 'created_at')


# =========================
# 🎯 GRADE SCALE
# =========================
@admin.register(GradeScale)
class GradeScaleAdmin(admin.ModelAdmin):
    list_display = ('grade', 'point', 'min_marks', 'max_marks')


admin.site.register(Notice)
admin.site.register(Message)
admin.site.register(Event)