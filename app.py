import streamlit as st
import math

# 1. Configuration de la page (Doit être la toute première commande Streamlit)
st.set_page_config(
    page_title="Calculatrice Évolutive", 
    layout="centered"
)

# 2. Section Titres et Présentation
st.title("Calculatrice Évolutive 4.1.1.1")
st.subheader("Moteur Complet Base 10")
st.caption("Développé par : Chagnon Julien Christian Robert")
st.markdown("---")

# 3. Entrées utilisateur
st.sidebar.header("Paramètres")
st.sidebar.write("Modifiez les valeurs pour recalculer instantanément.")

# Choix de l'opérateur
operateur = st.sidebar.selectbox(
    "Opérateur :", 
    options=["/", "*", "-", "+"], 
    index=0
)

# Blocs de saisie numérique
col1, col2 = st.columns(2)
with col1:
    num_a = st.number_input("Premier nombre (Numérateur) :", value=55555.0, format="%.2f")
with col2:
    num_b = st.number_input("Deuxième nombre (Dénominateur) :", value=4456.0, format="%.2f")

st.markdown("---")
st.markdown("### Résultats en direct")

# 4. Logique de calcul et sécurisation
if operateur == "/":
    if num_b == 0:
        st.error("🚨 Division par zéro impossible. Veuillez modifier le dénominateur.")
    else:
        # Calculs budgétaires (Logique de votre algorithme d'origine)
        part_brute = num_a / num_b
        part_poste_centimes = math.ceil(part_brute * 100) / 100
        somme_totale_parametre = part_poste_centimes * num_b
        somme_a_repartir = somme_totale_parametre - num_a
        
        # Affichage des fiches de résultats (Metrics)
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.metric(label="À COMPTER AU NUMÉRATEUR", value=f"{somme_a_repartir:.2f} €")
        with res_col2:
            st.metric(label="PART STRICTE NETTE PAR PERSONNE", value=f"{part_poste_centimes:.2f} €")
        
        # Explication textuelle dynamique
        st.info(
            f"**Explication :** Pour éviter une suite infinie, la part est fixée à `{part_poste_centimes:.2f}` €. "
            f"Pour `{num_b:.0f}` bénéficiaires, il faut rajouter `{somme_a_repartir:.2f}` €."
        )

# Calculs pour les autres opérateurs standard
else:
    resultat = 0.0
    if operateur == "*":
        resultat = num_a * num_b
    elif operateur == "-":
        resultat = num_a - num_b
    elif operateur == "+":
        resultat = num_a + num_b
        
    st.success(f"**Résultat de l'opération ({operateur}) :** {resultat:,.2f}")

