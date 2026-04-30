import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models import Base, Producteur, Culture

# Configuration de la page
st.set_page_config(
    page_title="Agri_app",
    page_icon="🌱",
    layout="wide"
)

# Logo en haut
st.image("logo.png", width=80)
st.title("🌱 Agri_app - Tableau de bord agricole")

# Connexion à la base SQLite
engine = create_engine("sqlite:///database.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Onglets de navigation
tab1, tab2, tab3 = st.tabs(["🏠 Accueil", "📝 Saisie", "📊 Rapports"])

# --- Onglet Accueil ---
with tab1:
    st.write("Bienvenue dans Agri_app. Voici une vue d’ensemble de vos données.")

    session = Session()
    nb_producteurs = session.execute(text("SELECT COUNT(*) FROM producteurs")).scalar()
    total_surface = session.execute(text("SELECT SUM(surface) FROM cultures")).scalar() or 0
    rendement_moyen = session.execute(text("SELECT AVG(rendement) FROM cultures")).scalar() or 0

    col1, col2, col3 = st.columns(3)
    col1.metric("👩‍🌾 Producteurs", nb_producteurs)
    col2.metric("🌾 Surface totale (ha)", f"{total_surface:.1f}")
    col3.metric("📈 Rendement moyen (t)", f"{rendement_moyen:.1f}")

# --- Onglet Saisie ---
with tab2:
    st.header("Ajouter un producteur et sa culture")
    nom = st.text_input("Nom du producteur")
    region = st.text_input("Région")
    type_culture = st.text_input("Type de culture")
    surface = st.number_input("Surface cultivée (ha)", min_value=0.0)
    rendement = st.number_input("Rendement (tonnes)", min_value=0.0)

    if st.button("Enregistrer"):
        session = Session()
        producteur = Producteur(nom=nom, region=region)
        session.add(producteur)
        session.commit()
        culture = Culture(type=type_culture, surface=surface, rendement=rendement, producteur_id=producteur.id)
        session.add(culture)
        session.commit()
        st.success("✅ Données enregistrées avec succès !")

# --- Onglet Rapports ---
with tab3:
    st.header("Analyse des données")
    session = Session()

    result_region = session.execute(text("""
        SELECT region, AVG(rendement) AS RendementMoyen
        FROM producteurs
        JOIN cultures ON producteurs.id = cultures.producteur_id
        GROUP BY region
    """)).fetchall()

    result_type = session.execute(text("""
        SELECT type, SUM(surface) AS SurfaceTotale
        FROM cultures
        GROUP BY type
    """)).fetchall()

    if result_region:
        st.subheader("📍 Rendement moyen par région")
        df_region = pd.DataFrame(result_region, columns=["Région", "Rendement moyen"])
        chart = alt.Chart(df_region).mark_bar().encode(
            x="Région",
            y="Rendement moyen",
            color="Région"
        )
        st.altair_chart(chart, width="stretch")


    if result_type:
        st.subheader("🌾 Surface totale par type de culture")
        df_type = pd.DataFrame(result_type, columns=["Type", "Surface totale"])
        fig, ax = plt.subplots()
        df_type.set_index("Type")["Surface totale"].plot(kind="bar", ax=ax, color="green")
        st.pyplot(fig)
