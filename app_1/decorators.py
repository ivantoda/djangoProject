from .models import RolesEnum
from django.shortcuts import redirect

def admin_auth_required(function):
    def wrap(*args, **kwargs):
        if args[0].user.role == RolesEnum.Admin:
            return function(*args, **kwargs)
        else:
            return redirect('login')
    return wrap

def profesor_auth_required(function):
    def wrap(*args, **kwargs):
        if args[0].user.role == RolesEnum.Profesor:
            return function(*args, **kwargs)
        else:
            return redirect('login')
    return wrap

def student_auth_required(function):
    def wrap(*args, **kwargs):
        if args[0].user.role == RolesEnum.Student:
            return function(*args, **kwargs)
        else:
            return redirect('login')
    return wrap