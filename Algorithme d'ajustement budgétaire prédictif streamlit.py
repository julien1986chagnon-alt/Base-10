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

# Initialisation sécurisée des variables d'état pour bloquer les conflits de rafraîchissement
if "calcul_execute" not in st.session_state:
    st.session_state.calcul_execute = False
    st.session_state.montant_net = ""
    st.session_state.part_nette = ""
    st.session_state.details = ""
    st.session_state.resultat_standard = ""
    st.session_state.type_op = ""

st.title("📊 Algorithme d'ajustement budgétaire prédictif")
st.subheader("Moteur Complet Base 10 — ZeroFloat Engine")
st.caption("Développé par Chagnon Julien Christian Robert — Tous droits réservés")

st.markdown("""
Cette application effectue les opérations standards et intègre un disjoncteur logique anti-infini exclusif pour la division.
""")

st.divider()

# Bloc des contrôles
operateur = st.selectbox(
    "Sélectionnez l'opération à effectuer :",
    ["/ (Division Confinée)", "+ (Addition)", "- (Soustraction)", "* (Multiplication)"],
    key="op_select_box"
)

max_profondeur = 6
if "/" in operateur:
    st.info("💡 Mode ZeroFloat activé : Ajustement automatique du numérateur.")
    max_profondeur = st.slider("Profondeur d'exploration du disjoncteur (chiffres max après la virgule) :", 1, 15, 6, key="prof_slider")

col1, col2 = st.columns(2)
with col1:
    a_saisie = st.text_input("Premier nombre (Numérateur - ex: 12) :", value="12", key="num_a_input")
with col2:
    b_saisie = st.text_input("Deuxième nombre (Dénominateur - ex: 11) :", value="11", key="num_b_input")

a_clean = a_saisie.replace(" ", "").replace(",", "")
b_clean = b_saisie.replace(" ", "").replace(",", "")

# Traitement de l'action utilisateur de façon déconnectée du rendu graphique direct
if st.button("🚀 Exécuter le calcul", type="primary", key="btn_calcul"):
    if not a_clean.isdigit() or not b_clean.isdigit():
        st.error("⚠️ Erreur : Veuillez entrer uniquement des nombres entiers positifs pour l'analyse.")
        st.session_state.calcul_execute = False
    else:
        num_a = int(a_clean)
        num_b = int(b_clean)
        st.session_state.calcul_execute = True
        
        if "+" in operateur:
            st.session_state.type_op = "add"
            st.session_state.resultat_standard = str(num_a + num_b)
        elif "-" in operateur:
            st.session_state.type_op = "sub"
            st.session_state.resultat_standard = str(num_a - num_b)
        elif "*" in operateur:
            st.session_state.type_op = "mul"
            st.session_state.resultat_standard = str(num_a * num_b)
        elif "/" in operateur:
            if num_b == 0:
                st.error("⚠️ Division par zéro impossible.")
                st.session_state.calcul_execute = False
            else:
                st.session_state.type_op = "div"
                m_net, p_nette, det = chercher_extension_base10(a_clean, b_clean, max_profondeur)
                st.session_state.montant_net = m_net
                st.session_state.part_nette = p_nette
                st.session_state.details = det

# Affichage des résultats basé UNIQUEMENT sur l'état mémorisé (Prévient mécaniquement l'erreur removeChild)
if st.session_state.calcul_execute:
    st.write("### 📜 Résultats de l'analyse")
    
    if st.session_state.type_op == "add":
        st.success(f"**RÉSULTAT DE L'ADDITION :** {st.session_state.resultat_standard}")
    elif st.session_state.type_op == "sub":
        st.success(f"**RÉSULTAT DE LA SOUSTRACTION :** {st.session_state.resultat_standard}")
    elif st.session_state.type_op == "mul":
        st.success(f"**RÉSULTAT DE LA MULTIPLICATION :** {st.session_state.resultat_standard}")
    elif st.session_state.type_op == "div":
        st.metric(label="MOTEUR ENTRÉE SÉCURISÉ (NUMÉRATEUR AJUSTÉ)", value=st.session_state.montant_net)
        st.metric(label="RÉPARTITION EXACTE PAR PERSONNE", value=st.session_state.part_nette)
        
        if "Fermeture réussie" in st.session_state.details:
            st.success(f"⚙️ **STATUT DU DISJONCTEUR :** {st.session_state.details}")
        else:
            st.warning(f"⚙️ **STATUT DU DISJONCTEUR :** {st.session_state.details}")

st.divider()
st.caption("© 2026 - Suite de Produits Algorithmiques J.C.R.C — Déploiement Agile Streamlit Cloud.")

