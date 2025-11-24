from flask import Blueprint, request, jsonify
from database import db
from modelos.cadaver import Cadaver
import json

cadaver_bp = Blueprint("cadaver_bp", __name__)

@cadaver_bp.get("/cadaver")
def obtener():
    cad = Cadaver.query.first()
    if not cad:
        return jsonify(None)
    return jsonify(cad.to_dict())

@cadaver_bp.post("/cadaver")
def guardar():
    data = request.json

    json_data = json.dumps(data, ensure_ascii=False)

    existente = Cadaver.query.first()
    if existente:
        existente.data = json_data
        db.session.commit()
        return jsonify({"ok": True, "msg": "Actualizado"})

    nuevo = Cadaver(data=json_data)
    db.session.add(nuevo)
    db.session.commit()

    return jsonify({"ok": True, "msg": "Guardado"})

@cadaver_bp.delete("/cadaver")
def borrar():
    cad = Cadaver.query.first()
    if cad:
        db.session.delete(cad)
        db.session.commit()

    return jsonify({"ok": True})
