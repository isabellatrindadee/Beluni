
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required

from .models import Atividade
from .forms import (
    AtividadeForm,
    AtividadeInterdisciplinarFormSet,
)
from disciplinas.models import Disciplina
from estudante.models import Estudante


def obter_estudante(usuario):
    return get_object_or_404(
        Estudante,
        pk=usuario.pk
    )


def atividades_do_estudante(estudante):
    return Atividade.objects.filter(
        disciplinas__estudante=estudante
    ).distinct()


def configurar_formset(formset, estudante):
    disciplinas = Disciplina.objects.filter(
        estudante=estudante
    )

    for formulario in formset.forms:
        if 'disciplina' in formulario.fields:
            formulario.fields['disciplina'].queryset = disciplinas


@login_required
@permission_required('atividade.view_atividade')
def listar_atividades(request):
    estudante = obter_estudante(request.user)

    atividades = (
        atividades_do_estudante(estudante)
        .prefetch_related('disciplinas')
    )

    return render(
        request,
        'atividade/listar.html',
        {'atividades': atividades}
    )


@login_required
@permission_required('atividade.add_atividade')
def criar_atividade(request, disciplina_id=None):
    estudante = obter_estudante(request.user)
    disciplina_inicial = None

    if disciplina_id is not None:
        disciplina_inicial = get_object_or_404(
            Disciplina,
            id=disciplina_id,
            estudante=estudante
        )

    if request.method == 'POST':
        form = AtividadeForm(request.POST)

        formset = AtividadeInterdisciplinarFormSet(
            request.POST,
            prefix='disciplinas'
        )

        configurar_formset(formset, estudante)

        if form.is_valid() and formset.is_valid():
            formularios_validos = [
                formulario
                for formulario in formset.forms
                if formulario.cleaned_data
                and not formulario.cleaned_data.get('DELETE', False)
            ]

            if not formularios_validos:
                form.add_error(
                    None,
                    'Associe a atividade a pelo menos uma disciplina.'
                )
            else:
                disciplinas_ids = [
                    formulario.cleaned_data['disciplina'].pk
                    for formulario in formularios_validos
                ]

                quantidade_proprias = Disciplina.objects.filter(
                    pk__in=disciplinas_ids,
                    estudante=estudante
                ).count()

                if quantidade_proprias != len(set(disciplinas_ids)):
                    form.add_error(
                        None,
                        'Selecione somente suas próprias disciplinas.'
                    )
                else:
                    atividade = form.save()

                    formset.instance = atividade
                    formset.save()

                    return redirect('listar_atividades')

    else:
        form = AtividadeForm()

        formset = AtividadeInterdisciplinarFormSet(
            prefix='disciplinas'
        )

        configurar_formset(formset, estudante)

        if disciplina_inicial is not None and formset.forms:
            formset.forms[0].initial['disciplina'] = (
                disciplina_inicial.pk
            )

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
    estudante = obter_estudante(request.user)

    atividade = get_object_or_404(
        atividades_do_estudante(estudante).prefetch_related(
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
    estudante = obter_estudante(request.user)

    atividade = get_object_or_404(
        atividades_do_estudante(estudante),
        id=id
    )

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

        configurar_formset(formset, estudante)

        if form.is_valid() and formset.is_valid():
            formularios_validos = [
                formulario
                for formulario in formset.forms
                if formulario.cleaned_data
                and not formulario.cleaned_data.get('DELETE', False)
            ]

            if not formularios_validos:
                form.add_error(
                    None,
                    'Associe a atividade a pelo menos uma disciplina.'
                )
            else:
                disciplinas_ids = [
                    formulario.cleaned_data['disciplina'].pk
                    for formulario in formularios_validos
                ]

                quantidade_proprias = Disciplina.objects.filter(
                    pk__in=disciplinas_ids,
                    estudante=estudante
                ).count()

                if quantidade_proprias != len(set(disciplinas_ids)):
                    form.add_error(
                        None,
                        'Selecione somente suas próprias disciplinas.'
                    )
                else:
                    form.save()
                    formset.save()

                    return redirect('listar_atividades')

    else:
        form = AtividadeForm(instance=atividade)

        formset = AtividadeInterdisciplinarFormSet(
            instance=atividade,
            prefix='disciplinas'
        )

        configurar_formset(formset, estudante)

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
    estudante = obter_estudante(request.user)

    atividade = get_object_or_404(
        atividades_do_estudante(estudante),
        id=id
    )

    if request.method == 'POST':
        atividade.delete()
        return redirect('listar_atividades')

    return render(
        request,
        'atividade/excluir.html',
        {'atividade': atividade}
    )
