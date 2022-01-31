from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from .forms import JoinForm, LoginForm, TaskForm,BudgetForm
from .models import Task, Budget
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Create your views here.
@login_required(login_url='organizer:login')
def index(request):
    if(request.method == "GET"):
        task_data = Task.objects.filter(user=request.user)
        budget_data = Budget.objects.filter(user=request.user)
        context = {
            "task_data": task_data,
            "budget_data": budget_data
        }
        return render(request, 'index.html', context)
    else:
        return HttpResponse("You're doing something tricky!")


@login_required(login_url='organizer:login')
def tasks(request):
    if (request.method == "GET" and "delete" in request.GET):
        id = request.GET["delete"]
        Task.objects.filter(id=id).delete()
        return redirect("organizer:tasks")
    else:
        table_data = Task.objects.filter(user=request.user)
        context = {
            "table_data": table_data
        }
        return render(request, 'tasks.html', context)

@login_required(login_url='organizer:login')
def budget(request):
    if (request.method == "GET" and "delete" in request.GET):
        id = request.GET["delete"]
        Budget.objects.filter(id=id).delete()
        return redirect("organizer:budget")
    else:
        table_data = Budget.objects.filter(user=request.user)
        context = {
            "table_data": table_data
        }
        return render(request, 'budget.html', context)

def budgetEdit(request, id):
    if (request.method == "GET"):
        taskEntry = Budget.objects.get(id=id)
        form = BudgetForm(instance=taskEntry)
        context = { "form_data" : form }
        return render(request, 'budget_edit.html', context)
    elif (request.method == "POST"):
		# Process form submission
        if ("edit" in request.POST):
            form = BudgetForm(request.POST)
            if (form.is_valid()):
                taskEntry = form.save(commit=False)
                taskEntry.user = request.user
                taskEntry.id = id
                taskEntry.save()
                return redirect("organizer:budget")
            else:
                context = {
                    "form_data": form
                }
                return render(request, 'budget_edit.html', context)
        else:
            print("5")
			#Cancel
            return redirect("organizer:budget")

def budgetAdd(request):
    if (request.method == "POST"):
        if ("add" in request.POST):
            add_form = BudgetForm(request.POST)
            if (add_form.is_valid()):
                description = add_form.cleaned_data["description"]
                entry = add_form.cleaned_data["category"]
                user = User.objects.get(id=request.user.id)
                actual = add_form.cleaned_data["actual"]
                projected = add_form.cleaned_data["projected"]
                Budget(user=user, description=description,
                             category=entry, actual=actual, projected=projected).save()
                return redirect("organizer:budget")
            else:
                context = {
                    "form_data": add_form
                }
                return render(request, 'organizer:budgetAdd', context)
        else:
            # Cancel
            return redirect("organizer:budget")
    else:
        context = {
            "form_data": BudgetForm()
        }
        return render(request, 'budget_add.html', context)


def about(request):
    return render(request, 'about.html')


def join(request):
    if (request.method == "POST"):
        join_form = JoinForm(request.POST)
        if (join_form.is_valid()):
            # Save form data to DB
            user = join_form.save()
            # Encrypt the password
            user.set_password(user.password)
            # Save encrypted password to DB
            user.save()
            # Success! Redirect to home page.
            return redirect("/organizer")
        else:
            # Form invalid, print errors to console
            context = {"join_form": join_form}
            return render(request, 'join.html', context)
    else:
        join_form = JoinForm()
        page_data = {"join_form": join_form}
        return render(request, 'join.html', page_data)


def user_login(request):

    if (request.method == 'POST'):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # First get the username and password supplied
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            # Django's built-in authentication function:
            user = authenticate(username=username, password=password)
            # If we have a user
            if user:
                # Check it the account is active
                if user.is_active:
                    # Log the user in.
                    login(request, user)
                    # Send the user back to homepage
                    return redirect("/")
                else:
                    # If account is not active:
                    return HttpResponse("Your account is not active.")
            else:
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(
                    username, password))
                return render(request, 'login.html', {"login_form": LoginForm})
    else:
        # Nothing has been provided for username or password.
        return render(request, 'login.html', {"login_form": LoginForm})


def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return redirect('organizer:login')


@login_required(login_url='organizer:login')
def add(request):
    if (request.method == "POST"):
        if ("add" in request.POST):
            add_form = TaskForm(request.POST)
            if (add_form.is_valid()):
                description = add_form.cleaned_data["description"]
                entry = add_form.cleaned_data["category"]
                user = User.objects.get(id=request.user.id)
                Task(user=user, description=description,
                             category=entry).save()
                return redirect("organizer:tasks")
            else:
                context = {
                    "form_data": add_form
                }
                return render(request, 'organizer:add', context)
        else:
            # Cancel
            return redirect("organizer:tasks")
    else:
        context = {
            "form_data": TaskForm()
        }
        return render(request, 'add.html', context)

@login_required(login_url='organizer:login')
def complete(request, id):
    task = Task.objects.filter(id=id)[0]
    if task.completed:
        task.completed = False
    else:
        task.completed = True
    
    task.save()
    return redirect('organizer:tasks')

@login_required(login_url='organizer:login')
def edit(request, id):
	if (request.method == "GET"):
		taskEntry = Task.objects.get(id=id)
		form = TaskForm(instance=taskEntry)
		context = { "form_data" : form }
		return render(request, 'edit.html', context)
	elif (request.method == "POST"):
		# Process form submission
		if ("edit" in request.POST):
			form = TaskForm(request.POST)
			if (form.is_valid()):
				taskEntry = form.save(commit=False)
				taskEntry.user = request.user
				taskEntry.id = id
				taskEntry.save()
				return redirect("organizer:tasks")
			else:
				context = {
				"form_data": form
				}
				return render(request, 'add.html', context)
		else:
			#Cancel
			return redirect("organizer:tasks")