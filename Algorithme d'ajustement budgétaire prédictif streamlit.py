import streamlit as st
import time

# La configuration de la page doit être la TOUTE PREMIÈRE commande Streamlit exécutée
st.set_page_config(
    page_title="Algorithme d'ajustement budgétaire prédictif",
    page_icon="📊",
    layout="centered"
)

# Alias pour préserver votre compatibilité historique si nécessaire
as_st = st

# Initialisation des variables d'état (Session State)
if "calc_triggered" not in st.session_state:
    st.session_state.calc_triggered = False
    st.session_state.calc_type = None
    st.session_state.res_data = {}

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


# ==========================================
# INTERFACE GRAPHIQUE STREAMLIT
# ==========================================

st.title("Algorithme d'ajustement budgétaire prédictif")
st.subheader("Moteur Complet Base 10 - ZeroFleet Engine")
st.caption("Développé par Chagnon Julien Christian Robert - Tous droits réservés")

st.divider()
st.info("Mode ZeroFleet activé : Ajustement automatique du numérateur.")

onglet_division, onglet_standard = st.tabs(["📊 Division Confinée", "⚙️ Operations Standards (+, -, *, /)"])

# --- ONGLET 1 : DIVISION CONFINÉE ---
with onglet_division:
    col1, col2 = st.columns(2)
    with col1:
        a_div = st.text_input("Premier nombre (Numérateur) :", value="12", key="div_num_a")
    with col2:
        b_div = st.text_input("Deuxième nombre (Dénominateur) :", value="11", key="div_num_b")
        
    prof_div = st.slider("Profondeur d'exploration du disjoncteur :", 1, 15, 6, key="div_prof")
    
    if st.button("Calculer la division", type="primary", key="btn_calc_div"):
        st.session_state.calc_triggered = True
        st.session_state.calc_type = "division"
        st.session_state.res_data = {"a": a_div, "b": b_div, "prof": prof_div}

# --- ONGLET 2 : OPERATIONS STANDARDS ---
with onglet_standard:
    op_std = st.selectbox("Opération :", ["+", "-", "*", "/"], key="std_op")
    
    col3, col4 = st.columns(2)
    with col3:
        a_std = st.text_input("Premier nombre :", value="12", key="std_num_a")
    with col4:
        b_std = st.text_input("Deuxième nombre :", value="11", key="std_num_b")
        
    if st.button("Calculer", type="primary", key="btn_calc_std"):
        st.session_state.calc_triggered = True
        st.session_state.calc_type = "standard"
        st.session_state.res_data = {"a": a_std, "b": b_std, "op": op_std}

# ==========================================
# ZONE RÉSULTATS IMPERMÉABLE AUX BUGS DOM
# ==========================================
st.divider()

if st.session_state.calc_triggered:
    data = st.session_state.res_data
    a_clean = data["a"].replace(" ", "").replace(",", "")
    b_clean = data["b"].replace(" ", "").replace(",", "")
    
    st.write("### Résultats de l'analyse")
    
    if not (a_clean.isdigit() and b_clean.isdigit()):
        st.markdown('<div translate="no" style="color:#ff4b4b; padding:10px; border-radius:5px; background-color:rgba(255,75,75,0.1)">⚠️ Veuillez entrer uniquement des nombres entiers positifs.</div>', unsafe_allow_html=True)
    else:
        # Traitement Onglet 1
        if st.session_state.calc_type == "division":
            b_int = int(b_clean)
            if b_int == 0:
                st.markdown('<div translate="no" style="color:#ff4b4b; padding:10px; border-radius:5px; background-color:rgba(255,75,75,0.1)">⚠️ Division par zéro impossible.</div>', unsafe_allow_html=True)
            else:
                q_ajuste, p_indiv, stat = chercher_extension_base10(a_clean, b_clean, data["prof"])
                
                st.markdown(f'<div translate="no" style="padding:10px; background:#f0f2f6; border-radius:5px; margin-bottom:10px;"><strong>Statut :</strong> {stat}</div>', unsafe_allow_html=True)
                st.markdown(f'<div translate="no" style="color:#09ab3b; padding:10px; border-radius:5px; background-color:rgba(9,171,59,0.1); margin-bottom:10px;"><strong>RESULTAT :</strong> {q_ajuste}</div>', unsafe_allow_html=True)
                st.markdown(f'<div translate="no" style="color:#09ab3b; padding:10px; border-radius:5px; background-color:rgba(9,171,59,0.1);"><strong>PART INDIVIDUELLE :</strong> {p_indiv}</div>', unsafe_allow_html=True)
                
        # Traitement Onglet 2
        elif st.session_state.calc_type == "standard":
            num_a = int(a_clean)
            num_b = int(b_clean)
            op = data["op"]
            
            res_val = 0
            if op == "+": res_val = num_a + num_b
            elif op == "-": res_val = num_a - num_b
            elif op == "*": res_val = num_a * num_b
            elif op == "/":
                if num_b == 0:
                    st.markdown('<div translate="no" style="color:#ff4b4b; padding:10px; border-radius:5px; background-color:rgba(255,75,75,0.1)">⚠️ Division par zéro impossible.</div>', unsafe_allow_html=True)
                    res_val = None
                else:
                    res_val = num_a / num_b
            
            if res_val is not None:
                st.markdown(f'<div translate="no" style="color:#09ab3b; padding:10px; border-radius:5px; background-color:rgba(9,171,59,0.1)"><strong>RESULTAT :</strong> {res_val}</div>', unsafe_allow_html=True)

st.caption("© 2026 - Suite de Produits Algorithmiques J.C.R.C - Déploiement Agile Streamlit Cloud.")

