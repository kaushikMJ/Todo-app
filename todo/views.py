from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from .forms import TodoForm
from .models import Todo
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.



def home(request):
	return render(request,'home.html')

def signupuser(request):
	#any time you enter a url in browser that is a GET request
	if request.method== 'GET':
		return render(request,'signupuser.html',{'form':UserCreationForm()})
	else:
		#check if password and confirm password are same
		if request.POST['password1'] == request.POST['password2']:
			try:
				userCreate= User.objects.create_user(request.POST['username'],password=request.POST['password1'])
				userCreate.save()
				login(request,userCreate)
				return redirect('currentTodos')
				#inside redirect don't write the html page but write the url endpoint that is name of path
				# userTodos=Todo.objects.filter(user = request.user)
				# return redirect(reverse('currentTodos', kwargs={"userTodos": userTodos,'c':c}))
			
			except IntegrityError:
				return render(request,'signupuser.html',{'form':UserCreationForm(),'error':'Same username already exists!'})
		
		else:
			return render(request,'signupuser.html',{'form':UserCreationForm(),'error':'Passwords not matching'})


@login_required
def logoutuser(request):
	logout(request);
	return redirect('home')



def loginuser(request):
	if request.method== 'GET':
		return render(request,'loginuser.html',{'form':AuthenticationForm()})
	else:
		#check if password and confirm password are same
		userFind=authenticate(request,username=request.POST['username'],password=request.POST['password'])

		#if no user exists then userFind is None
		if userFind is None:
			return render(request,'loginuser.html',{'form':AuthenticationForm(),'error':'Username or Password is incorrect'})
		
		else:
			login(request,userFind)
			return redirect('currentTodos')
			#inside redirect don't write the html page but write the url endpoint that is name of path
			
			# userTodos=Todo.objects.filter(user = request.user)
			#return redirect(reverse('currentTodos'),userTodos= userTodos,l=c)



@login_required
def createtodo(request):
	if request.method== 'GET':
		return render(request,'createtodo.html',{'form':TodoForm()})
	else:
		#commit=false,is useful when you get most of your model data from a form, but you need to populate some null=False fields with non-form data.Saving with commit=False gets you a model object, then you can add your extra data and save it.
		try:
			form=TodoForm(request.POST)

			newTodo=form.save(commit=False)
			newTodo.user=request.user
			newTodo.save()
			return redirect('currentTodos')
			
		
		except ValueError:
			return render(request,'createtodo.html',{'form':TodoForm(),'error':'The title is too big.Make the title short'})


@login_required
def currentTodos(request):
	#this shows al the todos a=which are not completed(ie dateCompleted=null)
	userTodos=Todo.objects.filter(user = request.user, dateCompleted__isnull=True)
	#userTodos.dateCreated= user|localtime
	#return redirect(reverse('currentTodos', kwargs={"userTodos": userTodos,'c':c}))
	return render(request,'currentTodos.html',{"userTodos": userTodos})



def completeTodos(request):
	try:

		#this shows al the todos a=which are  completed(ie dateCompleted!=null)
		userTodos=Todo.objects.filter(user = request.user, dateCompleted__isnull=False).order_by('-dateCompleted')
		#return redirect(reverse('currentTodos', kwargs={"userTodos": userTodos,'c':c}))
		return render(request,'completetodos.html',{"completeTodos": userTodos})

	except Exception as e:
		return redirect('loginuser')



@login_required
def viewTodo(request,todo_pk):

	#this shows al the todos a=which are not completed(ie dateCompleted=null)
	if request.method=='GET':
		todo=Todo.objects.get(pk=todo_pk)
		#form=TodoForm(initial={'title':todo.title , 'memo':todo.memo ,'important':todo.important})
		return render(request,'viewtodo.html',{"todo": todo})

	else:
		if request.POST.get('update'):
			todo=Todo.objects.get(id=todo_pk)
			print(request.POST['title'])
			todo.title=request.POST.get('title')
			todo.memo=request.POST.get('memo')
			imp=True
			if request.POST.get('important'):
				imp=True
			else:
				imp=False
			todo.important=imp
			todo.save()
			print('updated')
				

		elif request.POST.get('delete'):
			todo=Todo.objects.get(id=todo_pk)
			todo.delete()
			print('deleted')

		elif request.POST.get('complete'):
			todo=Todo.objects.get(id=todo_pk)
			todo.dateCompleted=datetime.now()
			todo.save()
			print('completed')
		print('do')
		return redirect('currentTodos')



