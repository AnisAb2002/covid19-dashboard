# Dashboard COVID-19 – Visualisation interactive

Un dashboard interactif pour explorer les données mondiales COVID-19 de l'OMS, construit avec **Python**, **Dash** et **Plotly**.

---

## Aperçu

> Le dashboard charge les données directement depuis l'OMS au premier lancement.  
> Si le réseau est indisponible, des données de démonstration réalistes sont générées automatiquement.

---

## Fonctionnalités

- **Carte mondiale** interactive des cas cumulés par pays.
- **Top 10 pays** avec filtre par région OMS.
- **Évolution temporelle** des nouveaux cas avec lissage sur 7 jours
- **Graphique en donut** – répartition par région OMS
- **Scatter plot** cas vs décès en échelle logarithmique.
- **KPIs (indicateur clé de performance)** globaux (total cas, décès, taux de létalité, nombre de pays)
- Filtres interactifs : **région OMS** et **sélection multi-pays**.

---

## Technologies utilisées

| Outil | Rôle |
|---|---|
| [Dash](https://dash.plotly.com/) | Framework web pour l'application |
| [Plotly](https://plotly.com/python/) | Graphiques interactifs |
| [Pandas](https://pandas.pydata.org/) | Traitement et nettoyage des données |
| [Requests](https://docs.python-requests.org/) | Téléchargement des données OMS |
| [Gunicorn](https://gunicorn.org/) | Serveur WSGI pour le déploiement |

---

## Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/AnisAb2002/covid19-dashboard
cd covid19-dashboard
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv

venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Lancer l'application

```bash
python app.py
```
L'application s'ouver sur le navigateur sur **http://localhost:8050** 

---

## Structure du projet

```
covid19-dashboard/
│
├── app.py              # Application principale Dash + tous les callbacks
├── data_loader.py      # Téléchargement et nettoyage des données OMS
├── requirements.txt    # Dépendances Python
├── Procfile            # Configuration déploiement (Render, Railway…)
├── .gitignore
│
├── assets/
│   └── style.css       # Thème dark custom
│
└── data/               # CSV OMS (auto-généré, ignoré par Git)
    └── WHO-COVID-19-global-data.csv
```

---

## Source des données

Les données proviennent de l'Organisation Mondiale de la Santé OMS :

 https://covid19.who.int/data

Le fichier `WHO-COVID-19-global-data.csv` est téléchargé automatiquement au démarrage et mis en cache localement pendant 24h.

---

## Déploiement

Le projet est prêt à être déployé gratuitement sur **[Render](https://render.com)**

### Sur Render :
1. Nouveau service Web → connecter le repo GitHub
2. **Build command** : `pip install -r requirements.txt`
3. **Start command** : `gunicorn app:server`
4. C'est tout !

---

## Anis  ABDAT -- Données OMS (WHO) -- Projet étudiant

---

*Projet réalisé dans le cadre de mon apprentissage en Data Science / Développement Python.*
