from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Record
from website.forms import RegistrationForm, AddRecordForm


def home(request):
    records = Record.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in.')
        else:
            messages.success(request, 'There was some error while logging in, Please try again.')
        return redirect('home')
    else:
        return render(request, 'home.html', {'records':records})

def login_user(request):
    pass

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')
    
    
def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and Login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username, password = password)
            login(request, user)
            messages.success(request, 'You have been successfuly registered.')
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form':form})

def customer_record(request, id):
    if request.user.is_authenticated:
        record = Record.objects.get(id=id)
        return render(request, 'record.html', {'record':record})
    else:
        messages.success(request, 'You are not logged in.')
        return redirect('home')
    

def delete_record(request, id):
    if request.user.is_authenticated:
        record = Record.objects.get(id=id)
        record.delete()
        messages.success(request, 'Record deleted.')
        return redirect('home')
    else:
        messages.success(request, 'You need to be logged in to delete record.')
        return redirect('home')
    

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if not request.user.is_authenticated:
        messages.success(request, 'You are not logged in.')
        return redirect('home')
    if request.method == 'POST':
        if form.is_valid():
            record = form.save()
            messages.success(request, 'Record added.')
            return redirect('home')
        else:
            messages.success(request,'Please enter valid data')
            redirect('add')
    else:
        return render(request, 'add_record.html', {'form':form})