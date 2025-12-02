from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Usuario

bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

@bp.route('/')
def listar():
    usuarios = Usuario.query.all()
    return render_template('usuarios/listar.html', usuarios=usuarios)

@bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        usuario = Usuario()
        usuario.usuario = request.form['usuario']
        usuario.nombre = request.form['nombre']
        usuario.apellido = request.form.get('apellido', '')
        usuario.rol = request.form.get('rol', 'cajero')
        usuario.establecer_password(request.form['password'])
        
        db.session.add(usuario)
        db.session.commit()
        flash('Usuario creado exitosamente', 'success')
        return redirect(url_for('usuarios.listar'))
    
    return render_template('usuarios/formulario.html', usuario=None)

@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    usuario = Usuario.query.get_or_404(id)
    
    if request.method == 'POST':
        usuario.usuario = request.form['usuario']
        usuario.nombre = request.form['nombre']
        usuario.apellido = request.form.get('apellido', '')
        usuario.rol = request.form.get('rol', 'cajero')
        
        if request.form.get('password'):
            usuario.establecer_password(request.form['password'])
        
        db.session.commit()
        flash('Usuario actualizado exitosamente', 'success')
        return redirect(url_for('usuarios.listar'))
    
    return render_template('usuarios/formulario.html', usuario=usuario)
