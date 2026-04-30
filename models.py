from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

# Définition de la base
Base = declarative_base()

class Producteur(Base):
    __tablename__ = "producteurs"
    id = Column(Integer, primary_key=True)
    nom = Column(String)
    region = Column(String)
    cultures = relationship("Culture", backref="producteur")

class Culture(Base):
    __tablename__ = "cultures"
    id = Column(Integer, primary_key=True)
    type = Column(String)
    surface = Column(Float)
    rendement = Column(Float)
    producteur_id = Column(Integer, ForeignKey("producteurs.id"))
