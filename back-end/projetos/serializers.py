from rest_framework import serializers

from projetos.models import Projeto


class ProjetoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projeto
        fields = (
            'id',
            'titulo',
            'descricao',
            'tecnologias',
            'link_repositorio',
            'user',
            'criado_em',
        )
        read_only_fields = ('id', 'user', 'criado_em')
