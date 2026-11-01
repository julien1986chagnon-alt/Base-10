import streamlit as st
import math
import time

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Calculatrice Évolutive 4.1.1.1",
    page_icon="🧮",
    layout="centered"
)

# Titre et En-tête de l'application
st.title("🧮 Calculatrice Évolutive 4.1.1.1")
st.subheader("Moteur Complet Base 10 - Confinement Algorithmique")
st.caption("Développé par : Chagnon Julien Christian Robert — Tous droits réservés")

st.markdown("---")

# Fonction maîtresse de calcul budgétaire anti-infinité
def calculer_complement_anti_infini(num_val, den_val):
    if den_val == 0:
        return None, None, "Division par zéro impossible"
        
    temps_debut = time.time()
    
    # 1. Calcul de la part brute théorique par personne
    part_brute = num_val / den_val
    
    # 2. On détermine la part propre au centime supérieur (2 décimales max)
    part_exacte_centimes = math.ceil(part_brute * 100) / 100
    
    # 3. Calcul de la somme totale qu'il faudrait avoir au départ
    somme_totale_necessaire = part_exacte_centimes * den_val
    
    # 4. Ce qu'il faut rajouter exactement dans le numérateur de départ
    somme_a_rajouter = somme_totale_necessaire - num_val
    
    duree = time.time() - temps_debut
    statut = f"Analyse anti-infinité réussie en {duree:.6f} secondes."
    
    return somme_a_rajouter, part_exacte_centimes, statut

# --- ZONE DE SAISIE DE L'INTERFACE ---

# Choix de l'opération
operateur = st.selectbox(
    "Choisissez l'opérateur mathématique :",
    options=["+", "-", "*", "/"],
    index=3 # Sélectionne par défaut la division
)

col1, col2 = st.columns(2)

with col1:
    if operateur == "/":
        num_a = st.number_input("Somme totale de départ (Numérateur) :", min_value=0.0, value=55555.0, step=1.0, format="%.2f")
    else:
        num_a = st.number_input("Premier nombre :", min_value=0.0, value=10.0, step=1.0)

with col2:
    if operateur == "/":
        num_b = st.number_input("Nombre de parts / Personnes (Dénominateur) :", min_value=0.0, value=4456.0, step=1.0, format="%.2f")
    else:
        num_b = st.number_input("Deuxième nombre :", min_value=0.0, value=5.0, step=1.0)

st.markdown("---")

# --- TRAITEMENT ET AFFICHAGE DES RÉSULTATS ---

if st.button("🚀 Lancer l'analyse du confinement", type="primary"):
    
    if operateur == "/":
        if num_b == 0:
            st.error("❌ Erreur : Division par zéro impossible.")
        else:
            with st.spinner("Analyse du disjoncteur ZeroFloat..."):
                argent_a_rajouter, part_personne, details = calculer_complement_anti_infini(num_a, num_b)
                
            # Affichage des résultats sous forme de cartes d'information (Metrics)
            st.success("✅ Analyse terminée avec succès !")
            
            m1, m2 = st.columns(2)
            m1.metric(
                label="À RAJOUTER AU NUMÉRATEUR DE DÉPART", 
                value=f"{argent_a_rajouter:.2f} €"
            )
            m2.metric(
                label="PART EXACTE NETTE PAR PERSONNE", 
                value=f"{part_personne:.2f} €"
            )
            
            # Message d'explication textuel clair
            st.info(
                f"**Explication budgétaire :** Pour éviter une suite infinie de chiffres après la virgule, "
                f"l'application fixe la part de chacun à **{part_personne:.2f} €**. "
                f"Pour que ce partage soit parfaitement rigoureux face aux **{int(num_b)}** bénéficiaires, "
                f"vous devez injecter **{argent_a_rajouter:.2f} €** supplémentaires à votre somme de départ."
            )
            
            st.caption(f"🔧 *Statut technique : {details}*")
            
    else:
        # Traitement des opérations standards
        if operateur == "+":
            resultat = num_a + num_b
        elif operateur == "-":
            resultat = num_a - num_b
        elif operateur == "*":
            resultat = num_a * num_b
            
        st.success(f"Résultat du calcul standard : **{resultat}**")

