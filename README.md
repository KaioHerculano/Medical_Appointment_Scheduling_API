# Medical Appointment Scheduling API

API desenvolvida com Django e Django Rest Framework para gestão de doutores e agendamento de consultas médicas.

## ✨ Features

- Gerenciamento completo (CRUD) de Médicos.
- Gerenciamento completo (CRUD) de Consultas.
- Autenticação segura via JSON Web Tokens (JWT).
- Busca de consultas por médico.
- Ambiente totalmente containerizado com Docker para desenvolvimento e produção.

## 🚀 Endpoints da API

A API está disponível em `http://localhost:8000/api/v1/` quando rodada localmente.
Para ambientes de deploy (staging/produção), utilize o domínio correspondente.

### Autenticação (Token JWT)
- `POST /api/v1/authentication/token/` - Obter token de acesso e refresh
- `POST /api/v1/authentication/token/refresh/` - Renovar token de acesso
- `POST /api/v1/authentication/token/verify/` - Verificar validade do token

### Médicos
- `GET /api/v1/doctors/` - Listar todos os médicos
- `POST /api/v1/doctors/` - Criar um novo médico
- `GET /api/v1/doctors/{id}/` - Obter detalhes de um médico específico
- `PUT /api/v1/doctors/{id}/` - Atualizar todos os campos de um médico
- `PATCH /api/v1/doctors/{id}/` - Atualizar parcialmente um médico
- `DELETE /api/v1/doctors/{id}/` - Excluir um médico

### Consultas
- `GET /api/v1/consultations/` - Listar todas as consultas
- `POST /api/v1/consultations/` - Criar uma nova consulta
- `GET /api/v1/consultations/{id}/` - Obter detalhes de uma consulta específica
- `PUT /api/v1/consultations/{id}/` - Atualizar todos os campos de uma consulta
- `PATCH /api/v1/consultations/{id}/` - Atualizar parcialmente uma consulta
- `DELETE /api/v1/consultations/{id}/` - Excluir uma consulta
- `GET /api/v1/consultations/doctor/{doctor_id}/` - Listar consultas de um médico específico

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python 3.11, Django 5.2, Django REST Framework
- **Banco de Dados:** PostgreSQL
- **Autenticação:** djangorestframework-simplejwt (JWT)
- **Gerenciamento de Dependências:** Poetry
- **Servidor WSGI:** Gunicorn
- **Containerização:** Docker, Docker Compose
- **Orquestração de CI/CD:** GitHub Actions
- **Testes:** Pytest
- **Qualidade de Código:** Black, Flake8, Isort

## ⚙️ Setup e Instalação

O projeto é projetado para ser executado com Docker, garantindo consistência entre os ambientes.

### Pré-requisitos
- Docker
- Docker Compose

### Passos para Execução

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/KaioHerculano/Medical_Appointment_Scheduling_API.git
    cd Medical_Appointment_Scheduling_API
    ```

2.  **Configure o Ambiente:**
    * **Para usar PostgreSQL (padrão):** Copie o arquivo de configuração de desenvolvimento. As variáveis neste arquivo já estão configuradas para o serviço do PostgreSQL no `docker-compose`.

        ```bash
        cp .env.dev .env
        ```

    * **(Opcional) Para usar SQLite:** Se desejar rodar com um banco de dados `db.sqlite3` local, você precisará alterar o arquivo `settings.py` para que o Django utilize a configuração de banco de dados nomeada `'dev'`.

3.  **Inicie a Aplicação:**
    O script de `entrypoint` irá executar as migrações do banco de dados (PostgreSQL ou SQLite, dependendo da sua configuração) automaticamente.

    ```bash
    docker-compose up -d --build
    ```
    A aplicação estará disponível em `http://localhost:8000`.

4.  **Crie um Superusuário (Opcional):**
    Este comando permite criar um usuário administrador para acessar o Django Admin.

    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

## ✅ Execução dos Testes

Os testes foram construídos utilizando a classe `APITestCase` do Django REST Framework e são executados dentro do ambiente Docker para garantir consistência.

-   **Para rodar a suíte de testes:**
    ```bash
    docker-compose exec web poetry run pytest
    ```

## 🚀 Fluxo de CI/CD

Este projeto utiliza **GitHub Actions** para automatizar o processo de integração contínua e deploy contínuo, garantindo a qualidade do código e a entrega eficiente para diferentes ambientes.

* **Branches Monitoradas:** `dev` e `main`.
* **Pipeline de Build:**
    * Ao fazer `push` para `dev` ou `main`, o pipeline de CI é acionado.
    * Ele configura o ambiente Python, instala dependências com Poetry, executa verificações de qualidade de código (Linting com Flake8, Black, Isort) e roda a suíte de testes unitários e de integração.
    * As variáveis de ambiente do PostgreSQL são selecionadas dinamicamente (`_PROD` para `main`, e `_DEV` para `dev`).
* **Pipeline de Deploy (CD):**
    * Após o sucesso do pipeline de build, o deploy é iniciado.
    * **Deploy para Desenvolvimento:** Commits na branch `dev` acionam o deploy para o ambiente de desenvolvimento, utilizando o `docker-compose.yml` padrão.
    * **Deploy para Produção:** Commits na branch `main` acionam o deploy para o ambiente de produção, utilizando o `docker-compose.prod.yml` e variáveis de ambiente específicas (`_PROD` para host, usuário e chaves SSH).
    * O deploy Pulls a última versão do código do repositório e reinicia os serviços Docker para aplicar as mudanças.

## 🧠 Decisões Técnicas

-   **Docker & Docker Compose:** Escolhidos para criar um ambiente padronizado e reprodutível, eliminando inconsistências entre desenvolvimento e produção e simplificando o setup do projeto.
-   **Gunicorn:** Utilizado como servidor WSGI de produção por ser robusto e performático, gerenciando múltiplos processos para lidar com requisições concorrentes, algo que o servidor de desenvolvimento do Django não suporta.
-   **Poetry:** Adotado para o gerenciamento de dependências e ambientes virtuais, por garantir a resolução de dependências de forma determinística e facilitar a separação entre pacotes de desenvolvimento e produção.
-   **GitHub Actions:** Implementado para automatizar os testes, linters e o deploy, garantindo um fluxo de trabalho ágil e confiável.

## 📝 Histórico do Desafio

Para um registro detalhado dos erros encontrados, decisões tomadas e melhorias propostas durante o desenvolvimento deste projeto, consulte o arquivo [CHALLENGE_LOG.md](CHALLENGE_LOG.md). (Sugestão: crie este arquivo para documentar sua jornada).

## 📜 Licença

Este projeto está licenciado sob a Licença MIT.

## 👨‍💻 Autor

- **Kaio Herculano** - [kaioherculano12@gmail.com](mailto:kaioherculano12@gmail.com)
