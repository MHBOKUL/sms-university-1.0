from django.contrib import admin
from .models import User, Department, Course, Student, Mark, Result


# =========================
# 👤 USER ADMIN
# =========================
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role")
    list_filter = ("role",)


# =========================
# 🏫 DEPARTMENT
# =========================
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


# =========================
# 📚 COURSE
# =========================
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "department")
    list_filter = ("department",)
    search_fields = ("name",)


# =========================
# 🎓 STUDENT
# =========================
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "department")
    list_filter = ("department",)


# =========================
# 📝 MARK
# =========================
@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "score")
    list_filter = ("course", "student")


# =========================
# 📊 RESULT
# =========================
@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("student", "gpa", "updated_at")