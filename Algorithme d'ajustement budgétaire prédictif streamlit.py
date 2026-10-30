import streamlit as st
import time

st.set_page_config(
    page_title="Algorithme d'ajustement budgétaire prédictif",
    page_icon="📊",
    layout="centered"
)

def evaluer_profondeur_b10(chaine_actuelle, dec_actuel, dmn_dec, limite_courante, solution):
    L = len(chaine_actuelle)
    if L >= limite_courante:
        if dec_actuel % dmn_dec == 0:
            solution["extension"] = chaine_actuelle
            solution["quotient"] = dec_actuel // dmn_dec
            return True
        return False
    for chiffre in "0123456789":
        nouveau_dec = dec_actuel * 10 + int(chiffre)
        if evaluer_profondeur_b10(chaine_actuelle + chiffre, nouveau_dec, dmn_dec, limite_courante, solution):
            return True
    return False

def chercher_extension_base10(num_str, dmn_str, _profondeur):
    num_dec_origine = int(num_str)
    dmn_dec = int(dmn_str)
    if dmn_dec == 0:
        return "Erreur", "0,0", "Division par zéro impossible"
    temps_debut = time.time()
    if num_dec_origine % dmn_dec == 0:
        temps_fin = time.time()
        return "0", str(num_dec_origine // dmn_dec), f"Fermeture immédiate en {(temps_fin - temps_debut):.6f} secondes"
    solution = {"extension": None, "quotient": None}
    extension_trouvee = False
    for niveau in range(1, _profondeur + 1):
        if evaluer_profondeur_b10("", num_dec_origine, dmn_dec, niveau, solution):
            extension_trouvee = True
            break
    temps_fin = time.time()
    duree = temps_fin - temps_debut
    if extension_trouvee:
        statut = f"Fermeture réussie en {duree:.6f} secondes"
        quotient_ajuste = f"{num_str},{solution['extension']}"
        q_str = str(solution["quotient"])
        longueur_out = len(solution["extension"])
        part_individuelle = f"({q_str[:-longueur_out]}),({q_str[-longueur_out:]})"
        return quotient_ajuste, part_individuelle, statut
    else:
        return "Calcul incomplet", "0,0", f"Aucune fermeture trouvée ({duree:.6f} s)"

st.title("Algorithme d'ajustement budgétaire prédictif")
st.subheader("Moteur Complet Base 10")

a_div = st.text_input("Premier nombre (Numérateur) :", value="12", key="k_a")
b_div = st.text_input("Deuxième nombre (Dénominateur) :", value="11", key="k_b")
prof_div = st.slider("Profondeur d'exploration :", 1, 15, 6, key="k_p")

if st.button("Calculer la division", type="primary", key="k_btn"):
    a_clean = a_div.replace(" ", "").replace(",", "")
    b_clean = b_div.replace(" ", "").replace(",", "")
    
    if a_clean.isdigit() and b_clean.isdigit():
        if int(b_clean) == 0:
            st.error("Division par zéro impossible.")
        else:
            q_ajuste, p_indiv, stat = chercher_extension_base10(a_clean, b_clean, prof_div)
            st.info(stat)
            st.success(f"RÉSULTAT : {q_ajuste}")
            st.success(f"PART INDIVIDUELLE : {p_indiv}")
    else:
        st.error("Veuillez entrer uniquement des nombres entiers positifs.")

