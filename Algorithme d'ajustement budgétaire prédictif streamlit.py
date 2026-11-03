import streamlit as st
import math

# 1. Configuration de la page
st.set_page_config(page_title="Calculatrice", layout="centered")

# 2. Titres
st.title("Calculatrice Evolutive 4.1.1.1")
st.subheader("Moteur Complet Base 10")
st.caption("Developpe par : Chagnon Julien Christian Robert")
st.markdown("---")

# 3. Entrées utilisateur en direct
operateur = st.selectbox("Operateur :", options=["/", "+", "-", "*"], index=0)
num_a = st.number_input("Premier nombre (Numerateur) :", value=55555.0)
num_b = st.number_input("Deuxieme nombre (Denominateur) :", value=4456.0)

st.markdown("---")
st.markdown("### Resultats en direct")

# 4. Logique de calcul directe (sans bouton, sans fonction externe)
if operateur == "/":
    if num_b == 0:
        st.error("Division par zero impossible")
    else:
        # Calcul direct
        part_brute = num_a / num_b
        part_exacte_centimes = math.ceil(part_brute * 100) / 100
        somme_totale_necessaire = part_exacte_centimes * num_b
        somme_a_rajouter = somme_totale_necessaire - num_a
        
        # Affichage basique et ultra-stable
        st.success(f"A RAJOUTER AU NUMERATEUR : {somme_a_rajouter:.2f} E")
        st.success(f"PART EXACTE NETTE PAR PERSONNE : {part_exacte_centimes:.2f} E")
        
        st.markdown(f"Explication : Pour eviter une suite infinie, la part est fixee a {part_exacte_centimes} E. Pour {int(num_b)} beneficiaires, il faut ajouter {somme_a_rajouter:.2f} E.")

else:
    resultat = 0.0
    if operateur == "+":
        resultat = num_a + num_b
    elif operateur == "-":
        resultat = num_a - num_b
    elif operateur == "*":
        resultat = num_a * num_b
    st.success(f"Resultat : {resultat}")

