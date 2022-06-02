from django.http import HttpRequest
from receitas.models import Receita
from django.shortcuts import render


def buscar(request: HttpRequest):
    receitas = Receita.objects.order_by('data_receita').filter(publicada=True)

    if 'buscar' in request.GET:
        nome_a_buscar = request.GET['buscar']
        if nome_a_buscar:
            receitas = receitas.filter(nome_receita__icontains=nome_a_buscar)

    dados = {
        'receitas': receitas
    }

    return render(request, 'receitas/buscar.html', dados)
