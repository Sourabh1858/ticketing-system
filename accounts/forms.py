from django import forms
from django.contrib.auth.models import User
from .models import NewUser

class LoginForm(forms.Form):
    fields = ['username', 'password']
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
class ProfileForm(forms.Form):
    fields = ['username', 'email']
    username = forms.CharField(
        max_length=150, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )
    email = forms.EmailField(
        max_length=150, 
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    project = forms.CharField(
        max_length=255,  # Adjust max_length according to your model
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )
    
class PasswordChangeForm(forms.Form):
    fields = ['old_password', 'new_password', 'confirm_password']
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        if new_password != confirm_password:
            raise forms.ValidationError('New password and confirm password do not match.')
        return cleaned_data

# class UserRegistrationForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

#     class Meta:
#         model = User
#         fields = ['username', 'password','project','email']
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-control'}),
#             'project': forms.TextInput(attrs={'class': 'form-control'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control'}),
#         }

#     def clean_password(self):
#         password = self.cleaned_data.get('password')
#         if len(password) < 8:
#             raise forms.ValidationError('Password must be at least 8 characters long.')
#         return password
# class UserRegistrationForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#     projects = forms.ModelMultipleChoiceField(
#         queryset=Project.objects.all(),
#         widget=forms.CheckboxSelectMultiple,
#         required=True  # Make it required or optional as per your needs
#     )

#     class Meta:
#         model = User
#         fields = ['username', 'password', 'email']  # Exclude 'projects' from User fields
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-control'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control'}),
#         }

#     def clean_password(self):
#         password = self.cleaned_data.get('password')
#         if len(password) < 8:
#             raise forms.ValidationError('Password must be at least 8 characters long.')
#         return password

#     def save(self, commit=True):
#         # First, save the user instance
#         user = super(UserRegistrationForm, self).save(commit=False)
#         user.set_password(self.cleaned_data['password'])  # Set the hashed password
#         if commit:
#             user.save()  # Save the user to the database

#             # Now create the NewUser instance
#             new_user_instance = NewUser.objects.create(user=user)  # Create NewUser instance

#             # Add selected projects to the new_user_instance
#             new_user_instance.projects.set(self.cleaned_data['projects'])

#         return user
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'password', 'email']  # Do not include 'project' here
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long.')
        return password