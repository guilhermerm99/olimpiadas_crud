from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from models.pais import Pais
from database import get_db

pais_bp = Blueprint('pais', __name__)

# Create
@pais_bp.route('/pais', methods=['POST'])
def criar_pais():
    db: Session = next(get_db())
    data = request.json
    novo_pais = Pais(nome=data['nome'], sigla=data['sigla'], bandeira=data.get('bandeira'))
    db.add(novo_pais)
    db.commit()
    return jsonify({"message": f"País {data['nome']} criado com sucesso."}), 201

# Read
@pais_bp.route('/pais', methods=['GET'])
def listar_paises():
    db: Session = next(get_db())
    paises = db.query(Pais).all()
    return jsonify([{"id": p.id_pais, "nome": p.nome, "sigla": p.sigla} for p in paises]), 200

# Update
@pais_bp.route('/pais/<int:id_pais>', methods=['PUT'])
def atualizar_pais(id_pais):
    db: Session = next(get_db())
    pais = db.query(Pais).filter_by(id_pais=id_pais).first()
    data = request.json
    if pais:
        pais.nome = data['nome']
        pais.sigla = data['sigla']
        pais.bandeira = data.get('bandeira')
        db.commit()
        return jsonify({"message": "País atualizado com sucesso."}), 200
    return jsonify({"message": "País não encontrado."}), 404

# Delete
@pais_bp.route('/pais/<int:id_pais>', methods=['DELETE'])
def deletar_pais(id_pais):
    db: Session = next(get_db())
    pais = db.query(Pais).filter_by(id_pais=id_pais).first()
    if pais:
        db.delete(pais)
        db.commit()
        return jsonify({"message": "País excluído com sucesso."}), 200
    return jsonify({"message": "País não encontrado."}), 404
