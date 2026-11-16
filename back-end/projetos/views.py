from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from projetos.models import Projeto
from projetos.serializers import ProjetoSerializer


class ProjetoViewSet(ModelViewSet):
    serializer_class = ProjetoSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Projeto.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
