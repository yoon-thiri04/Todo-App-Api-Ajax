from django.urls import path
from . import views
urlpatterns=[
path('task-list/',views.taskList,name='task-list'),
    path('task-create/',views.taskCreate,name='task-create'),
    path('task-detail/<int:pk>/',views.taskDetail,name='task-detail'),
    path('task-update/<int:pk>/',views.taskUpdate,name='task-update'),
    path('task-delete/<int:pk>/',views.taskDelete,name='task-delete'),
    path('signup/',views.signUp,name='signup'),
    path('user-list',views.userList,name='user-list'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),

]