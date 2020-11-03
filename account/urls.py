from django.urls import path
from .views import *

app_name = 'account'

urlpatterns = [
    path('', login, name='login'),
    path('signup/', login, name='login'),
    path('login_validate/', login_validate, name='login_validate'),
    path('index/', index, name='index'),
]
