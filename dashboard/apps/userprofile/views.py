from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect, HttpResponse


def signin(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    msg = ''
    user = authenticate(username=username, password=password)
    print (user)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/home')
        else:
            msg = 'Su usuario ha sido desabilitado'
    elif request.method == 'POST':
        msg = "Usuaro no encontrado"
    return render(request, 'signin.html', {'msg':msg})

def signout(request):
    logout(request)
    return HttpResponseRedirect('/')
