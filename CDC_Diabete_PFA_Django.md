# Cahier des Charges (CDC)
## Application Web de Détection du Risque de Diabète

---

<div style="background-color: #7CB342; color: white; padding: 20px; border-radius: 8px;">

**Référence** : CDC-DIABETE-PFA-2026-V1.0  
**Version** : 1.0  
**Date** : Juin 2026  
**Contexte** : Projet de Fin d'Année (PFA) — Environnement local  
**Stack** : Django + HTML/CSS/JS + SQLite + XGBoost

</div>

---

## 🎨 Palette de Couleurs du Projet

| Couleur | Code HEX | Utilisation |
|---------|----------|-------------|
| <span style="background:#7CB342; color:white; padding:2px 8px; border-radius:4px;">Vert Principal</span> | `#7CB342` | Header, boutons principaux, accents |
| <span style="background:#558B2F; color:white; padding:2px 8px; border-radius:4px;">Vert Foncé</span> | `#558B2F` | Titres, texte important |
| <span style="background:#8BC34A; color:white; padding:2px 8px; border-radius:4px;">Vert Clair</span> | `#8BC34A` | Fonds de sections, hover |
| <span style="background:#689F38; color:white; padding:2px 8px; border-radius:4px;">Vert Moyen</span> | `#689F38` | Icônes, badges |
| <span style="background:#F5F5F5; color:#333; padding:2px 8px; border-radius:4px;">Gris Clair</span> | `#F5F5F5` | Fonds de cartes, sections |
| <span style="background:#FFFFFF; color:#333; padding:2px 8px; border-radius:4px; border:1px solid #ddd;">Blanc</span> | `#FFFFFF` | Fond principal |
| <span style="background:#333333; color:white; padding:2px 8px; border-radius:4px;">Noir Texte</span> | `#333333` | Texte principal |
| <span style="background:#666666; color:white; padding:2px 8px; border-radius:4px;">Gris Texte</span> | `#666666` | Texte secondaire |

---

## I. Introduction et Objectifs du Projet

### 1.1 Contexte et Problématique

> 💚 **Le diabète** est l'une des maladies chroniques les plus répandues à l'échelle mondiale. Selon l'OMS, plus de **422 millions de personnes** sont atteintes de diabète. La détection précoce du risque diabétique est un enjeu majeur de santé publique.

Ce projet de fin d'année vise à développer une **application web intelligente et accessible**, permettant à des utilisateurs de soumettre leurs données médicales et d'obtenir instantanément une évaluation de leur risque de diabète, grâce à l'intégration d'un **modèle de Machine Learning pré-entraîné**.

### 1.2 Présentation du Projet

Le projet consiste en la conception et le développement d'une application web **full-stack** combinant :
- Une interface utilisateur simple et moderne (**HTML/CSS/JS**)
- Une infrastructure back-end robuste (**Django**)
- Un modèle **XGBClassifier (XGBoost)** fourni sous forme de fichier `.pkl`

### 1.3 Objectifs du Projet

#### ✅ Objectifs fonctionnels
- **Prédiction en temps réel** : Permettre à tout utilisateur authentifié de renseigner ses données cliniques et d'obtenir immédiatement un score de risque de diabète.
- **Sensibilisation au diabète** : Fournir des informations pédagogiques sur le diabète (symptômes, facteurs de risque, prévention).
- **Gestion des comptes utilisateurs** : Offrir un système complet d'inscription, de connexion et de gestion de profil.
- **Historique des prédictions** : Conserver l'historique des analyses effectuées par chaque utilisateur.
- **Administration système** : Fournir à l'administrateur un back-office pour superviser les utilisateurs.

#### ⚙️ Objectifs techniques
- Intégrer le fichier de modèle `xgboost_diabetes_model.pkl` dans l'application Django.
- Garantir la sécurité des données avec l'authentification Django native.
- Assurer la maintenabilité du code avec une architecture Django propre (MVT).
- Respecter le principe de moindre privilège pour les accès aux fonctionnalités sensibles.

