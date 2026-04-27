from .models import Mark, GradeScale, Result


# -----------------------------
# GRADE SYSTEM
# -----------------------------
def get_grade_and_point(total_percent):
    grades = GradeScale.objects.all()

    for g in grades:
        if g.min_marks <= total_percent <= g.max_marks:
            return g.grade, g.point

    return "F", 0.0


# -----------------------------
# GPA ENGINE (FIXED)
# -----------------------------
def calculate_student_gpa(student):
    marks = Mark.objects.filter(student=student).select_related('exam', 'course')

    courses = {}

    for m in marks:
        course = m.course

        if course not in courses:
            courses[course] = {
                "CT": None,
                "MID": None,
                "FINAL": None,
                "credit": course.credit
            }

        if m.exam.exam_type == "CT":
            courses[course]["CT"] = m
        elif m.exam.exam_type == "MID":
            courses[course]["MID"] = m
        elif m.exam.exam_type == "FINAL":
            courses[course]["FINAL"] = m

    total_points = 0
    total_credits = 0

    for course, data in courses.items():

        ct = data["CT"]
        mid = data["MID"]
        final = data["FINAL"]

        ct_score = (ct.marks_obtained / ct.exam.total_marks * 100) if ct else 0
        mid_score = (mid.marks_obtained / mid.exam.total_marks * 100) if mid else 0
        final_score = (final.marks_obtained / final.exam.total_marks * 100) if final else 0

        total_percent = (
            ct_score * 0.20 +
            mid_score * 0.30 +
            final_score * 0.50
        )

        grade, point = get_grade_and_point(total_percent)

        credit = data["credit"] or 1

        total_points += point * credit
        total_credits += credit

    if total_credits == 0:
        return 0, "F"

    return round(total_points / total_credits, 2), grade


# -----------------------------
# SAVE RESULT (FIXED - IMPORTANT)
# -----------------------------
def save_student_result(student):
    gpa, grade = calculate_student_gpa(student)

    Result.objects.update_or_create(
        student=student,
        defaults={
            "cgpa": gpa,
            "grade": grade
        }
    )


# -----------------------------
# LETTER GRADE (FOR UI)
# -----------------------------
def get_letter_grade(gpa):
    if gpa >= 3.75:
        return "A+"
    elif gpa >= 3.50:
        return "A"
    elif gpa >= 3.00:
        return "B"
    elif gpa >= 2.50:
        return "C"
    elif gpa >= 2.00:
        return "D"
    return "F"