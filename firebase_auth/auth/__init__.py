from flask import current_app, Flask
from config import DevelopmentConfig
from firebase_auth import initialize_firebase

def create_app(config=DevelopmentConfig):
    """Create an application instance with the desired configuration.
    
    Also where extentions and blueprints are registerd with the instance
    """
    app = Flask(__name__)
    app.config.from_object(config)

    # Initialize Firebase
    initialize_firebase()

    # Register Blueprints
    from auth.routes import bp as auth_bp

    app.register_blueprint(auth_bp)
    # Register Extensions
    

    # Test Route
    @app.route('/hello')
    def hello():
        return 'Hello, Auth'
    
    return app
