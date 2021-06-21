from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.
def index(request):
    return render(request, 'index.html')

def quotes(request):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.filter(id=request.session['user_id'])
    context = {
        'user': this_user[0],
        'quotes': Quote.objects.all()
    }
    return render(request, 'quotes.html', context)

def register(request):
    if request.method == 'POST':
        errors = User.objects.registration_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
    # hash password
        hashed_pw = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt()).decode()
    # create User
        new_user = User.objects.create(
            first_name=request.POST['first_name'], last_name=request.POST[
                'last_name'], email=request.POST['email'], password=hashed_pw
        )
    # create session
        request.session['user_id'] = new_user.id
        return redirect('/quotes')
    return redirect('/')

def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        this_user = User.objects.filter(email=request.POST['email'])
        request.session['user_id'] = this_user[0].id
        return redirect('/quotes')
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def post(request):
    errors = Quote.objects.quote_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/quotes')
    Quote.objects.create(author = request.POST['author'], message=request.POST['quote'], poster=User.objects.get(id=request.session['user_id']))
    return redirect('/quotes')

def profile(request, user_id):
    context = {
        'user': User.objects.get(id=user_id),
        'logged_in': User.objects.get(id=request.session['user_id'])
    }
    
    return render(request, 'profile.html', context)

def edit_account(request, user_id):
    context = {
        'user': User.objects.get(id=user_id)
    }
    return render(request, 'editprofile.html', context)

def update(request, user_id):
    errors = User.objects.update_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/myaccount/{user_id}')
    to_update = User.objects.get(id=user_id)
    to_update.first_name = request.POST['first_name']
    to_update.last_name = request.POST['last_name']
    to_update.email = request.POST['email']
    to_update.save()
    return redirect(f'/user/{user_id}')

def add_like(request, id):
    liked_quote = Quote.objects.get(id=id)
    user_liking = User.objects.get(id=request.session['user_id'])
    liked_quote.user_likes.add(user_liking)
    return redirect('/quotes')

def delete_quote(request, quote_id):
    to_delete = Quote.objects.get(id=quote_id)
    to_delete.delete()
    return redirect('/quotes')