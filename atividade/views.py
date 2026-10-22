from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required

from .models import Atividade
from .forms import (
    AtividadeForm,
    AtividadeInterdisciplinarFormSet,
)


@login_required
@permission_required('atividade.view_atividade')
def listar_atividades(request):
    atividades = Atividade.objects.prefetch_related('disciplinas').all()

    return render(
        request,
        'atividade/listar.html',
        {'atividades': atividades}
    )



@login_required
@permission_required('atividade.add_atividade')
def criar_atividade(request, disciplina_id=None):
    disciplina_inicial = None

    if disciplina_id is not None:
        disciplina_inicial = get_object_or_404(
            Disciplina,
            id=disciplina_id
        )

    if request.method == 'POST':
        form = AtividadeForm(request.POST)
        formset = AtividadeInterdisciplinarFormSet(
            request.POST,
            prefix='disciplinas'
        )

        if form.is_valid() and formset.is_valid():
            atividade = form.save()
            formset.instance = atividade
            formset.save()
            return redirect('listar_atividades')
    else:
        form = AtividadeForm()

        formset = AtividadeInterdisciplinarFormSet(
            prefix='disciplinas'
        )

        if disciplina_inicial is not None:
            formset.forms[0].initial['disciplina'] = disciplina_inicial

    return render(
        request,
        'atividade/criar.html',
        {
            'form': form,
            'formset': formset,
            'disciplina_inicial': disciplina_inicial,
        }
    )

@login_required
@permission_required('atividade.view_atividade')
def detalhar_atividade(request, id):
    atividade = get_object_or_404(
        Atividade.objects.prefetch_related(
            'disciplinas',
            'atividadeinterdisciplinar_set',
        ),
        id=id
    )

    return render(
        request,
        'atividade/detalhar.html',
        {'atividade': atividade}
    )


@login_required
@permission_required('atividade.change_atividade')
def editar_atividade(request, id):
    atividade = get_object_or_404(Atividade, id=id)

    if request.method == 'POST':
        form = AtividadeForm(
            request.POST,
            instance=atividade
        )
        formset = AtividadeInterdisciplinarFormSet(
            request.POST,
            instance=atividade,
            prefix='disciplinas'
        )

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('listar_atividades')
    else:
        form = AtividadeForm(instance=atividade)
        formset = AtividadeInterdisciplinarFormSet(
            instance=atividade,
            prefix='disciplinas'
        )

    return render(
        request,
        'atividade/editar.html',
        {
            'form': form,
            'formset': formset,
            'atividade': atividade,
        }
    )


@login_required
@permission_required('atividade.delete_atividade')
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
