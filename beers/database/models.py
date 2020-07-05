from datetime import datetime
from beers.app import db


class Beer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    sku = db.Column(db.String(255), unique=True, nullable=False)
    price = db.Column(db.DECIMAL(precision=8, scale=2), nullable=False)
    image = db.Column(db.String(255), unique=False, nullable=True)
    time_created = db.Column(db.DateTime, default=datetime.utcnow)
    time_modified = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<Beer %r>' % (self.username, )

    @staticmethod
    def create(name, sku, price, image):
        if isinstance(image, str):
            image = image.strip()
            if not image:
                image = None

        beer = Beer()
        beer.name = name
        beer.sku = sku
        beer.price = price
        beer.image = image
        db.session.add(beer)
        db.session.commit()
        return beer

    def modify(self, name, price, image):
        if isinstance(image, str):
            image = image.strip()
            if not image:
                image = None

        self.name = name
        self.price = price
        self.image = image
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
