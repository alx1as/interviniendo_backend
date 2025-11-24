from flask import Flask
from flask_cors import CORS
from config import Config
from database import db

# Crear la app primero
app = Flask(__name__)
app.config.from_object(Config)

CORS(app, supports_credentials=True)

# Inicializar DB
db.init_app(app)

# Importar modelos DESPUÉS de crear app y db
from modelos.poema import Poema
from modelos.comentario import Comentario

# Importar rutas DESPUÉS de modelos
from rutas.poemas import poemas_bp
from rutas.cadaver import cadaver_bp
from rutas.usuarios import usuarios_bp
from rutas.comentarios import comentarios_bp
from rutas.cadaver_db import cadaver_db_bp

# Registrar blueprints
app.register_blueprint(cadaver_db_bp, url_prefix="/api")
app.register_blueprint(poemas_bp, url_prefix="/api")
app.register_blueprint(cadaver_bp, url_prefix="/api")
app.register_blueprint(usuarios_bp, url_prefix="/api")
app.register_blueprint(comentarios_bp, url_prefix="/api")

##receteo de base de datos de prueba
# ─────────────────────────────────────────────
# ENDPOINT ADMIN PARA RESETEAR TODA LA BASE
# ─────────────────────────────────────────────
from flask import request, jsonify

@app.route("/api/admin/reset_db", methods=["POST"])
def reset_db():
    token = request.args.get("token")

    # Cambiá este token por uno privado momentáneo
    if token != "limpiar123":
        return jsonify({"error": "no autorizado"}), 403

    # Borrar todas las tablas
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        db.session.execute(table.delete())

    db.session.commit()

    return jsonify({"ok": True, "msg": "Base vaciada correctamente"})

# Crear tablas
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
