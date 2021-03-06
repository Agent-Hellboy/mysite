from django.shortcuts import render, redirect
import hashlib
import os
import random

from django.http import HttpResponse
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.files.storage import FileSystemStorage

from .models import User, File, Team
from users.forms import RegistrationForm, TeamForm
from .handle_file import file_handle


def index(request):
    return render(request, 'users/index.html')


def teaminfo(request):
    teams = Team.objects.all()
    n = len(teams)
    teams_users = []
    for i in teams:
        users = User.objects.filter(team=i)
        teams_users.append(users)
    return render(request, 'users/teaminfo.html', {'n': range(n), 'teams': teams, 'user_team': teams_users})


@login_required
def create_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You are successfully registered')
            return redirect('dashboard')
    else:
        form = TeamForm()

    return render(request, 'users/team.html', {'form': form})


def fhandle(request, name):
    path = "/".join(os.path.dirname(os.path.realpath(__file__)).split("/")[:-1])
    new_path = path + '/media/' + name
    with open(new_path) as f:
        text = f.read()
    file_handle(text)
    return redirect('dashboard')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            print(form.save())
            messages.success(request, 'You are successfully registered')
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'users/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            messages.success(request, 'You have successfully logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
    return render(request, 'users/login.html')


@login_required(login_url='/login/')
def upload(request):
    context = {}
    if request.method == "POST":
        uploaded_file = request.FILES["document"]
        if not check_title_presence(uploaded_file):
            messages.success(request, "New file save successfully.")
            path = save_on_server(uploaded_file)
            hash_val = hash_file(path)
            form = File(title=uploaded_file.name, hash_val=hash_val, user=request.user)
            form.save()
        else:
            # flash message that A similar file is already present  if hash value matches

            path = save_on_server(uploaded_file)
            hash_val = hash_file(path)
            if check_file_presence(hash_val):
                messages.warning(request, "A similar file is already present")
                os.remove(path)

            # hash value matches so no need to upload. if not, uploade it with different file name
            else:
                # save file on server with new name{version}
                title = path.split("/")[-1]
                form = File(title=title, hash_val=hash_val, user=request.user)
                form.save()
                messages.warning(
                    request,
                    "file with same name is already present adding it with new version ",
                )

    return render(request, 'users/upload.html', context)


@login_required(login_url='/login/')
def dashboard(request):
    context = {}
    file = File.objects.filter(user=request.user)
    context = {'file': file}
    print(context['file'])
    return render(request, 'users/dashboard.html', context)


def logout(request):
    auth.logout(request)
    messages.success(request, 'You have been logged out')
    return render(request, 'users/logout.html')


def hash_file(filename):
    """"This function returns the SHA-1 hash
    of the file passed into it"""

    # make a hash object
    h = hashlib.sha1()
    with open(filename, "rb") as file:

        # loop till the end of the file
        chunk = 0
        while chunk != b"":
            # read only 1024 bytes at a time
            chunk = file.read(1024)
            h.update(chunk)

    # return the hex representation of digest
    return h.hexdigest()


def check_title_presence(uploaded_file):
    """
    query database for filename and if it is present then return True else False
    """
    file = File.objects.filter(title=uploaded_file)
    if file:
        return True
    return False


def check_file_presence(hash_val):
    """

    """
    file = File.objects.filter(hash_val=hash_val)
    if file:
        return True
    return False


def save_on_server(uploaded_file):
    """

    """
    fs = FileSystemStorage()
    name = fs.save(uploaded_file.name, uploaded_file)
    url = fs.url(name)
    path = "/".join(os.path.dirname(os.path.realpath(__file__)).split("/")[:-1])
    return path + url
