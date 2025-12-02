from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Producto, CategoriaProducto

bp = Blueprint('productos', __name__, url_prefix='/productos')

@bp.route('/')
def listar():
    productos = Producto.query.filter_by(activo=True).all()
    return render_template('productos/listar.html', productos=productos)

@bp.route('/catalogo')
def catalogo():
    categorias = CategoriaProducto.query.all()
    categoria_id = request.args.get('categoria', type=int)
    
    if categoria_id:
        productos = Producto.query.filter_by(
            categoria_id=categoria_id, 
            activo=True
        ).all()
    else:
        productos = Producto.query.filter_by(activo=True).all()
    
    return render_template('productos/catalogo.html', 
                          productos=productos, 
                          categorias=categorias,
                          categoria_actual=categoria_id)

@bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        producto = Producto()
        producto.nombre = request.form['nombre']
        producto.sku = request.form['sku']
        producto.categoria_id = request.form['categoria_id']
        producto.descripcion = request.form.get('descripcion', '')
        producto.precio_venta = request.form['precio_venta']
        producto.precio_costo = request.form.get('precio_costo', 0)
        producto.stock = request.form.get('stock', 0)
        producto.unidad = request.form.get('unidad', 'unidad')
        
        db.session.add(producto)
        db.session.commit()
        flash('Producto creado exitosamente', 'success')
        return redirect(url_for('productos.listar'))
    
    categorias = CategoriaProducto.query.all()
    return render_template('productos/formulario.html', categorias=categorias, producto=None)

@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    producto = Producto.query.get_or_404(id)
    
    if request.method == 'POST':
        producto.nombre = request.form['nombre']
        producto.sku = request.form['sku']
        producto.categoria_id = request.form['categoria_id']
        producto.descripcion = request.form.get('descripcion', '')
        producto.precio_venta = request.form['precio_venta']
        producto.precio_costo = request.form.get('precio_costo', 0)
        producto.stock = request.form.get('stock', 0)
        producto.unidad = request.form.get('unidad', 'unidad')
        
        db.session.commit()
        flash('Producto actualizado exitosamente', 'success')
        return redirect(url_for('productos.listar'))
    
    categorias = CategoriaProducto.query.all()
    return render_template('productos/formulario.html', 
                          producto=producto, 
                          categorias=categorias)

@bp.route('/eliminar/<int:id>')
def eliminar(id):
    producto = Producto.query.get_or_404(id)
    producto.activo = False
    db.session.commit()
    flash('Producto eliminado exitosamente', 'success')
    return redirect(url_for('productos.listar'))