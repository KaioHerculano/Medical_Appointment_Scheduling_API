# Challenge Log - API de Consultas Médicas

Este documento detalha a evolução do desenvolvimento da API de Agendamento e Consultas Médicas, os desafios enfrentados e as decisões técnicas tomadas ao longo do projeto.

---

## 🔧 Setup Inicial

- **Framework:** Django REST Framework
- **Containerização:** Docker e Docker Compose
- **Gerenciador de dependências:** Poetry

### 🗓️ Dia 1 - Inicialização do Projeto

- Projeto Django criado com estrutura básica para agendamento de consultas e gerenciamento de médicos.
- Docker e Docker Compose configurados com suporte a PostgreSQL.
- Poetry configurado e dependências organizadas no `pyproject.toml`.
- Ambiente levantado com sucesso via `docker-compose up`.

**Decisões:**  
✅ Manter a paridade entre desenvolvimento e produção desde o início.  
✅ Separar ambientes (`.env.dev`, `.env.prod`) para facilitar testes e deploy.

---

## ☁️ Deploy na AWS

### 🗓️ Dia 2 - Primeira Subida na EC2

- Deploy realizado manualmente em instância Ubuntu (EC2).
- Ajustes no `ALLOWED_HOSTS` para incluir o IP público da instância.
- Docker configurado para aceitar variáveis via `env_file` no `docker-compose.yml`.

**Desafios e Soluções:**  
❌ `DisallowedHost` ao acessar pelo navegador → ✅ IP adicionado ao `.env`.  
❌ Falha ao copiar `.env.production` no build → ✅ Variáveis passadas via `env_file`.

**Resultado:** Aplicação disponível publicamente com sucesso.

---

## ⚙️ Funcionalidades Implementadas

- CRUD de médicos e pacientes.
- Agendamento de consultas com verificação de disponibilidade.
- Endpoint para listar consultas por médico e por paciente.
- Middleware de permissões para garantir acesso autorizado.
- Documentação Swagger integrada com `drf-spectacular`.

---

## 📄 Documentação e DevOps

### 🗓️ Dia 3 - CI/CD e Documentação

- Estrutura inicial de pipeline com GitHub Actions:
  - `Lint`
  - `Test`
  - `Build`
  - (Futura etapa de Deploy)
- Criação do `README.md` como ponto central de instruções e decisões.
- Remoção de IPs sensíveis da documentação pública.

**Melhorias Visadas:**  
🚧 Finalizar CI/CD com deploy automático na AWS.  
🚧 Configurar domínio com HTTPS via Let's Encrypt.  
🚧 Criar ambiente staging com subdomínio (`dev-api` etc).

---

## 🐞 Problemas Notáveis

- **Erro:** `DisallowedHost: Invalid HTTP_HOST header`
  - **Causa:** IP não listado no `ALLOWED_HOSTS`
  - **Solução:** Inserir IP no `.env`

- **Erro:** `failed to compute cache key: "/.env.production": not found`
  - **Causa:** `.env` ignorado no build por segurança
  - **Solução:** Passar variáveis em tempo de execução com `env_file`

---

## 🧭 Próximos Passos

- [ ] Automatizar pipeline de CI/CD até produção
- [ ] Configurar HTTPS com Nginx + Let's Encrypt
- [ ] Migrar PostgreSQL para Amazon RDS
- [ ] Implementar testes automatizados com cobertura
- [ ] Auditar segurança da API com ferramentas como OWASP ZAP

