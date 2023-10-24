from django.forms import ModelForm, Form
from .models import Document, CustomUser

class DocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = ['title']

class UserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'role']