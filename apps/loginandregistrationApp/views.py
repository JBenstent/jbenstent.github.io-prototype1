from django.shortcuts import render, redirect
import re
import bcrypt
from django.contrib import messages

from .models import User


def index(request):

    return render(request, 'index.html')

def register(request):

    if request.method == 'POST':
        check = True

        errors = []

        if len(request.POST['password']) < 8:
            messages.add_message(request, messages.ERROR, 'invalid password')
            check = False

        if request.POST['confirmpw'] != request.POST['password']:
            messages.add_message(request, messages.ERROR, 'Passwords do not match')
            check = False

        if len(request.POST['first_name']) == 0:
            messages.add_message(request, messages.ERROR, 'First name cannot be blank')
            check = False

        if len(request.POST['last_name']) == 0:
            messages.add_message(request, messages.ERROR, 'Last name cannot be blank')
            check = False

        if check ==  True:
            hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(password=hashed, first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'])

        context = {
        'errors': errors
        }

    return redirect('/')

def login(request):

    error1 = []
    try:
        user = User.objects.get(email=request.POST['email'])
        if bcrypt.hashpw(request.POST['password'].encode(), user.password.encode()) == user.password:
            return render(request, 'successful.html')
        else:
            messages.add_message(request, messages.ERROR, 'Invalid login')

    except:
        messages.add_message(request, messages.ERROR, 'Invalid login')
        return redirect('/')

    context = {
    'error1': error1
    }

    return redirect('/')
