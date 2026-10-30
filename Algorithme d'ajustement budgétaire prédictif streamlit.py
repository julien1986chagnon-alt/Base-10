import streamlit as st
import time

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Calculatrice Évolutive 4.1.1.1",
    page_icon="📊",
    layout="centered"
)

# """
# TITRE : Calculatrice Évolutive 4.1.1.1 - VERSION BASE 10 INTEGRALE
# Principe : Opérations standards et recherche de palier minimal pour la division
# Moteur : ZeroFloat Engine / Confinement Algorithmique
# Développé par : Chagnon Julien Christian Robert - Tous droits réservés
# """

# =====================================================================
# MOTEUR DE RECHERCHE DE EXTENSION (CONFINEMENT DIVISION BASE 10)
# =====================================================================

def evaluer_profondeur_b10(chaine_actuelle, dec_actuel, den_dec, limite_courante, solution):
    L = len(chaine_actuelle)
    if L == limite_courante:
        if dec_actuel % den_dec == 0:
            solution["extension"] = chaine_actuelle
            solution["quotient"] = dec_actuel // den_dec
            return True
        return False

    for chiffre in "0123456789":
        # ALGORITHME DE BASE 10 : Multiplicateur 10 pour décaler la cascade
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
    
    # Cas 0 : Si le montant de départ est déjà parfaitement divisible
    if num_dec_origine % den_dec == 0:
        temps_fin = time.time()
        return "0", str(num_dec_origine // den_dec), f"Fermeture immédiate en {temps_fin - temps_debut:.6f} secondes"

    solution = {"extension": None, "quotient": None}
    extension_trouvee = False
    
    # Utilisation de la profondeur choisie par l'utilisateur via le curseur
    for niveau in range(1, max_profondeur + 1):
        if evaluer_profondeur_b10("", num_dec_origine, den_dec, niveau, solution):
            extension_trouvee = True
            break
            
    temps_fin = time.time()
    duree = temps_fin - temps_debut
    
    if extension_trouvee:
        statut = f"Fermeture réussie en {duree:.6f} secondes"
        
        # Formatage visuel automatique du montant ajusté
        montant_ajuste = f"{num_str},{solution['extension']}"
        
        # Formatage du quotient pour l'affichage de la part individuelle
        q_str = str(solution["quotient"])
        longueur_ext = len(solution["extension"])
        part_individuelle = f"{q_str[:-longueur_ext]},{q_str[-longueur_ext:]}"
        return montant_ajuste, part_individuelle, statut
    else:
        return "Calcul incomplet", "0,0", f"Aucune fermeture trouvée jusqu'à la profondeur {max_profondeur} ({duree:.6f} s)"


# =====================================================================
# INTERFACE UTILISATEUR STREAMLIT
# =====================================================================

st.title("📊 Calculatrice Évolutive 4.1.1.1")
st.subheader("Moteur Complet Base 10 — ZeroFloat Engine")
st.caption("Développé par Chagnon Julien Christian Robert — Tous droits réservés")

st.markdown("""
Cette application effectue les opérations standards et intègre un **disjoncteur logique anti-infini** exclusif pour la division. 
Face à une virgule infinie, elle calcule le segment de confinement minimal requis à l'entrée pour équilibrer parfaitement la sortie.
""")

st.divider()

# 1. ORDRE CHANGÉ : On demande d'abord l'opérateur
operateur = st.radio(
    "Sélectionnez l'opération à effectuer :",
    ["+ (Addition)", "- (Soustraction)", "* (Multiplication)", "/ (Division Confinée)"],
    index=3,
    horizontal=True
)

# Options spécifiques pour la division
max_profondeur = 6
if "/" in operateur:
    # Activation exclusive du disjoncteur ZeroFloat pour la division
    st.info("💡 Mode ZeroFloat activated : Ajustement automatique du numérateur.")
    max_profondeur = st.slider("Profondeur d'exploration du disjoncteur (chiffres max après la virgule) :", 1, 15, 6)

# 2. On demande le premier nombre et le deuxième nombre
col1, col2 = st.columns(2)
with col1:
    a_saisie = st.text_input("Premier nombre (Numérateur - ex: 12) :", value="12")
with col2:
    b_saisie = st.text_input("Deuxième nombre (Dénominateur - ex: 11) :", value="11")

# Nettoyage des chaînes saisies et vérification numérique stricte
a_clean = a_saisie.replace(" ", "").replace(",", "")
b_clean = b_saisie.replace(" ", "").replace(",", "")

# Bouton de lancement du calcul
if st.button("🚀 Exécuter le calcul", type="primary"):
    if not a_clean.isdigit() or not b_clean.isdigit():
        st.error("⚠️ Erreur : Veuillez entrer uniquement des nombres entiers positifs pour l'analyse.")
    else:
        num_a = int(a_clean)
        num_b = int(b_clean)
        
        st.write("### 📜 Résultats de l'analyse")
        
        # Traitement selon l'opérateur choisi
        if "+" in operateur:
            res = num_a + num_b
            st.success(f"**RÉSULTAT DE L'ADDITION :** {res}")
            st.caption("Calcul standard exécuté instantanément.")
            
        elif "-" in operateur:
            res = num_a - num_b
            st.success(f"**RÉSULTAT DE LA SOUSTRACTION :** {res}")
            st.caption("Calcul standard exécuté instantanément.")
            
        elif "*" in operateur:
            res = num_a * num_b
            st.success(f"**RÉSULTAT DE LA MULTIPLICATION :** {res}")
            st.caption("Calcul standard exécuté instantanément.")
            
        elif "/" in operateur:
            if num_b == 0:
                st.error("⚠️ Division par zéro impossible.")
            else:
                with st.spinner("Analyse et calcul du confinement en cours..."):
                    montant_net, part_nette, details = chercher_extension_base10(a_clean, b_clean, max_profondeur)
                
                # Zone d'affichage des résultats structurels
                st.metric(label="MOTEUR ENTRÉE SÉCURISÉ (NUMÉRATEUR AJUSTÉ)", value=montant_net)
                st.metric(label="RÉPARTITION EXACTE PAR PERSONNE", value=part_nette)
                
                if "Fermeture réussie" in details:
                    st.success(f"⚙️ **STATUT DU DISJONCTEUR :** {details}")
                else:
                    st.warning(f"⚙️ **STATUT DU DISJONCTEUR :** {details}")

st.divider()
st.caption("© 2026 - Suite de Produits Algorithmiques J.C.R.C — Déploiement Agile Streamlit Cloud.")

