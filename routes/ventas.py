from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import db, Venta, ItemVenta, Producto, Cliente, MetodoPago, Pago
from datetime import datetime
from decimal import Decimal

bp = Blueprint('ventas', __name__, url_prefix='/ventas')

@bp.route('/')
def listar():
    ventas = Venta.query.order_by(Venta.fecha.desc()).all()
    return render_template('ventas/listar.html', ventas=ventas)

@bp.route('/nueva', methods=['GET', 'POST'])
def nueva():
    if request.method == 'POST':
        try:
            venta = Venta()
            venta.numero_documento = f"V-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            venta.cliente_id = request.form.get('cliente_id') if request.form.get('cliente_id') else None
            venta.subtotal = Decimal(request.form.get('subtotal', 0))
            venta.impuesto = Decimal(request.form.get('impuesto', 0))
            venta.descuento = Decimal(request.form.get('descuento', 0))
            venta.total = Decimal(request.form.get('total', 0))
            
            db.session.add(venta)
            db.session.flush()  # Para obtener el ID de la venta
            
            items_json = request.form.get('items', '[]')
            import json
            items = json.loads(items_json)
            
            for item_data in items:
                item = ItemVenta()
                item.venta_id = venta.id
                item.producto_id = item_data['producto_id']
                item.cantidad = Decimal(item_data['cantidad'])
                item.precio_unitario = Decimal(item_data['precio_unitario'])
                item.descuento = Decimal(item_data.get('descuento', 0))
                item.total_linea = Decimal(item_data['total_linea'])
                
                db.session.add(item)
                
                producto = Producto.query.get(item.producto_id)
                if producto:
                    producto.stock -= item.cantidad
            
            pago = Pago()
            pago.venta_id = venta.id
            pago.metodo_pago_id = request.form.get('metodo_pago_id', 1)
            pago.monto = venta.total
            db.session.add(pago)
            
            db.session.commit()
            flash('Venta registrada exitosamente', 'success')
            return redirect(url_for('ventas.ver', id=venta.id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error al procesar la venta: {str(e)}', 'danger')
            return redirect(url_for('ventas.nueva'))
    
    productos = Producto.query.filter_by(activo=True).all()
    clientes = Cliente.query.all()
    metodos_pago = MetodoPago.query.all()
    return render_template('ventas/nueva.html', 
                          productos=productos,
                          clientes=clientes,
                          metodos_pago=metodos_pago)

@bp.route('/ver/<int:id>')
def ver(id):
    venta = Venta.query.get_or_404(id)
    return render_template('ventas/ver.html', venta=venta)

@bp.route('/anular/<int:id>')
def anular(id):
    venta = Venta.query.get_or_404(id)
    
    for item in venta.items:
        producto = Producto.query.get(item.producto_id)
        if producto:
            producto.stock += item.cantidad
    
    venta.estado = 'anulada'
    db.session.commit()
    flash('Venta anulada exitosamente', 'info')
    return redirect(url_for('ventas.listar'))

@bp.route('/api/producto/<int:id>')
def api_producto(id):
    producto = Producto.query.get_or_404(id)
    return jsonify({
        'id': producto.id,
        'nombre': producto.nombre,
        'precio_venta': float(producto.precio_venta),
        'stock': float(producto.stock),
        'unidad': producto.unidad
    })