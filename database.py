import os

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def conectar_db(app):

    url = os.getenv("DATABASE_URL")

    if url:

        url = url.replace(
            "postgres://",
            "postgresql://",
            1
        )

    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = url

    app.config[
        "SQLALCHEMY_TRACK_MODIFICATIONS"
    ] = False

    db.init_app(app)


# =====================================
# TABLA USUARIOS
# =====================================

class Usuario(db.Model):

    __tablename__ = "usuarios"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre = db.Column(
        db.String(150),
        nullable=False
    )

    email = db.Column(
        db.String(200),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(300),
        nullable=False
    )

    premium = db.Column(
        db.Boolean,
        default=False
    )


# =====================================
# TABLA HISTORIAL
# =====================================

class Historial(db.Model):

    __tablename__ = "historial"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "usuarios.id"
        )
    )

    pregunta = db.Column(
        db.Text
    )

    respuesta = db.Column(
        db.Text
    )


# =====================================
# CREAR TABLAS
# =====================================

def crear_tablas(app):

    with app.app_context():

        db.create_all()

        print(
            "✅ Base de datos conectada"
        )
