from django.shortcuts import render, redirect, get_object_or_404
from .models import Meta
from .forms import MetaForm


def listar_metas(request):
    metas = Meta.objects.all()

    return render(
        request,
        'meta/listar.html',
        {'metas': metas}
    )


def criar_meta(request):
    if request.method == 'POST':
        form = MetaForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('listar_metas')
    else:
        form = MetaForm()

    return render(
        request,
        'meta/criar.html',
        {'form': form}
    )


def detalhar_meta(request, id):
    meta = get_object_or_404(Meta, id=id)

    return render(
        request,
        'meta/detalhar.html',
        {'meta': meta}
    )


def editar_meta(request, id):
    meta = get_object_or_404(Meta, id=id)

    if request.method == 'POST':
        form = MetaForm(request.POST, instance=meta)

        if form.is_valid():
            form.save()
            return redirect('listar_metas')
    else:
        form = MetaForm(instance=meta)

    return render(
        request,
        'meta/editar.html',
        {
            'form': form,
            'meta': meta
        }
    )


def excluir_meta(request, id):
    meta = get_object_or_404(Meta, id=id)

    if request.method == 'POST':
        meta.delete()
        return redirect('listar_metas')

    return render(
        request,
        'meta/excluir.html',
        {'meta': meta}
    )