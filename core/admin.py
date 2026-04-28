from django.contrib import admin
from .models import (
    Student, Department, Course, CourseRegistration,
    Exam, Mark, GradeScale, Result
)

from .utils import calculate_student_gpa, save_student_result


# =========================
# 🎨 ADMIN BRANDING
# =========================
admin.site.site_header = "🎓 Student Management System"
admin.site.site_title = "SMS Admin"
admin.site.index_title = "Dashboard"


# =========================
# 🔥 ACTION: Generate Result
# =========================
def generate_result(modeladmin, request, queryset):
    for student in queryset:
        save_student_result(student)

generate_result.short_description = "Generate Result (CGPA)"


# =========================
# 📌 INLINE (Course Registration inside Student)
# =========================
class CourseRegistrationInline(admin.TabularInline):
    model = CourseRegistration
    extra = 1


# =========================
# 🧑‍🎓 STUDENT ADMIN
# =========================
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'student_id', 'department', 'get_gpa')
    search_fields = ('name', 'student_id', 'email')
    list_filter = ('department', 'batch')
    ordering = ('student_id',)

    inlines = [CourseRegistrationInline]

    actions = [generate_result]

    def get_gpa(self, obj):
        gpa, grade = calculate_student_gpa(obj)
        return f"{gpa} / 4.00 ({grade})"

    get_gpa.short_description = "CGPA"


# =========================
# 📚 COURSE ADMIN
# =========================
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'course_title', 'credit', 'department')
    search_fields = ('course_code', 'course_title')
    list_filter = ('department',)


# =========================
# 🧪 EXAM ADMIN
# =========================
class ExamAdmin(admin.ModelAdmin):
    list_display = ('course', 'exam_type', 'total_marks', 'weight')
    list_filter = ('exam_type', 'course')

    def save_model(self, request, obj, form, change):
        weight_map = {
            "CT": 20,
            "MID": 30,
            "FINAL": 50
        }
        obj.weight = weight_map.get(obj.exam_type, 0)
        super().save_model(request, obj, form, change)


# =========================
# 🧾 MARK ADMIN
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
    search_fields = ('student__name', 'course__course_title')

    list_editable = ('marks_obtained',)

    def exam_type_display(self, obj):
        return obj.exam.get_exam_type_display()

    def total_marks_display(self, obj):
        return obj.exam.total_marks

    exam_type_display.short_description = "Exam Type"
    total_marks_display.short_description = "Total Marks"


# =========================
# 📊 RESULT ADMIN
# =========================
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'cgpa', 'grade', 'semester')
    list_filter = ('semester',)
    search_fields = ('student__name',)

    readonly_fields = ('cgpa', 'grade')

    def save_model(self, request, obj, form, change):
        gpa, grade = calculate_student_gpa(obj.student)
        obj.cgpa = gpa
        obj.grade = grade
        super().save_model(request, obj, form, change)


# =========================
# 🏫 DEPARTMENT ADMIN
# =========================
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')


# =========================
# 🎯 REGISTER ALL
# =========================
admin.site.register(Student, StudentAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseRegistration)
admin.site.register(Exam, ExamAdmin)
admin.site.register(Mark, MarkAdmin)
admin.site.register(GradeScale)
admin.site.register(Result, ResultAdmin)