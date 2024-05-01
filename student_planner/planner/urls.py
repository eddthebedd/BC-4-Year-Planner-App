from django.urls import path
from . import views
from .views import StudentDetailView

urlpatterns = [
    path('', views.StudentLandingPageView.as_view(), name='landing_student'),
    path('landing-student', views.StudentLandingPageView.as_view(), name='landing_student'),
    path('create-plan/', views.CreatePlanView.as_view(), name='create_plan'),
    path('course-plans/', views.CoursePlansView.as_view(), name='course_plans'),
    path('explore-major/', views.ExploreMajorView.as_view(), name='explore_major'),
    path("plan-semester/<int:semester_id>", views.PlanSemester.as_view(), name="detail"),
    path('admin-dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('student/<int:eagle_id>/', views.StudentDetailView.as_view(), name='student_detail'),
]