### 1.4 Périmètre du Projet

| Inclus | Hors périmètre |
|--------|---------------|
| Application web locale, API d'inférence ML, authentification Django, espace admin, historique des résultats, formulaire de contact | Réentraînement du modèle ML, application mobile, intégration avec des systèmes médicaux externes, téléconseils médicaux |
| Modèle ML | Le modèle `xgboost_diabetes_model.pkl` est fourni et intégré tel quel, sans modification |
| Déploiement | Application exécutée en local sur PC (`python manage.py runserver`) |

### 1.5 Parties Prenantes

| Rôle | Description |
|------|-------------|
| **Encadrant académique** | Professeur superviseur du PFA — validation et évaluation |
| **Étudiant développeur** | Conception, développement et documentation du projet |
| **Utilisateurs finaux** | Personnes souhaitant évaluer leur risque de diabète via l'application |
| **Administrateurs** | Personnel habilité gérant les utilisateurs et supervisant les activités |

---

## II. Description Fonctionnelle

Cette section décrit l'ensemble des pages de l'application, les parcours utilisateurs et administrateurs, ainsi que les interactions fonctionnelles attendues pour chaque composant.

### 2.1 Vue d'ensemble — Arborescence de l'Application

```
📁 PUBLIC (accessible sans connexion)
├── /                     → Page d'Accueil
├── /register             → Inscription
├── /login                → Connexion
└── /contact              → Page Contact

📁 PRIVÉ — Utilisateur authentifié
├── /dashboard            → Tableau de bord personnel
└── /detection            → Formulaire de Détection du Risque

📁 PRIVÉ — Administrateur uniquement
├── /admin/dashboard      → Tableau de bord administrateur
├── /admin/users          → Liste des utilisateurs
└── /admin/users/<id>     → Profil & historique d'un utilisateur
```

### 2.2 Page d'Accueil ( / )

#### 🎯 Objectif
Page de présentation publique du projet. Elle constitue le premier point de contact de l'utilisateur avec l'application et doit inspirer confiance et clarté.

#### 📋 Contenu et fonctionnalités
- **Section Hero** : Bannière principale avec titre accrocheur et boutons vers l'inscription et la connexion.
- **Section Sensibilisation** : Informations sur le diabète (définition, types, symptômes, facteurs de risque).
- **Section "Comment ça fonctionne"** : 3 étapes — Créer un compte, Renseigner les données, Obtenir le score.
- **Navigation principale** : Barre de navigation avec liens vers les pages publiques.
- **Pied de page** : Mentions légales et liens de confidentialité.

### 2.3 Page Inscription / Connexion

#### 2.3.1 Formulaire d'Inscription ( /register )
- **Champs requis** : Prénom, Nom, Email (unique), Mot de passe, Confirmation du mot de passe.
- **Validations** : Format email, force du mot de passe (min. 8 caractères), correspondance des mots de passe.
- **Post-inscription** : Redirection vers la page de connexion avec message de succès.

#### 2.3.2 Formulaire de Connexion ( /login )
- **Champs requis** : Email, Mot de passe.
- **Session** : Utilisation du système de sessions Django (login/logout natifs).
- **Messages d'erreur génériques** pour la sécurité (ne précisent pas si l'email ou le mot de passe est incorrect).

### 2.4 Page Formulaire de Détection ( /detection ) — Accès Restreint

> ⚠️ **Accès strictement réservé aux utilisateurs authentifiés**
>
> Toute tentative d'accès sans être connecté doit entraîner une redirection automatique vers la page de connexion (`/login`).
> La restriction est appliquée via le décorateur `@login_required` de Django.

#### 🎯 Objectif
Cette page constitue le cœur fonctionnel de l'application. Elle propose un formulaire médical structuré collectant les variables nécessaires au modèle XGBoost, puis affiche le résultat de la prédiction de manière claire et visuelle.

#### 📝 Ergonomie du formulaire
- **Structure simple** : Tous les champs affichés sur une seule page (pas de wizard complexe).
- **Aide contextuelle** : Chaque champ dispose d'une explication en langage accessible.
- **Validation en temps réel** : Retour visuel sur la validité des valeurs saisies (plages physiologiques).

