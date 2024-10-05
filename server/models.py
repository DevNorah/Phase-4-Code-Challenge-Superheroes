from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)

    # adds relationship 
    powers = db.relationship('HeroPower', back_populates='hero', cascade='all, delete-orphan')

    # add serialization rules
    serialize_rules = ('-powers.hero',)
   
    def __repr__(self):
        return f'<Hero {self.id}>'


class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)

    # add relationship
    heroes = db.relationship('HeroPower', back_populates='power'  , cascade='all, delete-orphan')

    # add serialization rules
    serialize_rules = ('-heroes.power',)
    
    # add validation
    @validates('description')
    def validate_description(self, key, value):
        if len(value) < 20:
            raise ValueError("Description must be at least 20 characters long")
        return value

    def __repr__(self):
        return f'<Power {self.id}>'


class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)

    # add relationships
    hero = db.relationship("Hero" ,back_populates = "powers")
    power = db.relationship("Power" ,back_populates = "heroes")
    
    # add serialization rules
    serialize_rules = ('-hero.powers', '-power.heroes')
   
    # add validation

    def __repr__(self):
        return f'<HeroPower {self.id}>'
