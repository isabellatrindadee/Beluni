
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required

from .models import Meta
from .forms import MetaForm
from estudante.models import Estudante


def obter_estudante(usuario):
    return get_object_or_404(
        Estudante,
        pk=usuario.pk
    )


def metas_do_estudante(estudante):
    return Meta.objects.filter(
        estudante=estudante
    )


def configurar_formulario(form, estudante):
    # O estudante não deve ser escolhido manualmente.
    if 'estudante' in form.fields:
        form.fields['estudante'].queryset = Estudante.objects.filter(
            pk=estudante.pk
        )
        form.fields['estudante'].required = False
        form.fields['estudante'].widget = (
            form.fields['estudante'].hidden_widget()
        )
        form.initial['estudante'] = estudante.pk


@login_required
@permission_required('meta.view_meta')
def listar_metas(request):
    estudante = obter_estudante(request.user)

    metas = metas_do_estudante(estudante).order_by('data')

    return render(
        request,
        'meta/listar.html',
        {'metas': metas}
    )


@login_required
@permission_required('meta.add_meta')
def criar_meta(request):
    estudante = obter_estudante(request.user)

    if request.method == 'POST':
        form = MetaForm(request.POST)
        configurar_formulario(form, estudante)

        if form.is_valid():
            meta = form.save(commit=False)
            meta.estudante = estudante
            meta.save()

            return redirect('listar_metas')
    else:
        form = MetaForm()
        configurar_formulario(form, estudante)

    return render(
        request,
        'meta/criar.html',
        {'form': form}
    )


@login_required
@permission_required('meta.view_meta')
def detalhar_meta(request, id):
    estudante = obter_estudante(request.user)

    meta = get_object_or_404(
        metas_do_estudante(estudante),
        id=id
    )

    return render(
        request,
        'meta/detalhar.html',
        {'meta': meta}
    )


@login_required
@permission_required('meta.change_meta')
def editar_meta(request, id):
    estudante = obter_estudante(request.user)

    meta = get_object_or_404(
        metas_do_estudante(estudante),
        id=id
    )

    if request.method == 'POST':
        form = MetaForm(
            request.POST,
            instance=meta
        )
        configurar_formulario(form, estudante)

        if form.is_valid():
            meta_editada = form.save(commit=False)
            meta_editada.estudante = estudante
            meta_editada.save()

            return redirect('listar_metas')
    else:
        form = MetaForm(instance=meta)
        configurar_formulario(form, estudante)

    return render(
        request,
        'meta/editar.html',
        {
            'form': form,
            'meta': meta
        }
    )


@login_required
@permission_required('meta.delete_meta')
def excluir_meta(request, id):
    estudante = obter_estudante(request.user)

    meta = get_object_or_404(
        metas_do_estudante(estudante),
        id=id
    )

    if request.method == 'POST':
        meta.delete()
        return redirect('listar_metas')

    return render(
        request,
        'meta/excluir.html',
        {'meta': meta}
    )


@login_required
@permission_required('meta.change_meta')
def alternar_meta(request, id):
    if request.method == 'POST':
        estudante = obter_estudante(request.user)

        meta = get_object_or_404(
            metas_do_estudante(estudante),
            id=id
        )

        meta.concluida = not meta.concluida
        meta.save(update_fields=['concluida'])

    return redirect('listar_metas')
