import streamlit as st
import math
import time

# 1. Configuration de la page
st.set_page_config(
    page_title="Calculatrice Evolutive 4.1.1.1",
    layout="centered"
)

# 2. En-tete textuel standard sans caracteres speciaux
st.title("Calculatrice Evolutive 4.1.1.1")
st.subheader("Moteur Complet Base 10")
st.caption("Developpe par : Chagnon Julien Christian Robert - Tous droits reserves")

st.markdown("---")

# 3. Fonction de calcul budgetaire anti-infinite
def calculer_complement_anti_infini(num_val, den_val):
    if den_val == 0:
        return 0.0, 0.0, "Division par zero impossible"
        
    temps_debut = time.time()
    
    # Calcul de la part brute theorique par personne
    part_brute = num_val / den_val
    
    # On determine la part propre au centime superieur (2 decimales max)
    part_exacte_centimes = math.ceil(part_brute * 100) / 100
    
    # Calcul de la somme totale qu'il faudrait avoir au depart
    somme_totale_necessaire = part_exacte_centimes * den_val
    
    # Ce qu'il faut rajouter exactement dans le numerateur de depart
    somme_a_rajouter = somme_totale_necessaire - num_val
    
    duree = time.time() - temps_debut
    statut = f"Analyse reussie en {duree:.6f} secondes."
    
    return somme_a_rajouter, part_exacte_centimes, statut

# 4. Zone de saisie fixe globale
operateur = st.selectbox(
    "Choisissez l'operateur :",
    options=["/", "+", "-", "*"],
    index=0
)

num_a = st.number_input("Premier nombre (Numerateur pour la division) :", min_value=0.0, value=55555.0, step=1.0)
num_b = st.number_input("Deuxieme nombre (Denominateur / Diviseur) :", min_value=0.0, value=4456.0, step=1.0)

st.markdown("---")

# 5. Declenchement du calcul
if st.button("Lancer l'analyse", type="primary"):
    
    if operateur == "/":
        if num_b == 0:
            st.error("Erreur : Division par zero impossible.")
        else:
            argent_a_rajouter, part_personne, details = calculer_complement_anti_infini(num_a, num_b)
            
            st.markdown("### Resultats de l'analyse")
            st.write(f"**A RAJOUTER AU NUMERATEUR DE DEPART :** {argent_a_rajouter:.2f} €")
            st.write(f"**PART EXACTE NETTE PAR PERSONNE :** {part_personne:.2f} €")
            
            st.markdown("---")
            st.write(
                f"Explication budgetaire : Pour eviter une suite infinie de chiffres apres la virgule, "
                f"l'application fixe la part de chacun a {part_personne:.2f} €. "
                f"Pour que ce partage soit parfaitement rigoureux face aux {int(num_b)} beneficiaires, "
                f"vous devez injecter {argent_a_rajouter:.2f} € supplementaires a votre somme de depart."
            )
            st.caption(f"Statut technique : {details}")
            
    else:
        # Traitement des autres operations standard
        resultat = 0.0
        if operateur == "+":
            resultat = num_a + num_b
        elif operateur == "-":
            resultat = num_a - num_b
        elif operateur == "*":
            resultat = num_a * num_b
            
        st.success(f"Resultat du calcul standard : {resultat}")
