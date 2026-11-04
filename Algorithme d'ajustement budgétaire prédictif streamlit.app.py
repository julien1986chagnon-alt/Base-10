import streamlit as st
import math

# ==============================================================================
# 1. CONFIGURATION STRICTE DE LA PAGE (Impérativement en premier)
# ==============================================================================
st.set_page_config(
    page_title="Calculatrice Évolutive Pro",
    layout="centered",
    initial_sidebar_state="auto"
)

# ==============================================================================
# 2. INTERFACE VISUELLE & TITRES
# ==============================================================================
st.title("Calculatrice Évolutive 4.1.1.1")
st.subheader("Moteur Complet d'Ajustement Budgétaire - Base 10")
st.caption("Développé par : Chagnon Julien Christian Robert")
st.markdown("---")

# ==============================================================================
# 3. ENTRÉES UTILISATEUR EN DIRECT
# ==============================================================================
st.sidebar.header("⚙️ Paramètres globaux")
st.sidebar.write("Modifiez les valeurs pour recalculer instantanément.")

# Sélection de l'opérateur principal
operateur = st.selectbox(
    "Sélectionnez l'opérateur mathématique :", 
    options=["/", "*", "-", "+"], 
    index=0
)

# Organisation des champs numériques en colonnes pour une meilleure lisibilité
col1, col2 = st.columns(2)

with col1:
    num_a = st.number_input(
        "Premier nombre (Numérateur / Valeur A) :", 
        value=55555.0, 
        format="%.2f"
    )

with col2:
    num_b = st.number_input(
        "Deuxième nombre (Dénominateur / Valeur B) :", 
        value=4456.0, 
        format="%.2f"
    )

st.markdown("---")

# ==============================================================================
# 4. LOGIQUE DE CALCUL ET AFFICHAGE EN DIRECT
# ==============================================================================
st.markdown("### 📈 Résultats de l'analyse budgétaire")

# Sécurisation immédiate contre la division par zéro
if operateur == "/" and num_b == 0:
    st.error("🚨 Erreur critique : La division par zéro est mathématiquement impossible.")
else:
    # 4.1. Calculs financiers et arrondis (Logique directe de votre code)
    part_brute = num_a / num_b
    part_particulier = math.ceil(part_brute * 100) / 100
    somme_totale_parametre = part_particulier * num_b
    somme_a_repartir = somme_totale_parametre - num_a
    
    # Présentation propre des métriques financières
    met_col1, met_col2 = st.columns(2)
    with met_col1:
        st.metric(
            label="À compter au numérateur", 
            value=f"{somme_a_repartir:,.2f} €"
        )
    with met_col2:
        st.metric(
            label="Part stricte nette par personne", 
            value=f"{part_particulier:,.2f} €"
        )
    
    st.markdown("---")

    # 4.2. Application du calcul selon l'opérateur de la liste déroulante
    resultat_standard = 0.0
    
    if operateur == "/":
        resultat_standard = num_a / num_b
    elif operateur == "*":
        resultat_standard = num_a * num_b
    elif operateur == "-":
        resultat_standard = num_a - num_b
    elif operateur == "+":
        resultat_standard = num_a + num_b

    # Affichage du résultat général
    st.info(f"**Calcul d'opération standard associé** : `{num_a}` {operateur} `{num_b}` = **{resultat_standard:,.4f}**")

# ==============================================================================
# 5. ZONE DE DOCUMENTATION ET CONTEXTE (Détail de la page)
# ==============================================================================
with st.expander("ℹ️ À propos de cette calculatrice budgétaire"):
    st.markdown("""
    **Explication des calculs automatiques :**
    * **Part brute** : Division simple et brute du numérateur par votre dénominateur.
    * **Part stricte** : Arrondi supérieur financier strict au centime supérieur (`math.ceil`).
    * **Ajustement budgétaire** : Différence calculée permettant d'équilibrer la répartition exacte de la structure financière.
    """)

