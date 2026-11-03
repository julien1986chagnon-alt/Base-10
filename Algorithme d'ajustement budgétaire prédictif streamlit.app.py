import streamlit as st
import math
import time
import os

# --- CORRECTIF SYSTEME FORCE POUR LES DROITS D'EXECUTION ---
try:
    # Force le script à donner les droits de lecture standards au système Linux
    os.chmod(__file__, 0o644)
except Exception:
    pass

# 1. Configuration de la page
st.set_page_config(page_title="Calculatrice", layout="centered")

# 2. En-tête textuel standard
st.title("Calculatrice Evolutive 4.1.1.1")
st.subheader("Moteur Complet Base 10")
st.caption("Developpe par : Chagnon Julien Christian Robert")
st.markdown("---")

# 3. Fonction de calcul budgetaire anti-infinite
def calculer_complement_anti_infini(num_val, den_val):
    if den_val == 0:
        return 0.0, 0.0, "Division par zero impossible"
    temps_debut = time.time()
    part_brute = num_val / den_val
    part_exacte_centimes = math.ceil(part_brute * 100) / 100
    somme_totale_necessaire = part_exacte_centimes * den_val
    somme_a_rajouter = somme_totale_necessaire - num_val
    duree = time.time() - temps_debut
    statut = f"Analyse reussie en {duree:.6f} secondes."
    return somme_a_rajouter, part_exacte_centimes, statut

# 4. Zone de saisie fixe globale
operateur = st.selectbox("Opereur :", options=["/", "+", "-", "*"], index=0)
num_a = st.number_input("Premier nombre :", min_value=0.0, value=55555.0, step=1.0)
num_b = st.number_input("Deuxieme nombre :", min_value=0.0, value=4456.0, step=1.0)

st.markdown("---")

# 5. Declenchement du calcul
if st.button("Lancer l'analyse", type="primary"):
    if operateur == "/":
        if num_b == 0:
            st.error("Erreur : Division par zero impossible.")
        else:
            argent_a_rajouter, part_personne, details = calculer_complement_anti_infini(num_a, num_b)
            
            st.markdown("### Resultats de l'analyse")
            st.write(f"A RAJOUTER AU NUMERATEUR : {argent_a_rajouter:.2f} E")
            st.write(f"PART EXACTE NETTE : {part_personne:.2f} E")
            
            texte_explication = "Explication : Pour eviter une suite infinie, l'application fixe la part a " + str(part_personne) + " E. Pour que ce partage soit rigoureux face aux " + str(int(num_b)) + " beneficiaires, injectez " + str(argent_a_rajouter) + " E."
            st.write(texte_explication)
            st.caption(details)
    else:
        resultat = 0.0
        if operateur == "+":
            resultat = num_a + num_b
        elif operateur == "-":
            resultat = num_a - num_b
        elif operateur == "*":
            resultat = num_a * num_b
        st.success(f"Resultat : {resultat}")

