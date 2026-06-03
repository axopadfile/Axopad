from flask import Blueprint, jsonify, request
from app.services.registry import launcher, discovery, analyst
from app.utils.logger import get_logger

bp = Blueprint("token", __name__)
logger = get_logger(__name__)


@bp.post("/launch")
def launch():
    body = request.get_json(silent=True) or {}
    for f in ["name", "ticker", "creator"]:
        if not body.get(f):
            return jsonify({"error": f"Missing: {f}"}), 400
    try:
        token = launcher.launch(
            name=body["name"],
            ticker=body["ticker"],
            description=body.get("description", ""),
            creator=body["creator"],
            image_url=body.get("image_url", ""),
            twitter=body.get("twitter", ""),
            telegram=body.get("telegram", ""),
            website=body.get("website", ""),
        )
        return jsonify(token.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Launch error: {e}")
        return jsonify({"error": str(e)}), 500


@bp.get("/<token_id>")
def get_token(token_id: str):
    token = launcher.get(token_id)
    if not token:
        return jsonify({"error": "Token not found"}), 404
    d = token.to_dict()
    d["graduation_progress"] = round(discovery.graduation_progress(token), 4)
    d["curve"] = token.curve.to_dict()
    return jsonify(d)


@bp.get("/")
def list_tokens():
    status = request.args.get("status")
    tokens = launcher.list_all(status=status)
    return jsonify({"tokens": [t.to_dict() for t in tokens], "total": len(tokens)})


@bp.post("/<token_id>/analyze")
def analyze(token_id: str):
    token = launcher.get(token_id)
    if not token:
        return jsonify({"error": "Token not found"}), 404
    summary = (
        f"{token.ticker} ({token.name}): "
        f"market cap {token.market_cap_sol():.2f} SOL, "
        f"price {token.curve.price:.10f} SOL, "
        f"volume {token.volume_sol:.2f} SOL, "
        f"{token.trade_count} trades, {token.holder_count} holders, "
        f"status {token.status.value}, "
        f"graduation progress {discovery.graduation_progress(token)*100:.1f}%"
    )
    try:
        result = analyst.analyze(summary)
        return jsonify(result.to_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 500
