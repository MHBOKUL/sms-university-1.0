from django.shortcuts import render, get_object_or_404
from django.http import FileResponse
import os

from .models import (
    Student, Result, Mark,
    Department, Notice, Message, Event
)

from .utils import calculate_student_gpa, get_letter_grade
from .pdf_utils import generate_student_pdf


# =========================
# 🏠 DASHBOARD (FULL DYNAMIC)
# =========================
def dashboard(request):

    # GPA distribution (safe + dynamic)
    gpa_data = [
        Result.objects.filter(cgpa__gte=3.75).count(),
        Result.objects.filter(cgpa__gte=3.50, cgpa__lt=3.75).count(),
        Result.objects.filter(cgpa__gte=3.00, cgpa__lt=3.50).count(),
        Result.objects.filter(cgpa__gte=2.50, cgpa__lt=3.00).count(),
        Result.objects.filter(cgpa__gte=2.00, cgpa__lt=2.50).count(),
        Result.objects.filter(cgpa__lt=2.00).count(),
    ]

    return render(request, "dashboard.html", {
        # 📊 CORE STATS
        "students_count": Student.objects.count(),
        "results_count": Result.objects.count(),
        "departments_count": Department.objects.count(),

        # 📌 LATEST DATA
        "latest_students": Student.objects.order_by('-id')[:5],
        "notices": Notice.objects.order_by('-id')[:5] if hasattr(__import__('core.models'), 'Notice') else [],
        "messages": Message.objects.order_by('-id')[:5] if hasattr(__import__('core.models'), 'Message') else [],
        "events": Event.objects.order_by('id')[:5] if hasattr(__import__('core.models'), 'Event') else [],

        # 📈 CHART DATA
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
# 📄 TRANSCRIPT (HTML)
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
# 📥 DOWNLOAD PDF
# =========================
def download_transcript(request, pk):
    student = get_object_or_404(Student, pk=pk)

    file_path = generate_student_pdf(student)

    return FileResponse(
        open(file_path, 'rb'),
        as_attachment=True,
        filename=f"{student.student_id}_transcript.pdf"
    )


# =========================
# 🔍 SEARCH
# =========================
def search_student(request):
    q = request.GET.get("q")
    students = Student.objects.filter(name__icontains=q) if q else []

    return render(request, "search.html", {
        "students": students
    })

    from django.db.models import Count
from .models import Student, Result, Department, Notice, Message, Event


def dashboard(request):

    # 📊 GPA breakdown (REAL dynamic)
    gpa_data = [
        Result.objects.filter(cgpa__gte=3.75).count(),
        Result.objects.filter(cgpa__gte=3.50, cgpa__lt=3.75).count(),
        Result.objects.filter(cgpa__gte=3.00, cgpa__lt=3.50).count(),
        Result.objects.filter(cgpa__gte=2.50, cgpa__lt=3.00).count(),
        Result.objects.filter(cgpa__gte=2.00, cgpa__lt=2.50).count(),
        Result.objects.filter(cgpa__lt=2.00).count(),
    ]

    return render(request, "dashboard.html", {
        # 📌 COUNTS (REAL TIME)
        "students_count": Student.objects.count(),
        "results_count": Result.objects.count(),
        "departments_count": Department.objects.count(),

        # 📌 LATEST DATA
        "latest_students": Student.objects.order_by("-id")[:5],
        "notices": Notice.objects.order_by("-id")[:5],
        "messages": Message.objects.order_by("-id")[:5],
        "events": Event.objects.order_by("date")[:5],

        # 📊 CHART
        "gpa_data": gpa_data,
    })