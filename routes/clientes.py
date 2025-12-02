from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Cliente

bp = Blueprint('clientes', __name__, url_prefix='/clientes')

@bp.route('/')
def listar():
    clientes = Cliente.query.all()
    return render_template('clientes/listar.html', clientes=clientes)

@bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        cliente = Cliente()
        cliente.nombre = request.form['nombre']
        cliente.apellido = request.form.get('apellido', '')
        cliente.telefono = request.form.get('telefono', '')
        cliente.email = request.form.get('email', '')
        cliente.tipo = request.form.get('tipo', 'regular')
        
        db.session.add(cliente)
        db.session.commit()
        flash('Cliente creado exitosamente', 'success')
        return redirect(url_for('clientes.listar'))
    
    return render_template('clientes/formulario.html', cliente=None)

@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    cliente = Cliente.query.get_or_404(id)
    
    if request.method == 'POST':
        cliente.nombre = request.form['nombre']
        cliente.apellido = request.form.get('apellido', '')
        cliente.telefono = request.form.get('telefono', '')
        cliente.email = request.form.get('email', '')
        cliente.tipo = request.form.get('tipo', 'regular')
        
        db.session.commit()
        flash('Cliente actualizado exitosamente', 'success')
        return redirect(url_for('clientes.listar'))
    
    return render_template('clientes/formulario.html', cliente=cliente)

@bp.route('/eliminar/<int:id>')
def eliminar(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    flash('Cliente eliminado exitosamente', 'success')
    return redirect(url_for('clientes.listar'))

@bp.route('/ver/<int:id>')
def ver(id):
    cliente = Cliente.query.get_or_404(id)
    return render_template('clientes/ver.html', cliente=cliente)