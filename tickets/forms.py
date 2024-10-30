from .models import Ticket, Comment
from django import forms
from accounts.models import NewUser
from django.contrib.auth.models import User

class DateInput(forms.DateInput):
    input_type = 'date'
    
class TicketForm(forms.ModelForm):
    project = forms.ChoiceField(
        choices=NewUser.PROJECT_OPTIONS, 
        required=True, 
        label="Select Project", 
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Ticket
        fields = ['project', 'assignee', 'title', 'description', 'priority', 'category', 'status', 'due_date']
        widgets = {
            'due_date': DateInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        self.fields['project'].empty_label = "Select the project"
        self.fields['assignee'].empty_label = "Select assignee"
        self.fields['assignee'].widget = forms.Select(attrs={'class': 'form-control'})
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['priority'].widget.attrs.update({'class': 'form-control'})
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['status'].widget.attrs.update({'class': 'form-control'})
        self.fields['due_date'].widget.attrs.update({'class': 'form-control'})
        
        # Limit assignee choices based on selected project
        if 'project' in self.data:
            selected_project = self.data.get('project')
            users_with_project = NewUser.objects.filter(project=selected_project).values_list('user', flat=True)
            self.fields['assignee'].queryset = User.objects.filter(id__in=users_with_project)
        else:
            self.fields['assignee'].queryset = User.objects.none()  # No users initially

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs.update({'class': 'form-control'})