from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Cliente(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column('first_name', db.String(120), nullable=False)
    apellido = db.Column('last_name', db.String(120))
    telefono = db.Column('phone', db.String(80))
    email = db.Column(db.String(150))
    tipo = db.Column('type', db.String(50))
    
    ventas = db.relationship('Venta', backref='cliente', lazy=True)

class MetodoPago(db.Model):
    __tablename__ = 'payment_methods'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column('name', db.String(100), nullable=False)
    detalles = db.Column('details', db.String(200))
    
    pagos = db.relationship('Pago', backref='metodo_pago', lazy=True)

class Pago(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column('sale_id', db.Integer, db.ForeignKey('sales.id'))
    metodo_pago_id = db.Column('payment_method_id', db.Integer, 
                                db.ForeignKey('payment_methods.id'))
    monto = db.Column('amount', db.Numeric(12, 2), nullable=False)
    pagado_en = db.Column('paid_at', db.DateTime, default=datetime.utcnow)

class CategoriaProducto(db.Model):
    __tablename__ = 'product_categories'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column('name', db.String(120), nullable=False)
    descripcion = db.Column('description', db.Text)
    creado_en = db.Column('created_at', db.DateTime, default=datetime.utcnow)
    
    productos = db.relationship('Producto', backref='categoria', lazy=True)

class Producto(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    categoria_id = db.Column('category_id', db.Integer, 
                             db.ForeignKey('product_categories.id'))
    sku = db.Column(db.String(80), unique=True)
    nombre = db.Column('name', db.String(200), nullable=False)
    descripcion = db.Column('description', db.Text)
    unidad = db.Column('unit', db.String(30))
    precio_costo = db.Column('cost_price', db.Numeric(12, 2))
    precio_venta = db.Column('sale_price', db.Numeric(12, 2), nullable=False)
    stock = db.Column(db.Numeric(12, 2), default=0)
    activo = db.Column('active', db.Boolean, default=True)
    creado_en = db.Column('created_at', db.DateTime, default=datetime.utcnow)

class ItemCompra(db.Model):
    __tablename__ = 'purchase_items'
    id = db.Column(db.Integer, primary_key=True)
    compra_id = db.Column('purchase_id', db.Integer, 
                          db.ForeignKey('purchases.id'))
    producto_id = db.Column('product_id', db.Integer, 
                            db.ForeignKey('products.id'))
    cantidad = db.Column('quantity', db.Numeric(12, 3), nullable=False)
    costo_unitario = db.Column('unit_cost', db.Numeric(12, 2))
    total_linea = db.Column('line_total', db.Numeric(12, 2))
    
    producto = db.relationship('Producto', backref='items_compra')

class Compra(db.Model):
    __tablename__ = 'purchases'
    id = db.Column(db.Integer, primary_key=True)
    nombre_proveedor = db.Column('supplier_name', db.String(200))
    numero_documento = db.Column('document_number', db.String(120))
    fecha = db.Column('date', db.DateTime, default=datetime.utcnow)
    subtotal = db.Column(db.Numeric(12, 2), default=0)
    impuesto = db.Column('tax', db.Numeric(12, 2), default=0)
    total = db.Column(db.Numeric(12, 2), nullable=False)
    
    items = db.relationship('ItemCompra', backref='compra', lazy=True)

class ItemVenta(db.Model):
    __tablename__ = 'sale_items'
    id = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column('sale_id', db.Integer, db.ForeignKey('sales.id'))
    producto_id = db.Column('product_id', db.Integer, 
                            db.ForeignKey('products.id'))
    cantidad = db.Column('quantity', db.Numeric(12, 3), nullable=False)
    precio_unitario = db.Column('unit_price', db.Numeric(12, 2))
    descuento = db.Column('discount', db.Numeric(12, 2), default=0)
    total_linea = db.Column('line_total', db.Numeric(12, 2))
    
    producto = db.relationship('Producto', backref='items_venta')

class Venta(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column('customer_id', db.Integer, 
                           db.ForeignKey('customers.id'), nullable=True)
    usuario_id = db.Column('user_id', db.Integer, 
                           db.ForeignKey('users.id'), nullable=True)
    numero_documento = db.Column('document_number', db.String(120))
    fecha = db.Column('date', db.DateTime, default=datetime.utcnow)
    subtotal = db.Column(db.Numeric(12, 2), default=0)
    impuesto = db.Column('tax', db.Numeric(12, 2), default=0)
    descuento = db.Column('discount', db.Numeric(12, 2), default=0)
    total = db.Column(db.Numeric(12, 2), nullable=False)
    estado = db.Column('status', db.String(50), default='completada')
    
    items = db.relationship('ItemVenta', backref='venta', lazy=True, cascade='all, delete-orphan')
    pagos = db.relationship('Pago', backref='venta', lazy=True, cascade='all, delete-orphan')

class Usuario(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column('username', db.String(80), unique=True, nullable=False)
    hash_password = db.Column('password_hash', db.String(255), nullable=False)
    nombre = db.Column('first_name', db.String(120))
    apellido = db.Column('last_name', db.String(120))
    rol = db.Column('role', db.String(50), default='cajero')
    activo = db.Column('active', db.Boolean, default=True)
    creado_en = db.Column('created_at', db.DateTime, default=datetime.utcnow)
    
    ventas = db.relationship('Venta', backref='usuario', lazy=True)
    
    def establecer_password(self, password):
        self.hash_password = generate_password_hash(password)
    
    def verificar_password(self, password):
        return check_password_hash(self.hash_password, password)