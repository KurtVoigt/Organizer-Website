from django.urls import path

from . import views

app_name = "organizer"
urlpatterns = [
    path('', views.index, name='index'),
    path('join', views.join, name= "join"),
    path('login', views.user_login, name = "login"),
    path('logout', views.user_logout, name = "logout"),
    path('tasks', views.tasks, name = "tasks"),
    path('budget', views.budget, name = "budget"),
    path('about', views.about, name = "about"),
    path('tasks/add', views.add, name = "add"),
    path('tasks/complete', views.tasks, name="complete"),
    path('tasks/complete/<int:id>', views.complete, name = "completeNO"),
    path('tasks/edit', views.edit, name = "edit"),
    path('tasks/edit/<int:id>', views.edit, name = "editNO"),
    path('budget/edit', views.budgetEdit, name="budgetEdit"),
    path('budget/edit/<int:id>', views.budgetEdit, name="budgetEdit"),
    path('budget/add', views.budgetAdd, name="budgetAdd"),


]