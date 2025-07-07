import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from io import BytesIO

# --- CONFIGURATION DE LA PAGE --- Si tu vois cette page, félicitations, tu peux réadapter le code pour tes besoins. au besoin tu peux me faire signe au fannyarouna@outlook.fr
st.set_page_config(page_title="Générateur de Données Avancé ", page_icon="✨", layout="wide")

# --- LISTES DE BASE ---
NOMS = ["Kouassi","Fanny" , "Kouassi" , "Kone", "Traore", "Kouadio", "Yao", "Gueu", "Ouattara", "Bamba", "Diomande", "Soro", "Gnon", "Meite", "Dao", "Sangare", "Koulibaly", "Cisse", "Diallo", "Diarra", "Sylla", "Fofana"]
PRENOMS_H = ["Adama", "Arouna","Mamadou", "Sekou", "Ibrahim", "Moussa", "Ousmane", "Yacouba", "Issa", "Drissa", "Fousseni", "Abdoulaye", "Hamed", "Jean", "Didier", "Eric", "Hassan", "Ali", "Salif", "Daouda", "Karim"]
PRENOMS_F = ["Aya", "Ahou", "Akissi", "Mariam", "Fatoumata", "Awa", "Aminata", "Rokia", "Fanta", "Maimouna", "Nathalie", "Sandrine", "Carine", "Fatou", "Bintou", "Kadidiatou", "Sali", "Aïcha", "Adja", "Aïssata"]
DEPARTEMENTS_DEFAUT = ["Ressources Humaines", "Finance", "IT", "Marketing", "Ventes", "Opérations", "Direction"]
FONCTIONS_PAR_DEPARTEMENT = {
    "Ressources Humaines": ["Chargé RH", "Gestionnaire Paie", "Responsable RH"], "Finance": ["Comptable", "Contrôleur de Gestion", "Analyste Financier"],
    "IT": ["Développeur", "Administrateur Système", "Chef de Projet IT"], "Marketing": ["Chargé de Communication", "Chef de Produit", "Spécialiste SEO"],
    "Ventes": ["Commercial Terrain", "Responsable Commercial", "Ingénieur d'Affaires"], "Opérations": ["Logisticien", "Responsable de Production", "Qualiticien"],
    "Direction": ["Directeur Général", "Directeur Financier", "Directeur des Opérations"]
}
NIVEAUX_ETUDE = ["Bac", "Bac+2/BTS", "Bac+3/Licence", "Bac+5/Master", "Doctorat"]
DIPLOMES_PAR_DEPARTEMENT = {
    "Ressources Humaines": ["Gestion des RH", "Psychologie du travail"], "Finance": ["Comptabilité et Gestion", "Finance d'entreprise"],
    "IT": ["Informatique de Gestion", "Génie Logiciel", "Réseaux et Systèmes"], "Marketing": ["Marketing & Communication", "Commerce Digital"],
    "Ventes": ["Techniques de Commercialisation", "Ingénierie d'Affaires"], "Opérations": ["Logistique et Transport", "Gestion de Production"], "Direction": ["Administration des Entreprises (MBA)", "Management Stratégique"]
}
CAPITALES_DEFAUT = ["Abidjan", "Yamoussoukro", "Dakar", "Lagos", "Accra", "Paris", "Londres", "New York", "Dubaï", "Johannesburg", "Nairobi", "Cotonou", "Bamako"]

