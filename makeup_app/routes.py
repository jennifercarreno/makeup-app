from flask import Blueprint, request, render_template, redirect, url_for, flash
from makeup_app.models import User, Product, Comment
from makeup_app.extensions import app, db
from makeup_app.forms import ProductForm
from sqlalchemy import delete

main = Blueprint("main", __name__)

@main.route('/')
def homepage():
    all_prds = Product.query.all()
    return render_template('home.html', prds= all_prds)

@main.route('/new_product',methods=['GET', 'POST'])
def new_product():
    form = ProductForm()

    if form.validate_on_submit():
        new_product = Product(
            name = form.name.data,
            rating = form.rating.data,
            review = form.review.data
        )
        db.session.add(new_product)
        db.session.commit()

        flash('Success! New Product Added')
        return redirect(url_for('main.prd_detail', product_id = new_product.id))
    else: 
        return render_template('new_prd.html', form = form)

@main.route('/product/<product_id>', methods=['GET', 'POST'])
def prd_detail(product_id):
    product = Product.query.get(product_id)
    return render_template('prd_detail.html', product = product)

@main.route('/product/<product_id>/delete', methods=['POST'])
def prd_delete(product_id):
    sql2 = delete(Product).where(Product.id == product_id)

    db.session.execute(sql2)
    db.session.commit()
    flash('Product Deleted')
    return redirect(url_for('main.homepage'))