from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings

# Create your views here.



@login_required
def registrar_usuario(request, template_name='registrar.html'):
    user = request.user
    if user.is_staff:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            tipo = request.POST['tipo_usuario']
            try:
                if tipo == 'administrador':
                    user = User.objects.create_user(username, email, password)
                    user.is_staff = True
                    user.save()
                else:
                    user = User.objects.create_user(username, email, password)
                return redirect('listar_usuario')
            except:
                messages.error(request, 'Username/Senha inválido')
                return redirect('registrar_usuario')
    else:
        messages.error(request, 'Permissão negada')
        return redirect('listar_usuario')
    return render(request, template_name, {})

@login_required
def listar_usuario(request, template_name='listar.html'):
    users = User.objects.all()
    return render(request, template_name,{'lista': users})


def logar(request, template_name="login.html"):
    next = request.GET.get('next', '/listar_usuario/')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(next)
        else:
            messages.error(request, 'Usuário ou senha incorretos.')
            return HttpResponseRedirect(settings.LOGIN_URL)
    return render(request, template_name, {'redirect_to': next})

@login_required
def remover_usuario(request, pk, template_name='delete.html'):
    user = request.user
    if user.has_perm('user.delete_user'):
        try:
            usuario = User.objects.get(pk=pk)
            if request.method == "POST":
                usuario.delete()
                return redirect('listar_usuario')
        except:
            messages.error(request, 'Usuário não encontrado.')
            return redirect('listar_usuario')
    else:
        messages.error(request, 'Permissão negada.')
        return redirect('listar_usuario')
    return render(request, template_name, {'usuario': usuario})


def deslogar(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)