#### 📊 Résultat de Prédiction
- **Score de risque** : Affichage du score de probabilité (valeur entre 0 et 1, exprimée en pourcentage).
- **Jauge visuelle** : Indicateur coloré (vert 🟢 / orange 🟡 / rouge 🔴) représentant le niveau de risque.
- **Interprétation** : Message personnalisé selon le niveau de risque. Mention explicite : *non diagnostic médical*.
- **Sauvegarde automatique** : Le résultat est enregistré dans l'historique de l'utilisateur.

### 2.5 Page Contact ( /contact )
- **Formulaire** : Nom, Email, Sujet (liste déroulante), Message.
- **Protection anti-spam** : Mécanisme honeypot simple (champ caché).
- **Transmission** : Les messages sont enregistrés en base de données pour consultation par l'admin.
- **Accusé de réception** : Message de confirmation affiché après envoi.

### 2.6 Espace Administrateur ( /admin/* )

> 🔒 **Accès exclusif aux comptes avec rôle ADMIN**
>
> L'accès à toutes les routes `/admin/*` est soumis à une double vérification : utilisateur connecté **ET** rôle `'ADMIN'`.
> Un utilisateur standard recevra une erreur **403 Forbidden**.

#### 2.6.1 Dashboard Administrateur ( /admin/dashboard )
- **Statistiques globales** : Nombre total d'utilisateurs inscrits, nombre de prédictions réalisées.
- **Répartition des niveaux de risque** : Compteurs simples (Faible / Modéré / Élevé).
- **Messages de contact non lus** : Alertes visuelles.

#### 2.6.2 Liste des Utilisateurs ( /admin/users )
- **Tableau paginé** : ID, Nom, Prénom, Email, Date d'inscription, Nombre de prédictions, Statut.
- **Recherche** : Par nom ou email.
- **Actions** : Consulter le profil détaillé, Suspendre / Réactiver un compte.

#### 2.6.3 Profil Utilisateur Détaillé ( /admin/users/<id> )
- **Informations du compte** : Données d'identité, date d'inscription, statut.
- **Historique complet** : Tableau chronologique de toutes les analyses avec score et niveau de risque.
- **Export** : Possibilité d'exporter l'historique en CSV.

---

## III. Architecture Technique

### 3.1 Vue d'Ensemble de l'Architecture

> 📌 **Architecture MVT (Model-View-Template) Django**

| Couche | Technologie |
|--------|-------------|
| **Front-End** | HTML5, CSS3, JavaScript vanilla, Django Template Language |
| **Back-End** | Django 5.x (Python 3.11+) |
| **Base de données** | SQLite3 (fichier local `db.sqlite3`) |
| **Machine Learning** | XGBoost, joblib, NumPy |
| **Authentification** | Sessions Django + décorateurs `@login_required` |
| **Fichiers statiques** | Dossier `/static/` (CSS, JS, images) |

### 3.2 Intégration du Modèle XGBoost

#### Caractéristiques du modèle fourni

| Paramètre | Valeur |
|-----------|--------|
| **Fichier** | `xgboost_diabetes_model.pkl` |
| **Type** | XGBClassifier (XGBoost Sklearn API) |
| **Objectif** | `binary:logistic` (classification binaire) |
| **Métrique d'évaluation** | `logloss` (Log Loss) |
| **learning_rate** | 0.1 |
| **max_depth** | 3 |
| **n_estimators** | 44 |
| **subsample** | 0.8 |
| **colsample_bytree** | 0.8 |
| **Sortie du modèle** | `predict_proba()` : probabilité [0-1] |

#### Chargement et utilisation du modèle

Le modèle sera chargé une seule fois au démarrage de l'application Django et conservé en mémoire pour des performances optimales.

