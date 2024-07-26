from flask import Blueprint, request, jsonify, send_from_directory
from models import db, Ingrediente
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

bp = Blueprint('ingredients', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/ingredients', methods=['POST'])
def create_ingredient():
    try:
        if 'imagen' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['imagen']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            data = request.form
            nuevo_ingrediente = Ingrediente(
                nombre=data['nombre'],
                descripcion=data.get('descripcion', ''),
                tipo=data['tipo'],
                imagen=filename,
                precio=float(data['precio'])
            )
            db.session.add(nuevo_ingrediente)
            db.session.commit()
            return jsonify({"id": nuevo_ingrediente.id}), 201

        return jsonify({"error": "File not allowed"}), 400
    except Exception as e:
        print(f"Error en create_ingredient: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@bp.route('/ingredients', methods=['GET'])
def search_ingredients():
    try:
        ingredientes = Ingrediente.query.all()
        return jsonify([{
            'id': i.id,
            'nombre': i.nombre,
            'descripcion': i.descripcion,
            'tipo': i.tipo,
            'precio': i.precio,
            'imagen': i.imagen
        } for i in ingredientes])
    except Exception as e:
        print(f"Error en search_ingredients: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

#-----
@bp.route('/ingredients/<int:id>', methods=['DELETE'])
def delete_ingredient(id):
    try:
        ingrediente = Ingrediente.query.get(id)
        if not ingrediente:
            return jsonify({"error": "Ingrediente no encontrado"}), 404

        # Eliminar archivo de imagen si existe
        if ingrediente.imagen:
            filepath = os.path.join(UPLOAD_FOLDER, ingrediente.imagen)
            if os.path.exists(filepath):
                os.remove(filepath)

        db.session.delete(ingrediente)
        db.session.commit()
        return jsonify({"message": "Ingrediente eliminado"}), 200
    except Exception as e:
        print(f"Error en delete_ingredient: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
#-------


@bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
