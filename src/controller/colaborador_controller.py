
from flask import Blueprint, request, jsonify
from src.model.colaborador_model import Colaborador
from src.model import db
from src.security.security import hash_senha, checar_senha
from flasgger import swag_from

# request -> trabalha com as requisições. Pega o conteúdo da requisição
# jsonify -> Trabalha com as respostas. Converte um dado em Json

bp_colaborador = Blueprint('colaborador', __name__, url_prefix='/colaborador')

@bp_colaborador.route('/todos-colaboradores')
def pegar_dados_todos_colaboradores():
    # Paginação para melhorar desempenho
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    query = db.select(
        Colaborador.id,
        Colaborador.nome,
        Colaborador.cargo,
        Colaborador.salario,
        Colaborador.email
    )
    
    colaboradores_pag = db.session.execute(
        query.limit(per_page).offset((page - 1) * per_page)
    ).all()
    
    colaboradores_list = []
    for c in colaboradores_pag:
        colaboradores_list.append({
            'id': c.id,
            'nome': c.nome,
            'cargo': c.cargo,
            'salario': float(c.salario) if c.salario else None,
            'email': c.email
        })
    
    return jsonify({
        'page': page,
        'per_page': per_page,
        'colaboradores': colaboradores_list
    }), 200

@bp_colaborador.route('/cadastrar', methods=['POST'])
@swag_from('../docs/colaborador/cadastrar_colaborador.yml')
def cadastrar_novo_colaborador(): 
    
    dados_requisicao = request.get_json() 

    required_fields = ['nome', 'email', 'senha', 'cargo', 'salario']
    missing_fields = [field for field in required_fields if field not in dados_requisicao]
    if missing_fields:
        return jsonify({'mensagem': f'Campos obrigatórios faltando: {", ".join(missing_fields)}'}), 400
    
    novo_colaborador = Colaborador(
        nome=dados_requisicao['nome'], # Pegue do json o valor relacionado a chave nome
        email=dados_requisicao['email'],
        senha= hash_senha(dados_requisicao['senha']) ,
        cargo=dados_requisicao['cargo'],
        salario=dados_requisicao['salario']
    )
    
#   INSERT INTO tb_colaborador (nome, email, senha, cargo, salario) VALUES (VALOR1,VALOR2,VALOR3,VALOR4,VALOR5)
    db.session.add(novo_colaborador)
    db.session.commit() # Essa linha executa a query
    
    return jsonify( {'mensagem': 'Dado cadastrado com sucesso'}), 201

# Endereco/colaborador/atualizar/1
from flask_jwt_extended import jwt_required, get_jwt_identity

@bp_colaborador.route('/atualizar/<int:id_colaborador>', methods=['PUT'])
@jwt_required()
@swag_from('../docs/colaborador/atualizar_colaborador.yml')
def atualizar_dados_do_colaborador(id_colaborador):
    dados_requisicao = request.get_json()
    colaborador = db.session.get(Colaborador, id_colaborador)
    if not colaborador:
        return jsonify({'mensagem': 'Colaborador não encontrado'}), 404

    if 'nome' in dados_requisicao:
        colaborador.nome = dados_requisicao['nome']
    if 'cargo' in dados_requisicao:
        colaborador.cargo = dados_requisicao['cargo']
    if 'email' in dados_requisicao:
        colaborador.email = dados_requisicao['email']
    if 'salario' in dados_requisicao:
        colaborador.salario = dados_requisicao['salario']

    db.session.commit()
    return jsonify({'mensagem': 'Dados do colaborador atualizados com sucesso'}), 200

@bp_colaborador.route('/deletar/<int:id_colaborador>', methods=['DELETE'])
@jwt_required()
def deletar_colaborador(id_colaborador):
    colaborador = db.session.get(Colaborador, id_colaborador)
    if not colaborador:
        return jsonify({'mensagem': 'Colaborador não encontrado'}), 404
    db.session.delete(colaborador)
    db.session.commit()
    return jsonify({'mensagem': 'Colaborador deletado com sucesso'}), 200


from flask_jwt_extended import create_access_token

@bp_colaborador.route('/login', methods=['POST'])
def login():
    
    dados_requisicao = request.get_json()
    
    email = dados_requisicao.get('email')
    senha = dados_requisicao.get('senha')
    
    if not email or not senha:
        return jsonify({'mensagem': 'Todos os dados precisam ser preenchidos'}), 400
    
    # SELECT * FROM [TABELA]
    colaborador = db.session.execute(
        db.select(Colaborador).where(Colaborador.email == email)
    ).scalar() # -> A linha de informação OU None
    
    if not colaborador:
        return jsonify({'mensagem': 'Usuario não encontrado'}), 404
    
    colaborador = colaborador.to_dict()
    
    if email == colaborador.get('email') and checar_senha(senha, colaborador.get('senha')):
        access_token = create_access_token(identity=colaborador.get('email'))
        return jsonify({'mensagem': 'Login realizado com sucesso', 'access_token': access_token}), 200
    else:
        return jsonify({'mensagem': 'Credenciais invalidas'}), 400
    
    