# --- FONCTIONS DE GÉNÉRATION ---
def generer_donnees_rh(params):
    personnel_data = []
    today = datetime.now().date()
    n = params['nombre_lignes']
    villes = params['villes_options']
    departements = params['departements_options']
    prop_cdi = params['proportion_cdi']
    periode_embauche = params['periode_embauche']
    prop_anomalies = params['pourcentage_anomalies']
    start_date, end_date = periode_embauche
    if isinstance(start_date, datetime): start_date = start_date.date()
    if isinstance(end_date, datetime): end_date = end_date.date()
    total_days = (end_date - start_date).days

    for i in range(1, n + 1):
        dep = random.choice(departements)
        cat = random.choices(["Employé", "Agent de maîtrise", "Cadre"], weights=[0.5, 0.3, 0.2], k=1)[0]
        if cat == "Cadre": niveau_etude = random.choices(NIVEAUX_ETUDE, weights=[0.0, 0.1, 0.2, 0.6, 0.1], k=1)[0]
        elif cat == "Agent de maîtrise": niveau_etude = random.choices(NIVEAUX_ETUDE, weights=[0.1, 0.5, 0.4, 0.0, 0.0], k=1)[0]
        else: niveau_etude = random.choices(NIVEAUX_ETUDE, weights=[0.6, 0.3, 0.1, 0.0, 0.0], k=1)[0]
        date_embauche_dt = start_date + timedelta(days=random.randint(0, total_days))
        annees_experience = (today - date_embauche_dt).days / 365.25

        personnel_data.append({
            "Matricule": f"AGRH-P17-{i:03d}", "Nom": random.choice(NOMS),
            "Prénom": random.choice(PRENOMS_H if random.choice(["Homme", "Femme"]) == "Homme" else PRENOMS_F),
            "Date de Naissance": (date_embauche_dt - timedelta(days=random.randint(20*365, 50*365))).strftime('%Y-%m-%d'),
            "Date d'Embauche": date_embauche_dt.strftime('%d/%m/%Y'),
            "Années d'expérience": round(annees_experience, 1), "Genre": random.choice(["Homme", "Femme"]),
            "Département": dep, "Fonction": random.choice(FONCTIONS_PAR_DEPARTEMENT.get(dep, ["Non défini"])),
            "Catégorie CSP": cat, "Niveau d'étude": niveau_etude,
            "Intitulé du diplôme": random.choice(DIPLOMES_PAR_DEPARTEMENT.get(dep, ["Non défini"])),
            "Type de Contrat": "CDI" if random.random() < (prop_cdi / 100) else "CDD",
            "Ville": random.choice(villes), "Statut": random.choices(["Actif", "Inactif"], weights=[0.95, 0.05], k=1)[0]
        })

    df = pd.DataFrame(personnel_data)
    nb_anomalies = int(n * (prop_anomalies / 100))
    if nb_anomalies > 0:
        for _ in range(nb_anomalies):
            col_anomalie = random.choice(["Date de Naissance", "Ville", "Date d'Embauche"])
            idx_anomalie = random.randint(0, n - 1)
            df.loc[[idx_anomalie], col_anomalie] = np.nan
    return df

def generer_base_paie(df_personnel):
    paie_data = []
    salaire_base = {"Employé": (220000, 445000), "Agent de maîtrise": (450000, 850000), "Cadre": (850000, 1500000)}
    for _, row in df_personnel.iterrows():
        salaire = random.randint(*salaire_base.get(row['Catégorie CSP'], (120000, 500000))) # Valeurs par défaut si catégorie inconnue
        prime = random.randint(50000, 500000) if random.random() < 0.6 else 0
        paie_data.append({"Matricule": row['Matricule'], "Salaire de Base": salaire, "Prime Annuelle": prime})
    return pd.DataFrame(paie_data)

def generer_base_evaluations(df_personnel):
    eval_data = []
    personnel_evalue = df_personnel.sample(frac=0.9)
    commentaires = {1: "Performance très insuffisante.", 2: "Potentiel d'amélioration notable.", 3: "Atteint les attentes.", 4: "Dépasse les attentes.", 5: "Performance exceptionnelle."}
    for _, row in personnel_evalue.iterrows():
        score = random.choices([1, 2, 3, 4, 5], weights=[0.05, 0.15, 0.5, 0.25, 0.05], k=1)[0]
        eval_data.append({
            "Matricule Employé": row['Matricule'],
            "Date Évaluation": (datetime(2025, 1, 15) + timedelta(days=random.randint(0, 150))).strftime('%Y-%m-%d'),
            "Score Performance (sur 5)": score, "Commentaire Évaluateur": commentaires.get(score, "Non renseigné"),
            "Objectifs Atteints (%)": round(random.uniform(70.0, 120.0), 1)
        })
    return pd.DataFrame(eval_data)

