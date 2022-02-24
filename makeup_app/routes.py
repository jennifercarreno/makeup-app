from flask import Blueprint, request, render_template, redirect, url_for, flash
from makeup_app.models import User, Product, Comment
from makeup_app.extensions import app, db
from makeup_app.forms import ProductForm, CommentForm
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
    form = ProductForm()
    comment_form = CommentForm()
    prd_comments = []

    all_comments = Comment.query.all()

    if form.validate_on_submit():
        form.populate_obj(product)
        db.session.commit()
        flash('Success! Item Updated')
        product = Product.query.get(product_id)

        for comment in all_comments:
            if comment.prd == product_id:
                prd_comments.append(comment)
                print(prd_comments)

        return redirect(url_for('main.prd_detail', product = product, product_id = product_id, comments=prd_comments))
    else:
        product = Product.query.get(product_id)

        for comment in all_comments:
            print(comment.prd)
            print(product_id)
            if comment.prd == int(product_id):
                prd_comments.append(comment)

        print("form not submitted :(")
        print(prd_comments)
        return render_template('prd_detail.html', product = product, form=form, comment_form=comment_form, comments=prd_comments)

@main.route('/product/<product_id>/delete', methods=['POST'])
def prd_delete(product_id):
    sql2 = delete(Product).where(Product.id == product_id)

    db.session.execute(sql2)
    db.session.commit()
    flash('Product Deleted')
    return redirect(url_for('main.homepage'))

# comments 
@main.route('/new_comment/<product_id>', methods=['POST'])
def new_comment(product_id):
    product = Product.query.get(product_id)
    form = CommentForm()
    prd_form = ProductForm()

    if form.validate_on_submit():
        new_comment = Comment(
            name = form.name.data,
            comment = form.comment.data,
            prd = product_id
        )

        db.session.add(new_comment)
        db.session.commit()

        flash('Success! New Comment Added')
        return redirect(url_for('main.prd_detail', product = product, product_id = product_id))
    else:
        print(" comment form not submitted ")
        return render_template('prd_detail.html', product = product, form=prd_form, comment_form=form)

@main.route('/comment/<comment_id>/delete', methods=['POST'])
def comment_delete(comment_id):
    sql2 = delete(Comment).where(Comment.id == comment_id)

    db.session.execute(sql2)
    db.session.commit()
    flash('Comment Deleted')
    return redirect(url_for('main.homepage'))