```python
# views.py
import joblib
import numpy as np
from django.conf import settings
from django.contrib.auth.decorators import login_required

# Chargement du modèle au démarrage
MODEL_PATH = settings.BASE_DIR / 'models' / 'xgboost_diabetes_model.pkl'
ml_model = joblib.load(MODEL_PATH)

@login_required
def predict_view(request):
    if request.method == 'POST':
        # Récupération des données du formulaire
        features = np.array([[
            float(request.POST['pregnancies']),
            float(request.POST['glucose']),
            float(request.POST['blood_pressure']),
            float(request.POST['skin_thickness']),
            float(request.POST['insulin']),
            float(request.POST['bmi']),
            float(request.POST['diabetes_pedigree']),
            float(request.POST['age'])
        ]])
        probability = ml_model.predict_proba(features)[0][1]
        risk_score = float(probability)
        # Sauvegarde en base et affichage du résultat...
```

### 3.3 Structure du Projet Django

```
diabetes_project/
├── manage.py
├── db.sqlite3
├── requirements.txt
├── diabetes_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── models/
│   ├── __init__.py
│   ├── xgboost_diabetes_model.pkl
│   └── load_model.py
├── accounts/
│   ├── views.py (register, login, logout)
│   ├── urls.py
│   └── forms.py
├── detection/
│   ├── views.py (formulaire + prédiction)
│   ├── urls.py
│   └── forms.py
├── admin_panel/
│   ├── views.py (dashboard, users, details)
│   ├── urls.py
│   └── decorators.py (admin_required)
├── contact/
│   ├── views.py
│   ├── urls.py
│   └── forms.py
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── register.html
│   ├── login.html
│   ├── dashboard.html
│   ├── detection.html
│   ├── detection_result.html
│   ├── contact.html
│   └── admin/
│       ├── dashboard.html
│       ├── users_list.html
│       └── user_detail.html
└── static/
    ├── css/style.css
    ├── js/script.js
    └── images/
```

### 3.4 Modèle de Base de Données (SQLite)

#### Table : `users` (extension de AbstractUser)

| Colonne | Type | Description |
|---------|------|-------------|
| `id` | Integer (PK) | Identifiant unique auto-incrémenté |
| `email` | CharField(255) UNIQUE | Adresse email (identifiant de connexion) |
| `password` | CharField(255) | Mot de passe hashé (PBKDF2/bcrypt) |
| `first_name` | CharField(100) | Prénom |
| `last_name` | CharField(100) | Nom de famille |
| `role` | CharField(10) | Rôle : `'user'` ou `'admin'` |
| `is_active` | BooleanField | Compte actif ou suspendu |
| `date_joined` | DateTimeField | Date d'inscription |
| `last_login` | DateTimeField | Dernière connexion |

#### Table : `predictions`

| Colonne | Type | Description |
|---------|------|-------------|
| `id` | Integer (PK) | Identifiant unique |
| `user` | ForeignKey → users | Référence vers l'utilisateur |
| `pregnancies` | IntegerField | Nombre de grossesses |
| `glucose` | FloatField | Glucose (mg/dL) |
| `blood_pressure` | FloatField | Pression diastolique (mmHg) |
| `skin_thickness` | FloatField | Épaisseur pli cutané (mm) |
| `insulin` | FloatField | Insuline sérique (mu U/ml) |
| `bmi` | FloatField | Indice de Masse Corporelle |
| `diabetes_pedigree` | FloatField | Fonction génétique |
| `age` | IntegerField | Âge (années) |
| `risk_score` | FloatField | Probabilité [0.0 - 1.0] |
| `risk_level` | CharField(10) | `LOW` / `MEDIUM` / `HIGH` |
| `created_at` | DateTimeField | Date de l'analyse |

#### Table : `contact_messages`

| Colonne | Type | Description |
|---------|------|-------------|
| `id` | Integer (PK) | Identifiant unique |
| `sender_name` | CharField(150) | Nom de l'expéditeur |
| `sender_email` | CharField(255) | Email de l'expéditeur |
| `subject` | CharField(100) | Sujet du message |
| `message` | TextField | Corps du message |
| `is_read` | BooleanField | Lu par l'admin ? |
| `created_at` | DateTimeField | Date d'envoi |

