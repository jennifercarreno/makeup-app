from asyncore import file_dispatcher
from crypt import methods
from email.mime import image
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from makeup_app.models import Collection, User, Review
from makeup_app.extensions import app, db, bcrypt
from makeup_app.forms import  ReviewForm, SignUpForm, LoginForm, CollectionForm
from sqlalchemy import delete
import requests, json

main = Blueprint("main", __name__)
auth = Blueprint("auth", __name__)
api = requests.get('http://makeup-api.herokuapp.com/api/v1/products.json')
products = json.loads(api.text)
tags = ['Chemical Free', 'Gluten Free', 'Hypoallergenic', 'Organic', 'Vegan', 'Cruelty Free', 'Oil Free']

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
    return render_template('search_results.html', prds= prds, search = search, tags=tags)

# filters
@main.route('/filter', methods=['GET', 'POST'])
def filter():
    filtered_prd = []
    prds = []
    search = request.form['search']
    filter = request.form['filter']
    for i in range(len(products)):

        if products[i].get("name").lower() == search.lower():
            prds.append(products[i])
        elif products[i].get("brand") == search.lower():
            prds.append(products[i])
        elif products[i].get("product_type").lower() == search.lower():
            prds.append(products[i])

    for prd in prds:
        if filter in prd.get('tag_list'):
            filtered_prd.append(prd)

    return render_template('search_results.html', prds=filtered_prd, search = search, tags=tags)
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
                print(type(products[p].get('brand')))
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

# deletes a review
@main.route('/review/<review_id>/delete', methods=['POST'])
@login_required
def delete_review(review_id):
    del_rv = delete(Review).where(Review.id == review_id)

    db.session.execute(del_rv)
    db.session.commit()
    flash('Review Deleted')
    return redirect(url_for('main.homepage'))

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

            collections = []
            all_collections = Collection.query.all()
            for collection in all_collections:
                if collection.created_by == current_user:
                    collections.append(collection)

    return render_template('prd_detail.html', product = product, review_form = review_form, reviews = prd_reviews, collections = collections)

# collections

@main.route('/collections', methods=['GET', 'POST'])
def collections():
    form = CollectionForm()
    test = []
    collections = Collection.query.all()
    for collection in collections:
        test.append(collection)
        print(collection.created_by)

    return render_template('collections.html', form = form, test = test)

@main.route('/collections/new_collection', methods=['GET', 'POST'])
@login_required
def new_collection():
    form  = CollectionForm()

    if form.validate_on_submit():
        print("form submitted")
        new_collection = Collection(
            title = form.title.data,
            description = form.description.data,
            products = 'empty',
            created_by = current_user
        )
        db.session.add(new_collection)
        db.session.commit()

        flash('Success! New Review Added')
        return redirect(url_for('main.collections', form = form, collections = collections))
    else:
        print(form.errors)
        return "error in submitting review"    

@main.route('/collections/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    product = request.form['product_id']
    selected_collection = request.form['collection_id']
    test_collection = Collection.query.get(selected_collection)

    for collection in Collection.query.all():
        if collection.created_by == current_user:
            test_collection.products.append(product)
            print(test_collection.products)
            flash(f'Sucess! new product added to {test_collection.title}')
    return redirect(url_for('main.collections'))

# single collection, iterate through products (get the product from the id)
@main.route('/collections/<collection_id>', methods=['GET'])
def collection_detail(collection_id):
    collection = Collection.query.get(collection_id)
    print(collection)
    print(collection.id, collection_id)
    collection_products = []
    

    for prd in collection.products:
        for i in range(len(products)):
            if products[i].get('id') == int(prd):
                if collection.id == int(collection_id):
                    collection_products.append(products[i])
                # print(f'prd:{prd} product:{products[i]}')
        
    print(collection.products)
    return render_template('collection_detail.html', collection = collection, collection_products = collection_products)

# deletes a collection
@main.route('/collections/<collection_id>/delete', methods=['POST'])
@login_required
def delete_collection(collection_id):
    del_col = delete(Collection).where(Collection.id == collection_id)

    db.session.execute(del_col)
    db.session.commit()
    flash('Collection Deleted')
    return redirect(url_for('main.homepage'))
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



