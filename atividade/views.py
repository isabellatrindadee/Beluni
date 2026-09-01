from django.shortcuts import render, redirect, get_object_or_404
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


def detalhar_atividade(request, id):
    atividade = get_object_or_404(Atividade, id=id)

    return render(
        request,
        'atividade/detalhar.html',
        {'atividade': atividade}
    )


def editar_atividade(request, id):
    atividade = get_object_or_404(Atividade, id=id)

    if request.method == 'POST':
        form = AtividadeForm(request.POST, instance=atividade)

        if form.is_valid():
            form.save()
            return redirect('listar_atividades')
    else:
        form = AtividadeForm(instance=atividade)

    return render(
        request,
        'atividade/editar.html',
        {
            'form': form,
            'atividade': atividade
        }
    )


def excluir_atividade(request, id):
    atividade = get_object_or_404(Atividade, id=id)

    if request.method == 'POST':
        atividade.delete()
        return redirect('listar_atividades')

    return render(
        request,
        'atividade/excluir.html',
        {'atividade': atividade}
    )