### 3.5 Authentification et Gestion des Sessions

- **Sessions Django** : Utilisation du système natif `django.contrib.auth` avec sessions stockées côté serveur.
- **Décorateurs** : `@login_required` pour les pages privées, `@user_passes_test` pour l'espace admin.
- **Stockage** : Les sessions sont stockées dans la base SQLite (`SESSION_ENGINE` par défaut).
- **Déconnexion** : Fonction `logout()` native de Django qui invalide la session.

### 3.6 Stack Technologique

| Couche | Technologie |
|--------|-------------|
| **Front-End** | HTML5, CSS3, JavaScript vanilla, Django Template Language |
| **Back-End** | Python 3.11+, Django 5.x |
| **Machine Learning** | XGBoost, joblib, NumPy, Scikit-learn |
| **Base de données** | SQLite3 (fichier local) |
| **Authentification** | `django.contrib.auth` (sessions natives) |
| **Serveur de développement** | `python manage.py runserver` (localhost:8000) |
| **Gestion des dépendances** | pip + `requirements.txt` |

---

## IV. Spécifications Techniques des Données

### 4.1 Variables d'Entrée du Formulaire de Détection

Le modèle XGBoost est basé sur le jeu de données **Pima Indians Diabetes**. Il requiert exactement **8 variables d'entrée**.

| Variable | Description médicale | Type | Plage valide | Aide utilisateur |
|----------|----------------------|------|--------------|------------------|
| **Pregnancies** | Nombre de grossesses antérieures | Entier | 0 – 20 | Indiquez 0 si vous êtes un homme ou n'avez jamais été enceinte |
| **Glucose** | Concentration plasmatique en glucose 2h après test | Décimal | 0 – 300 mg/dL | Valeur obtenue lors d'un test HGPO |
| **BloodPressure** | Pression artérielle diastolique | Décimal | 0 – 130 mmHg | Valeur basse de votre tension artérielle |
| **SkinThickness** | Épaisseur du pli cutané tricipital | Décimal | 0 – 100 mm | Mesure au niveau du triceps. Saisir 0 si inconnue |
| **Insulin** | Insuline sérique 2h après test | Décimal | 0 – 900 | Taux d'insuline sanguin. Saisir 0 si non disponible |
| **BMI** | Indice de Masse Corporelle | Décimal | 10 – 70 kg/m² | Poids(kg) ÷ Taille²(m). Calculateur intégré |
| **DiabetesPedigreeFunction** | Fonction génétique de risque héréditaire | Décimal | 0.0 – 2.5 | Indicateur basé sur les antécédents familiaux |
| **Age** | Âge de l'utilisateur | Entier | 1 – 120 ans | Votre âge actuel en années révolues |

### 4.2 Fonctionnalités Complémentaires du Formulaire

- **Calculateur d'IMC intégré** : Champs Poids (kg) et Taille (cm) permettant de calculer automatiquement l'IMC.
- **Valeurs par défaut** : Aucune valeur par défaut. Tous les champs sont obligatoires (0 autorisé pour données inconnues).
- **Avertissement médical** : Mention explicite : *"Cet outil fournit une estimation statistique et ne constitue pas un diagnostic médical."*

### 4.3 Format de la Requête et Réponse

> 📌 **Format de la requête POST (formulaire Django)**

```
pregnancies=2
glucose=148.0
blood_pressure=72.0
skin_thickness=35.0
insulin=0.0
bmi=33.6
diabetes_pedigree=0.627
age=50
```

> 📌 **Format de la réponse (affichage dans le template)**

```
risk_score = 0.7823
risk_percentage = 78.23%
risk_level = 'HIGH'
risk_label = 'Risque élevé de diabète'
recommendation = 'Consultez votre médecin rapidement.'
```

### 4.4 Classification des Niveaux de Risque

