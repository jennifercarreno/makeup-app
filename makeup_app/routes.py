from crypt import methods
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from makeup_app.models import User, Product, Comment
from makeup_app.extensions import app, db, bcrypt
from makeup_app.forms import ProductForm, CommentForm, SignUpForm, LoginForm
from sqlalchemy import delete
import requests, json

main = Blueprint("main", __name__)
auth = Blueprint("auth", __name__)
api = requests.get('http://makeup-api.herokuapp.com/api/v1/products.json')
products = json.loads(api.text)


@main.route('/')
def homepage():
    return render_template('home.html', prds= products[:15] )

# @main.route('/new_product',methods=['GET', 'POST'])
# @login_required
# def new_product():
#     form = ProductForm()

#     if form.validate_on_submit():
#         new_product = Product(
#             name = form.name.data,
#             rating = form.rating.data,
#             review = form.review.data,
#             created_by = current_user
#         )
#         db.session.add(new_product)
#         db.session.commit()

#         flash('Success! New Product Added')
#         return redirect(url_for('main.prd_detail', product_id = new_product.id))
#     else: 
#         return render_template('new_prd.html', form = form)

@main.route('/product/<product_id>', methods=['GET', 'POST'])
def prd_detail(product_id):
    for i in range(len(products)):
        if products[i].get('id') == int(product_id):
            product = products[i]

            comment_form = CommentForm()
            prd_comments = []
            all_comments = Comment.query.all()
            for comment in all_comments:
           
                if comment.prd == int(product_id):
                    prd_comments.append(comment)
    return render_template('prd_detail.html', product = product, comment_form = comment_form, comments = prd_comments)

    

# @main.route('/product/<product_id>/delete', methods=['POST'])
# @login_required
# def prd_delete(product_id):
#     sql2 = delete(Product).where(Product.id == product_id)

#     db.session.execute(sql2)
#     db.session.commit()
#     flash('Product Deleted')
#     return redirect(url_for('main.homepage'))

# @main.route('/product/<product_id>/edit', methods=['GET', 'POST'])
# @login_required
# def prd_edit(product_id):
#     product = Product.query.get(product_id)
#     form = ProductForm(obj = product)
#     if form.validate_on_submit():
#         form.populate_obj(product)
#         db.session.commit()
#         flash('Success! Item Updated')
#         product = Product.query.get(product_id)

#         return redirect(url_for('main.prd_detail', product = product, product_id = product_id))
#     else:
#         return render_template('edit_prd.html', form = form, product = product)


# comments 
@main.route('/new_comment/<product_id>', methods=['POST'])
@login_required
def new_comment(product_id):
    product = Product.query.get(product_id)
    form = CommentForm()
    prd_form = ProductForm()

    if form.validate_on_submit():
        new_comment = Comment(
            comment = form.comment.data,
            prd = product_id,
            created_by = current_user

        )

        db.session.add(new_comment)
        db.session.commit()

        flash('Success! New Comment Added')
        return redirect(url_for('main.prd_detail', product = product, product_id = product_id))
    else:
        print(" comment form not submitted ")
        return render_template('prd_detail.html', product = product, form=prd_form, comment_form=form)

@main.route('/comment/<comment_id>/delete', methods=['POST'])
@login_required
def comment_delete(comment_id):
    sql2 = delete(Comment).where(Comment.id == comment_id)

    db.session.execute(sql2)
    db.session.commit()
    flash('Comment Deleted')
    return redirect(url_for('main.homepage'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    print('in signup')
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Account Created.')
        print('created')
        return redirect(url_for('auth.login'))
    print(form.errors)
    return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, remember=True)
        next_page = request.args.get('next')
        return redirect(next_page if next_page else url_for('main.homepage'))
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))

@main.route('/search', methods=['GET', 'POST'])
def search():
    prds = []
    search = request.form['search']
    for i in range(len(products)):

        if products[i].get("name") == search:
            prds.append(products[i])
        elif products[i].get("brand") == search:
            prds.append(products[i])
        elif products[i].get("product_type") == search:
            prds.append(products[i])


    return render_template('home.html', prds= prds)
