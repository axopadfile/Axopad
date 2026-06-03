from flask import Blueprint, jsonify, request
from app.services.registry import trade_engine
from app.utils.logger import get_logger

bp = Blueprint("trade", __name__)
logger = get_logger(__name__)


@bp.post("/buy")
def buy():
    body = request.get_json(silent=True) or {}
    for f in ["token_id", "trader", "sol_in"]:
        if f not in body:
            return jsonify({"error": f"Missing: {f}"}), 400
    try:
        trade = trade_engine.buy(
            token_id=body["token_id"],
            trader=body["trader"],
            sol_in=float(body["sol_in"]),
            min_tokens_out=float(body["min_tokens_out"]) if body.get("min_tokens_out") else None,
        )
        return jsonify(trade.to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Buy error: {e}")
        return jsonify({"error": str(e)}), 500


@bp.post("/sell")
def sell():
    body = request.get_json(silent=True) or {}
    for f in ["token_id", "trader", "tokens_in"]:
        if f not in body:
            return jsonify({"error": f"Missing: {f}"}), 400
    try:
        trade = trade_engine.sell(
            token_id=body["token_id"],
            trader=body["trader"],
            tokens_in=float(body["tokens_in"]),
            min_sol_out=float(body["min_sol_out"]) if body.get("min_sol_out") else None,
        )
        return jsonify(trade.to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Sell error: {e}")
        return jsonify({"error": str(e)}), 500


@bp.get("/quote")
def quote():
    token_id = request.args.get("token_id")
    side = request.args.get("side", "buy")
    amount = float(request.args.get("amount", 0))
    if not token_id or amount <= 0:
        return jsonify({"error": "token_id and positive amount required"}), 400
    q = trade_engine.quote(token_id, side, amount)
    if not q:
        return jsonify({"error": "Token not found"}), 404
    return jsonify({
        "input_amount": q.input_amount,
        "output_amount": q.output_amount,
        "price_before": q.price_before,
        "price_after": q.price_after,
        "price_impact_pct": round(q.price_impact_pct, 4),
        "fee": q.fee,
    })


@bp.get("/history")
def history():
    token_id = request.args.get("token_id")
    limit = min(int(request.args.get("limit", 50)), 200)
    trades = trade_engine.get_trades(token_id=token_id, limit=limit)
    return jsonify({"trades": [t.to_dict() for t in trades], "total": len(trades)})
