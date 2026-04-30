
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Producteur, Culture

engine = create_engine("sqlite:///database.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Producteurs fictifs
p1 = Producteur(nom="Jean Dupont", region="Centre")
p2 = Producteur(nom="Marie Kouassi", region="Nord")
p3 = Producteur(nom="Aliou Diallo", region="Sud")

session.add_all([p1, p2, p3])
session.commit()

# Cultures fictives
c1 = Culture(type="Maïs", surface=50, rendement=120, producteur_id=p1.id)
c2 = Culture(type="Cacao", surface=30, rendement=80, producteur_id=p2.id)
c3 = Culture(type="Riz", surface=40, rendement=100, producteur_id=p3.id)
c4 = Culture(type="Café", surface=20, rendement=60, producteur_id=p1.id)

session.add_all([c1, c2, c3, c4])
session.commit()

print("✅ Données fictives insérées avec succès !")