| Plage de score | Niveau | Couleur | Action recommandée |
|----------------|--------|---------|-------------------|
| **< 30%** | 🟢 Faible | `#7CB342` | Conseils de prévention générale |
| **30% – 60%** | 🟡 Modéré | `#F9A825` | Recommandation de suivi médical |
| **> 60%** | 🔴 Élevé | `#E53935` | Recommandation de consultation urgente |

### 4.5 Validation des Données

Toutes les données reçues sont validées via les **Formulaires Django** (`forms.py`) avant toute transmission au modèle XGBoost.

> 📌 **Exemple de validation Django (forms.py)**

```python
from django import forms

class PredictionForm(forms.Form):
    pregnancies = forms.IntegerField(min_value=0, max_value=20)
    glucose = forms.FloatField(min_value=0, max_value=300)
    blood_pressure = forms.FloatField(min_value=0, max_value=130)
    skin_thickness = forms.FloatField(min_value=0, max_value=100)
    insulin = forms.FloatField(min_value=0, max_value=900)
    bmi = forms.FloatField(min_value=10, max_value=70)
    diabetes_pedigree = forms.FloatField(min_value=0.0, max_value=2.5)
    age = forms.IntegerField(min_value=1, max_value=120)
```

---

## V. Contraintes de Sécurité

> ⚠️ **Données de santé — Classification Sensible**
>
> Les données collectées (mesures biologiques, scores de risque) sont des données de santé à caractère personnel.
> Même en environnement local, les bonnes pratiques de sécurité doivent être appliquées.

### 5.1 Protection des Données

- **Principe de minimisation** : Seules les 8 données strictement nécessaires au modèle ML sont collectées.
- **Finalité explicite** : Les utilisateurs sont informés de la finalité du traitement (évaluation du risque — usage non médical).
- **Consentement** : Acceptation des CGU lors de l'inscription (case à cocher obligatoire).
- **Droit à l'effacement** : L'utilisateur peut supprimer son compte et toutes ses données associées.
- **Mention légale** : Affichée sur la page de résultat — l'application ne fournit pas de diagnostic médical.

### 5.2 Sécurité de l'Application

#### Chiffrement et mots de passe
- **Mots de passe** : Hashés avec PBKDF2 (algorithme par défaut de Django, configurable vers bcrypt).
- **Aucun mot de passe** n'est jamais stocké en clair.

