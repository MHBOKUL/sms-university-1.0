from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .decorators import role_required


def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )

        if user:
            login(request, user)

            if user.role == "admin":
                return redirect("/admin-dashboard/")
            elif user.role == "teacher":
                return redirect("/teacher-dashboard/")
            else:
                return redirect("/student-dashboard/")

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("/login/")


@login_required
@role_required("admin")
def admin_dashboard(request):
    return render(request, "accounts/admin_dashboard.html")


@login_required
@role_required("teacher")
def teacher_dashboard(request):
    return render(request, "accounts/teacher_dashboard.html")


@login_required
@role_required("student")
def student_dashboard(request):
    return render(request, "accounts/student_dashboard.html")