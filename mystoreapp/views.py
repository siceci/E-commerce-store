from flask import Blueprint, render_template, url_for, request, session, flash, redirect
from .models import Cat, Vinyl, Order
from datetime import datetime
from .forms import CheckoutForm
from . import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    cats = Cat.query.order_by(Cat.name).all()
    return render_template('index.html', cats=cats)

@main_bp.route('/vinyls/<int:catid>')
def catalog(catid):
    vinyls = Vinyl.query.filter(Vinyl.cat_id==catid)
    return render_template('catalog.html', vinyls=vinyls)

@main_bp.route('/vinyldetail/<int:id>', methods=['GET'])
def vinyldetail(id):
    vinyls = Vinyl.query.get_or_404(id)
    return render_template('/vinyldetail.html', vinyls=vinyls)
    
@main_bp.route('/vinyls')
def search():
    search = request.args.get('search')
    search = '%{}%'.format(search) 
    vinyls = Vinyl.query.filter(Vinyl.description.like(search)).all()
    return render_template('catalog.html', vinyls=vinyls)


@main_bp.route('/order', methods=['POST','GET'])
def order():
    vinyl_id = request.values.get('vinyl_id')

    if 'order_id'in session.keys():
        order = Order.query.get(session['order_id'])
    else:
        order = None

    if order is None:
        order = Order(status = False, firstname='', surname='', email='', phone='', totalcost=0)
        try:
            db.session.add(order)
            db.session.commit()
            session['order_id'] = order.id
        except:
            print('failed at creating a new order')
            order = None
    
    totalprice = 0
    if order is not None:
        for vinyl in order.vinyls:
            totalprice = totalprice + vinyl.price
    
    if vinyl_id is not None and order is not None:
        vinyl = Vinyl.query.get(vinyl_id)
        if vinyl not in order.vinyls:
            try:
                order.vinyls.append(vinyl)
                db.session.commit()
            except:
                return 'There was an issue adding the item to your basket'
            return redirect(url_for('main.order'))
        else:
            flash('item already in basket')
            return redirect(url_for('main.order'))
    return render_template('order.html', order = order, totalprice=totalprice)

@main_bp.route('/deleteorderitem', methods=['POST'])
def deleteorderitem():
    id=request.form['id']
    if 'order_id' in session:
        order = Order.query.get_or_404(session['order_id'])
        vinyl_to_delete = Vinyl.query.get(id)
        try:
            order.vinyls.remove(vinyl_to_delete)
            db.session.commit()
            return redirect(url_for('main.order'))
        except:
            return 'Problem deleting item from order'
    return redirect(url_for('main.order'))

@main_bp.route('/deleteorder')
def deleteorder():
    if 'order_id' in session:
        del session['order_id']
        flash('All items deleted')
    return redirect(url_for('main.index'))

@main_bp.route('/checkout', methods=['POST','GET'])
def checkout():
    form = CheckoutForm() 
    if 'order_id' in session:
        order = Order.query.get_or_404(session['order_id'])
       
        if form.validate_on_submit():
            order.status = True
            order.firstname = form.firstname.data
            order.surname = form.surname.data
            order.email = form.email.data
            order.phone = form.phone.data
            totalcost = 0
            for vinyl in order.vinyls:
                totalcost = totalcost + vinyl.price
            order.totalcost = totalcost
            try:
                db.session.commit()
                del session['order_id']
                flash('Thanks for your order! We would send you the shippment and payment details via email once order confirmed.')
                return redirect(url_for('main.index'))
            except:
                return 'There was an issue completing your order'
    return render_template('checkout.html', form=form)

