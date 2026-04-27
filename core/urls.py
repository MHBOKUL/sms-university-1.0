from django.urls import path
from . import views

urlpatterns = [
    # 🏠 Dashboard
    path("dashboard/", views.dashboard, name="dashboard"),

    # 🧑‍🎓 Students
    path("students/", views.student_list, name="student_list"),

    # 📊 Results
    path("results/", views.result_list, name="result_list"),

    # 👤 Student Profile (Web view)
    path("student/<int:pk>/", views.student_profile, name="student_profile"),

    # 📄 Live Transcript Page (HTML version)
    path("student/<int:pk>/transcript/", views.student_transcript, name="student_transcript"),

    # 📥 Download Transcript (PDF)
    path("student/<int:pk>/download/", views.download_transcript, name="download_transcript"),

    # 🔍 Search
    path("search/", views.search_student, name="search_student"),
]