from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound
# from django.contrib.auth import authenticate
from .forms import Login, Create, ContentStatus
from app.models import Content, Book
from .models import Moderator
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login
# from django.contrib.auth import authenticate, login
from .authentication import ModeratorBackend
# Create your views here.
# def authenticate(request, username=None, password=None):
#     try:
#         email = username
#         moderator = Moderator.objects.get(email=email)
#         if check_password(password, moderator.password):
#             return moderator
#     except Moderator.DoesNotExist:
#         return None
#     return None

# def login(request, user):
#     request.session['uid'] = user.id;

# Admin Login
def login_view(request):
    if request.method == 'POST':
        form = Login(request.POST)

        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            mod = authenticate(request, username=email, password=password)
            if mod is not None:
                login(request, mod)
                return HttpResponseRedirect('/admin/dashboard')
            else:
                return HttpResponseRedirect('/admin/login')
    else:
        form = Login()
    return render(request, 'form.html', {'form': form})

# Admin Add
def create_view(request):
    if request.method == 'POST':
        form = Create(request.POST)

        if form.is_valid():
            return HttpResponseRedirect('/admin/dashboard')
    else:
        form = Create()
    return render(request, 'form.html', {'form': form})


# View Content Table
def list_unpublished_content(request):
    if request.method == 'POST':
        form = ContentStatus(request.POST)

        if form.is_valid():
            try:
                content = Content.objects.get(id=request.POST['id'])
                if request.POST['status'] == 'publish':
                    content.active = True
                    content.save()
            except Content.DoesNotExist:
                return HttpResponseNotFound()
            return HttpResponseRedirect('/admin/unpublished-content-list')
    else:
        content = Content.objects(active=False)
        return render(request, 'list.html', {'content' : content , 'published': False})

def list_published_content(request):
    if request.method == 'POST':
        form = ContentStatus(request.POST)

        if form.is_valid():
            try:
                content = Content.objects.get(id=request.POST['id'])
                if request.POST['status'] == 'unpublish':
                    content.active = False
                    content.save()
            except Content.DoesNotExist:
                return HttpResponseNotFound()
            return HttpResponseRedirect('/admin/published-content-list')
    else:
        content = Content.objects(active=False)
        return render(request, 'list.html', {'content' : content, 'published': True})

def list_published_book(request):
    if request.method == 'POST':
        form = ContentStatus(request.POST)

        if form.is_valid():
            try:
                book = Book.objects.get(id=request.POST['id'])
                if request.POST['status'] == 'unpublish':
                    book.active = False
                    book.save()
            except Book.DoesNotExist:
                return HttpResponseNotFound()
            return HttpResponseRedirect('/admin/published-book-list')
    else:
        book = Book.objects(active__ne=False)
        return render(request, 'list.html', {'book' : book, 'published': True})

def list_unpublished_book(request):
    if request.method == 'POST':
        form = ContentStatus(request.POST)

        if form.is_valid():
            try:
                book = Book.objects.get(id=request.POST['id'])
                if request.POST['status'] == 'publish':
                    book.active = True
                    book.save()
            except Book.DoesNotExist:
                return HttpResponseNotFound()
            return HttpResponseRedirect('/admin/unpublished-book-list')
    else:
        book = Book.objects(active=False)
        return render(request, 'list.html', {'book' : book, 'published': False})