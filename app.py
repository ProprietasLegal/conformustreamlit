import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="ConformU – Analyse RGPD", layout="centered")

st.image("logo_conformu.png", width=180)
st.title("ConformU – Analyse de conformité RGPD")
st.markdown("**Obtenez la conformité légale de votre entreprise sur le marché européen.**")

url = st.text_input("Entrez l’URL de votre site web :", "https://")

if st.button("Lancer l’analyse"):
    if not url.startswith("http"):
        st.warning("Veuillez entrer une URL valide (avec https://)")
    else:
        with st.spinner("Analyse en cours..."):
            try:
                html = requests.get(url, timeout=10).text
                soup = BeautifulSoup(html, "html.parser")
                text = soup.get_text(separator=' ', strip=True).lower()

                checklist = [
                    {"label": "Mentions légales", "score": 10, "keyword": "mentions légales"},
                    {"label": "Politique de confidentialité", "score": 10, "keyword": "politique de confidentialité"},
                    {"label": "Formulaire de contact", "score": 10, "tag": "form"},
                    {"label": "Conditions générales", "score": 5, "keyword": "conditions générales"},
                    {"label": "Liens vers réseaux sociaux", "score": 5, "keywords": ["facebook.com", "linkedin.com", "twitter.com"]},
                    {"label": "HTTPS activé", "score": 5, "https": True},
                    {"label": "Mention RGPD", "score": 5, "keyword": "rgpd"},
                    {"label": "Newsletter détectée", "score": 5, "keyword": "newsletter"},
                    {"label": "Google Analytics / Tag Manager", "score": 10, "script_keywords": ["gtag", "googletagmanager", "analytics"]}
                ]

                total_score = 0
                st.subheader("✅ Résultats par critère")

                for item in checklist:
                    found = False
                    if "keyword" in item:
                        found = item["keyword"] in text
                    elif "keywords" in item:
                        found = any(k in html for k in item["keywords"])
                    elif "tag" in item:
                        found = bool(soup.find(item["tag"]))
                    elif "script_keywords" in item:
                        found = any(k in html for k in item["script_keywords"])
                    elif "https" in item:
                        found = url.startswith("https")

                    score = item["score"] if found else 0
                    total_score += score
                    icon = "✅" if found else "❌"
                    color = "green" if found else "red"
                    st.markdown(f"<span style='color:{color}'>{icon} {item['label']} ({score} pts)</span>", unsafe_allow_html=True)

                st.markdown("---")
                st.subheader("📊 Score global")

                percent = int((total_score / 65) * 100)
                color = "red" if percent < 50 else "orange" if percent < 80 else "green"
                st.markdown(f"""<div style='text-align:center;'>
                    <div style='margin:auto;width:140px;height:140px;border-radius:70px;
                    background-color:{color};display:flex;align-items:center;
                    justify-content:center;font-size:28px;color:white;font-weight:bold;'>
                    {percent}/100
                    </div></div>""", unsafe_allow_html=True)

                st.markdown("---")
                st.markdown("📚 **Références légales RGPD :**")
                st.markdown("""
- **Article 5** – Principes relatifs au traitement des données  
- **Article 6** – Licéité du traitement  
- **Article 12 à 14** – Transparence et information  
- **Article 24** – Responsabilité du responsable de traitement  
- **Article 25** – Protection des données dès la conception  
- **Article 30** – Registre des traitements
""")

                st.markdown("---")
                st.info("💡 Vous souhaitez obtenir un accompagnement juridique personnalisé ? [Contactez-nous](mailto:contact@conformu.eu)")

            except Exception as e:
                st.error(f"Erreur lors de l’analyse : {e}")