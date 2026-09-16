from datetime import timedelta

from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Notificacao
from atividade.models import Atividade


def gerar_notificacoes():
    hoje = timezone.localdate()
    data_notificacao = hoje + timedelta(days=1)

    atividades = Atividade.objects.filter(
        data=data_notificacao
    ).exclude(
        status='concluida'
    )

    for atividade in atividades:

        estudantes = atividade.disciplinas.values_list(
            'estudante',
            flat=True
        ).distinct()

        for estudante_id in estudantes:

            mensagem = (
                f'A atividade "{atividade.titulo}" '
                f'deve ser entregue amanhã ({atividade.data.strftime("%d/%m/%Y")}).'
            )

            Notificacao.objects.get_or_create(
                atividade=atividade,
                estudante_id=estudante_id,
                defaults={
                    'mensagem': mensagem
                }
            )


def listar_notificacoes(request):
    gerar_notificacoes()

    notificacoes = Notificacao.objects.all().order_by('atividade__data')

    return render(
        request,
        'notificacao/listar.html',
        {'notificacoes': notificacoes}
    )


def visualizar_notificacao(request, id):
    notificacao = get_object_or_404(
        Notificacao,
        id=id
    )

    return render(
        request,
        'notificacao/visualizar.html',
        {'notificacao': notificacao}
    )


def excluir_notificacao(request, id):
    notificacao = get_object_or_404(
        Notificacao,
        id=id
    )

    if request.method == 'POST':
        notificacao.delete()

        return render(
            request,
            'notificacao/listar.html',
            {
                'notificacoes': Notificacao.objects.all()
            }
        )

    return render(
        request,
        'notificacao/excluir.html',
        {'notificacao': notificacao}
    )