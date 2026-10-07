from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required

from .models import Disciplina
from .forms import DisciplinaForm


@permission_required('disciplinas.view_disciplina')
def listar_disciplinas(request):
    disciplinas = Disciplina.objects.all()

    return render(
        request,
        'disciplinas/listar.html',
        {'disciplinas': disciplinas}
    )


@permission_required('disciplinas.add_disciplina')
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


@permission_required('disciplinas.view_disciplina')
def detalhar_disciplina(request, id):
    disciplina = get_object_or_404(Disciplina, id=id)

    return render(
        request,
        'disciplinas/detalhar.html',
        {'disciplina': disciplina}
    )


@permission_required('disciplinas.change_disciplina')
def editar_disciplina(request, id):
    disciplina = get_object_or_404(Disciplina, id=id)

    if request.method == 'POST':
        form = DisciplinaForm(
            request.POST,
            instance=disciplina
        )

        if form.is_valid():
            form.save()
            return redirect('listar_disciplinas')
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


@permission_required('disciplinas.delete_disciplina')
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