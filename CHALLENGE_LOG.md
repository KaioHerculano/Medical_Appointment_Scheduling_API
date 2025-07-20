Diário de Bordo do Desafio - API de Agendamento
Este documento registra a jornada de desenvolvimento, os desafios encontrados, as decisões tomadas e as melhorias propostas durante a criação da API de Agendamento Médico.

Visão Geral do Desafio
O objetivo principal foi construir uma API RESTful robusta para gerenciamento de médicos e consultas, utilizando Django e Docker, e prepará-la para um ambiente de produção na AWS.

Log de Atividades e Decisões
Dia 1: Setup Inicial e Containerização
Atividade: Estrutura inicial do projeto Django criada.

Decisão: Adotar o Docker e Docker Compose desde o início para garantir a paridade entre os ambientes de desenvolvimento e produção.

Decisão: Utilizar o Poetry para gerenciamento de dependências, por sua capacidade de criar builds determinísticos com o poetry.lock.

Resultado: Ambiente de desenvolvimento rodando com sucesso via docker-compose up.

Dia 2: Deploy na AWS e Configuração do Ambiente
Atividade: Primeiro deploy realizado em uma instância EC2 (Ubuntu) na AWS.

Desafio: Erro DisallowedHost ao tentar acessar a aplicação pelo IP público.

Solução: Adicionado o IP da instância à variável ALLOWED_HOSTS no arquivo .env e reiniciado os contêineres.

Desafio: Dificuldade em encontrar e carregar o arquivo .env correto durante o build do Docker.

Solução: Removida a cópia do .env no Dockerfile e adotada a prática de injetar as variáveis de ambiente via a opção env_file no docker-compose.yml, o que é mais seguro e flexível.

Resultado: Aplicação acessível publicamente na AWS.

Dia 3: Automação e Documentação
Atividade: Planejamento da pipeline de CI/CD.

Decisão: Utilizar o GitHub Actions pela sua integração nativa com o repositório. O plano inicial inclui etapas de lint, test, build e deploy.

Atividade: Criação da documentação inicial do projeto.

Decisão: O README.md foi estruturado para ser o ponto central de informação, contendo setup, instruções de teste e decisões técnicas.

Desafio: Expor IPs públicos no README.md foi identificado como um risco de segurança.

Solução: Os IPs foram removidos e a documentação foi atualizada para uma abordagem mais genérica, recomendando o uso de nomes de domínio.

Erros Notáveis e Soluções
Erro: DisallowedHost: Invalid HTTP_HOST header

Causa: O Django, por segurança, só aceita requisições de domínios listados em ALLOWED_HOSTS. Ao acessar via IP público, este não estava na lista.

Solução: Adicionar o IP público da instância EC2 à variável ALLOWED_HOSTS no arquivo de ambiente (.env) e reiniciar a aplicação.

Erro: failed to compute cache key: "/.env.production": not found durante o docker build.

Causa: O arquivo .env.production estava listado no .dockerignore ou não existia no contexto do build.

Solução: A melhor solução foi parar de copiar arquivos .env para a imagem. Em vez disso, usamos a diretiva env_file no docker-compose.yml para carregar as variáveis em tempo de execução, o que é mais seguro e flexível.

Melhorias Propostas para o Futuro:

[CI/CD] Implementar o Fluxo no GitHub Actions: Concluir a implementação da pipeline de CI/CD para automatizar completamente os testes e o deploy.

[Infraestrutura] Usar Nomes de Domínio: Registrar um domínio e configurar subdomínios (ex: api.meuprojeto.com e dev-api.meuprojeto.com) para os ambientes, utilizando o AWS Route 53.

[Segurança] Implementar HTTPS: Configurar o Nginx para usar certificados SSL/TLS do Let's Encrypt, garantindo que toda a comunicação com a API seja criptografada.

[Banco de Dados] Migrar para AWS RDS: Para um ambiente de produção mais robusto, substituir o contêiner do PostgreSQL por uma instância gerenciada do Amazon RDS, que oferece backups automáticos, escalabilidade e maior confiabilidade.

[Documentação da API] Usar Swagger/OpenAPI: Integrar o drf-yasg ou drf-spectacular para gerar uma documentação interativa da API (Swagger UI), facilitando os testes e o consumo dos endpoints.