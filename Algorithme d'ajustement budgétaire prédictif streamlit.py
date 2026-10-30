import streamlit as st
import time

st.set_page_config(
    page_title="Algorithme d'ajustement budgétaire prédictif",
    page_icon="📊",
    layout="centered"
)

def evaluer_profondeur_b10(chaine_actuelle, dec_actuel, den_dec, limite_courante, solution):
    L = len(chaine_actuelle)
    if L == limite_courante:
        if dec_actuel % den_dec == 0:
            solution["extension"] = chaine_actuelle
            solution["quotient"] = dec_actuel // den_dec
            return True
        return False

    for chiffre in "0123456789":
        nouveau_dec = dec_actuel * 10 + int(chiffre)
        if evaluer_profondeur_b10(chaine_actuelle + chiffre, nouveau_dec, den_dec, limite_courante, solution):
            return True
    return False

def chercher_extension_base10(num_str, den_str, max_profondeur):
    num_dec_origine = int(num_str)
    den_dec = int(den_str)
    
    if den_dec == 0:
        return "Erreur", "0,0", "Division par zéro impossible"
        
    temps_debut = time.time()
    
    if num_dec_origine % den_dec == 0:
        temps_fin = time.time()
        return "0", str(num_dec_origine // den_dec), f"Fermeture immédiate en {temps_fin - temps_debut:.6f} secondes"

    solution = {"extension": None, "quotient": None}
    extension_trouvee = False
    
    for niveau in range(1, max_profondeur + 1):
        if evaluer_profondeur_b10("", num_dec_origine, den_dec, niveau, solution):
            extension_trouvee = True
            break
            
    temps_fin = time.time()
    duree = temps_fin - temps_debut
    
    if extension_trouvee:
        statut = f"Fermeture réussie en {duree:.6f} secondes"
        montant_ajuste = f"{num_str},{solution['extension']}"
        q_str = str(solution["quotient"])
        longueur_ext = len(solution["extension"])
        part_individuelle = f"{q_str[:-longueur_ext]},{q_str[-longueur_ext:]}"
        return montant_ajuste, part_individuelle, statut
    else:
        return "Calcul incomplet", "0,0", f"Aucune fermeture trouvée ({duree:.6f} s)"

st.title("📊 Algorithme d'ajustement budgétaire prédictif")
st.subheader("Moteur Complet Base 10 — ZeroFloat Engine")
st.caption("Développé par Chagnon Julien Christian Robert — Tous droits réservés")

st.divider()

# Création de deux espaces étanches pour empêcher le crash visuel de Streamlit
onglet_division, onglet_standard = st.tabs(["/ Division Confinée", "➕ Operations Standards (+, -, *)"])

with onglet_division:
    st.info("💡 Mode ZeroFloat activé : Ajustement automatique du numérateur.")
    max_profondeur = st.slider("Profondeur d'exploration du disjoncteur :", 1, 15, 6, key="prof_div")
    
    col1, col2 = st.columns(2)
    with col1:
        a_div = st.text_input("Premier nombre (Numérateur) :", value="12", key="num_a_div")
    with col2:
        b_div = st.text_input("Deuxième nombre (Dénominateur) :", value="11", key="num_b_div")
        
    if st.button("🚀 Calculer la division", type="primary", key="btn_div"):
        a_clean = a_div.replace(" ", "").replace(",", "")
        b_clean = b_div.replace(" ", "").replace(",", "")
        
        if a_clean.isdigit() and b_clean.isdigit():
            if int(b_clean) == 0:
                st.error("⚠️ Division par zéro impossible.")
            else:
                m_net, p_nette, det = chercher_extension_base10(a_clean, b_clean, max_profondeur)
                st.write("### 📜 Résultats de l'analyse")
                st.metric(label="MOTEUR ENTRÉE SÉCURISÉ (NUMÉRATEUR AJUSTÉ)", value=m_net)
                st.metric(label="RÉPARTITION EXACTE PAR PERSONNE", value=p_nette)
                st.success(f"⚙️ {det}")
        else:
            st.error("⚠️ Veuillez entrer uniquement des nombres entiers positifs.")

with onglet_standard:
    op_std = st.selectbox("Opération :", ["+", "-", "*"], key="op_std")
    col3, col4 = st.columns(2)
    with col3:
        a_std = st.text_input("Premier nombre :", value="12", key="num_a_std")
    with col4:
        b_std = st.text_input("Deuxième nombre :", value="11", key="num_b_std")
        
    if st.button("🚀 Calculer", type="primary", key="btn_std"):
        a_clean = a_std.replace(" ", "").replace(",", "")
        b_clean = b_std.replace(" ", "").replace(",", "")
        
        if a_clean.isdigit() and b_clean.isdigit():
            num_a = int(a_clean)
            num_b = int(b_clean)
            st.write("### 📜 Résultats")
            if op_std == "+":
                st.success(f"**RÉSULTAT :** {num_a + num_b}")
            elif op_std == "-":
                st.success(f"**RÉSULTAT :** {num_a - num_b}")
            elif op_std == "*":
                st.success(f"**RÉSULTAT :** {num_a * num_b}")
        else:
            st.error("⚠️ Veuillez entrer uniquement des nombres entiers positifs.")

st.divider()
st.caption("© 2026 - Suite de Produits Algorithmiques J.C.R.C — Déploiement Agile Streamlit Cloud.")

