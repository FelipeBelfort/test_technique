# Glados – Développeur Full-Stack

Bienvenue dans le projet **Glados**, une plateforme de gestion de maison connectée développée dans le cadre d’un processus de recrutement pour un stage chez Glados.

## 🔍 Présentation

Glados est une startup visionnaire fondée par la légendaire Chell Aperture, dont l’objectif était de connecter toutes les maisons du monde. Après sa disparition tragique suite à une indigestion de gâteau à la patate, l’entreprise a été reprise par son neveu Dave LIDE.

Afin d’honorer la mémoire de Chell et de débloquer des subventions importantes, une première version fonctionnelle de Glados doit être livrée rapidement.

---

## 🎯 Objectif du projet

Développer une application full-stack qui permet de :

- Visualiser les entités d’une maison connectée.
- Filtrer ces entités selon leur type, pièce ou statut.
- Contrôler les entités (modifier leur statut, valeur, etc.).
- Ajouter une fonction de synthèse vocale pour rendre l’interface plus vivante.

---

## 🧩 Stack technique

- **Backend** : Flask (Python)
- **Frontend** : Vue.js avec TailwindCSS
- **Base de données** : PostgreSQL
- **Gestion de conteneurs** : Docker & Docker Compose
- **Tests** : Pytest (TDD)
- **CI/CD local** : via `Makefile`

---

## 🚀 Étapes du projet

### ✅ Étape 1 – Lancer le projet (DEVOPS)
- Récupération du code.
- Conteneurisation du backend et du frontend via Docker.
- Lancement des services via `docker compose`.

### ✅ Étape 2 – Ajout de filtres sur les entités (BACKEND)
- Amélioration de la route `/entities` :
  - Ajout de filtres par pièce et par statut.
  - Mise en place de tests unitaires (TDD).

### ✅ Étape 3 – Visualisation des entités (FRONTEND)
- Refonte de l’interface utilisateur.
- Affichage dynamique des entités avec leurs informations (type, pièce, statut, etc.).
- UI/UX personnalisée.

### ✅ Étape 4 – Contrôle des entités (FULLSTACK)
- Création de routes REST pour modifier les entités.
- Intégration des actions côté frontend.

### ✅ Étape 5 – Synthèse vocale (FULLSTACK)
- Lecture à voix haute des entités et de leurs états.
- Utilisation de l’API Web Speech ou équivalent.

---
