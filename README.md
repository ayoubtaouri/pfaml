# Détection du risque de diabète (XGBoost + Django)

Modèle de Machine Learning qui prédit le risque de diabète à partir de données médicales, déployé dans une application web Django permettant d'obtenir une prédiction en temps réel.

## Résultats

Évaluation sur 20 000 patients (jeu de test) :

| Métrique | Valeur |
|---|---|
| Accuracy | 92,31 % |
| ROC-AUC | 97,72 % |
| Recall (classe diabétique) | 88,29 % |
| Precision (classe diabétique) | 52,87 % |
| F1-score (classe diabétique) | 66,14 % |
| Validation croisée (5 plis) | 92,33 % (± 0,15 %) |

La précision sur la classe diabétique est volontairement sacrifiée au profit du rappel : en dépistage, il vaut mieux quelques fausses alertes que des cas manqués.

## Données

- **Source :** [Diabetes Prediction Dataset (Kaggle)](https://www.kaggle.com/datasets/iammustafatz/diabetes-prediction-dataset)
- **Taille :** 100 000 patients, 9 colonnes, aucune valeur manquante
- **Variables :** `gender`, `age`, `hypertension`, `heart_disease`, `smoking_history`, `bmi`, `HbA1c_level`, `blood_glucose_level`
- **Cible :** `diabetes` (0 = non, 1 = oui)
- **Déséquilibre :** 8,5 % de patients diabétiques (8 500 sur 100 000)

## Méthode

1. **Exploration :** structure, valeurs manquantes, distribution de la cible, statistiques descriptives.
2. **Préparation :** encodage des variables catégorielles (`gender`, `smoking_history`).
3. **Découpage :** 80 % entraînement (80 000) / 20 % test (20 000).
4. **Déséquilibre des classes :** pondération avec `scale_pos_weight` (≈ 10,76).
5. **Modèle :** XGBoost (300 itérations), suivi du `logloss` sur le jeu de validation.
6. **Évaluation :** accuracy, ROC-AUC, précision, rappel, F1 et validation croisée à 5 plis.
7. **Sauvegarde :** modèle sérialisé avec `joblib` puis rechargé dans Django.

### Variables les plus importantes

| Variable | Importance |
|---|---|
| HbA1c_level | 40,1 % |
| blood_glucose_level | 32,2 % |
| age | 8,7 % |

## Technologies

Python, Pandas, NumPy, Scikit-learn, XGBoost, Matplotlib, Seaborn, Joblib, Django

## Installation et lancement

```bash
# 1. Cloner le projet
git clone https://github.com/<votre-compte>/<nom-du-projet>.git
cd <nom-du-projet>

# 2. Créer l'environnement et installer les dépendances
python -m venv venv
source venv/bin/activate        # Windows : venv\Scripts\activate
pip install -r requirements.txt

# 3. Lancer l'application web
python manage.py runserver
```

Ouvrir ensuite http://127.0.0.1:8000, saisir les informations du patient et obtenir la prédiction.

> Pour réentraîner le modèle, ouvrir le notebook `<nom-du-notebook>.ipynb` et exécuter toutes les cellules.

## Structure du projet

```
├── notebook/          # Analyse, entraînement et évaluation du modèle
├── model/             # Modèle entraîné (.joblib)
├── webapp/            # Application Django
├── requirements.txt
└── README.md
```

*(Adaptez les noms de dossiers à votre projet.)*

## Limites

- Projet à but pédagogique : il **ne remplace pas un diagnostic médical**.
- Le jeu de données est public et ne reflète pas forcément une population réelle.
- La précision sur la classe diabétique reste modérée (≈ 53 %), ce qui entraîne des faux positifs.

## Auteur

**Ayoub Taouri** — Étudiant ingénieur en Développement Digital & SI, EMSI Rabat
[LinkedIn](https://linkedin.com/in/Taouri-Ayoub) · Ayoub.taouri430@gmail.com
