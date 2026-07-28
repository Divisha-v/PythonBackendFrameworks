from flask import Flask, jsonify
from config import Config
from courses.routes import courses_bp
from flask_migrate import Migrate
from courses.models import db





migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    migrate.init_app(app,db)

    app.register_blueprint(courses_bp)



    # Global 404 Error Handler
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "status": "error",
            "message": "Resource not found"
        }), 404


    # Global 500 Error Handler
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "status": "error",
            "message": "Internal Server Error"
        }), 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)