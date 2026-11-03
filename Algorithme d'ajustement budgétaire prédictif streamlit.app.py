import streamlit as st
import math
import time

# =============================================================================
# 1. Configuration de la page
# =============================================================================
st.set_page_config(
    page_title="Calculatrice Évolutive 4.1.1.1",
    layout="centered"
)

# =============================================================================
# 2. En-tête textuel
# =============================================================================
st.title("Calculatrice Évolutive 4.1.1.1")
st.subheader("Moteur Complet Base 10")
st.caption("Développé par : Chagnon Julien Christian Robert - Tous droits réservés")
st.markdown("---")

# =============================================================================
# 3. Fonction de calcul budgétaire anti-infinie
# =============================================================================
def calculer_complement_anti_infini(num_val, den_val):
    if den_val == 0:
        return 0.0, 0.0, "Division par zéro impossible"
        
    temps_debut = time.time()
    
    # Calcul de la part brute théorique par personne
    part_brute = num_val / den_val
    
    # On détermine la part propre au centime supérieur (2 décimales max)
    part_exacte_centimes = math.ceil(part_brute * 100) / 100
    
    # Calcul de la somme totale qu'il faudrait avoir au départ
    somme_totale_necessaire = part_exacte_centimes * den_val
    
    # Ce qu'il faut rajouter exactement dans le numérateur de départ
    somme_a_rajouter = somme_totale_necessaire - num_val
    
    duree = time.time() - temps_debut
    statut = f"Analyse réussie en {duree:.6f} secondes."
    
    return somme_a_rajouter, part_exacte_centimes, statut

# =============================================================================
# 4. Zone de saisie globale (Alignée à gauche)
# =============================================================================
operateur = st.selectbox(
    "Choisissez l'opérateur :",
    options=["/", "+", "-", "*"],
    index=0
)

num_a = st.number_input(
    "Premier nombre (Numérateur pour la division) :", 
    min_value=0.0, 
    value=55555.0, 
    step=1.0
)

num_b = st.number_input(
    "Deuxième nombre (Dénominateur / Diviseur) :", 
    min_value=0.0, 
    value=4456.0, 
    step=1.0
)

st.markdown("---")

# =============================================================================
# 5. Déclenchement du calcul et affichage des résultats
# =============================================================================
if st.button("Lancer l'analyse", type="primary"):
    
    # --- Cas spécifique de la division ---
    if operateur == "/":
        if num_b == 0:
            st.error("Erreur : Division par zéro impossible.")
        else:
            # Appel de la fonction de calcul
            argent_a_rajouter, part_personne, details = calculer_complement_anti_infini(num_a, num_b)
            
            st.markdown("### 📊 Résultats de l'analyse")
            st.write(f"**A RAJOUTER AU NUMÉRATEUR DE DÉPART :** {argent_a_rajouter:.2f} €")
            st.write(f"**PART EXACTE NETTE PAR PERSONNE :** {part_personne:.2f} €")
            st.markdown("---")
            
            # Utilisation de triple guillemets pour éviter les bugs d'affichage de texte sur Streamlit
            st.write(f"""
            **Explication budgétaire :** Pour éviter une suite infinie de chiffres après la virgule, 
            l'application fixe la part de chacun à **{part_personne:.2f} €**.
            
            Pour que ce partage soit parfaitement rigoureux face aux **{int(num_b)}** bénéficiaires, 
            vous devez injecter **{argent_a_rajouter:.2f} €** supplémentaires à votre somme de départ.
            """)
            
            st.caption(f"Statut technique : {details}")
            
    # --- Cas des autres opérations standards ---
    else:
        resultat = 0.0
        if operateur == "+":
            resultat = num_a + num_b
        elif operateur == "-":
            resultat = num_a - num_b
        elif operateur == "*":
            resultat = num_a * num_b
            
        st.success(f"Résultat du calcul standard : {resultat}")

