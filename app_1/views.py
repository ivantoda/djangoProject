import datetime
import os
from django.shortcuts import render
from app_1.forms import DocumentForm, UserForm
from app_1.models import Document, RolesEnum, Student_Document, CustomUser
from django.contrib.auth import login, logout
from django.http import *
from django.shortcuts import redirect
from django.core.paginator import Paginator
from app_1.validate import Validate
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import make_password
from app_1.decorators import admin_auth_required, profesor_auth_required, student_auth_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from projekt.settings import MEDIA_ROOT

def index_view(request):
    return render(request, 'index.html')

def login_view(request):
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = Validate.authenticate_user(username, password)
        print(user)
        if user is not None:
            if user.is_active:
                login(request, user)
                user_object = CustomUser.objects.get(username=username)
                role = user_object.role
                id = user_object.id
                return redirect(role, id=id)
        return render(request, 'login.html', {"message" : 'neispravni podaci, pokušajte ponovno'})
    return render(request, 'login.html')
def logout_view(request):
    logout(request)
    return redirect('login')

@admin_auth_required
def add_user(request):
    admin_id = request.user.id
    if request.method == 'GET':
        form = UserForm()
        return render(request, 'add_user.html', {"form" : form, "admin_data" : admin_id})
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.date_joined = datetime.datetime.now() 
            input_password = new_user.password
            new_user.password = make_password(input_password,salt=None, hasher='default')
            new_user.save()
            form.save_m2m()
            print("User added")
        else:
            error_message = 'Error! Provjerite sve podatke'
            messages.error(request, error_message)
            return render(request, 'add_user.html', {"form" : form, "admin_data" : admin_id})
        return redirect(RolesEnum.Admin, id=admin_id)
    
@admin_auth_required
def admin_view(request, id):
    admin_id = request.user.id
    admin = CustomUser.objects.get(pk=admin_id)
    
    filtering_method = request.GET.get('select_filtering')
    if filtering_method is None:
        users = CustomUser.objects.all()
    else:
        users = CustomUser.objects.filter(role=filtering_method)
    
    paginator = Paginator(users, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin_index.html', {"admin_data" : admin, "user_data" : page_obj})

@admin_auth_required
def update_user(request, id):
    admin_id = request.user.id
    existing_user = CustomUser.objects.get(pk=id)
    if request.method == 'GET':
        form = UserForm(instance=existing_user)
        return render(request, 'update_user.html', {"form" : form, "admin_data" : admin_id})
    elif request.method == 'POST':
        form = UserForm(request.POST, instance=existing_user)
        if form.is_valid():
            input_password = existing_user.password
            existing_user.password = make_password(input_password,salt=None, hasher='default')
            form.save()
        return redirect(RolesEnum.Admin, id=admin_id) 

@admin_auth_required
def delete_user(request, id):
    ad_id = request.user.id
    user = CustomUser.objects.get(pk=id)
    user.delete()
    return redirect(RolesEnum.Admin, id=ad_id)

@profesor_auth_required
def profesor_view(request, id):
    profesor_id = request.user.id
    profesor = CustomUser.objects.get(pk=profesor_id)
    sorting_order = request.GET.get('order', 'date_asc')

    if sorting_order == 'date_asc':
        documents = Document.objects.filter(creator_id=profesor_id).order_by('created')
    elif sorting_order == 'date_desc':
        documents = Document.objects.filter(creator_id=profesor_id).order_by('-created')
    else:
        documents = Document.objects.filter(creator_id=profesor_id).order_by('created')

    paginator = Paginator(documents, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'profesor_index.html', {"profesor_data" : profesor, "document_data" : page_obj})


@profesor_auth_required
def add_document(request):
    profesor_id = request.user.id
    
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        
        if form.is_valid():
            doc = form.save(commit=False)
            doc.created = datetime.datetime.now()
            doc.creator_id = profesor_id
            
            request_file = request.FILES.get('document')
            
            if request_file:
                
                if not request_file.name.endswith('.txt'):
                    return HttpResponseBadRequest("Samo .txt datoteke su dozovljene.")
                
                fs = FileSystemStorage(location=MEDIA_ROOT)
                new_file = fs.save(request_file.name, request_file)
                fileurl = fs.url(new_file)
                doc.path = fileurl
                doc.save()
                form.save_m2m()
                return redirect(RolesEnum.Profesor, id=profesor_id)
            else:
                return HttpResponseBadRequest("Niste odabrali datoteku.")
    else:
        form = DocumentForm()

    return render(request, 'add_document.html', {"form": form, "profesor_data": profesor_id})

    
@profesor_auth_required
def update_document(request, id):
    profesor_id = request.user.id
    existing_document = Document.objects.get(pk=id)
    if request.method == 'GET':
        form = DocumentForm(instance=existing_document)
        return render(request, 'update_document.html', {"form" : form, "profesor_data" : profesor_id})
    elif request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=existing_document)
        if form.is_valid():
            new_document = form.save(commit=False)

            request_file = request.FILES['document'] if 'document' in request.FILES else None

            if request_file:
                fs = FileSystemStorage(location=MEDIA_ROOT)
                new_file = fs.save(request_file.name, request_file)
                fileurl = os.path.join(MEDIA_ROOT, new_file)
                fileurl = fileurl.replace("\\", "/").replace("%20", " ").replace("%23", "#")
                new_document.path = fileurl
                print(fileurl)

                print(existing_document.path)
                old_file_path = os.path.normpath(os.path.join(MEDIA_ROOT, existing_document.path[7:].replace("%20", " ")))
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)

            new_document.save()
        return redirect(RolesEnum.Profesor, id=profesor_id)

