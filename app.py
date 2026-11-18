from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///veron_store.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de la Base de Datos (El Cliente / Lead)
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    red_social = db.Column(db.String(50)) # Ej: Facebook, Instagram, WhatsApp
    producto_interes = db.Column(db.String(200))
    estado = db.Column(db.String(50), default='Nuevo Lead') # Nuevo Lead, Negociando, Ganado, Perdido
    notas = db.Column(db.Text)

# Ruta principal: Ver todos los clientes
@app.route('/')
def index():
    clientes = Cliente.query.all()
    return render_template('index.html', clientes=clientes)

# Ruta para agregar un nuevo cliente
@app.route('/add', methods=['POST'])
def add_cliente():
    nuevo_cliente = Cliente(
        nombre=request.form['nombre'],
        red_social=request.form['red_social'],
        producto_interes=request.form['producto_interes'],
        notas=request.form['notas']
    )
    db.session.add(nuevo_cliente)
    db.session.commit()
    return redirect(url_for('index'))

# Ruta para cambiar el estado (Ej: de "Nuevo Lead" a "Ganado")
@app.route('/update_status/<int:id>', methods=['POST'])
def update_status(id):
    cliente = Cliente.query.get_or_404(id)
    cliente.estado = request.form['estado']
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Crea la base de datos si no existe
    app.run(debug=True)