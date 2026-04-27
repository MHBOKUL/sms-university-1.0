from django.shortcuts import render, get_object_or_404
from django.http import FileResponse
import os

from .models import Student, Result, Mark
from .utils import calculate_student_gpa, get_letter_grade
from .pdf_utils import generate_student_pdf


# =========================
# 🏠 DASHBOARD
# =========================
def dashboard(request):
    students_count = Student.objects.count()
    results_count = Result.objects.count()

    latest_students = Student.objects.select_related('department').order_by('-id')[:5]

    # GPA distribution (REAL DATA)
    a_plus = Result.objects.filter(cgpa__gte=3.75).count()
    a = Result.objects.filter(cgpa__gte=3.50, cgpa__lt=3.75).count()
    b = Result.objects.filter(cgpa__gte=3.00, cgpa__lt=3.50).count()
    c = Result.objects.filter(cgpa__gte=2.50, cgpa__lt=3.00).count()
    d = Result.objects.filter(cgpa__gte=2.00, cgpa__lt=2.50).count()
    f = Result.objects.filter(cgpa__lt=2.00).count()

    return render(request, "dashboard.html", {
        "students_count": students_count,
        "results_count": results_count,
        "latest_students": latest_students,
        "gpa_data": [a_plus, a, b, c, d, f]
    })


# =========================
# 🧑‍🎓 STUDENT LIST
# =========================
def student_list(request):
    students = Student.objects.select_related('department').all()

    return render(request, "students.html", {
        "students": students
    })


# =========================
# 📊 RESULT LIST
# =========================
def result_list(request):
    results = Result.objects.select_related('student')

    return render(request, "results.html", {
        "results": results
    })


# =========================
# 👤 STUDENT PROFILE
# =========================
def student_profile(request, pk):
    student = get_object_or_404(
        Student.objects.select_related('department'),
        pk=pk
    )

    marks = Mark.objects.filter(student=student).select_related('course', 'exam')

    gpa, _ = calculate_student_gpa(student)
    letter = get_letter_grade(gpa)

    return render(request, "student_profile.html", {
        "student": student,
        "marks": marks,
        "gpa": gpa,
        "grade": letter
    })


# =========================
# 📄 LIVE TRANSCRIPT (HTML)
# =========================
def student_transcript(request, pk):
    student = get_object_or_404(
        Student.objects.select_related('department'),
        pk=pk
    )

    marks = Mark.objects.filter(student=student).select_related('course', 'exam')

    gpa, _ = calculate_student_gpa(student)
    letter = get_letter_grade(gpa)

    return render(request, "student_transcript.html", {
        "student": student,
        "marks": marks,
        "gpa": gpa,
        "grade": letter
    })


# =========================
# 📄 DOWNLOAD TRANSCRIPT (PDF FIXED)
# =========================
def download_transcript(request, pk):
    student = get_object_or_404(Student, pk=pk)

    file_path = generate_student_pdf(student)

    # 🔥 safety check
    if not os.path.exists(file_path):
        raise FileNotFoundError("PDF generation failed")

    response = FileResponse(open(file_path, 'rb'), as_attachment=True)

    # 💣 CACHE FIX (IMPORTANT)
    response["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"

    response["Content-Disposition"] = (
        f'attachment; filename="{student.student_id}_transcript.pdf"'
    )

    return response


# =========================
# 🔍 SEARCH STUDENT
# =========================
def search_student(request):
    query = request.GET.get("q")

    students = Student.objects.filter(name__icontains=query) if query else []

    return render(request, "search.html", {
        "students": students,
        "query": query
    })