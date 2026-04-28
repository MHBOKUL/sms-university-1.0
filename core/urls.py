from django.urls import path
from . import views

urlpatterns = [

    # 🏠 HOME / DASHBOARD
    path("", views.dashboard, name="dashboard"),

    # 🧑‍🎓 STUDENTS
    path("students/", views.student_list, name="student_list"),
    path("student/<int:pk>/", views.student_profile, name="student_profile"),

    # 📊 RESULTS
    path("results/", views.result_list, name="result_list"),

    # 🔍 SEARCH SYSTEM
    path("search/", views.search_student, name="search_student"),

    # 📄 TRANSCRIPT SYSTEM
    path("student/<int:pk>/transcript/", views.student_transcript, name="student_transcript"),
    path("student/<int:pk>/download/", views.download_transcript, name="download_transcript"),
]