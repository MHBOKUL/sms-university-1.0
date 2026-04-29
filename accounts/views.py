from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import User, Student, Course, Department, Mark


# =========================
# 🔐 LOGIN
# =========================
def login_view(request):
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        # 🔥 SAFE CHECK
        if user is not None:
            login(request, user)

            if user.role == "admin":
                return redirect("admin_dashboard")
            elif user.role == "teacher":
                return redirect("teacher_dashboard")
            else:
                return redirect("student_dashboard")

        return render(request, "accounts/login.html", {
            "error": "Wrong username or password"
        })

    return render(request, "accounts/login.html")


# =========================
# 🔓 LOGOUT
# =========================
def logout_view(request):
    logout(request)
    return redirect("login")


# =========================
# 🧠 ADMIN DASHBOARD
# =========================
@login_required
def admin_dashboard(request):

    return render(request, "accounts/admin_dashboard.html", {
        "students": Student.objects.count(),
        "courses": Course.objects.count(),
        "departments": Department.objects.count(),
    })


# =========================
# 👨‍🏫 TEACHER DASHBOARD
# =========================
@login_required
def teacher_dashboard(request):

    return render(request, "accounts/teacher_dashboard.html")


# =========================
# 🎓 STUDENT DASHBOARD
# =========================
@login_required
def student_dashboard(request):

    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return render(request, "accounts/student_dashboard.html", {
            "error": "Student profile not found"
        })

    marks = Mark.objects.filter(student=student)

    return render(request, "accounts/student_dashboard.html", {
        "student": student,
        "marks": marks
    })