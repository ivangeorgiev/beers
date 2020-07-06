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
    
    @staticmethod
    def seed():
        Beer.create('Бургаско', 123456, 1.19, 'https://cdncloudcart.com/15635/products/images/206/bira-burgasko-svetlo-500-ml-ken-image_5e24491fc2a15_800x800.jpeg?1579436338')
        Beer.create('Загорка', 123457, 2.00, 'https://shami.bg/uploads/2019/06/38b3674a0aaee5a32c1193d8cab7104b.png')
        Beer.create('Tuborg', 123458, 1.50, 'https://cdn.nokovandson.com/crop/276/490/480//I0/I0pLF5nGwJ.png')
