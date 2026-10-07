from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required

from .models import Notificacao
from .forms import NotificacaoForm


@login_required
@permission_required('notificacao.view_notificacao')
def listar_notificacoes(request):
    notificacoes = Notificacao.objects.all()

    return render(
        request,
        'notificacao/listar.html',
        {'notificacoes': notificacoes}
    )


@login_required
@permission_required('notificacao.view_notificacao')
def detalhar_notificacao(request, id):
    notificacao = get_object_or_404(Notificacao, id=id)

    return render(
        request,
        'notificacao/detalhar.html',
        {'notificacao': notificacao}
    )


@login_required
@permission_required('notificacao.change_notificacao')
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


@login_required
@permission_required('notificacao.delete_notificacao')
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