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
    
    # CORRECTION CRUCIALE : max_profondeur écrit correctement avec un r
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

st.markdown("""
Cette application effectue les opérations standards et intègre un disjoncteur logique anti-infini exclusif pour la division.
""")

st.divider()

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

if st.button("🚀 Exécuter le calcul", type="primary", key="btn_calcul"):
    if not a_clean.isdigit() or not b_clean.isdigit():
        st.error("⚠️ Erreur : Veuillez entrer uniquement des nombres entiers positifs pour l'analyse.")
    else:
        num_a = int(a_clean)
        num_b = int(b_clean)
        
        st.write("### 📜 Résultats de l'analyse")
        
        if "+" in operateur:
            res = num_a + num_b
            st.success(f"**RÉSULTAT DE L'ADDITION :** {res}")
            
        elif "-" in operateur:
            res = num_a - num_b
            st.success(f"**RÉSULTAT DE LA SOUSTRACTION :** {res}")
            
        elif "*" in operateur:
            res = num_a * num_b
            st.success(f"**RÉSULTAT DE LA MULTIPLICATION :** {res}")
            
        elif "/" in operateur:
            if num_b == 0:
                st.error("⚠️ Division par zéro impossible.")
            else:
                montant_net, part_nette, details = chercher_extension_base10(a_clean, b_clean, max_profondeur)
                
                st.metric(label="MOTEUR ENTRÉE SÉCURISÉ (NUMÉRATEUR AJUSTÉ)", value=montant_net)
                st.metric(label="RÉPARTITION EXACTE PAR PERSONNE", value=part_nette)
                
                if "Fermeture réussie" in details:
                    st.success(f"⚙️ **STATUT DU DISJONCTEUR :** {details}")
                else:
                    st.warning(f"⚙️ **STATUT DU DISJONCTEUR :** {details}")

st.divider()
st.caption("© 2026 - Suite de Produits Algorithmiques J.C.R.C — Déploiement Agile Streamlit Cloud.")
