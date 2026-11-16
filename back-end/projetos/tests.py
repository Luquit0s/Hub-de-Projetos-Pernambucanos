from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from projetos.models import Projeto


class ProjetoApiTests(APITestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username='pesquisador',
            password='senha-de-teste',
        )
        self.other_user = user_model.objects.create_user(
            username='outro',
            password='senha-de-teste',
        )
        self.client.force_authenticate(user=self.user)

    def test_list_only_returns_authenticated_users_projects(self):
        own_project = Projeto.objects.create(
            titulo='Projeto próprio',
            descricao='Descrição',
            tecnologias='Python',
            link_repositorio='https://example.com/own',
            user=self.user,
        )
        Projeto.objects.create(
            titulo='Projeto de outra pessoa',
            descricao='Descrição',
            tecnologias='Python',
            link_repositorio='https://example.com/other',
            user=self.other_user,
        )

        response = self.client.get(reverse('projeto-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([item['id'] for item in response.data], [own_project.id])

    def test_user_cannot_retrieve_another_users_project(self):
        other_project = Projeto.objects.create(
            titulo='Projeto de outra pessoa',
            descricao='Descrição',
            tecnologias='Python',
            link_repositorio='https://example.com/other',
            user=self.other_user,
        )

        response = self.client.get(
            reverse('projeto-detail', args=[other_project.id])
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_assigns_authenticated_user(self):
        response = self.client.post(
            reverse('projeto-list'),
            {
                'titulo': 'Novo projeto',
                'descricao': 'Descrição',
                'tecnologias': 'Python',
                'link_repositorio': 'https://example.com/new',
                'user': self.other_user.id,
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Projeto.objects.get(id=response.data['id']).user, self.user)

    def test_unauthenticated_requests_are_rejected(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(reverse('projeto-list'))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_endpoints_obtain_and_refresh_tokens(self):
        self.client.force_authenticate(user=None)
        token_response = self.client.post(
            reverse('token_obtain_pair'),
            {
                'username': 'pesquisador',
                'password': 'senha-de-teste',
            },
            format='json',
        )

        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', token_response.data)
        self.assertIn('refresh', token_response.data)

        refresh_response = self.client.post(
            reverse('token_refresh'),
            {'refresh': token_response.data['refresh']},
            format='json',
        )

        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_response.data)
