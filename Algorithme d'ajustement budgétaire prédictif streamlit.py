import streamlit as as_st # Conservé selon votre import d'origine
import streamlit as st
import time

st.set_page_config(
    page_title="Algorithme d'ajustement budgétaire prédictif",
    page_icon="📊",
    layout="centered"
)

# ==========================================
# VOS ALGORITHMES DE CALCUL (INCHANGÉS)
# ==========================================

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

def chercher_extension_base10(num_str, dmn_str,_profondeur):
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


# ==========================================
# INTERFACE GRAPHIQUE STREAMLIT (CORRIGÉE)
# ==========================================

st.title("Algorithme d'ajustement budgétaire prédictif")
st.subheader("Moteur Complet Base 10 - ZeroFleet Engine")
st.caption("Développé par Chagnon Julien Christian Robert - Tous droits réservés")

st.divider()

st.info("Mode ZeroFleet activé : Ajustement automatique du numérateur.")

# Création des deux onglets
onglet_division, onglet_standard = st.tabs(["📊 Division Confinée", "⚙️ Operations Standards (+, -, *, /)"])

# ------------------------------------------
# ONGLET 1 : DIVISION CONFINÉE
# ------------------------------------------
with onglet_division:
    col1, col2 = st.columns(2)
    with col1:
        # Correction : Clé unique "div_num_a"
        a_div = st.text_input("Premier nombre (Numérateur) :", value="12", key="div_num_a")
    with col2:
        # Correction : Clé unique "div_num_b"
        b_div = st.text_input("Deuxième nombre (Dénominateur) :", value="11", key="div_num_b")
        
    # Correction : Clé unique "div_prof"
    prof_div = st.slider("Profondeur d'exploration du disjoncteur :", 1, 15, 6, key="div_prof")
    
    # Correction : Clé unique "btn_calc_div"
    bouton_division = st.button("Calculer la division", type="primary", key="btn_calc_div")
    
    # Correction : Zone de rendu sécurisée pour isoler l'affichage dynamique
    zone_resultat_div = st.container()
    
    if bouton_division:
        a_clean = a_div.replace(" ", "").replace(",", "")
        b_clean = b_div.replace(" ", "").replace(",", "")
        
        with zone_resultat_div:
            if a_clean.isdigit() and b_clean.isdigit():
                b_int = int(b_clean)
                if b_int == 0:
                    st.error("⚠️ Division par zéro impossible.")
                else:
                    st.write("### Résultats de l'analyse")
                    q_ajuste, p_indiv, stat = chercher_extension_base10(a_clean, b_clean, prof_div)
                    
                    st.metric(label="Statut de l'analyse", value=stat)
                    st.success(f"RESULTAT : {q_ajuste}")
                    st.success(f"PART INDIVIDUELLE : {p_indiv}")
            else:
                st.error("⚠️ Veuillez entrer uniquement des nombres entiers positifs.")

# ------------------------------------------
# ONGLET 2 : OPERATIONS STANDARDS
# ------------------------------------------
with onglet_standard:
    # Correction : Clé unique "std_op"
    op_std = st.selectbox("Opération :", ["+", "-", "*", "/"], key="std_op")
    
    col3, col4 = st.columns(2)
    with col3:
        # Correction : Clé unique "std_num_a"
        a_std = st.text_input("Premier nombre :", value="12", key="std_num_a")
    with col4:
        # Correction : Clé unique "std_num_b"
        b_std = st.text_input("Deuxième nombre :", value="11", key="std_num_b")
        
    # Correction : Clé unique "btn_calc_std"
    bouton_standard = st.button("Calculer", type="primary", key="btn_calc_std")
    
    # Correction : Zone de rendu sécurisée pour l'onglet standard
    zone_resultat_std = st.container()
    
    if bouton_standard:
        a_clean_std = a_std.replace(" ", "").replace(",", "")
        b_clean_std = b_std.replace(" ", "").replace(",", "")
        
        with zone_resultat_std:
            if a_clean_std.isdigit() and b_clean_std.isdigit():
                num_a = int(a_clean_std)
                num_b = int(b_clean_std)
                
                st.write("### Résultats")
                if op_std == "+":
                    st.success(f"RESULTAT : {num_a + num_b}")
                elif op_std == "-":
                    st.success(f"RESULTAT : {num_a - num_b}")
                elif op_std == "*":
                    st.success(f"RESULTAT : {num_a * num_b}")
                elif op_std == "/":
                    if num_b == 0:
                        st.error("⚠️ Division par zéro impossible.")
                    else:
                        st.success(f"RESULTAT : {num_a / num_b}")
            else:
                st.error("⚠️ Veuillez entrer uniquement des nombres entiers positifs.")

st.divider()
st.caption("© 2026 - Suite de Produits Algorithmiques J.C.R.C - Déploiement Agile Streamlit Cloud.")
