# Medical Appointment Scheduling API

API desenvolvida com Django e Django Rest Framework para gestão de doutores e agendamento de consultas médicas.

## ✨ Features

- Gerenciamento completo (CRUD) de Médicos.
- Gerenciamento completo (CRUD) de Consultas.
- Autenticação segura via JSON Web Tokens (JWT).
- Busca de consultas por médico.
- Ambiente totalmente containerizado com Docker para desenvolvimento e produção.

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python 3.11, Django 5.2, Django REST Framework
- **Banco de Dados:** PostgreSQL
- **Autenticação:** djangorestframework-simplejwt (JWT)
- **Gerenciamento de Dependências:** Poetry
- **Servidor WSGI:** Gunicorn
- **Containerização:** Docker, Docker Compose
- **Testes:** Pytest
- **Qualidade de Código:** Black

## ⚙️ Setup e Instalação

Existem duas maneiras de executar o projeto: via Docker (recomendado) ou configurando um ambiente local.

### 1. Rodando com Docker (Recomendado)

Este método garante um ambiente padronizado e isolado, idêntico ao de produção.

**Pré-requisitos:**
- Docker
- Docker Compose

**Passos:**
1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/seu-usuario/Medical_Appointment_Scheduling_API.git](https://github.com/seu-usuario/Medical_Appointment_Scheduling_API.git)
   cd Medical_Appointment_Scheduling_API
   ```

2. **Crie o arquivo de ambiente:**
   Use o arquivo `.env.dev` como base para o ambiente de desenvolvimento.
   ```bash
   cp .env.dev .env
   ```

3. **Construa e inicie os contêineres:**
   ```bash
   docker-compose up -d --build
   ```
   A aplicação estará disponível em `http://localhost:8000`.

4. **Execute as migrações do banco de dados:**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. **Crie um superusuário (Opcional):**
   Este comando permite criar um usuário administrador para acessar o Django Admin.
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

### 2. Rodando Localmente

1. **Clone o repositório** e instale os pré-requisitos (Python 3.11+, Poetry, PostgreSQL).

2. **Instale as dependências:**
   ```bash
   poetry install
   ```

3. **Ative o ambiente virtual:**
   ```bash
   poetry shell
   ```

4. **Configure o `.env`** com as credenciais do seu banco de dados local.

5. **Execute as migrações e inicie o servidor:**
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

## ✅ Execução dos Testes

Os testes foram construídos utilizando a classe `APITestCase` do Django REST Framework para simular requisições à API.

-   **Para rodar os testes com Docker:**
    ```bash
    docker-compose exec web poetry run pytest
    ```

-   **Para rodar os testes localmente:**
    ```bash
    poetry run pytest
    ```

## 🧠 Decisões Técnicas

-   **Docker & Docker Compose:** Escolhidos para criar um ambiente padronizado e reprodutível, eliminando inconsistências entre desenvolvimento e produção e simplificando o setup do projeto.
-   **Gunicorn:** Utilizado como servidor WSGI de produção por ser robusto e performático, gerenciando múltiplos processos para lidar com requisições concorrentes, algo que o servidor de desenvolvimento do Django não suporta.
-   **Poetry:** Adotado para o gerenciamento de dependências e ambientes virtuais, por garantir a resolução de dependências de forma determinística e facilitar a separação entre pacotes de desenvolvimento e produção.
-   **GitHub Actions:** Selecionado para CI/CD pela sua integração nativa com o repositório, permitindo automatizar os processos de teste e deploy de forma segura e eficiente.

## 📝 Histórico do Desafio

Para um registro detalhado dos erros encontrados, decisões tomadas e melhorias propostas durante o desenvolvimento deste projeto, consulte o arquivo [CHALLENGE_LOG.md](CHALLENGE_LOG.md). (Sugestão: crie este arquivo para documentar sua jornada).

## 📜 Licença

Este projeto está licenciado sob a Licença MIT.

## 👨‍💻 Autor

- **Kaio Herculano** - [kaioherculano12@gmail.com](mailto:kaioherculano12@gmail.com)
