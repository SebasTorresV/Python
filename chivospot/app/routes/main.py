from __future__ import annotations

from flask import Blueprint, jsonify

main_bp = Blueprint("main", __name__)


@main_bp.get("/health")
def health():
    """Return a simple health check payload."""
    return jsonify({"status": "ok"})


@main_bp.get("/")
def index() -> str:
    """Temporary landing page placeholder until templates arrive."""
    return (
        "Bienvenido a Chivospot. Pronto podrás descubrir eventos cercanos desde "
        "esta página."
    )
