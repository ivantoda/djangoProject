from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class RolesEnum(models.TextChoices):
    Admin = 'administrator'
    Student = 'student'
    Profesor = 'profesor'
    Nema = 'none'

class CustomUser(AbstractUser):
    pass
    role = models.CharField(max_length=64, choices = RolesEnum.choices, default = RolesEnum.Nema)

class Document(models.Model):
    title = models.CharField(max_length=200)
    path = models.CharField(max_length=200)
    created = models.DateTimeField()
    creator = models.ForeignKey(CustomUser, on_delete=models.SET_DEFAULT, null=True, default=None)
    
    def __str__(self):
        return '%s %s %s' %(self.title, self.path, self.created, self.creator)

class Student_Document(models.Model):
    student_id = models.ForeignKey(CustomUser, limit_choices_to={'role': 'student'}, on_delete=models.CASCADE)
    document_id = models.ForeignKey(Document, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s' %(self.student_id, self.document_id)