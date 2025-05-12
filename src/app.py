# RESPONSAVEL POR CRIAR A APLICAÇÃO 
from flask import Flask, jsonify, redirect
from src.controller.colaborador_controller import bp_colaborador
from src.controller.reembolso_controller import bp_reembolso
from src.model import db
from config import Config
from flask_cors import CORS
from flasgger import Swagger
from flask_jwt_extended import JWTManager

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app, origins="*")
    app.register_blueprint(bp_colaborador)
    app.register_blueprint(bp_reembolso)
    if test_config:
        app.config.from_object(test_config)
    else:
        app.config.from_object(Config)

    db.init_app(app)
    jwt = JWTManager(app)

    swagger = Swagger(app, config=swagger_config)

    import logging

    @app.route('/apispec.json')
    def apispec():
        specs = swagger.get_apispecs()
        if specs:
            logging.info("Especificação OpenAPI gerada com sucesso.")
            return jsonify(specs[0])
        else:
            logging.error("Falha ao gerar a especificação OpenAPI.")
            return jsonify({"error": "Especificação não disponível"}), 500

    @app.route('/')
    def index():
        return redirect('/apidocs/')

    with app.app_context():
        db.create_all()
    return app
