from django.urls import path
from . import views

urlpatterns = [
path('', views.index),
path('quotes', views.quotes),
path('register', views.register),
path('login', views.login),
path('logout', views.logout),
path('myaccount/<int:user_id>', views.edit_account),
path('add_quote', views.post),
path('user/<int:user_id>', views.profile),
path('user/<int:user_id>/update', views.update),
path('like/<int:id>', views.add_like),
path('<int:quote_id>/delete', views.delete_quote),
]
