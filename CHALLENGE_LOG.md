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

**Decisões:** ✅ Manter a paridade entre desenvolvimento e produção desde o início.  
✅ Separar ambientes (`.env.dev`, `.env.production`) para facilitar testes e deploy.

---

## ☁️ Deploy na AWS

### 🗓️ Dia 2 - Primeira Subida na EC2

- Deploy realizado manualmente em instância Ubuntu (EC2).  
- Ajustes no `ALLOWED_HOSTS` para incluir o IP público da instância.  
- Docker configurado para aceitar variáveis via `env_file` no `docker-compose.yml`.

**Desafios e Soluções:** ❌ `DisallowedHost` ao acessar pelo navegador → ✅ IP adicionado ao `.env`.  
❌ Falha ao copiar `.env.production` no build → ✅ Variáveis passadas via `env_file`.

**Resultado:** Aplicação disponível publicamente com sucesso.

---

## ⚙️ Funcionalidades Implementadas

- CRUD de médicos e pacientes.  
- Agendamento de consultas com verificação de disponibilidade.  
- Endpoint para listar consultas por médico e por paciente.  
- Middleware de permissões para garantir acesso autorizado.  
- Autenticação JWT implementada.
- Documentação Swagger integrada com `drf-spectacular`.

---

## 📄 Documentação e DevOps

### 🗓️ Dia 3 - CI/CD e Documentação

- Estrutura inicial de pipeline com GitHub Actions criada para:  
  - `Lint` (flake8, black, isort)  
  - `Test` (testes automatizados Django)  
  - `Build` da imagem Docker  
  - `Deploy` automático para ambientes de desenvolvimento e produção (dev e main)

- Variáveis de ambiente configuradas via GitHub Secrets para maior segurança.  
- Deploy configurado para usar docker-compose com migrate automático nos containers, diferenciando `docker-compose.yml` para dev e `docker-compose.prod.yml` para produção.
- Remoção de IPs sensíveis da documentação pública.

**Resultado:** O processo de integração e e entrega contínua está padronizado e automatizado, com deploy direcionado corretamente para `dev` e `main`, reduzindo erros humanos e acelerando o ciclo de deploy.

---

## 🐞 Problemas Notáveis

- **Erro:** `DisallowedHost: Invalid HTTP_HOST header`  
  - **Causa:** IP não listado no `ALLOWED_HOSTS`  
  - **Solução:** Inserir IP no `.env`

- **Erro:** `failed to compute cache key: "/.env.production": not found`  
  - **Causa:** `.env` ignorado no build por segurança  
  - **Solução:** Passar variáveis em tempo de execução com `env_file`

- **Erro:** `dial tcp: lookup ***: no such host` durante o deploy via GitHub Actions.
  - **Causa:** Configuração incorreta do segredo SSH_HOST_PROD/SSH_HOST, que estava recebendo um caminho de chave SSH em vez do endereço IP público ou nome de domínio do servidor. O runner do GitHub Actions não conseguia resolver o "host" fornecido.
  - **Solução:** Corrigir os segredos no GitHub Actions para que `SSH_HOST_PROD` e `SSH_HOST` contivessem o endereço IP público correto do servidor (ou nome de domínio resolúvel externamente).

---

## 🧭 Próximos Passos

- [x] Automatizar pipeline de CI/CD até produção  
- [ ] Configurar HTTPS com Nginx + Let's Encrypt  
- [ ] Migrar PostgreSQL para Amazon RDS  
- [ ] Implementar testes automatizados com cobertura  
- [ ] Auditar segurança da API com ferramentas como OWASP ZAP
