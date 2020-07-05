from datetime import datetime
from orders.app import db


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer)
    beers = db.relationship('OrderBeer', backref='order')
    is_open = db.Column(db.Boolean, default=True)
    time_created = db.Column(db.DateTime, default=datetime.utcnow)
    time_modified = db.Column(db.DateTime, onupdate=datetime.utcnow)

    @staticmethod
    def get_opened_order(owner_id):
        order = Order.query.filter_by(owner_id=owner_id, is_open=True).first()

        if order is None:
            order = Order()
            order.owner_id = owner_id
            order.is_open = True
            db.session.add(order)
            db.session.commit()

        return order

    def checkout(self):
        if len(self.beers) == 0:
            return

        self.is_open = False
        db.session.add(self)
        db.session.commit()

    def add_beer(self, sku, quantity):
        found = False

        for beer in self.beers:
            if beer.sku == sku:
                beer.quantity += quantity
                found = True
                break

        if not found:
            beer = OrderBeer()
            beer.sku = sku
            beer.quantity = quantity
            self.beers.append(beer)

        db.session.add(self)
        db.session.commit()

    def remove_beer(self, sku):
        for beer in self.beers:
            if beer.sku == sku:
                self.beers.remove(beer)
                db.session.add(self)
                db.session.commit()
                return


class OrderBeer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    sku = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    time_created = db.Column(db.DateTime, default=datetime.utcnow)
    time_modified = db.Column(db.DateTime, onupdate=datetime.utcnow)
