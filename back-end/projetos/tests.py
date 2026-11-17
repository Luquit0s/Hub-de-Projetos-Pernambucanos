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

    def test_user_can_update_and_delete_own_project(self):
        project = Projeto.objects.create(
            titulo='Projeto editável',
            descricao='Descrição',
            tecnologias='Python',
            link_repositorio='https://example.com/editable',
            user=self.user,
        )

        update_response = self.client.patch(
            reverse('projeto-detail', args=[project.id]),
            {'titulo': 'Projeto atualizado'},
            format='json',
        )
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        project.refresh_from_db()
        self.assertEqual(project.titulo, 'Projeto atualizado')

        delete_response = self.client.delete(
            reverse('projeto-detail', args=[project.id])
        )
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Projeto.objects.filter(id=project.id).exists())

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

    def test_allowed_frontend_origin_receives_cors_header(self):
        response = self.client.get(
            reverse('projeto-list'),
            HTTP_ORIGIN='http://localhost:3000',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response['Access-Control-Allow-Origin'],
            'http://localhost:3000',
        )

    def test_cors_preflight_is_supported(self):
        self.client.force_authenticate(user=None)

        response = self.client.options(
            reverse('projeto-list'),
            HTTP_ORIGIN='http://localhost:3000',
            HTTP_ACCESS_CONTROL_REQUEST_METHOD='POST',
            HTTP_ACCESS_CONTROL_REQUEST_HEADERS='authorization,content-type',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response['Access-Control-Allow-Origin'],
            'http://localhost:3000',
        )
        self.assertIn('POST', response['Access-Control-Allow-Methods'])

    def test_user_can_register_and_access_account(self):
        self.client.force_authenticate(user=None)

        register_response = self.client.post(
            reverse('register'),
            {
                'username': 'novo-pesquisador',
                'email': 'novo@example.com',
                'password': 'senha-segura-123',
            },
            format='json',
        )

        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('password', register_response.data)

        login_response = self.client.post(
            reverse('token_obtain_pair'),
            {
                'username': 'novo-pesquisador',
                'password': 'senha-segura-123',
            },
            format='json',
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {login_response.data['access']}"
        )
        me_response = self.client.get(reverse('current-user'))

        self.assertEqual(me_response.status_code, status.HTTP_200_OK)
        self.assertEqual(me_response.data['email'], 'novo@example.com')

    def test_user_can_edit_and_delete_own_account(self):
        response = self.client.patch(
            reverse('current-user'),
            {'first_name': 'Pesquisador', 'password': 'nova-senha-123'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Pesquisador')
        self.assertTrue(self.user.check_password('nova-senha-123'))

        delete_response = self.client.delete(reverse('current-user'))

        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            get_user_model().objects.filter(id=self.user.id).exists()
        )

    def test_logout_revokes_refresh_token(self):
        self.client.force_authenticate(user=None)
        login_response = self.client.post(
            reverse('token_obtain_pair'),
            {
                'username': 'pesquisador',
                'password': 'senha-de-teste',
            },
            format='json',
        )
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {login_response.data['access']}"
        )

        logout_response = self.client.post(
            reverse('logout'),
            {'refresh': login_response.data['refresh']},
            format='json',
        )
        self.assertEqual(logout_response.status_code, status.HTTP_204_NO_CONTENT)

        refresh_response = self.client.post(
            reverse('token_refresh'),
            {'refresh': login_response.data['refresh']},
            format='json',
        )
        self.assertEqual(refresh_response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_cannot_revoke_another_users_refresh_token(self):
        self.client.force_authenticate(user=None)
        login_response = self.client.post(
            reverse('token_obtain_pair'),
            {
                'username': 'outro',
                'password': 'senha-de-teste',
            },
            format='json',
        )
        self.client.force_authenticate(user=self.user)

        logout_response = self.client.post(
            reverse('logout'),
            {'refresh': login_response.data['refresh']},
            format='json',
        )

        self.assertEqual(logout_response.status_code, status.HTTP_400_BAD_REQUEST)
