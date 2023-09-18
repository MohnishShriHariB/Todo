from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from .forms import todoforms
from .models import todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required
def signupuser(request):
        if request.method=='GET':
            return render(request,'todowoo\signupuser.html',{'form':UserCreationForm()})
        else:
            if request.POST['password1']==request.POST['password2']:
                try:
                    user=User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                    user.save()
                    login(request,user)
                    return redirect('currenttodo')
                except IntegrityError:
                    return render(request,'todowoo\signupuser.html',{'form':UserCreationForm(),'error':"User Name already exists.Please enter a deferent username"})
            else:
                return render(request,'todowoo\signupuser.html',{'form':UserCreationForm(),'error':"Passwords did not match"})
@login_required
def currenttodo(request):
    todos=todo.objects.filter(user=request.user,Completed__isnull=True)
    return render(request,'todowoo/currenttodo.html',{'todos':todos})
def home(request):
    return render(request,'todowoo\home.html')
@login_required
def logoutuser(request):
    if request.method=="POST":
        logout(request)
        return redirect('home')
def loginuser(request):
    if request.method=="GET":
        return render(request,'todowoo\loginuser.html',{'form':AuthenticationForm()})
    else:
        user=authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request,'todowoo\loginuser.html',{'form':AuthenticationForm(),'error':"Username or password is Incorrect!!!"})
        else:
            login(request,user)
            return redirect('currenttodo')
@login_required
def createtodo(request):
    if request.method=="GET":
        return render(request,'todowoo\createtodo.html',{'form':todoforms()})
    else:
        try:
            forms=todoforms(request.POST)
            newform=forms.save(commit=False)
            newform.user=request.user
            newform.save()
            return redirect('currenttodo')
        except ValueError:
            return render(request,'todowoo\createtodo.html',{'form':todoforms(),'error':"Bad Data entered. Try Again"})
@login_required
def viewtodo(request,todo_pk):
    todos=get_object_or_404(todo,pk=todo_pk,user=request.user)
    if request.method=="GET":

        form=todoforms(instance=todos)
        return render(request,'todowoo/viewtodo.html',{'todos':todos,'form':form})
    else:
        try:
            form=todoforms(request.POST,instance=todos)
            form.save()
            return redirect('currenttodo')
        except ValueError:
            return render(request,'todowoo/viewtodo.html',{'todos':todos,'form':form,'error':"Bad Info"})
@login_required
def completetodo(request,todo_pk):
    todos=get_object_or_404(todo,pk=todo_pk,user=request.user)
    if request.method=="POST":
        todos.Completed=timezone.now()
        todos.save()
        return redirect('currenttodo')
@login_required
def deletetodo(request,todo_pk):
    todos=get_object_or_404(todo,pk=todo_pk,user=request.user)
    if request.method=="POST":
        todos.delete()
        return redirect('currenttodo')
@login_required
def completedtodo(request):
    todos=todo.objects.filter(user=request.user,Completed__isnull=False).order_by('-Completed')
    return render(request,'todowoo/completedtodo.html',{'todos':todos})
