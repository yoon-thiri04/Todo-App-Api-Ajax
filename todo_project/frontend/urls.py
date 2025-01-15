from django.urls import path
from . import views
urlpatterns=[
    path('todo/',views.list, name='list'),
    path('',views.signup,name='signup'),
    path('login/',views.login,name='login'),
]