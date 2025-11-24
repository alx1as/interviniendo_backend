from flask import Blueprint, request, jsonify
from database import db
from modelos.cadaver import Cadaver
import json

cadaver_db_bp = Blueprint("cadaver_db_bp", __name__)


@cadaver_db_bp.get("/cadaver")
def obtener():
    cad = Cadaver.query.first()
    if not cad:
        return jsonify(None)
    return jsonify(cad.to_dict())


@cadaver_db_bp.post("/cadaver")
def guardar():
    data = request.json

    # convertir dict a string JSON
    serializado = json.dumps(data, ensure_ascii=False)

    existente = Cadaver.query.first()
    if existente:
        existente.data = serializado
        db.session.commit()
        return jsonify({"ok": True, "msg": "Actualizado"})

    nuevo = Cadaver(data=serializado)
    db.session.add(nuevo)
    db.session.commit()

    return jsonify({"ok": True, "msg": "Guardado"})


@cadaver_db_bp.delete("/cadaver")
def borrar():
    cad = Cadaver.query.first()
    if cad:
        db.session.delete(cad)
        db.session.commit()
    return jsonify({"ok": True})
