from datetime import timedelta

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone

from .models import Notificacao
from .forms import NotificacaoForm
from estudante.models import Estudante
from atividade.models import Atividade


def gerar_notificacoes_pendentes(request):
    hoje = timezone.localdate()
    data_entrega = hoje + timedelta(days=1)

    atividades = Atividade.objects.filter(
        data=data_entrega,
        status__iexact='Pendente'
    )

    estudantes = Estudante.objects.all()

    for atividade in atividades:
        for estudante in estudantes:
            Notificacao.objects.get_or_create(
                estudante=estudante,
                atividade=atividade,
                defaults={
                    'mensagem': (
                        f'A atividade "{atividade.titulo}" '
                        'deve ser entregue amanhã!'
                    )
                }
            )


@login_required
@permission_required('notificacao.view_notificacao')
def listar_notificacoes(request):
    gerar_notificacoes_pendentes(request)

    notificacoes = Notificacao.objects.all()

    return render(
        request,
        'notificacao/listar.html',
        {'notificacoes': notificacoes}
    )


@login_required
@permission_required('notificacao.view_notificacao')
def detalhar_notificacao(request, pk):
    notificacao = get_object_or_404(Notificacao, pk=pk)

    return render(
        request,
        'notificacao/visualizar.html',
        {'notificacao': notificacao}
    )


@login_required
@permission_required('notificacao.change_notificacao')
def editar_notificacao(request, pk):
    notificacao = get_object_or_404(Notificacao, pk=pk)

    if request.method == 'POST':
        form = NotificacaoForm(
            request.POST,
            instance=notificacao
        )

        if form.is_valid():
            form.save()
            return redirect('notificacao:listar_notificacoes')
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


@login_required
@permission_required('notificacao.delete_notificacao')
def excluir_notificacao(request, pk):
    notificacao = get_object_or_404(Notificacao, pk=pk)

    if request.method == 'POST':
        notificacao.delete()
        return redirect('notificacao:listar_notificacoes')

    return render(
        request,
        'notificacao/excluir.html',
        {'notificacao': notificacao}
    )