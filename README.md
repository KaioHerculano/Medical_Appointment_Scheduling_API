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

O projeto é projetado para ser executado com Docker, garantindo consistência entre os ambientes.

### Pré-requisitos
- Docker
- Docker Compose

### Passos para Execução

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/seu-usuario/Medical_Appointment_Scheduling_API.git](https://github.com/seu-usuario/Medical_Appointment_Scheduling_API.git)
   cd Medical_Appointment_Scheduling_API
   ```

2. **Configure o Ambiente:**
    - **Para usar PostgreSQL (padrão):** Copie o arquivo de configuração de desenvolvimento. As variáveis neste arquivo já estão configuradas para o serviço do PostgreSQL no `docker-compose`.
      ```bash
      cp .env.dev .env
      ```
    - **(Opcional) Para usar SQLite:** Se desejar rodar com um banco de dados `db.sqlite3` local, você precisará alterar o arquivo `settings.py` para que o Django utilize a configuração de banco de dados nomeada `'dev'`.

3. **Inicie a Aplicação:**
   O script de `entrypoint` irá executar as migrações do banco de dados (PostgreSQL ou SQLite, dependendo da sua configuração) automaticamente.
   ```bash
   docker-compose up -d --build
   ```
   A aplicação estará disponível em `http://localhost:8000`.

4. **Crie um Superusuário (Opcional):**
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

## 🧠 Decisões Técnicas

-   **Docker & Docker Compose:** Escolhidos para criar um ambiente padronizado e reprodutível, eliminando inconsistências entre desenvolvimento e produção e simplificando o setup do projeto.
-   **Gunicorn:** Utilizado como servidor WSGI de produção por ser robusto e performático, gerenciando múltiplos processos para lidar com requisições concorrentes, algo que o servidor de desenvolvimento do Django não suporta.
-   **Poetry:** Adotado para o gerenciamento de dependências e ambientes virtuais, por garantir a resolução de dependências de forma determinística e facilitar a separação entre pacotes de desenvolvimento e produção.

## 📝 Histórico do Desafio

Para um registro detalhado dos erros encontrados, decisões tomadas e melhorias propostas durante o desenvolvimento deste projeto, consulte o arquivo [CHALLENGE_LOG.md](CHALLENGE_LOG.md). (Sugestão: crie este arquivo para documentar sua jornada).

## 📜 Licença

Este projeto está licenciado sob a Licença MIT.

## 👨‍💻 Autor

- **Kaio Herculano** - [kaioherculano12@gmail.com](mailto:kaioherculano12@gmail.com)
