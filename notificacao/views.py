from django.shortcuts import render, get_object_or_404, redirect
from .models import Notificacao
from .forms import NotificacaoForm


def listar_notificacoes(request):
    notificacoes = Notificacao.objects.all()
    return render(
        request,
        'notificacao/listar.html',
        {'notificacoes': notificacoes}
    )


def detalhar_notificacao(request, id):
    notificacao = get_object_or_404(Notificacao, id=id)

    return render(
        request,
        'notificacao/detalhar.html',
        {'notificacao': notificacao}
    )


def editar_notificacao(request, id):
    notificacao = get_object_or_404(Notificacao, id=id)

    if request.method == 'POST':
        form = NotificacaoForm(
            request.POST,
            instance=notificacao
        )

        if form.is_valid():
            form.save()
            return redirect('listar_notificacoes')

    else:
        form = NotificacaoForm(
            instance=notificacao
        )

    return render(
        request,
        'notificacao/editar.html',
        {
            'form': form,
            'notificacao': notificacao
        }
    )


def excluir_notificacao(request, id):
    notificacao = get_object_or_404(Notificacao, id=id)

    if request.method == 'POST':
        notificacao.delete()
        return redirect('listar_notificacoes')

    return render(
        request,
        'notificacao/excluir.html',
        {'notificacao': notificacao}
    )