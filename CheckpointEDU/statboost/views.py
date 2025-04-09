from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Assignment, Mood, Announcement, Planner
from .forms import AssignmentForm, MoodForm, PlannerForm, AnnouncementForm
from django.contrib.auth.models import Group
from django.http import HttpResponse

# Login View
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')  # Grab role from form

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Match role and redirect
            if role == "Student":
                return redirect('student_dashboard')
            elif role == "Lecturer":
                return redirect('lecturer_dashboard')
            else:
                return render(request, 'login.html', {
                    'error': "Invalid role selected for this user."
                })
        else:
            return render(request, 'login.html', {
                'error': "Invalid username or password."
            })

    return render(request, 'login.html')


# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')


# Dashboard for student
@login_required
def student_dashboard(request):
    assignments = Assignment.objects.filter(user=request.user)
    moods = Mood.objects.filter(user=request.user).order_by('-date')[:5]
    announcements = Announcement.objects.all().order_by('-date')[:5]  # Students see all announcements

    return render(request, 'student_dashboard.html', {
        'assignments': assignments,
        'moods': moods,
        'announcements': announcements
    })


# Dashboard for lecturer
@login_required
def lecturer_dashboard(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            # Associate the announcement with the lecturer
            announcement = form.save(commit=False)
            announcement.user = request.user  # Lecturers can post their own announcements
            announcement.save()
            return redirect('lecturer_dashboard')
    else:
        form = AnnouncementForm()

    announcements = Announcement.objects.filter(user=request.user).order_by('-date')  # Lecturers see their own announcements
    moods = Mood.objects.all()

    return render(request, 'lecturer_dashboard.html', {
        'form': form,
        'announcements': announcements,
        'moods': moods
    })


# View for creating assignments
@login_required
def assignment_tracker(request):
    assignments = Assignment.objects.filter(user=request.user)

    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.user = request.user  # Automatically associate the assignment with the logged-in user
            assignment.save()
            return redirect('assignment_tracker')  # Redirect back to the assignment tracker page
    else:
        form = AssignmentForm()

    return render(request, 'assignment_tracker.html', {'assignments': assignments, 'form': form})


# Mood submission
@login_required
def submit_mood(request):
    if request.method == 'POST':
        form = MoodForm(request.POST)
        if form.is_valid():
            mood = form.save(commit=False)
            mood.user = request.user
            mood.save()
            return redirect('student_dashboard')
    else:
        form = MoodForm()

    return render(request, 'submit_mood.html', {'form': form})


# Planner page for students
@login_required
def planner(request):
    planner_items = Planner.objects.filter(user=request.user)

    if request.method == 'POST':
        form = PlannerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('planner')
    else:
        form = PlannerForm()

    return render(request, 'planner.html', {
        'planner_items': planner_items,
        'form': form
    })


# Update assignment view (for both student and lecturer)
@login_required
def update_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            return redirect('assignment_tracker')
    else:
        form = AssignmentForm(instance=assignment)

    return render(request, 'update_assignment.html', {'form': form})


# Edit Announcement for Lecturers
@login_required
def update_announcement(request, announcement_id):
    # Only allow the lecturer who created it to edit
    announcement = get_object_or_404(Announcement, id=announcement_id, user=request.user)

    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            return redirect('lecturer_dashboard')
    else:
        form = AnnouncementForm(instance=announcement)

    return render(request, 'update_announcement.html', {'form': form})


# Delete Announcement for Lecturers
@login_required
def delete_announcement(request, announcement_id):
    try:
        # Only allow the lecturer who created it to delete
        announcement = get_object_or_404(Announcement, id=announcement_id, user=request.user)
        announcement.delete()
        return redirect('lecturer_dashboard')
    except Announcement.DoesNotExist:
        return redirect('lecturer_dashboard')  # If announcement doesn't exist or user tries to delete a non-owned announcement


# Delete Assignment for Students and Lecturers
@login_required
def delete_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    # Check if the logged-in user is the owner of the assignment
    if assignment.user == request.user:
        assignment.delete()  # Delete the assignment
        return redirect('assignment_tracker')  # Redirect back to the assignment tracker page
    else:
        return redirect('assignment_tracker')  # Redirect if user is not the owner (could also add an error message)


# Redirect user to the login page if they visit the root URL
def redirect_to_login(request):
    return redirect('login')
