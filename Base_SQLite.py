import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Fonction pour créer la table si elle n'existe pas
def create_table():
    conn = sqlite3.connect('ma_base.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS utilisateurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            prenom TEXT,
            age INTEGER,
            mail TEXT,
            date_connexion TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Fonction pour insérer un utilisateur dans la base de données avec la date actuelle
def inserer_utilisateur(nom, prenom, age, mail):
    conn = sqlite3.connect('ma_base.db')
    cursor = conn.cursor()
    date_connexion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Date actuelle
    cursor.execute('''
        INSERT INTO utilisateurs (nom, prenom, age, mail, date_connexion)
        VALUES (?, ?, ?, ?, ?)
    ''', (nom, prenom, age, mail, date_connexion))
    conn.commit()
    conn.close()

# Fonction pour supprimer un utilisateur de la base de données par ID
def supprimer_utilisateur(id):
    conn = sqlite3.connect('ma_base.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM utilisateurs WHERE id = ?', (id,))
    conn.commit()
    conn.close()

# Fonction pour récupérer les données de la base de données
def recuperer_donnees():
    conn = sqlite3.connect('ma_base.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM utilisateurs')
    utilisateurs = cursor.fetchall()
    columns = [col[0] for col in cursor.description]  # Récupérer les noms des colonnes
    conn.close()

    # Création d'un DataFrame pandas
    df = pd.DataFrame(utilisateurs, columns=columns)
    return df

# Création de la table si elle n'existe pas
create_table()

# Interface utilisateur avec le formulaire
st.title('Formulaire Streamlit avec SQLite')

nom = st.text_input('Nom')
prenom = st.text_input('Prénom')
age = st.number_input('Âge', min_value=0, max_value=150, value=0)
mail = st.text_input('Email')

if st.button('Envoyer'):
    # Insertion des données dans la base de données avec la date actuelle
    inserer_utilisateur(nom, prenom, age, mail)
    st.success('Données envoyées avec succès!')

# Affichage des données de la base de données
df = recuperer_donnees()
st.write(df)

# Colonnes pour saisir l'ID et afficher le bouton de suppression
col1, col2 = st.columns([1, 3])
with col1:
    id_a_supprimer = st.text_input("Entrez l'ID de l'utilisateur à supprimer:")

with col2:
    if st.button('Supprimer') and id_a_supprimer:
        supprimer_utilisateur(int(id_a_supprimer))
        st.success(f"Utilisateur avec ID {id_a_supprimer} supprimé avec succès!")

# Affichage de la notification de suppression
if st.button('Actualiser'):
    recuperer_donnees()















