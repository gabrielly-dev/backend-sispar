# Projeto Sispar - API Backend

## Descrição
API backend para gerenciamento de colaboradores e reembolsos, seguindo o padrão MVC. Implementa autenticação, validação, documentação Swagger e deploy.

## Tecnologias
- Python 3
- Flask
- SQLAlchemy
- Flask-JWT-Extended
- Flasgger (Swagger)
- Flask-CORS

## Como clonar e executar

1. Clone o repositório:
```
git clone <URL_DO_REPOSITORIO>
cd Sispar-t3
```

2. Crie e ative um ambiente virtual:
```
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Instale as dependências:
```
pip install -r requirements.txt
```

4. Configure variáveis de ambiente no arquivo `.env` (exemplo):
```
FLASK_APP=src.run.py
FLASK_ENV=development
JWT_SECRET_KEY=sua_chave_secreta
DATABASE_URL=sqlite:///db.sqlite3
```

5. Execute a aplicação:
```
flask run
```

## Rotas principais

### Colaborador
- `POST /colaborador/cadastrar` - Cadastrar novo colaborador
- `POST /colaborador/login` - Login colaborador
- `GET /colaborador/todos-colaboradores` - Listar todos colaboradores (token requerido)
- `PUT /colaborador/atualizar/<id>` - Atualizar colaborador (token requerido)
- `DELETE /colaborador/deletar/<id>` - Deletar colaborador (token requerido)

### Reembolso
- `GET /reembolso/todos-reembolsos` - Listar todos reembolsos (token requerido)
- `POST /reembolso/solicitar` - Solicitar novo reembolso (token requerido)
- `GET /reembolso/prestacao/<num_prestacao>` - Buscar reembolso por número de prestação (token requerido)
- `PUT /reembolso/atualizar/<id>` - Atualizar reembolso (token requerido)
- `DELETE /reembolso/deletar/<id>` - Deletar reembolso (token requerido)

## Documentação
A documentação Swagger está disponível em:
```
http://localhost:5000/apidocs/
```

## Extras implementados
- Autorização com tokens JWT nas rotas protegidas
- Documentação Swagger para todas as rotas
- Rotas de atualização e deleção para colaboradores e reembolsos
- Relacionamento entre colaboradores e reembolsos no banco de dados

## Observações
- Utilize o Git Flow para gerenciamento de branches (desenvolvimento e produção)
- Validações adicionais podem ser implementadas conforme necessidade

## Contato
Para dúvidas ou contribuições, abra uma issue ou envie um pull request.

---
Projeto final do ciclo Fullstack Be-digital
