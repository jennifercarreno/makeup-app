from crypt import methods
from email.mime import image
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from makeup_app.models import User, Review
from makeup_app.extensions import app, db, bcrypt
from makeup_app.forms import  ReviewForm, SignUpForm, LoginForm
from sqlalchemy import delete
import requests, json

main = Blueprint("main", __name__)
auth = Blueprint("auth", __name__)
api = requests.get('http://makeup-api.herokuapp.com/api/v1/products.json')
products = json.loads(api.text)

# home page
@main.route('/')
def homepage():
    return render_template('home.html', prds=products[:12] )

# searches
@main.route('/search', methods=['GET', 'POST'])
def search():
    prds = []
    search = request.form['search']
    for i in range(len(products)):

        if products[i].get("name").lower() == search.lower():
            prds.append(products[i])
        elif products[i].get("brand") == search.lower():
            prds.append(products[i])
        elif products[i].get("product_type").lower() == search.lower():
            prds.append(products[i])

    return render_template('home.html', prds= prds)

@main.route('/search/<product_brand>', methods=['GET', 'POST'])
def search_brand(product_brand):
    prds = []
    brand = product_brand

    for i in range(len(products)):
        if products[i].get('brand') == brand:
            prds.append(products[i])
    return render_template('home.html', prds = prds)
# filters

# eyes
@main.route('/filter/eyes', methods=['GET', 'POST'])
def filter_eyes():
    prds = []
    eyes = ['eyebrow', 'eyeliner', 'eyeshadow', 'mascara']
    for i in range(len(eyes)):
        for p in range(len(products)):
            if products[p].get('product_type') == eyes[i]:
                prds.append(products[p])

    return render_template('home.html', prds=prds )

# lips
@main.route('/filter/lips', methods=['GET', 'POST'])
def filter_lips():
    prds = []
    lips = ['lip_liner', 'lipstick']
    for i in range(len(lips)):
        for p in range(len(products)):
            if products[p].get('product_type') == lips[i]:
                prds.append(products[p])

    return render_template('home.html', prds=prds )

# face
@main.route('/filter/face', methods=['GET', 'POST'])
def filter_face():
    prds = []
    face = ['blush', 'bronzer', 'foundation']
    for i in range(len(face)):
        for p in range(len(products)):
            if products[p].get('product_type') == face[i]:
                prds.append(products[p])

    return render_template('home.html', prds=prds )

# creates a new review
@main.route('/new_review/<product_id>', methods=['GET', 'POST'])
@login_required
def new_review(product_id):
    form = ReviewForm()

    for i in range(len(products)):
        if products[i].get('id') == int(product_id):
            product = products[i]


    if form.validate_on_submit():
        print("form submitted")
        new_review = Review(
            prd_name = product.get('name'),
            rating = form.rating.data,
            review = form.review.data,
            created_by = current_user
        )
        db.session.add(new_review)
        db.session.commit()

        flash('Success! New Review Added')
        return redirect(url_for('main.prd_detail', product_id = product_id, product = product))
    else:
        print(form.errors)
                # render_template('prd_detail.html', product_id = product_id, product = product, review_form = review_form)
        return "error in submitting review"   

# displays a product
@main.route('/product/<product_id>', methods=['GET', 'POST'])
def prd_detail(product_id):
    review_form = ReviewForm()

    for i in range(len(products)):
        if products[i].get('id') == int(product_id):
            product = products[i]

            prd_reviews = []
            all_reviews = Review.query.all()
            for review in all_reviews:
                if review.prd_name == product.get("name"):
                    prd_reviews.append(review)

    return render_template('prd_detail.html', product = product, comment_form = comment_form, review_form = review_form, comments = prd_comments, reviews = prd_reviews)

# collections

@main.route('/collections', methods=['GET'])
def collections():
    return render_template('collections.html')
# comments 



# authentication

# sign up
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

# log in
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, remember=True)
        next_page = request.args.get('next')
        return redirect(next_page if next_page else url_for('main.homepage'))
    return render_template('login.html', form=form)

# log out
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))



