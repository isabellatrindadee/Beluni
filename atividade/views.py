from django.shortcuts import render, redirect
from .models import Atividade
from .forms import AtividadeForm


def listar_atividades(request):
    atividades = Atividade.objects.all()

    return render(
        request,
        'atividade/listar.html',
        {'atividades': atividades}
    )


def criar_atividade(request):
    if request.method == 'POST':
        form = AtividadeForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('listar_atividades')
    else:
        form = AtividadeForm()

    return render(
        request,
        'atividade/criar.html',
        {'form': form}
    )