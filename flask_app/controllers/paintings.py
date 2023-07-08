from flask import render_template, request, session, redirect
from flask_app import app
from flask_app.models.painting import Painting
from flask_app.models.user import User

@app.route('/paintings')
def paintings():
    if not 'user_id' in session:
        return redirect('/')
    
    logged_user = User.get_by_id({'id' : session['user_id']})

    result = Painting.get_all()
    return render_template("paintings.html", logged_user = logged_user, paintings = result)

@app.route('/paintings/new')
def get_create_page():
    logged_user = User.get_by_id({'id' : session['user_id']})
    return render_template('new_painting.html', logged_user = logged_user)

@app.route('/paintings/new', methods=['POST'])
def create():
    if not Painting.validation(request.form):
        return redirect('/paintings/new')
    Painting.create(request.form)
    return redirect('/paintings')

@app.route('/paintings/<int:id>')
def show(id):
    logged_user = User.get_by_id({'id' : session['user_id']})
    painting = Painting.get_by_id({'id': id})
    return render_template('show_painting.html', painting = painting, logged_user = logged_user)

@app.route('/paintings/<int:id>/edit')
def show_edit_page(id):
    logged_user = User.get_by_id({'id' : session['user_id']})
    painting = Painting.get_by_id({'id': id})
    return render_template('edit_painting.html', painting = painting, logged_user = logged_user)

@app.route('/paintings/<int:id>/edit', methods = ['POST'])
def update(id):
    if not Painting.validation(request.form):
        return redirect(f'/paintings/{id}/edit')
    
    painting = Painting.update(request.form)
    return redirect("/paintings")

@app.route('/paintings/delete/<int:id>')
def delete(id):
    result = Painting.delete({'id': id})
    return redirect('/paintings')