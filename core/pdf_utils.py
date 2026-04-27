import os
import time
from django.conf import settings
from reportlab.pdfgen import canvas
from .models import Mark, Result


def generate_student_pdf(student):

    media_dir = settings.MEDIA_ROOT or os.path.join(settings.BASE_DIR, "media")
    os.makedirs(media_dir, exist_ok=True)

    # 🔥 UNIQUE FILE EVERY TIME (IMPORTANT FIX)
    file_name = f"{student.student_id}_{int(time.time())}.pdf"
    file_path = os.path.join(media_dir, file_name)

    c = canvas.Canvas(file_path)

    c.setFont("Helvetica-Bold", 18)
    c.drawString(120, 780, "UNIVERSITY TRANSCRIPT")

    c.setFont("Helvetica", 12)
    c.drawString(50, 740, f"Name: {student.name}")
    c.drawString(50, 720, f"ID: {student.student_id}")

    result = Result.objects.filter(student=student).first()
    if result:
        c.drawString(50, 690, f"CGPA: {result.cgpa}")
        c.drawString(50, 670, f"Grade: {result.grade}")

    y = 620
    marks = Mark.objects.filter(student=student)

    for m in marks:
        c.drawString(50, y, m.course.course_title)
        c.drawString(250, y, m.exam.exam_type)
        c.drawString(380, y, str(m.marks_obtained))
        y -= 20

    c.save()

    return file_path