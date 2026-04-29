from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse
from django.db.models import Count
from django.contrib.auth.decorators import login_required

import os

from .models import (
    Student, Result, Mark,
    Department, Course,
    Notice, Message, Event
)

from .utils import calculate_student_gpa, get_letter_grade
from .pdf_utils import generate_student_pdf
from accounts.decorators import role_required
import json

# =========================
# 🏠 DASHBOARD (ONLY ONE)
# =========================
def dashboard(request):

    gpa_labels = ["A+", "A", "B", "C", "D", "F"]

    gpa_data = [
        Result.objects.filter(cgpa__gte=3.75).count(),
        Result.objects.filter(cgpa__gte=3.50, cgpa__lt=3.75).count(),
        Result.objects.filter(cgpa__gte=3.00, cgpa__lt=3.50).count(),
        Result.objects.filter(cgpa__gte=2.50, cgpa__lt=3.00).count(),
        Result.objects.filter(cgpa__gte=2.00, cgpa__lt=2.50).count(),
        Result.objects.filter(cgpa__lt=2.00).count(),
    ]

    return render(request, "dashboard.html", {
        "students_count": Student.objects.count(),
        "results_count": Result.objects.count(),
        "departments_count": Department.objects.count(),

        "latest_students": Student.objects.order_by("-id")[:5],
        "notices": Notice.objects.order_by("-id")[:5],
        "messages": Message.objects.order_by("-id")[:5],
        "events": Event.objects.order_by("-id")[:5],

        "gpa_labels": gpa_labels,   # 🔥 THIS LINE WAS MISSING
        "gpa_data": gpa_data,
    })


# =========================
# 🧑‍🎓 STUDENT LIST
# =========================
def student_list(request):
    return render(request, "students.html", {
        "students": Student.objects.all()
    })


# =========================
# 📊 RESULT LIST
# =========================
def result_list(request):
    return render(request, "results.html", {
        "results": Result.objects.select_related("student")
    })


# =========================
# 👤 STUDENT PROFILE
# =========================
def student_profile(request, pk):

    student = get_object_or_404(Student, pk=pk)

    marks = Mark.objects.filter(student=student).select_related("course", "exam")

    gpa, _ = calculate_student_gpa(student)
    grade = get_letter_grade(gpa)

    return render(request, "student_profile.html", {
        "student": student,
        "marks": marks,
        "gpa": gpa,
        "grade": grade
    })


# =========================
# 📄 TRANSCRIPT VIEW
# =========================
def student_transcript(request, pk):

    student = get_object_or_404(Student, pk=pk)

    marks = Mark.objects.filter(student=student).select_related("course", "exam")

    gpa, _ = calculate_student_gpa(student)
    grade = get_letter_grade(gpa)

    return render(request, "student_transcript.html", {
        "student": student,
        "marks": marks,
        "gpa": gpa,
        "grade": grade
    })


# =========================
# 📥 PDF DOWNLOAD
# =========================
def download_transcript(request, pk):

    student = get_object_or_404(Student, pk=pk)

    file_path = generate_student_pdf(student)

    return FileResponse(
        open(file_path, "rb"),
        as_attachment=True,
        filename=f"{student.student_id}_transcript.pdf"
    )


# =========================
# 🔍 SEARCH STUDENT
# =========================
def search_student(request):

    q = request.GET.get("q")

    students = Student.objects.filter(name__icontains=q) if q else []

    return render(request, "search.html", {
        "students": students
    })


# =========================
# 📚 ADD COURSE (FIXED)
# =========================
@login_required
@role_required("teacher")
def add_course(request):

    departments = Department.objects.all()

    dept_id = request.GET.get("department")

    courses = Course.objects.all()

    if dept_id:
        courses = courses.filter(department_id=dept_id)

    if request.method == "POST":
        Course.objects.create(
            course_code=request.POST.get("course_code"),
            course_title=request.POST.get("course_title"),
            credit=request.POST.get("credit"),
            department_id=request.POST.get("department")
        )

        return redirect(f"/course/add/?department={request.POST.get('department')}")

    return render(request, "accounts/add_course.html", {
        "departments": departments,
        "courses": courses,
        "dept_id": dept_id
    })