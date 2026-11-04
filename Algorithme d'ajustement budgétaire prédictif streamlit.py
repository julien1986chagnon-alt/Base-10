import streamlit as st
import math

# 1. Configuration de la page
st.set_page_config(page_title="Calculatrice", layout="centered")

# 2. Titres
st.title("Calculatrice Évolutive 4.1.1.1")
st.subheader("Moteur Complet Base 10")
st.caption("Développé par : Chagnon Julien Christian Robert")
st.markdown("---")

# 3. Entrées utilisateur en direct
operateur = st.selectbox("Opérateur :", options=["/", "*", "-", "+"], index=0)
num_a = st.number_input("Premier nombre (Numérateur) :", value=55555.0)
num_b = st.number_input("Deuxième nombre (Dénominateur) :", value=4456.0)

st.markdown("---")
st.markdown("### Résultats en direct")

# 4. Logique de calcul directe
if operateur == "/" and num_b == 0:
    st.error("Division par zéro impossible")
else:
    # Calculs de base
    part_brute = num_a / num_b
    part_particulier = math.ceil(part_brute * 100) / 100
    somme_totale_parametre = part_particulier * num_b
    somme_a_repartir = somme_totale_parametre - num_a
    
    # Affichage en direct
    st.success(f"À COMPTER AU NUMÉRATEUR : {somme_a_repartir:.2f} €")
    st.success(f"PART STRICTE NETTE PAR PERSONNE : {part_particulier:.2f} €")
    
    st.markdown("---")

    # Calcul alternatif selon l'opérateur sélectionné
    resultat = 0.0
    if operateur == "/":
        resultat = num_a / num_b
    elif operateur == "*":
        resultat = num_a * num_b
    elif operateur == "-":
        resultat = num_a - num_b
    elif operateur == "+":
        resultat = num_a + num_b
        
    st.success(f"Résultat : {resultat}")

