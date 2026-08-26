from django.shortcuts import render, redirect, get_object_or_404
from .models import Estudante
from .forms import EstudanteForm


def listar_estudantes(request):
    estudantes = Estudante.objects.all()

    return render(
        request,
        'estudante/listar.html',
        {'estudantes': estudantes}
    )


def criar_estudante(request):
    if request.method == 'POST':
        form = EstudanteForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('listar_estudantes')
    else:
        form = EstudanteForm()

    return render(
        request,
        'estudante/criar.html',
        {'form': form}
    )


def detalhar_estudante(request, id):
    estudante = get_object_or_404(Estudante, id=id)

    return render(
        request,
        'estudante/detalhar.html',
        {'estudante': estudante}
    )


def editar_estudante(request, id):
    estudante = get_object_or_404(Estudante, id=id)

    if request.method == 'POST':
        form = EstudanteForm(request.POST, instance=estudante)

        if form.is_valid():
            form.save()
            return redirect('detalhar_estudante', id=estudante.id)
    else:
        form = EstudanteForm(instance=estudante)

    return render(
        request,
        'estudante/editar.html',
        {
            'form': form,
            'estudante': estudante
        }
    )


def excluir_estudante(request, id):
    estudante = get_object_or_404(Estudante, id=id)

    if request.method == 'POST':
        estudante.delete()
        return redirect('listar_estudantes')

    return render(
        request,
        'estudante/excluir.html',
        {'estudante': estudante}
    )