@profesor_auth_required
def delete_document(request, id):
    profesor_id = request.user.id
    doc = Document.objects.get(pk=id)
    try:
        file_path = os.path.normpath(os.path.join(MEDIA_ROOT, doc.path.lstrip('/')))
        if os.path.exists(file_path):
            os.remove(file_path)
            doc.delete()
        else:
            print(f"Datoteke ne postoji: {file_path}")
    except Exception as e:
        print(f"Error pri brisanju datoteke: {str(e)}")
    return redirect(RolesEnum.Profesor, id=profesor_id)


@profesor_auth_required
def share_document(request, id):
    profesor_id = request.user.id
    document = Document.objects.get(pk=id)
    students = CustomUser.objects.filter(role='student')
    relationships = Student_Document.objects.filter(document_id=id)
    checked_students = [relationship.student_id for relationship in relationships]

    if request.method == "POST":
        new_checked_students_id = [int(student_id) for student_id in request.POST.getlist('student_checkbox')]
        
        for relationship in relationships:
            if relationship.student_id not in new_checked_students_id:
                relationship.delete()
        
        for student_id in new_checked_students_id:
            if not relationships.filter(student_id=student_id).exists():
                student = get_object_or_404(CustomUser, pk=student_id, role='student')
                relationship = Student_Document(student_id=student, document_id=document)
                relationship.save()

        return redirect(RolesEnum.Profesor, id=profesor_id)
    
    return render(request, 'share_document.html', {"profesor_data": profesor_id, "document_data": document, "student_data": students, "checked_students": checked_students})

@student_auth_required
def student_view(request, id):
    st_id = request.user.id
    student = CustomUser.objects.get(pk=st_id)
    relations = Student_Document.objects.filter(student_id_id=st_id)
    professors = CustomUser.objects.filter(role='profesor')
    
    filtering_method = request.GET.get('select_filtering')
    filter_by_prof = CustomUser.objects.filter(username=filtering_method).first()
    documents = []
    for r in relations:
        document = Document.objects.get(pk=r.document_id_id)
        if filter_by_prof is None:
            documents.append(document)
        elif filter_by_prof is not None:
            if document.creator_id == filter_by_prof.id:
                documents.append(document)
    
    sorting_order = request.GET.get('order', 'date_asc')
    if sorting_order == 'title_asc':
        documents = sorted(documents, key=lambda doc: doc.title)
    elif sorting_order == 'title_desc':
        documents = sorted(documents, key=lambda doc: doc.title, reverse=True)
    elif sorting_order == 'date_asc':
        documents = sorted(documents, key=lambda doc: doc.created)
    elif sorting_order == 'date_desc':
        documents = sorted(documents, key=lambda doc: doc.created, reverse=True)
    else:
        documents = sorted(documents, key=lambda doc: doc.created)
    
    paginator = Paginator(documents, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'student_index.html', {"student_data" : student, "document_data" : page_obj, "profesor_data" : professors})

@student_auth_required
def download_file(request, file_path):

    file_path = os.path.join(MEDIA_ROOT, file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="text/plain")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

@profesor_auth_required
def ispit(request):
    data = []
    profesor_id = request.user.id
    documents = Document.objects.filter(creator_id=profesor_id)
    shared = 0
    not_shared = 0
    for d in documents:
        if Student_Document.objects.filter(document_id = d).count() > 0:
            shared = shared + 1
        else:
            not_shared = not_shared + 1

    data.append({
        'created' : documents.count(),
        'shared': shared,
        'not_shared': not_shared,
        'documents': documents
    })
    return render(request, 'test.html', {'docs': data})

@profesor_auth_required
def ispit2(request):
    profesor_id = request.user.id
    Documents = Document.objects.filter(creator_id = profesor_id)
    return render(request, 'test2.html', {'documenst': Documents})