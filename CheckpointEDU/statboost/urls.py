from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboards
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('lecturer_dashboard/', views.lecturer_dashboard, name='lecturer_dashboard'),
    
    # Assignments
    path('assignments/create/', views.assignment_tracker, name='create_assignment'),  # Create assignment
    path('assignments/all/', views.assignment_tracker, name='assignment_tracker_all'),  # View assignments
    path('assignment-tracker/', views.assignment_tracker, name='assignment_tracker'),  # Added this line
    path('assignments/update/<int:assignment_id>/', views.update_assignment, name='update_assignment'),
    path('assignments/delete/<int:assignment_id>/', views.delete_assignment, name='delete_assignment'),

    # Announcements
    path('announcement/update/<int:announcement_id>/', views.update_announcement, name='update_announcement'),
    path('announcement/delete/<int:announcement_id>/', views.delete_announcement, name='delete_announcement'),

    # Mood submission
    path('submit-mood/', views.submit_mood, name='submit_mood'),

    # Planner page (new)
    path('planner/', views.planner, name='planner'),  # Update this line to match the view name

    # Root URL (redirect to login)
    path('', views.redirect_to_login, name='redirect_to_login'),
]
