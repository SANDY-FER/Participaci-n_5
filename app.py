from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Conectar a la base de datos SQLite
def get_db_connection():
    conn = sqlite3.connect('almacen.db')
    conn.row_factory = sqlite3.Row
    return conn

# Crear la base de datos y la tabla si no existe
def create_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS producto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Página principal: Listar productos
@app.route('/')
def index():
    conn = get_db_connection()
    productos = conn.execute('SELECT * FROM producto').fetchall()
    conn.close()
    return render_template('index.html', productos=productos)

# Página para agregar un producto
@app.route('/agregar', methods=('GET', 'POST'))
def agregar_producto():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        cantidad = request.form['cantidad']
        precio = request.form['precio']
        
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO producto (descripcion, cantidad, precio)
            VALUES (?, ?, ?)
        ''', (descripcion, cantidad, precio))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    return render_template('agregar_producto.html')

# Página para editar un producto
@app.route('/editar/<int:id>', methods=('GET', 'POST'))
def editar_producto(id):
    conn = get_db_connection()
    producto = conn.execute('SELECT * FROM producto WHERE id = ?', (id,)).fetchone()
    
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        cantidad = request.form['cantidad']
        precio = request.form['precio']
        
        conn.execute('''
            UPDATE producto SET descripcion = ?, cantidad = ?, precio = ?
            WHERE id = ?
        ''', (descripcion, cantidad, precio, id))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    conn.close()
    return render_template('editar_producto.html', producto=producto)

# Eliminar un producto
@app.route('/eliminar/<int:id>', methods=('POST',))
def eliminar_producto(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM producto WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    create_db()  # Crear la base de datos al iniciar
    app.run(debug=True)
