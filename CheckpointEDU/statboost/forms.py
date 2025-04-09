from django import forms
from .models import Assignment, Mood, Planner, Announcement

# Form for creating/updating assignments
class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date', 'completed']  # Ensure 'description' is included in the form

# Form for submitting mood
class MoodForm(forms.ModelForm):
    class Meta:
        model = Mood
        fields = ['mood']  # This assumes the 'Mood' model has a 'mood' field to store the mood selection

# Form for the student planner
class PlannerForm(forms.ModelForm):
    class Meta:
        model = Planner
        fields = ['task', 'due_date', 'completed']  # Ensure this matches the 'Planner' model fields

# Form for posting announcements (Lecturer)
class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['content']  # Allows the lecturer to create announcements with just the 'content' field
