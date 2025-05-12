from flask import Blueprint, request, jsonify
from src.model.reembolso_model import Reembolso
from src.model import db
from flask_jwt_extended import jwt_required
from flasgger import swag_from
from datetime import datetime

bp_reembolso = Blueprint('reembolso', __name__, url_prefix='/reembolso')

@bp_reembolso.route('/todos-reembolsos', methods=['GET'])
@jwt_required()
@swag_from('../docs/reembolso/todos_reembolsos.yml')
def pegar_todos_reembolsos():
    reembolsos = db.session.execute(
        db.select(Reembolso)
    ).scalars().all()
    reembolsos_list = [ {
        'id': r.id,
        'colaborador': r.colaborador,
        'empresa': r.empresa,
        'num_prestacao': r.num_prestacao,
        'descricao': r.descricao,
        'data': r.data.isoformat() if r.data else None,
        'tipo_reembolso': r.tipo_reembolso,
        'centro_custo': r.centro_custo,
        'ordem_interna': r.ordem_interna,
        'divisao': r.divisao,
        'pep': r.pep,
        'moeda': r.moeda,
        'distancia_km': r.distancia_km,
        'valor_km': r.valor_km,
        'valor_faturado': float(r.valor_faturado) if r.valor_faturado else None,
        'despesa': float(r.despesa) if r.despesa else None,
        'id_colaborador': r.id_colaborador,
        'status': r.status
    } for r in reembolsos]
    return jsonify(reembolsos_list), 200

@bp_reembolso.route('/solicitar', methods=['POST'])
@jwt_required()
@swag_from('../docs/reembolso/solicitar_reembolso.yml')
def solicitar_reembolso():
    dados = request.get_json()
    data_str = dados.get('data')
    data_obj = None
    if data_str:
        try:
            data_obj = datetime.strptime(data_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'mensagem': 'Formato de data inválido. Use AAAA-MM-DD.'}), 400
    novo_reembolso = Reembolso(
    colaborador=dados.get('colaborador'),
    empresa=dados.get('empresa'),
    num_prestacao=dados.get('num_prestacao'),
    descricao=dados.get('descricao'),
    data=data_obj,
    tipo_reembolso=dados.get('tipo_reembolso'),
    centro_custo=dados.get('centro_custo'),
    ordem_interna=dados.get('ordem_interna'),
    divisao=dados.get('divisao'),
    pep=dados.get('pep'),
    moeda=dados.get('moeda'),
    distancia_km=dados.get('distancia_km'),
    valor_km=dados.get('valor_km'),
    valor_faturado=dados.get('valor_faturado'),
    despesa=dados.get('despesa'),
    id_colaborador=dados.get('id_colaborador'),
    status=dados.get('status', 'Em analise')
    )
    db.session.add(novo_reembolso)
    db.session.commit()
    return jsonify({'mensagem': 'Reembolso solicitado com sucesso'}), 201

@bp_reembolso.route('/prestacao/<int:num_prestacao>', methods=['GET'])
@jwt_required()
def buscar_reembolso_por_prestacao(num_prestacao):
    reembolso = db.session.execute(
        db.select(Reembolso).where(Reembolso.num_prestacao == num_prestacao)
    ).scalar()
    if not reembolso:
        return jsonify({'mensagem': 'Reembolso não encontrado'}), 404
    reembolso_dict = {
        'id': reembolso.id,
        'colaborador': reembolso.colaborador,
        'empresa': reembolso.empresa,
        'num_prestacao': reembolso.num_prestacao,
        'descricao': reembolso.descricao,
        'data': reembolso.data.isoformat() if reembolso.data else None,
        'tipo_reembolso': reembolso.tipo_reembolso,
        'centro_custo': reembolso.centro_custo,
        'ordem_interna': reembolso.ordem_interna,
        'divisao': reembolso.divisao,
        'pep': reembolso.pep,
        'moeda': reembolso.moeda,
        'distancia_km': reembolso.distancia_km,
        'valor_km': reembolso.valor_km,
        'valor_faturado': float(reembolso.valor_faturado) if reembolso.valor_faturado else None,
        'despesa': float(reembolso.despesa) if reembolso.despesa else None,
        'id_colaborador': reembolso.id_colaborador,
        'status': reembolso.status
    }
    return jsonify(reembolso_dict), 200

@bp_reembolso.route('/atualizar/<int:id_reembolso>', methods=['PUT'])
@jwt_required()
def atualizar_reembolso(id_reembolso):
    dados = request.get_json()
    reembolso = db.session.get(Reembolso, id_reembolso)
    if not reembolso:
        return jsonify({'mensagem': 'Reembolso não encontrado'}), 404

    for key, value in dados.items():
        if hasattr(reembolso, key):
            setattr(reembolso, key, value)
    db.session.commit()
    return jsonify({'mensagem': 'Reembolso atualizado com sucesso'}), 200

@bp_reembolso.route('/deletar/<int:id_reembolso>', methods=['DELETE'])
@jwt_required()
def deletar_reembolso(id_reembolso):
    reembolso = db.session.get(Reembolso, id_reembolso)
    if not reembolso:
        return jsonify({'mensagem': 'Reembolso não encontrado'}), 404
    db.session.delete(reembolso)
    db.session.commit()
    return jsonify({'mensagem': 'Reembolso deletado com sucesso'}), 200
