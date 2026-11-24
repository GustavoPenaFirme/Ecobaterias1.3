# EcoBateria

Sistema web acessível para gestão e mapeamento de pontos de coleta de pilhas e baterias.

**Projeto Integrador em Computação II — UNIVESP (2026)**

Grupo: Gustavo da Silva Pena Firme, Thiago Moura, Lucas Vieira, Eric Amadeu de Lima  
Orientador: Monize Luiz Santos

## Funcionalidades

- Cadastro e autenticação de usuários
- Área do cliente (painel) com registro de arrecadações
- Listagem de pontos de coleta
- Painel administrativo (pontos, indicadores, solicitações)
- Interface com recursos de acessibilidade (skip-link, labels, contraste, navegação por teclado)
- Pronto para deploy em nuvem (Render / Gunicorn + PostgreSQL)

## Tecnologias

- Python 3 / Flask
- Flask-SQLAlchemy + Flask-Login
- SQLite (local) ou PostgreSQL (produção)
- HTML/CSS acessível

## Como rodar localmente

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

Acesse: http://127.0.0.1:5000

### Contas de demonstração

| Perfil | E-mail | Senha |
|--------|--------|--------|
| Usuário | pena.gustavo@gmail.com | senha123 |
| Admin | admin@ecobateria.app | admin123 |

## Deploy (Render)

1. Conecte este repositório no [Render](https://render.com)
2. Crie um **Web Service** (Python) e um **PostgreSQL**
3. Variáveis de ambiente:
   - `SECRET_KEY` — chave secreta forte
   - `DATABASE_URL` — connection string do PostgreSQL (fornecida pelo Render)
4. Start command: `gunicorn "app:create_app()"`

## Estrutura

```
ecobateria/
├── app.py              # Application factory
├── config.py
├── models.py           # User, PontoColeta, Arrecadacao, SolicitacaoRetirada
├── routes/
│   ├── auth.py
│   ├── main.py
│   └── admin.py
├── templates/
├── static/css/
├── requirements.txt
├── Procfile
└── README.md
```

## Licença

Uso acadêmico — UNIVESP Projeto Integrador 2026.
