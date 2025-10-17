from flask import Flask
from flask_cors import CORS
from api.routes import chat_bp
from utils.config import Config


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)


    # Register blueprints
    app.register_blueprint(chat_bp, url_prefix='/api')


    # Error handlers
    @app.errorhandler(400)
    def bad_request(e):
        return {'error': 'Bad Request'}, 400


    @app.errorhandler(500)
    def server_error(e):
        return {'error': 'Internal Server Error'}, 500


    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)