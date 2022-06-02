from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import auth, messages
from receitas.models import Receita


def cadastro(request: HttpRequest):
    if request.method == "POST":

        nome = request.POST.get('nome')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if campo_vazio(nome):
            messages.error(request, 'Nome não pode ser vazio.')
            return redirect('cadastro')

        if campo_vazio(email):
            messages.error(request, 'Email não pode ser vazio.')
            return redirect('cadastro')

        if senhas_nao_sao_iguias(password, password2):
            messages.error(request, 'As senhas não são iguais.')
            return redirect('cadastro')

        if usuario_ja_cadastrado(email, nome):
            messages.error(request, 'Usuário já cadastrado.')
            return redirect('cadastro')

        user = User.objects.create_user(
            username=nome, email=email, password=password)

        user.save()

        messages.success(request, 'Cadastro realizado com sucesso.')

        return redirect('login')
    else:
        return render(request, 'usuarios/cadastro.html')


def login(request: HttpRequest):

    if request.method == "POST":
        senha = request.POST.get('senha')
        email = request.POST.get('email')

        if campo_vazio(senha):
            messages.error(request, 'Senha não pode ser vazia.')
            return redirect('cadastro')

        if campo_vazio(email):
            messages.error(request, 'Email não pode ser vazio.')
            return redirect('cadastro')

        if User.objects.filter(email=email).exists():
            name = User.objects.filter(
                email=email).values_list('username', flat=True)[0]

            user = auth.authenticate(request, username=name, password=senha)

            if user is not None:
                auth.login(request, user)

            return redirect('dashboard')

    return render(request, 'usuarios/login.html')


def logout(request: HttpRequest):
    auth.logout(request)

    return redirect('index')


def dashboard(request: HttpRequest):
    if request.user.is_authenticated:
        id = request.user.id

        receitas = Receita.objects.order_by('-data_receita').filter(pessoa=id)

        dados = {
            'receitas': receitas
        }

        return render(request, 'usuarios/dashboard.html', dados)

    else:
        return redirect('index')


def campo_vazio(campo: str):
    return not campo.strip()


def senhas_nao_sao_iguias(senha: str, senha2: str):
    return senha != senha2


def usuario_ja_cadastrado(email: str, nome: str):
    return User.objects.filter(username=nome).exists() or \
        User.objects.filter(email=email).exists()
