from django.shortcuts import render, redirect
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