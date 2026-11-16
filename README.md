# Hub-de-Projetos-Pernambucanos

“  Recife é um polo de excelência em ensino e pesquisa, abrigando universidades, institutos federais e centros de inovação de renome (UFPE, UPE, IFPE, CESAR School, etc.). Anualmente, milhares de pesquisas, teses, dissertações e projetos inovadores são desenvolvidos, muitos com enorme potencial de aplicação prática. 
No entanto, esse conhecimento permanece, em grande parte, restrito ao ambiente acadêmico. Gestores públicos e empresários locais não possuem um canal centralizado e de fácil acesso para descobrir o que está sendo produzido. Essa falha de comunicação representa uma imensa perda de oportunidade: a cidade busca soluções para problemas que a academia pode já estar resolvendo, e o mercado demanda inovações que poderiam nascer dessas pesquisas.

Este desafio visa solucionar a desconexão entre o conhecimento gerado nas universidades e a demanda por inovação no governo e no mercado. A proposta é criar o "Hub de Inovação e Pesquisa de Recife", um dashboard online e interativo que centraliza e categoriza os projetos acadêmicos e pesquisas da cidade. Com filtros inteligentes e contatos diretos, a plataforma permitirá que empresas e gestores públicos encontrem soluções, talentos e oportunidades de parceria, transformando o conhecimento acadêmico em desenvolvimento econômico e social.  “

  Nós, integrantes da Capi+, decidimos assumir esse desafio por acreditar que esta problemática atualmente está precisando de mais visibilidade. Existem diversos projetos inovadores por todo Pernambuco, como por exemplo o EcoTuba — uma pesquisa que desenvolve sistemas de monitoramento de tubarões no estado, facilitando a identificação de suas localizações. Por conta dessa falta de visibilidade, consequentemente acaba sendo difícil os projetos serem desenvolvidos pela falta de investimento por parte das empresas.

## Requisitos
Para instalar e rodar este projeto você precisa:

- Node.js (Ambiente de execução para Javascript)
- Git (Caso vá clonar o repositório pelo terminal)
- NPM (Gerenciador de pacotes instalado junto com o Node)

## Como rodar o Servidor
Caso tenha baixado o arquivo ZIP, extraia-o. Se preferir clonar via GitHub, abra o terminal e digite:

```
git clone <url-do-repositorio>
```
```
cd Hub-de-Projetos-Pernambucanos
```
Instale as dependências do projeto (caso ainda não estejam instaladas):

* npm install
* npm start

## Linguagems Utilizadas
* Javascript (Backend e Frontend)

## Frameworks e Bibliotecas Utilizadas
* Node.js (Ambiente de execução)

<br>

## SESSÃO BACK-END

Esta seção contém o guia completo para configuração, instalação de dependências e execução do servidor **Back-end (Django / Python)** do projeto **Hub de Projetos Pernambucanos**.

---

## 1. Pré-requisitos

- **Python 3.10+** instalado
- **Git** (caso vá clonar o repositório)

---

## 2. Passo a Passo para Execução

### Passo 1: Entrar na pasta do Back-end
Toda a execução de comandos, configurações e servidor devem ser realizados estritamente dentro da pasta `back-end`:

```bash
cd back-end
```

### Passo 2: Criar e Ativar o Ambiente Virtual (`venv`)

1. **Criar o ambiente isolado:**
   ```bash
   python -m venv venv
   ```

2. **Ativar o ambiente:**
   - **Windows (PowerShell):**
     ```powershell
     .\venv\Scripts\Activate
     ```
   - **Windows (CMD):**
     ```cmd
     .\venv\Scripts\activate.bat
     ```
   - **Linux / macOS:**
     ```bash
     source venv/bin/activate
     ```

> **Nota:** Certifique-se de que o identificador `(venv)` está visível no seu terminal antes de prosseguir.

### Passo 3: Instalar as Dependências

Com o ambiente virtual ativado, instale os pacotes listados no `requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

### Passo 4: Configurar Variáveis de Ambiente (`.env`)

Crie um arquivo `.env` dentro do diretório `back-end/` (no mesmo nível do `manage.py`) com o seguinte conteúdo:

```env
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
```

### Passo 5: Executar Migrações do Banco de Dados

Para gerar e aplicar a estrutura das tabelas no banco de dados local (SQLite):

```bash
python manage.py makemigrations
python manage.py migrate
```

### Passo 6: Iniciar o Servidor

Execute o comando para subir o servidor de desenvolvimento:

```bash
python manage.py runserver
```

O servidor estará acessível em: `http://127.0.0.1:8000/`

---
*Para encerrar a execução do servidor, pressione `CTRL + C` no terminal.*