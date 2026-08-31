from django.shortcuts import render, redirect, get_object_or_404
from .models import Disciplina
from .forms import DisciplinaForm


def listar_disciplinas(request):
    disciplinas = Disciplina.objects.all()

    return render(
        request,
        'disciplinas/listar.html',
        {'disciplinas': disciplinas}
    )


def criar_disciplina(request):
    if request.method == 'POST':
        form = DisciplinaForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('listar_disciplinas')
    else:
        form = DisciplinaForm()

    return render(
        request,
        'disciplinas/criar.html',
        {'form': form}
    )


def detalhar_disciplina(request, id):
    disciplina = get_object_or_404(Disciplina, id=id)

    return render(
        request,
        'disciplinas/detalhar.html',
        {'disciplina': disciplina}
    )


def editar_disciplina(request, id):
    disciplina = get_object_or_404(Disciplina, id=id)

    if request.method == 'POST':
        form = DisciplinaForm(request.POST, instance=disciplina)

        if form.is_valid():
            form.save()
            return redirect('detalhar_disciplina', id=disciplina.id)
    else:
        form = DisciplinaForm(instance=disciplina)

    return render(
        request,
        'disciplinas/editar.html',
        {
            'form': form,
            'disciplina': disciplina
        }
    )


def excluir_disciplina(request, id):
    disciplina = get_object_or_404(Disciplina, id=id)

    if request.method == 'POST':
        disciplina.delete()
        return redirect('listar_disciplinas')

    return render(
        request,
        'disciplinas/excluir.html',
        {'disciplina': disciplina}
    )