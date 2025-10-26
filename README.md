# Zenos Finly

Resumo rápido
-------------

Zenos Finly é uma aplicação Django para gerenciamento financeiro (contas, transações, cartões, faturas, transações recorrentes e um módulo de investimentos). Este README descreve os pontos-chave do projeto e os passos para executar a aplicação localmente.

Stack principal
---------------
- Backend: Python 3.11, Django 5.x
- Banco: PostgreSQL (configurado via variáveis de ambiente)
- Frontend tooling: Node.js + Tailwind / PostCSS (apenas para build de CSS)
- Estrutura recomendada: código Django dentro de `backend/`, templates em `backend/templates`, app principal `cash_flow`

Estrutura importante (resumo)
-----------------------------
- backend/manage.py — entrypoint Django
- backend/app/ — settings, asgi, wsgi
- backend/cash_flow/ — app principal (models, views, templates)
- backend/templates/ — templates globais
- static/ — assets (Tailwind output)
- .env — variáveis de ambiente (não comitar)
- package.json / package-lock.json — frontend build tools

Pré-requisitos
--------------
- Windows (PowerShell) — instruções abaixo usam PowerShell
- Python 3.11
- PostgreSQL (ou ajuste DATABASES para outro SGDB)
- Node.js + npm
- git

Instalação / Quickstart (Windows PowerShell)
--------------------------------------------
1. Clone o repositório:
   ```powershell
   git clone <repo-url>
   cd zenos-finly
   ```

2. Crie e ative virtualenv:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
   ```

3. Instale dependências Python:
   ```powershell
   pip install -r requirements.txt
   ```
   - Se receber erro `ModuleNotFoundError: No module named 'dotenv'`, instale:
     ```powershell
     pip install python-dotenv
     ```

4. Instale dependências Node (se for usar build de CSS/Tailwind):
   ```powershell
   npm install
   ```
   - Build de CSS (exemplo, ajuste conforme scripts no package.json):
     ```powershell
     npm run build
     ```

5. Configure variáveis de ambiente
   - Copie o `.env` de exemplo (ou crie) na raiz do projeto e preencha:
     ```
     DB_NAME=zenos_finly
     DB_USER=postgres
     DB_PASS=senha
     DB_HOST=localhost
     DB_PORT=5432
     DEBUG=True
     SECRET_KEY=sua-chave-secreta
     ```
   - O arquivo `.env` já deve estar listado em `.gitignore` (não comitar).

6. Configure o banco (Postgres)
   - Crie o banco e o usuário conforme as variáveis acima.
   - Execute migrações:
     ```powershell
     cd backend
     python manage.py migrate
     ```

7. Crie superuser:
   ```powershell
   python manage.py createsuperuser
   ```

8. Inicie o servidor de desenvolvimento:
   ```powershell
   python manage.py runserver
   ```
   - Acesse: http://127.0.0.1:8000/

Notas de configuração e debugging
---------------------------------
- DJANGO_SETTINGS_MODULE
  - O projeto já define `DJANGO_SETTINGS_MODULE = 'app.settings'` em manage.py/asgi/wsgi. Execute comandos a partir da pasta `backend` (onde está `manage.py`) ou ajuste `PYTHONPATH`.
  - VS Code launch.json já configura `program: ${workspaceFolder}\backend\manage.py` e `env.PYTHONPATH: ${workspaceFolder}\backend`.

- Usuário customizado
  - O app usa `AUTH_USER_MODEL = 'cash_flow.User'` (settings). Se alterar o modelo de usuário após migrações iniciais, atenção: pode ser necessário resetar DB/migrations.

- Erros comuns
  - ModuleNotFoundError: No module named 'dotenv' → instalar `python-dotenv`.
  - ModuleNotFoundError: No module named 'controle_pedidos' → referências antigas ao nome do pacote; verifique `DJANGO_SETTINGS_MODULE`, `ROOT_URLCONF` e PYTHONPATH.
  - Clash em campos do usuário (groups / user_permissions) → verifique se existe duplicação de modelos User; manter `AUTH_USER_MODEL` consistente.

- Arquivos ignorados pelo git
  - Assegure que `.gitignore` inclui: `venv/`, `node_modules/`, `.env`, `__pycache__/`, `*.pyc`, `db.sqlite3` (se aplicável), `staticfiles/`, `.vscode/`.

Como desenvolver
----------------
- Views principais em `backend/cash_flow/views.py`
- Gerenciadores/serviços em `backend/cash_flow/api/` (ex.: `transaction_manager.py`, `bank_account_manager.py`)
- Modelos em `backend/cash_flow/models.py`
- Template de formulário de transação: `backend/templates/transaction_form.html`
- Para criar um novo app:
  ```powershell
  cd backend
  python manage.py startapp <nome_app>
  ```
  - Adicione o app em `INSTALLED_APPS` em `backend/app/settings.py`.

Testes
------
- Rodar testes Django:
  ```powershell
  cd backend
  python manage.py test
  ```

Boas práticas
-------------
- Não comitar `.env` ou segredos.
- Fazer migrações e revisar `AUTH_USER_MODEL` antes de rodar em produção.
- Usar branches e PRs para alterações maiores.

Contribuição
------------
- Abra uma issue descrevendo o problema ou a feature.
- Crie branch, implemente e envie PR com descrição clara das mudanças.

Licença
-------
- Ajuste conforme necessidade; se não definido, inclua uma licença no repositório.

Contato
-------
- Para dúvidas técnicas, use
