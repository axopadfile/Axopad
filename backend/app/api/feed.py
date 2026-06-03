from flask import Blueprint, jsonify, request
from app.services.registry import discovery

bp = Blueprint("feed", __name__)


def _serialize(tokens):
    return [
        {**t.to_dict(), "graduation_progress": round(discovery.graduation_progress(t), 4)}
        for t in tokens
    ]


@bp.get("/trending")
def trending():
    limit = min(int(request.args.get("limit", 20)), 100)
    return jsonify({"tokens": _serialize(discovery.trending(limit))})


@bp.get("/new")
def newest():
    limit = min(int(request.args.get("limit", 20)), 100)
    return jsonify({"tokens": _serialize(discovery.newest(limit))})


@bp.get("/graduating")
def graduating():
    limit = min(int(request.args.get("limit", 20)), 100)
    return jsonify({"tokens": _serialize(discovery.about_to_graduate(limit))})


@bp.get("/graduated")
def graduated():
    limit = min(int(request.args.get("limit", 20)), 100)
    return jsonify({"tokens": _serialize(discovery.graduated(limit))})
