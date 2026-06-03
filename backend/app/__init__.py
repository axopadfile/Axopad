import logging, warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from flask import Flask, jsonify
from flask_cors import CORS
from app.config import Config
from app.utils.logger import get_logger

logger = get_logger(__name__)


def create_app(config_class: type = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.json.ensure_ascii = False
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    logging.getLogger("werkzeug").setLevel(logging.WARNING)

    from app.api.token import bp as token_bp
    from app.api.trade import bp as trade_bp
    from app.api.feed import bp as feed_bp

    app.register_blueprint(token_bp, url_prefix="/api/token")
    app.register_blueprint(trade_bp, url_prefix="/api/trade")
    app.register_blueprint(feed_bp, url_prefix="/api/feed")

    @app.route("/health")
    def health():
        return jsonify({"status": "ok", "service": "axopad"})

    logger.info("Axopad backend initialized")
    return app
