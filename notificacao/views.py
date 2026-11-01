
from datetime import timedelta

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Notificacao
from .forms import NotificacaoForm
from estudante.models import Estudante
from atividade.models import Atividade


def gerar_notificacoes_pendentes(estudante):
    hoje = timezone.localdate()
    data_entrega = hoje + timedelta(days=1)

    # Busca somente atividades das disciplinas do estudante
    atividades = Atividade.objects.filter(
        disciplinas__estudante=estudante,
        data=data_entrega,
        status__iexact='Pendente'
    ).distinct()

    for atividade in atividades:
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
def listar_notificacoes(request):
    estudante = get_object_or_404(
        Estudante,
        pk=request.user.pk
    )

    gerar_notificacoes_pendentes(estudante)

    notificacoes = Notificacao.objects.filter(
        estudante=estudante
    ).order_by('-id')

    return render(
        request,
        'notificacao/listar.html',
        {'notificacoes': notificacoes}
    )


@login_required
def detalhar_notificacao(request, pk):
    notificacao = get_object_or_404(
        Notificacao,
        pk=pk,
        estudante_id=request.user.pk
    )

    return render(
        request,
        'notificacao/visualizar.html',
        {'notificacao': notificacao}
    )


@login_required
def editar_notificacao(request, pk):
    notificacao = get_object_or_404(
        Notificacao,
        pk=pk,
        estudante_id=request.user.pk
    )

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
def excluir_notificacao(request, pk):
    notificacao = get_object_or_404(
        Notificacao,
        pk=pk,
        estudante_id=request.user.pk
    )

    if request.method == 'POST':
        notificacao.delete()
        return redirect('notificacao:listar_notificacoes')

    return render(
        request,
        'notificacao/excluir.html',
        {'notificacao': notificacao}
    )