#### Configuration de sécurité Django
- **CSRF** : Protection automatique sur tous les formulaires POST (token CSRF intégré).
- **SQL Injection** : Impossible grâce à l'ORM Django (requêtes paramétrées automatiques).
- **XSS** : Échappement automatique des variables dans les templates Django.
- **CORS** : Non applicable (application monolithique, pas d'API externe).

### 5.3 Contrôle d'Accès et Autorisation

#### Restriction des pages privées
- **Décorateur `@login_required`** : Toute vue privée (`/dashboard`, `/detection`) vérifie l'authentification. Redirection vers `/login` si non connecté.
- **Middleware Django** : Gestion automatique des sessions et de l'authentification.

#### Restriction de l'espace administrateur
- **Décorateur personnalisé `@admin_required`** : Vérifie que l'utilisateur a le rôle `'ADMIN'`.
- **Création admin** : Un compte admin est créé manuellement (`python manage.py createsuperuser` ou script d'initialisation).
- **Aucune interface publique** ne permet de s'auto-promouvoir administrateur.

### 5.4 Protection contre les Attaques Courantes

| Type d'attaque | Mesure de protection |
|----------------|---------------------|
| **Injection SQL** | ORM Django avec requêtes paramétrées automatiques |
| **XSS (Cross-Site Scripting)** | Échappement automatique des templates Django |
| **CSRF** | Token CSRF sur tous les formulaires POST |
| **Brute Force (connexion)** | Messages d'erreur génériques + limitation via middleware (optionnel) |
| **Injection de données ML** | Validation stricte des plages via Django Forms |
| **Exposition du fichier .pkl** | Stocké hors du dossier `static/` (dossier `models/` non accessible) |
| **IDOR** | Vérification que l'utilisateur connecté accède uniquement à ses propres données |

### 5.5 Journalisation

- **Logs Django** : Journalisation des erreurs serveur dans des fichiers locaux.
- **Logs d'audit** : Enregistrement des connexions, inscriptions et actions admin (optionnel, via middleware personnalisé).

### 5.6 Politique de Gestion des Mots de Passe

| Règle | Spécification |
|-------|---------------|
| **Longueur minimale** | 8 caractères |
| **Complexité requise** | Au moins 1 majuscule, 1 chiffre, 1 caractère spécial |
| **Algorithme de hachage** | PBKDF2 (Django par défaut) |
| **Réinitialisation** | Lien par email (optionnel pour PFA) |
| **Transmission** | Jamais en clair dans les logs |

---

## Annexes

### Annexe A — Glossaire

| Terme | Définition |
|-------|-----------|
| **XGBoost** | eXtreme Gradient Boosting — algorithme d'apprentissage automatique basé sur des arbres de décision |
| **XGBClassifier** | Implémentation XGBoost compatible API Scikit-learn pour la classification |
| **binary:logistic** | Objectif du modèle pour classification binaire — retourne une probabilité entre 0 et 1 |
| **logloss** | Métrique d'évaluation (Log Loss) — mesure la précision des prédictions de probabilité |
| **predict_proba()** | Méthode retournant les probabilités d'appartenance à chaque classe |
| **.pkl** | Format de sérialisation Python (Pickle) pour sauvegarder des objets Python |
| **Django** | Framework web Python haut niveau encourageant le développement rapide |
| **MVT** | Model-View-Template — architecture de Django (équivalent MVC) |
| **ORM** | Object-Relational Mapping — interaction avec la BDD via des objets Python |
| **IMC / BMI** | Indice de Masse Corporelle — Poids(kg) / Taille²(m) |
| **HGPO** | Hyperglycémie Provoquée par voie Orale — test de tolérance au glucose |
| **CSRF** | Cross-Site Request Forgery — attaque par usurpation de requête |
| **PBKDF2** | Password-Based Key Derivation Function 2 — algorithme de hachage de mots de passe |

### Annexe B — Critères d'Acceptation (Definition of Done)

- ✅ **Fonctionnel** : Toutes les pages décrites en Section II sont implémentées et testées manuellement.
- ✅ **ML** : L'endpoint de prédiction charge le fichier `.pkl` et retourne des résultats cohérents.
- ✅ **Sécurité** : Les routes privées redirigent les utilisateurs non authentifiés. Les routes admin retournent 403 pour les rôles non-admin.
- ✅ **Tests** : Formulaires validés, authentification fonctionnelle, prédiction opérationnelle.
- ✅ **Documentation** : Rapport PFA rédigé avec captures d'écran et explications du code.

### Annexe C — Planning Indicatif du PFA

| Phase | Durée | Tâches principales |
|-------|-------|-------------------|
| **Analyse & Conception** | 1 semaine | Rédaction du CDC, maquettes HTML/CSS, modélisation BDD |
| **Développement Back-End** | 2 semaines | Modèles Django, authentification, API prédiction, admin |
| **Développement Front-End** | 2 semaines | Templates HTML/CSS/JS, formulaires, dashboard |
| **Intégration ML** | 1 semaine | Chargement du `.pkl`, tests de prédiction, ajustements |
| **Tests & Debug** | 1 semaine | Tests fonctionnels, correction de bugs, validation des formulaires |
| **Documentation** | 3 jours | Rapport PFA, manuel utilisateur, présentation |

### Annexe D — Dépendances Python (requirements.txt)

> 📌 **Fichier `requirements.txt`**

```
Django>=5.0,<6.0
xgboost>=2.0.0
scikit-learn>=1.3.0
joblib>=1.3.0
numpy>=1.24.0
pandas>=2.0.0
python-dotenv>=1.0.0  # Pour les variables d'environnement
```

---

<div style="text-align: center; color: #666; font-style: italic;">

*Fin du document — Cahier des Charges v1.0 — PFA 2026*

</div>
