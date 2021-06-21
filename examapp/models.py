from django.db import models
from datetime import datetime
import re, bcrypt

# Create your models here.
EMAIL_REGEX = re.compile('^[_a-z0-9-]+(.[_a-z0-9-]+)@[a-z0-9-]+(.[a-z0-9-]+)(.[a-z]{2,4})$')

class UserManager(models.Manager):
    def registration_validator(self, post_data):
        errors = {}
        existing_users = User.objects.filter(email=post_data['email'])
        #length of the first name
        if len(post_data['first_name']) < 2:
            errors['first_name'] = "First name must be 2 characters or more"
        # length of last NameError
        if len(post_data['last_name']) < 2:
            errors['last_name'] = "Last name must be 2 characters or more"
        # email matches format
        if len(post_data['email'])==0:
            errors['email'] = "You must enter an email"
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Must be a valid email"
        # email is unique
        current_users = User.objects.filter(email = post_data['email'])
        if len(current_users) > 0:
            errors['duplicate'] = "Email already in use"
        # password was entered
        if len(post_data['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long"
        #matches
        if post_data['password'] != post_data['confirm_password']:
            errors['nonmatch'] = "Your password does not match"
        return errors
    
    def login_validator(self, post_data):
        errors = {}
        existing_user = User.objects.filter(email=post_data['email'])
        check = User.objects.filter(email=post_data['email'])
        if len(post_data['email']) == 0:
            errors['email'] = "Enter email"
        if len(post_data['password']) < 8:
            errors['password'] = "Enter 8 character password"
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Must be a valid email"
        if not check:
            errors['email'] = "Email has not been registered."
        elif bcrypt.checkpw(post_data['password'].encode(), existing_user[0].password.encode()) != True:
            errors['nonmatch'] = "Email and password do not match"
        return errors
    
    def update_validator(self, post_data):
        errors = {}
        if len(post_data['first_name']) == 0:
            errors['first_name'] = "Please enter a first name!"
        if len(post_data['first_name']) == 0:
            errors['first_name'] = "Please enter a last name!"
        if len(post_data['email']) == 0:
            errors['email'] = "Enter email"
        elif not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Must be a valid email"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class QuoteManager(models.Manager):
    def quote_validator(self, postData):
        errors = {}
        # check if author is more than 3
        if len(postData['author']) < 4:
            errors['author'] = "Author must be more than 3 characters!"
            # check if quote is more than 10
        if len(postData['quote']) < 11:
            errors['quote'] = "Quote must more than 10 characters long!"
        return errors

class Quote(models.Model):
    author = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name='user_quotes', on_delete=models.CASCADE)
    user_likes = models.ManyToManyField(User, related_name='liked_quotes')
    objects = QuoteManager()