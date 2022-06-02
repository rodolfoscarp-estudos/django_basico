from django.shortcuts import get_object_or_404, render, redirect
from receitas.models import Receita
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def index(request: HttpRequest):
    receitas = Receita.objects.order_by('data_receita').filter(publicada=True)

    paginator = Paginator(receitas, 6)
    page = request.GET.get('page')
    receitas_por_pagina = paginator.get_page(page)

    dados = {
        'receitas': receitas_por_pagina
    }

    return render(request, 'receitas/index.html', dados)


def receita(request: HttpRequest, receita_id: int):
    receita_a_exibir = get_object_or_404(Receita, pk=receita_id)

    context = {
        'receita': receita_a_exibir,
    }

    return render(request, 'receitas/receita.html', context)


def cria_receita(request: HttpRequest):
    if request.method == "POST":
        nome_receita = request.POST.get('nome_receita')
        ingredientes = request.POST.get('ingredientes')
        modo_preparo = request.POST.get('modo_preparo')
        tempo_preparo = request.POST.get('tempo_preparo')
        rendimento = request.POST.get('rendimento')
        categoria = request.POST.get('categoria')
        foto_receita = request.FILES.get('foto_receita')

        user = get_object_or_404(User, pk=request.user.id)

        receita = Receita.objects.create(
            pessoa=user,
            nome_receita=nome_receita, ingredientes=ingredientes,
            modo_preparo=modo_preparo, tempo_preparo=tempo_preparo,
            rendimento=rendimento, categoria=categoria,
            foto_receita=foto_receita
        )

        receita.save()

        return redirect('dashboard')
    else:
        return render(request, 'receitas/cria_receita.html')


def deleta_receita(request: HttpRequest, receita_id: int):
    receita = get_object_or_404(Receita, pk=receita_id)
    receita.delete()

    return redirect('dashboard')


def edita_receita(request: HttpRequest, receita_id: int):

    receita = get_object_or_404(Receita, pk=receita_id)

    receita_a_editar = {
        'receita': receita
    }

    return render(request, 'receitas/edita_receita.html', receita_a_editar)


def atualiza_receita(request: HttpRequest):
    if request.method == "POST":
        receita_id = request.POST.get('receita_id')

        receita = Receita.objects.get(pk=receita_id)

        receita.nome_receita = request.POST.get('nome_receita')
        receita.ingredientes = request.POST.get('ingredientes')
        receita.modo_preparo = request.POST.get('modo_preparo')
        receita.tempo_preparo = request.POST.get('tempo_preparo')
        receita.rendimento = request.POST.get('rendimento')
        receita.categoria = request.POST.get('categoria')
        if 'foto_receita' in request.FILES:
            receita.foto_receita = request.FILES.get('foto_receita')

        receita.save()

        return redirect('dashboard')
