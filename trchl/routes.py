import json
import os
import secrets
from sys import api_version
import requests
from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from PIL import Image
from trchl import app, bcrypt, db
from trchl.forms import FormEditProfile, FormLogin, FormNewPost, FormRegister
from trchl.models import Post, User


@app.route("/")
def index():
    posts = Post.query.order_by(Post.id_post.desc()).all()
    qnt_posts = len(posts)
    return render_template('index.html', posts=posts, qnt_posts=qnt_posts)


@app.route("/fluffy")
def fluffy():
    url = "https://dog.ceo/api/breed/corgi/images/random"
    response = requests.request("GET", url)
    corgi = json.loads(response.text)['message']
    print(f"ans== {corgi} and type== {type(corgi)}")

    return render_template('fluffy.html', corgi=corgi)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form_login = FormLogin()

    if form_login.validate_on_submit():
        user = User.query.filter_by(email=form_login.email.data).first()
        if user and bcrypt.check_password_hash(user.passwd, form_login.passwd.data):
            login_user(user, remember=form_login.remember_session.data)
            # Login successfull message and redirecting to index
            flash(f'Login successfull. You are now logged as {form_login.email.data}', 'alert-success')
            next_parameter = request.args.get('next')
            if next_parameter:
                return redirect(next_parameter)
            else:
                return redirect(url_for('index'))
        else:
            flash(f"Login attempt failed. E-mail ({form_login.email.data}) and password don't match or  e-mail not registered.", 'alert-danger')

    return render_template('login.html', form_login=form_login)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form_register = FormRegister()

    if form_register.validate_on_submit():
        crypt_passwd = bcrypt.generate_password_hash(form_register.passwd.data)
        user = User(username=form_register.username.data, email=form_register.email.data, passwd=crypt_passwd)
        db.session.add(user)
        db.session.commit()

        # Login successfull message and redirecting to index
        flash(f"{form_register.email.data} account's create successfully!", 'alert-success')
        return redirect(url_for('login'))

    return render_template('register.html', form_register=form_register)


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/users")
@login_required
def users():
    users_list = User.query.all()
    return render_template('users.html', users_list=users_list)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been successfully logged out!', 'alert-primary')
    return redirect(url_for('index'))


@app.route("/profile")
@login_required
def profile():
    profile_pic = url_for('static', filename=f'profile_pictures/{current_user.profile_pic}')
    return render_template('profile.html', profile_pic=profile_pic)


def save_profile_pic(picture):
    # adds a random name to each picture to avoid duplicated names
    cod = secrets.token_hex(8)
    name, extension = os.path.splitext(picture.filename)
    final_pic_name = name + cod + extension
    full_path = os.path.join(app.root_path, 'static/profile_pictures', final_pic_name)
    # resize picture
    size = (320, 320)
    resized_pic = Image.open(picture)
    resized_pic.thumbnail(size, Image.LANCZOS)
    # saves the pictures in the right folder
    resized_pic.save(full_path)
    # change the path and file name of users picture
    return final_pic_name


def update_tech(form):
    favs_list = []
    for field in form:
        if 'tech_' in field.name:
            if field.data:
                favs_list.append(field.label.text)
    return ', '.join(favs_list)


@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form_edit = FormEditProfile()
    if form_edit.validate_on_submit():
        current_user.fullname = form_edit.fullname.data
        current_user.email = form_edit.email.data
        current_user.username = form_edit.username.data
        current_user.place = form_edit.place.data
        # checking if the user added a new picture to the form
        if form_edit.profile_pic.data:
            pic_name = save_profile_pic(form_edit.profile_pic.data)
            current_user.profile_pic = pic_name
        if form_edit.remove_pic.data == "I don't want a picture":
            current_user.profile_pic = 'default.jpg'
        current_user.fav_tech = update_tech(form_edit)
        db.session.commit()
        flash(f'Profile updated successfully!', 'alert-success')
        return redirect(url_for('profile'))
    elif request.method == "GET":
        form_edit.fullname.data = current_user.fullname
        form_edit.username.data = current_user.username
        form_edit.email.data = current_user.email
        form_edit.place.data = current_user.place

    profile_pic = url_for('static', filename=f'profile_pictures/{current_user.profile_pic}')
    return render_template('edit_profile.html', profile_pic=profile_pic, form_edit=form_edit)


@app.route("/post/newpost", methods=['GET', 'POST'])
@login_required
def new_post():
    form_new_post = FormNewPost()
    if form_new_post.validate_on_submit():
        post = Post(title=form_new_post.title.data, body=form_new_post.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Post submitted successfully!", 'alert-success')
        return redirect(url_for('index'))
    return render_template('newpost.html', form_new_post=form_new_post)


@app.route('/post/<id_post>', methods=['GET', 'POST'])
@login_required
def show_post(id_post):
    post = Post.query.get(id_post)
    if current_user == post.author:
        # The form to edit a post is basically the same used to create a new post, the difference is that they will load the previous information to be edited
        form_edit_post = FormNewPost()
        if request.method == 'GET':
            form_edit_post.title.data = post.title
            form_edit_post.body.data = post.body
        if form_edit_post.validate_on_submit():
            post.title = form_edit_post.title.data
            post.body = form_edit_post.body.data
            db.session.commit()
            flash('Changes saved successfully', 'alert-info')
    else:
        # If the current_user isn't the psot author, the form won't be shown
        form_edit_post = None
    return render_template('post.html', post=post, form_edit_post=form_edit_post)


@app.route('/post/<id_post>/remove', methods=['GET', 'POST'])
@login_required
def remove_post(id_post):
    post = Post.query.get(id_post)
    # Making sure that current_user is the author, then removing it from db
    if current_user == post.author:
        db.session.delete(post)
        db.session.commit()
        flash('Post removed successfully', 'alert-danger')
        return redirect(url_for('index'))
    else:
        abort(403)
