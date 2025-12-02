from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Compra, ItemCompra, Producto
from decimal import Decimal
from datetime import datetime

bp = Blueprint('compras', __name__, url_prefix='/compras')

@bp.route('/')
def listar():
    compras = Compra.query.order_by(Compra.fecha.desc()).all()
    return render_template('compras/listar.html', compras=compras)

@bp.route('/nueva', methods=['GET', 'POST'])
def nueva():
    if request.method == 'POST':
        try:
            compra = Compra()
            compra.nombre_proveedor = request.form['nombre_proveedor']
            compra.numero_documento = f"C-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            compra.subtotal = Decimal(request.form.get('subtotal', 0))
            compra.impuesto = Decimal(request.form.get('impuesto', 0))
            compra.total = Decimal(request.form.get('total', 0))
            
            db.session.add(compra)
            db.session.flush()
            
            import json
            items = json.loads(request.form.get('items', '[]'))
            
            for item_data in items:
                item = ItemCompra()
                item.compra_id = compra.id
                item.producto_id = item_data['producto_id']
                item.cantidad = Decimal(item_data['cantidad'])
                item.costo_unitario = Decimal(item_data['costo_unitario'])
                item.total_linea = Decimal(item_data['total_linea'])
                
                db.session.add(item)
                
                producto = Producto.query.get(item.producto_id)
                if producto:
                    producto.stock += item.cantidad
                    if item.costo_unitario > 0:
                        producto.precio_costo = item.costo_unitario
            
            db.session.commit()
            flash('Compra registrada exitosamente', 'success')
            return redirect(url_for('compras.ver', id=compra.id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error al procesar la compra: {str(e)}', 'danger')
    
    productos = Producto.query.filter_by(activo=True).all()
    return render_template('compras/nueva.html', productos=productos)

@bp.route('/ver/<int:id>')
def ver(id):
    compra = Compra.query.get_or_404(id)
    return render_template('compras/ver.html', compra=compra)