from . import db
from flask_wtf import FlaskForm

class Cat(db.Model):
    __tablename__ = 'cats'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    image = db.Column(db.String(60), nullable=False, default = 'defaultcat.jpg')
    vinyls = db.relationship('Vinyl', backref='Cat', cascade="all, delete-orphan")

    def __repr__(self):
        str = "ID: {}, Name: {}, Image: {}\n" 
        str = str.format(self.id, self.name, self.image)
        return str

orderdetails = db.Table('orderdetails', 
    db.Column('order_id', db.Integer,db.ForeignKey('orders.id'), nullable=False),
    db.Column('vinyl_id',db.Integer,db.ForeignKey('vinyls.id'),nullable=False),
    db.PrimaryKeyConstraint('order_id', 'vinyl_id') )

class Vinyl(db.Model):
    __tablename__ = 'vinyls'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),nullable=False)
    artist = db.Column(db.String(64),nullable=False)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(60), nullable=False)
    price = db.Column(db.Float, nullable=False)
    cat_id = db.Column(db.Integer, db.ForeignKey('cats.id'))
    
    def __repr__(self):
        str = "ID: {}, Name: {}, Artist{}, Description: {}, Image: {}, Price: {}, Cat: {}\n" 
        str = str.format(self.id, self.name, self.description, self.image, self.price, self.cat_id)
        return str

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, default=False)
    firstname = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    email = db.Column(db.String(128))
    shippingaddress = db.Column(db.String(250))
    phone = db.Column(db.String(32))
    totalcost = db.Column(db.Float)
    date = db.Column(db.DateTime)
    vinyls = db.relationship("Vinyl", secondary=orderdetails, backref="orders")
    
    def __repr__(self):
        str = "ID: {}, Status: {}, First Name: {}, Surname: {}, Email: {}, Shipping Address: {}, Phone: {}, Date: {}, Vinyls: {}, Total Cost: {}\n" 
        str = str.format(self.id, self.status, self.firstname, self.surname, self.email, self.shippingaddress, self.phone, self.date, self.vinyls, self.totalcost)
        return str
