from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'truth777'

# toolbar = DebugToolbarExtension(app)


connect_db(app)
db.create_all()


@app.route('/')
def root():
    
posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("posts/home.html", posts=posts)
    return redirect("/users")


@app.route('/users')
def users_index():
    
    users = User.query.order_by(User.last_name, User.first_name).all()
    
    
    return render_template('index.html', users=users)


@app.route('/users/new', methods=["GET"])
def users_new_form():
    

    return render_template('add.html')

@app.route("/users/new", methods=["POST"])
def users_add_form():
    

    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>')
def display_users(user_id):
    

    user = User.query.get_or_404(user_id)
    return render_template('display.html', user=user)


@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    

    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users") 

  

  @app.route('/users/<int:user_id>/posts/new')
def posts_new_form(user_id):
   

    user = User.query.get_or_404(user_id)
    return render_template('posts/add.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def posts_new(user_id):
    """Handle form submission for creating a new post for a specific user"""

    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user)

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")

    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def posts_show(post_id):
    

    post = Post.query.get_or_404(post_id)
    return render_template('posts/display.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):
    

    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    

    return redirect(f"/users/{post.user_id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_destroy(post_id):
    

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title} successfully removed.")

    return redirect(f"/users/{post.user_id}")