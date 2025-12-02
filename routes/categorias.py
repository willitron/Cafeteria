from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, CategoriaProducto

bp = Blueprint('categorias', __name__, url_prefix='/categorias')

@bp.route('/')
def listar():
    categorias = CategoriaProducto.query.all()
    return render_template('categorias/listar.html', categorias=categorias)

@bp.route('/nueva', methods=['GET', 'POST'])
def nueva():
    if request.method == 'POST':
        categoria = CategoriaProducto()
        categoria.nombre = request.form['nombre']
        categoria.descripcion = request.form.get('descripcion', '')
        
        db.session.add(categoria)
        db.session.commit()
        flash('Categoría creada exitosamente', 'success')
        return redirect(url_for('categorias.listar'))
    
    return render_template('categorias/formulario.html', categoria=None)

@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    categoria = CategoriaProducto.query.get_or_404(id)
    
    if request.method == 'POST':
        categoria.nombre = request.form['nombre']
        categoria.descripcion = request.form.get('descripcion', '')
        
        db.session.commit()
        flash('Categoría actualizada exitosamente', 'success')
        return redirect(url_for('categorias.listar'))
    
    return render_template('categorias/formulario.html', categoria=categoria)

@bp.route('/eliminar/<int:id>')
def eliminar(id):
    categoria = CategoriaProducto.query.get_or_404(id)
    
    if categoria.productos:
        flash('No se puede eliminar una categoría con productos asociados', 'warning')
    else:
        db.session.delete(categoria)
        db.session.commit()
        flash('Categoría eliminada exitosamente', 'success')
    
    return redirect(url_for('categorias.listar'))