# --- INTERFACE UTILISATEUR (UI) ---
st.title("✨ Générateur de Données Avancé")
st.markdown("Configurez et générez des jeux de données RH sur mesure pour vos analyses. Besoin d'une formation en management de la data RH ?? || Contactez moi : fannyarouna@outlook.fr")

# == PANNEAU DE CONFIGURATION LATÉRAL ==
with st.sidebar:
    # --- Ajout du Logo ---
    try:
        st.image("logo_agrhacademy.png", width=150)  # Remplacez par le chemin/URL de votre logo
    except FileNotFoundError:
        st.warning("Logo non trouvé. Veuillez placer 'logo_agrhacademy.png' dans le même dossier que l'application.")
    except Exception as e:
        st.error(f"Erreur lors du chargement du logo : {e}")

    st.header("⚙️ Paramètres de Génération")

    with st.expander("1. Paramètres Généraux", expanded=True):
        nombre_lignes = st.number_input("Nombre d'employés", min_value=10, max_value=10000, value=500, step=10)

    with st.expander("2. Données Organisationnelles", expanded=False):
        villes_options = st.multiselect("Villes à inclure", options=CAPITALES_DEFAUT, default=["Abidjan", "Paris", "Dakar"])
        departements_options = st.multiselect("Départements à inclure", options=DEPARTEMENTS_DEFAUT, default=DEPARTEMENTS_DEFAUT)

    with st.expander("3. Paramètres du Contrat", expanded=False):
        proportion_cdi = st.slider("Proportion de contrats CDI (%)", min_value=0, max_value=100, value=85)
        start_date_default = datetime(2010, 1, 1).date()
        end_date_default = datetime.now().date()
        periode_embauche = st.date_input("Période d'embauche", value=(start_date_default, end_date_default), min_value=datetime(2000, 1, 1).date())

    with st.expander("4. Qualité des Données", expanded=False):
        pourcentage_anomalies = st.slider("Pourcentage de valeurs manquantes (%)", min_value=0, max_value=50, value=5)

    st.markdown("---")
    if st.button("🚀 Générer le Jeu de Données"):
        params = {
            'nombre_lignes': nombre_lignes,
            'villes_options': villes_options if villes_options else CAPITALES_DEFAUT,
            'departements_options': departements_options if departements_options else DEPARTEMENTS_DEFAUT,
            'proportion_cdi': proportion_cdi,
            'periode_embauche': periode_embauche,
            'pourcentage_anomalies': pourcentage_anomalies
        }

        with st.spinner("Création des données en cours..."):
            st.session_state.df_personnel = generer_donnees_rh(params)
            st.session_state.df_paie = generer_base_paie(st.session_state.df_personnel)
            st.session_state.df_evals = generer_base_evaluations(st.session_state.df_personnel)
            st.session_state.data_ready = True

    # --- Ajout du Copyright dans le pied de page de la sidebar ---
    st.sidebar.markdown("""
    ---
    <small>Copyright © 2025 - FANNY AROUNA</small>
    <br>
    <small>GESTIONNAIRE DE SYSTEME D'iNFORMATION DES RESSOURCES HUMAINES</small>
    <br>
    <small>CONSULTAT FORMATEUR DATA MANAGEMENT / POWER BI / EXCEL / RH</small>
    <br>
    <small>INTEGRATEUR DE SOLUTION INFORMATIQUE</small>
    """, unsafe_allow_html=True)

# == AFFICHAGE PRINCIPAL ==
if 'data_ready' in st.session_state and st.session_state.data_ready:
    st.header("📊 Aperçu des Données Générées")
    st.dataframe(st.session_state.df_personnel.head(10))

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        st.session_state.df_personnel.to_excel(writer, sheet_name='Personnel', index=False)
        st.session_state.df_paie.to_excel(writer, sheet_name='Paie', index=False)
        st.session_state.df_evals.to_excel(writer, sheet_name='Évaluations', index=False)

    st.session_state.processed_data = output.getvalue()

    st.download_button(
        label="📥 Télécharger le Fichier Excel",
        data=st.session_state.processed_data,
        file_name="Jeu_de_Donnees_RH_Sur_Mesure.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("Configurez vos paramètres dans le panneau de gauche et cliquez sur 'Générer le Jeu de Données'.")
