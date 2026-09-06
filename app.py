from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # Permite peticiones desde el frontend JS

def init_db():
    """Crea la base de datos y la tabla de reportes si no existen."""
    conn = sqlite3.connect('loop_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reportes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            descripcion TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/api/reportar', methods=['POST'])
def guardar_reporte():
    """Recibe la petición POST desde el formulario en JavaScript."""
    datos = request.get_json()
    usuario = datos.get('usuario')
    descripcion = datos.get('descripcion')

    # Validar que los campos no vengan vacíos
    if not usuario or not descripcion:
        return jsonify({'error': 'Faltan datos obligatorios'}), 400

    # Insertar en la base de datos SQLite
    conn = sqlite3.connect('loop_database.db')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO reportes (usuario, descripcion) VALUES (?, ?)',
        (usuario, descripcion)
    )
    conn.commit()
    conn.close()

    return jsonify({'mensaje': 'Reporte guardado exitosamente en la base de datos'}), 200

if __name__ == '__main__':
    init_db()
    print("Base de datos lista. Servidor de LOOP escuchando en http://127.0.0.1:5000")
    app.run(port=5000, debug=True)