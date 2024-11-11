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


# class EditTicketForm(forms.ModelForm):
#     project = forms.CharField(
#         disabled=True, 
#         label="Project", 
#         required=False,
#         widget=forms.TextInput(attrs={'class': 'form-control'})
#     )

#     class Meta:
#         model = Ticket
#         fields = [ 'assignee','title', 'description', 'priority', 'category', 'status', 'due_date']
#         widgets = {
#             'assignee': forms.Select(attrs={'disabled': 'disabled', 'class': 'form-control'}),
#             'title': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
#             'description': forms.Textarea(attrs={'readonly': 'readonly', 'class': 'form-control'}),
#             'priority': forms.Select(attrs={'disabled': 'disabled', 'class': 'form-control'}),
#             'category': forms.Select(attrs={'disabled': 'disabled', 'class': 'form-control'}),
#             'status': forms.Select(attrs={'class': 'form-control'}),  # Editable and required
#             'due_date': forms.DateInput(attrs={'readonly': 'readonly', 'type': 'date', 'class': 'form-control'}),
            
#         }

#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)
#         super().__init__(*args, **kwargs)
        
#         # Populate the project field based on the NewUser model
#         if user:
#             new_user_instance = NewUser.objects.filter(user=user).first()
#             self.fields['project'].initial = new_user_instance.project if new_user_instance else "No Project Assigned"
        
#         # Make fields optional except 'status'
#         for field_name, field in self.fields.items():
#             if field_name != 'status':
#                 field.required = False
        
#         # Set field order to have 'project' above 'title'
#         self.order_fields(['project', 'assignee', 'title', 'description', 'priority', 'category', 'status', 'due_date'])
class EditTicketForm(forms.ModelForm):
    project = forms.CharField(
        disabled=True, 
        label="Project", 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Ticket
        fields = ['assignee', 'title', 'description', 'priority', 'category', 'status', 'due_date']
        widgets = {
            'assignee': forms.Select(attrs={'disabled': 'disabled', 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'readonly': 'readonly', 'class': 'form-control'}),
            'priority': forms.Select(attrs={'disabled': 'disabled', 'class': 'form-control'}),
            'category': forms.Select(attrs={'disabled': 'disabled', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),  # Editable and required
            'due_date': forms.DateInput(attrs={'readonly': 'readonly', 'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        ticket = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        # Set project field based on the assignee's project or display "No Project Assigned" if none
        if ticket and ticket.assignee:
            assignee = ticket.assignee
            new_user_instance = NewUser.objects.filter(user=assignee).first()
            self.fields['project'].initial = new_user_instance.project if new_user_instance else "No Project Assigned"
        
        # If the user is a superuser and the ticket does not belong to them, show the assignee's project
        if user and user.is_superuser and ticket and ticket.assignee != user:
            assignee = ticket.assignee
            new_user_instance = NewUser.objects.filter(user=assignee).first()
            self.fields['project'].initial = new_user_instance.project if new_user_instance else "No Project Assigned"
        
        # Make fields optional except 'status'
        for field_name, field in self.fields.items():
            if field_name != 'status':
                field.required = False
        
        # Set field order to have 'project' above 'title'
        self.order_fields(['project', 'assignee', 'title', 'description', 'priority', 'category', 'status', 'due_date'])
