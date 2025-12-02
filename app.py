from flask import Flask, redirect, url_for
from config import Config
from models import db
from routes import productos, ventas, clientes, usuarios, compras, categorias

app = Flask(__name__)
app.config.from_object(Config)

# Inicializar base de datos
db.init_app(app)

# Registrar blueprints
app.register_blueprint(productos.bp)
app.register_blueprint(ventas.bp)
app.register_blueprint(clientes.bp)
app.register_blueprint(usuarios.bp)
app.register_blueprint(compras.bp)
app.register_blueprint(categorias.bp)

@app.route('/')
def index():
    return redirect(url_for('productos.catalogo'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Crear datos de ejemplo
        from models import CategoriaProducto, Producto, MetodoPago
        
        if CategoriaProducto.query.count() == 0:
            categorias = [
                CategoriaProducto(nombre='Bebidas Calientes', descripcion='Café, té y chocolate'),
                CategoriaProducto(nombre='Bebidas Frías', descripcion='Jugos, batidos y sodas'),
                CategoriaProducto(nombre='Postres', descripcion='Tortas, galletas y dulces'),
                CategoriaProducto(nombre='Snacks', descripcion='Bocadillos y aperitivos')
            ]
            for cat in categorias:
                db.session.add(cat)
            
            productos = [
                Producto(nombre='Café Americano', categoria_id=1, sku='CAF001', 
                        precio_venta=2.50, stock=100, unidad='taza'),
                Producto(nombre='Cappuccino', categoria_id=1, sku='CAF002', 
                        precio_venta=3.50, stock=100, unidad='taza'),
                Producto(nombre='Latte', categoria_id=1, sku='CAF003', 
                        precio_venta=4.00, stock=100, unidad='taza'),
                Producto(nombre='Jugo Natural', categoria_id=2, sku='JUG001', 
                        precio_venta=3.00, stock=50, unidad='vaso'),
                Producto(nombre='Batido de Fresa', categoria_id=2, sku='BAT001', 
                        precio_venta=4.50, stock=50, unidad='vaso'),
                Producto(nombre='Torta de Chocolate', categoria_id=3, sku='TOR001', 
                        precio_venta=3.50, stock=20, unidad='porción'),
                Producto(nombre='Croissant', categoria_id=4, sku='SNK001', 
                        precio_venta=2.00, stock=30, unidad='unidad')
            ]
            for prod in productos:
                db.session.add(prod)
            
            metodos = [
                MetodoPago(nombre='Efectivo', detalles='Pago en efectivo'),
                MetodoPago(nombre='Tarjeta', detalles='Tarjeta de crédito/débito'),
                MetodoPago(nombre='Transferencia', detalles='Transferencia bancaria')
            ]
            for metodo in metodos:
                db.session.add(metodo)
            
            db.session.commit()
            print("Datos de ejemplo creados exitosamente")
    
    app.run(debug=True)