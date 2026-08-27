from django.shortcuts import render, redirect, get_object_or_404
from .models import Notificacao
from .forms import NotificacaoForm


# LISTAR NOTIFICAÇÕES
def listar_notificacoes(request):
    notificacoes = Notificacao.objects.all()

    return render(
        request,
        'notificacao/listar.html',
        {'notificacoes': notificacoes}
    )


# CRIAR NOTIFICAÇÃO
def criar_notificacao(request):
    if request.method == 'POST':
        form = NotificacaoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('listar_notificacoes')
    else:
        form = NotificacaoForm()

    return render(
        request,
        'notificacao/criar.html',
        {'form': form}
    )


# VISUALIZAR NOTIFICAÇÃO
def visualizar_notificacao(request, id):
    notificacao = get_object_or_404(Notificacao, id=id)

    return render(
        request,
        'notificacao/visualizar.html',
        {'notificacao': notificacao}
    )


# EDITAR NOTIFICAÇÃO
def editar_notificacao(request, id):
    notificacao = get_object_or_404(Notificacao, id=id)

    if request.method == 'POST':
        form = NotificacaoForm(request.POST, instance=notificacao)

        if form.is_valid():
            form.save()
            return redirect('listar_notificacoes')
    else:
        form = NotificacaoForm(instance=notificacao)

    return render(
        request,
        'notificacao/editar.html',
        {
            'form': form,
            'notificacao': notificacao
        }
    )


# EXCLUIR NOTIFICAÇÃO
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