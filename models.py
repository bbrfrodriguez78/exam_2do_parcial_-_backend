from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Ingrediente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)
    tipo = db.Column(db.String(50), nullable=False)
    imagen = db.Column(db.String(200), nullable=True)
    precio = db.Column(db.Float, nullable=False)