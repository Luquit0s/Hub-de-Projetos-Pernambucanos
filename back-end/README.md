# API - Hub de Projetos Pernambucanos

Backend REST desenvolvido com Django, Django REST Framework e JWT. A API permite criar contas, autenticar usuários e gerenciar projetos particulares.

## Tecnologias

- Python 3.10+
- Django 6.1
- Django REST Framework
- Simple JWT
- SQLite
- django-cors-headers

## Executando o backend

No PowerShell:

```powershell
cd back-end
python -m venv venv
.\venv\Scripts\Activate
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py runserver
```

A API ficará disponível em:

```text
http://127.0.0.1:8000
```

Para verificar a saúde do servidor:

```http
GET /ping
```

Resposta:

```text
ok
```

## Configuração do ambiente

O arquivo `.env` fica na raiz do backend:

```env
SECRET_KEY=uma-chave-secreta
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

`CORS_ALLOWED_ORIGINS` aceita uma lista de origens separadas por vírgula. Em produção, informe somente os domínios reais do frontend.

## Autenticação

A autenticação usa dois tokens JWT:

- **access**: usado nas requisições protegidas.
- **refresh**: usado para renovar o access token e fazer logout.

Nas rotas protegidas, envie:

```http
Authorization: Bearer <access>
```

As rotas de cadastro e login não exigem autenticação. As rotas de usuário e projetos exigem um access token válido.

## Endpoints

Base URL:

```text
http://127.0.0.1:8000
```

### Criar usuário

```http
POST /api/auth/register/
Content-Type: application/json
```

Body:

```json
{
  "username": "pesquisador",
  "email": "pesquisador@example.com",
  "first_name": "Ana",
  "last_name": "Silva",
  "password": "senha-segura-123"
}
```

Resposta `201 Created`:

```json
{
  "id": 1,
  "username": "pesquisador",
  "email": "pesquisador@example.com",
  "first_name": "Ana",
  "last_name": "Silva"
}
```

O campo `password` nunca é retornado. A senha deve ter pelo menos 8 caracteres e passar pelos validadores do Django.

### Login

```http
POST /api/token/
Content-Type: application/json
```

Body:

```json
{
  "username": "pesquisador",
  "password": "senha-segura-123"
}
```

Resposta `200 OK`:

```json
{
  "refresh": "<refresh-token>",
  "access": "<access-token>"
}
```

### Renovar access token

```http
POST /api/token/refresh/
Content-Type: application/json
```

Body:

```json
{
  "refresh": "<refresh-token>"
}
```

Resposta `200 OK`:

```json
{
  "access": "<novo-access-token>"
}
```

### Consultar usuário autenticado

```http
GET /api/auth/me/
Authorization: Bearer <access-token>
```

Resposta `200 OK`:

```json
{
  "id": 1,
  "username": "pesquisador",
  "email": "pesquisador@example.com",
  "first_name": "Ana",
  "last_name": "Silva"
}
```

### Editar usuário autenticado

Use `PATCH` para alterar apenas os campos necessários:

```http
PATCH /api/auth/me/
Authorization: Bearer <access-token>
Content-Type: application/json
```

Body:

```json
{
  "first_name": "Maria",
  "password": "nova-senha-123"
}
```

Resposta `200 OK`: retorna os dados atualizados, sem a senha.

### Excluir usuário autenticado

```http
DELETE /api/auth/me/
Authorization: Bearer <access-token>
```

Resposta: `204 No Content`.

A exclusão também remove os projetos do usuário.

### Logout

O logout invalida o refresh token no servidor:

```http
POST /api/auth/logout/
Authorization: Bearer <access-token>
Content-Type: application/json
```

Body:

```json
{
  "refresh": "<refresh-token>"
}
```

Resposta: `204 No Content`.

Depois do logout, o refresh token não poderá ser usado novamente.

## Projetos

Cada projeto pertence ao usuário autenticado. O backend filtra automaticamente os resultados, portanto um usuário nunca lista, altera ou exclui projetos de outra conta.

Campos:

| Campo | Tipo | Obrigatório | Observação |
|---|---|---:|---|
| `titulo` | string | sim | Máximo de 255 caracteres |
| `descricao` | string | sim | Descrição do projeto |
| `tecnologias` | string | sim | Pode conter várias tecnologias |
| `link_repositorio` | URL | sim | URL válida |
| `user` | inteiro | não | Preenchido pelo backend |
| `criado_em` | data | não | Preenchido pelo backend |

### Criar projeto

```http
POST /api/projetos/
Authorization: Bearer <access-token>
Content-Type: application/json
```

Body:

```json
{
  "titulo": "Monitoramento costeiro",
  "descricao": "Sistema para monitorar áreas costeiras.",
  "tecnologias": "Python, Django, PostgreSQL",
  "link_repositorio": "https://github.com/exemplo/monitoramento"
}
```

Resposta `201 Created`:

```json
{
  "id": 1,
  "titulo": "Monitoramento costeiro",
  "descricao": "Sistema para monitorar áreas costeiras.",
  "tecnologias": "Python, Django, PostgreSQL",
  "link_repositorio": "https://github.com/exemplo/monitoramento",
  "user": 1,
  "criado_em": "2026-11-17T15:00:00Z"
}
```

O campo `user` enviado pelo cliente é ignorado. O projeto sempre é associado ao usuário do token.

### Listar projetos

```http
GET /api/projetos/
Authorization: Bearer <access-token>
```

Resposta `200 OK`:

```json
[
  {
    "id": 1,
    "titulo": "Monitoramento costeiro",
    "descricao": "Sistema para monitorar áreas costeiras.",
    "tecnologias": "Python, Django, PostgreSQL",
    "link_repositorio": "https://github.com/exemplo/monitoramento",
    "user": 1,
    "criado_em": "2026-11-17T15:00:00Z"
  }
]
```

Os projetos são ordenados do mais recente para o mais antigo.

### Consultar projeto

```http
GET /api/projetos/<id>/
Authorization: Bearer <access-token>
```

Retorna `404 Not Found` quando o projeto não existe ou pertence a outro usuário.

### Editar projeto

Para alteração parcial:

```http
PATCH /api/projetos/<id>/
Authorization: Bearer <access-token>
Content-Type: application/json
```

Body:

```json
{
  "titulo": "Monitoramento costeiro atualizado"
}
```

Também é possível usar `PUT` enviando todos os campos editáveis.

### Excluir projeto

```http
DELETE /api/projetos/<id>/
Authorization: Bearer <access-token>
```

Resposta: `204 No Content`.

## Códigos HTTP comuns

| Código | Significado |
|---:|---|
| `200` | Operação realizada com sucesso |
| `201` | Recurso criado |
| `204` | Operação realizada sem conteúdo de resposta |
| `400` | Dados inválidos ou token de logout ausente/inválido |
| `401` | Access token ausente, inválido ou expirado |
| `404` | Recurso inexistente ou não pertencente ao usuário |

## Testes

Execute os testes do backend com:

```powershell
python manage.py test
```

Os testes cobrem autenticação JWT, cadastro, edição e exclusão de usuários, logout, CORS e CRUD de projetos.
