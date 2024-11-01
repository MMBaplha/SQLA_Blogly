"""Blogly application."""

from flask import Flask, render_template, redirect, request, flash, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__, template_folder="templates")

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mbAlpha7343'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

app.app_context().push()

connect_db(app)
db.create_all()

@app.route('/')
def home():
    """Redirect to list of users."""

    return redirect('/users')

@app.route('/users')
def list_users():
    """List users and show information of users."""

    users = User.query.all()
    return render_template("/users/list.html", users=users)

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete a user and redirect to the list of users."""

    user = User.query.get_or_404(user_id) 
    db.session.delete(user)  
    db.session.commit() 
    flash(f"User {user.first_name} {user.last_name} has been deleted.")
    return redirect(url_for('list_users'))  

@app.route('/users/new', methods=['GET'])
def new_user():
    """Show form to add a new user."""

    return render_template('/users/new_user.html')

@app.route('/users/new', methods=['POST'])
def add_user():
    """Add user and redirect to list."""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form.get('image_url', '')

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    flash(f"User {first_name} {last_name} added!")
    return redirect('/users')

@app.route('/users/<int:user_id>', methods=['GET'])
def user_detail(user_id):
    """Show details of a specific user."""

    user = User.query.get_or_404(user_id)
    return render_template('/users/user_detail.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    """Edit user details."""
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.image_url = request.form.get('image_url', '')
        db.session.commit()
        flash(f"User {user.first_name} {user.last_name} has been updated.")
        return redirect(url_for('user_detail', user_id=user.id))

    return render_template('/users/edit_user.html', user=user)

if __name__ == "__main__":
    app.run(debug=True)