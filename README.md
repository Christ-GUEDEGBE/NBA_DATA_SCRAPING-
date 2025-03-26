# 🏀 NBA Stats Scraper & Cloud Data Pipeline  

Ce projet permet de scraper des statistiques NBA depuis le site officiel et de les stocker dans une **base de données PostgreSQL hébergée sur le cloud**. Le tout est **containerisé avec Docker** et peut être automatisé via **GitHub Actions** ou un service cloud.  

## 🚀 Fonctionnalités  

✅ **Scraping avancé** → Extraction des statistiques NBA à l'aide de Selenium.  
✅ **Stockage Cloud** → Envoi des données vers une base PostgreSQL distante.  
✅ **Dockerisation** → Exécution facile grâce à un conteneur Docker.  
✅ **Automatisation** → Planification de l'extraction à intervalles réguliers.  

---

## 📁 Structure du projet  

nba-stats-scraper/ │── data/ # (Dossier pour stocker les fichiers CSV localement si besoin) │── src/ │ ├── scraper.py # Script Python pour le scraping │ ├── db_utils.py # Fonctions pour interagir avec PostgreSQL │── .env # Variables d'environnement (PostgreSQL, Selenium config) │── Dockerfile # Configuration du conteneur Docker │── docker-compose.yml # Orchestration des services (DB + Scraper) │── requirements.txt # Dépendances Python │── README.md # Documentation du projet

yaml
Copy
Edit

---

## 📦 Installation  

### 1️⃣ Prérequis  
- **Python 3.8+**  
- **Docker & Docker Compose**  
- Un **compte Railway.app** ou **AWS RDS** pour PostgreSQL  

### 2️⃣ Cloner le repo  

```bash
git clone https://github.com/ton-pseudo/nba-stats-scraper.git
cd nba-stats-scraper
3️⃣ Configurer les variables d’environnement
Créer un fichier .env :

ini
Copy
Edit
DB_HOST=your_cloud_db_host
DB_PORT=5432
DB_NAME=your_db_name
DB_USER=your_username
DB_PASSWORD=your_password
🛠️ Exécution
1️⃣ Exécuter le scraping en local
bash
Copy
Edit
pip install -r requirements.txt
python src/scraper.py
2️⃣ Lancer avec Docker
bash
Copy
Edit
docker-compose up --build
🎯 Automatisation
📌 Via GitHub Actions
Un workflow peut être configuré pour exécuter le script chaque jour/semaine.

☁️ Déploiement Cloud
Le scraper peut être exécuté sur Google Cloud Run ou AWS Lambda.

📊 Résultat attendu
Les données récupérées sont stockées dans une table PostgreSQL et peuvent être utilisées pour du Machine Learning ou de l’analyse avancée.

🏗️ Prochaines améliorations
🔹 API FastAPI → Exposer les données via une API REST.
🔹 Dashboard Power BI / Streamlit → Visualisation des données.
🔹 Ajout d’un stockage S3 → Sauvegarde des données en CSV sur le cloud.

🏀 Auteur
👨‍💻 Divin
🚀 Ingénieur passionné par la Data Science et l’Automatisation
📌 LinkedIn

📝 Licence
Ce projet est sous licence MIT. Libre à toi de le modifier et de l'améliorer !

markdown
Copy
Edit

---

🎯 **Ce README est ultra complet et prêt à être copié-collé** !  
✅ Il **explique bien le projet**  
✅ Il **donne toutes les étapes d’installation**  
✅ Il **prépare le terrain pour des évolutions futures**  

Si tu veux, on peut maintenant :  
- Ajouter **Dockerfile & docker-compose.yml**  
- **Configurer PostgreSQL sur Railway.app**  
- **Automatiser avec GitHub Actions**  

**Qu’est-ce que tu veux attaquer en premier ?** 🚀🔥

