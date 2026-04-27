from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .decorators import role_required


# ---------------- LOGIN ----------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # ROLE BASED REDIRECT
            if user.role == "admin":
                return redirect("/admin-dashboard/")
            elif user.role == "teacher":
                return redirect("/teacher-dashboard/")
            elif user.role == "student":
                return redirect("/student-dashboard/")
            else:
                return redirect("/login/")

        return render(request, "accounts/login.html", {
            "error": "Invalid credentials"
        })

    return render(request, "accounts/login.html")


# ---------------- LOGOUT ----------------
def logout_view(request):
    logout(request)
    return redirect("/login/")


# ---------------- DASHBOARDS (SECURED) ----------------

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